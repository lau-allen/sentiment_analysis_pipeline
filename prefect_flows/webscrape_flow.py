from prefect import flow, task
from tasks.extract_webscrape.webscraper import web_scraper

@flow
def webscrape_extract():
    urls = ['https://finance.yahoo.com/news/']
    ws = web_scraper(urls)
    print(ws.length)

    return 

if __name__ == '__main__':
    webscrape_extract()