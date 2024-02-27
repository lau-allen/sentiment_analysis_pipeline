#libraries
from prefect import flow, task
from implementations.extract_webscrape.webscraper import web_scraper
import config
import asyncio
from prefect_dask import DaskTaskRunner, get_dask_client
import dask 
import dask.distributed
from implementations.io.io import io
import datetime 

#initialize dask client for parallelization of flows 
client = dask.distributed.Client()


def url_filter(url:str,block_set:set) -> bool:
    """
    Filter function to remove un-needed URLs from results. 

    Args:
        url (str): URL string 
        block_set (set): Set of unwanted URL strings 

    Returns:
        bool: T/F
    """
    if url in block_set:
        return False
    else:
        return True 

def extract_news_text(ws:web_scraper,website:str) -> dict:
    """
    Definiton of task to extract raw text data from news links from a defined website. 

    Args:
        ws (web_scraper): web_scraper object containing the URLs to be scraped 
        website (str): defined top-level website 

    Returns:
        list: list of tuples ((text, title of article),URL source)
    """
    #perform async requests of news articles, returns tuples of (raw HTML data, URL source) 
    link_to_data = ws.async_request(ws.url_to_links[website])
    return link_to_data

def yahoo_url_filter(urls:list) -> list:
    """
    Definition of task to perform URL filtering and data validation for 
    Yahoo Finance News 

    Args:
        urls (list): List of URLs 

    Returns:
        list: formatted and cleaned list of URLs to request data from 
    """
    #filter unwanted links 
    filtered_urls = list(filter(lambda url: url_filter(url,config.yahoo_fin_block_set), urls))
    #perform data validation on URLs to ensure they are complete URLs 
    for i in range(len(filtered_urls)):
        if not filtered_urls[i].startswith('https'):
            filtered_urls[i] = 'https://finance.yahoo.com'+filtered_urls[i]
    return filtered_urls

def marketwatch_url_filter(urls:list) -> list:
    """
    Definition of task to perform URL filtering and data validation for 
    MarketWatch News 

    Args:
        urls (list): List of URLs 

    Returns:
        list: formatted and cleaned list of URLs to request data from 
    """
    #filter unwanted links 
    filtered_urls = list(filter(lambda url: url.startswith('https://www.marketwatch.com/story'), urls))
    return filtered_urls

@task 
def extract_yahoo_finance_news(ws:web_scraper,website:str) -> dict:
    """
    Definition of task to extract Yahoo Finance News 

    Args:
        ws (web_scraper): web_scraper object containing the URLs to be scraped 
        website (str): top-level website string

    Returns:
        list: list of tuples (HTML data, URL Source)
    """
    #perform filter of unwanted links and append domain if needed 
    filtered_urls = yahoo_url_filter(ws.url_to_links[website]) 
    #update yahoo finance key 
    ws.url_to_links[website] = filtered_urls
    #extract data
    link_to_data = extract_news_text(ws,website)
    return link_to_data


@task 
def extract_marketwatch_news(ws:web_scraper,website:str) -> dict:
    """
    Definition of task to extract MarketWatch News 

    Args:
        ws (web_scraper): web_scraper object containing the URLs to be scraped 
        website (str): top-level website string

    Returns:
        list: list of tuples (HTML data, URL Source)
    """
    #perform filter of unwanted links and append domain if needed 
    filtered_urls = marketwatch_url_filter(ws.url_to_links[website]) 
    #update marketwatch key 
    ws.url_to_links[website] = filtered_urls
    #extract data
    link_to_data = extract_news_text(ws,website)
    return link_to_data

@flow 
def extract_urls_to_news(urls:list) -> web_scraper:
    """
    Defintion of sub-flow to extract links to news articles 
    from top-level news source websites 

    Args:
        urls (list): List of top-level news sources

    Returns:
        web_scraper: web_scraper object containing the URLs to be scraped and implementation to scrape websites 
    """
    #define web_scraper object with defined list of urls
    ws = web_scraper(urls)
    #retrieve all links from top-level URL 
    ws.all_links()
    #return the web_scraper object 
    return ws 

@flow(task_runner=DaskTaskRunner(address=client.scheduler.address))
def extract_news(web_scraper:web_scraper,websites:list) -> None:
    """
    Extract text information from news links existing on the top-level websites given. 
    Perform flow using Dask Clusters for parallelization of work. Retrieval of text within
    news links is performed asynchronously using asyncio, asynchttp 

    Args:
        web_scraper (web_scraper): web_scraper object that contains async methods and URL info 
        websites (list): list of top-level websites to scrape 

    Returns:
        tuple: tuple of lists containing (text data, title, URL source)
    """
    #PrefectFuture Object 
    future_yahoo = extract_yahoo_finance_news.submit(web_scraper,websites[0])
    future_marketwatch = extract_marketwatch_news.submit(web_scraper,websites[1])
    
    #return dask client 
    with get_dask_client():
        #upload webscraper implmenetation to dask workers 
        client.upload_file('/opt/sentiment_analysis_pipeline/prefect_flows/implementations/extract_webscrape/webscraper.py')
        #retrive data 
        yahoo_data = future_yahoo.result()
        marketwatch_data = future_marketwatch.result()
    
    return [('finance_yahoo_news',yahoo_data),('marketwatch_latest_news',marketwatch_data)]

@flow 
def push_to_s3(data:list) -> None:
    """
    Push data to S3 Bucket 

    Args:
        data (list): list of tuples (website name, dict of data)
    """
    #define io object 
    i_o = io()
    #define timestamp for file name 
    t_stamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    #write data to json in temp dir 
    for website,d in data:
        i_o.write_to_json(d,f'{website}_{t_stamp}')
    #push data to s3 bucket 
    i_o.pushObject_to_S3()
    #clean up io object 
    del i_o
    return 

@flow
def webscrape_extract() -> None:
    """
    Defintion of main extract entry flow to obtain HTML data from 
    defined top-level finance news sources 
    """
    #define list of finance websites to scrape 
    websites = ['https://finance.yahoo.com/news/','https://www.marketwatch.com/latest-news?mod=top_nav']
    #kickoff extract_urls_to_news links flow
    ws = extract_urls_to_news(websites)
    #extract text data from the defined websites 
    website_datalist = extract_news(ws,websites)
    #push data into cloud storage 
    push_to_s3(website_datalist)
    return 


if __name__ == '__main__':
    #kickoff webscrape extract flow 
    webscrape_extract()
