#libraries
from prefect import flow, task
from tasks.extract_webscrape.webscraper import web_scraper
import config

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

@task 
def extract_news_text(ws:web_scraper,website:str) -> list:
    """
    Definiton of task to extract raw text data from news links from a defined website. 

    Args:
        ws (web_scraper): web_scraper object containing the URLs to be scraped 
        website (str): defined top-level website 

    Returns:
        list: list of tuples ((text, title of article),URL source)
    """
    #perform async requests of news articles, returns tuples of (raw HTML data, URL source) 
    data = ws.async_request(ws.url_to_links[website])
    #get raw text from news articles 
    data = map(lambda x: (ws.get_raw_text(x[0]),x[1]),data)
    #return tuple of (raw text data, URL source)
    return list(data)

@task 
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

@task 
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

@flow 
def extract_yahoo_finance_news(ws:web_scraper,website:str) -> list:
    """
    Definition of sub-flow to extract Yahoo Finance News 

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
    data = extract_news_text(ws,website)
    #return data
    return data

@flow 
def extract_marketwatch_news(ws:web_scraper,website:str) -> list:
    """
    Definition of sub-flow to extract MarketWatch News 

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
    data = extract_news_text(ws,website)
    #return data
    return data

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
    #kickoff yahoo finance extract sub-flow 
    yahoo_data = extract_yahoo_finance_news(ws,websites[0])
    #kickoff marketwatch extract sub-flow 
    marketwatch_data = extract_marketwatch_news(ws,websites[1])
    return 




if __name__ == '__main__':
    #kickoff webscrape extract flow 
    webscrape_extract()
