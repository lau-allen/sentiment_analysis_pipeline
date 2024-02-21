#libraries 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service 
from webdriver_manager.chrome import ChromeDriverManager
import asyncio
import aiohttp
import async_timeout

class web_scraper:
    """
    web_scaper object encapsulates all logic for 
    web scraping HTML data sources
    """

    def __init__(self,url_sources:list) -> None:
        """
        Generator function 

        Args:
            url_sources (list): list of URLs to scrape 
        """
        self.data_sources = url_sources
        self.length = len(self.data_sources)
        
    def all_links(self) -> dict:
        #define driver options 
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-dev-shm-usage')
        #define google chrome driver for selenium request 
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
        #define dictionary of data 
        url_linkdata = {}
        #request HTML from url and store into a dictionary format
        for url in self.data_sources:
            #request data 
            driver.get(url)
            #create bs4 soup 
            soup = BeautifulSoup(driver.page_source,'lxml')
            #filter for links
            all_href = map(lambda x: x.get('href'),soup.find_all('a',href=True))
            #add data into dict 
            url_linkdata[url] = all_href 

        return url_linkdata

    #async get html from url 
    async def get_html(self,session, url):
        #get html text from session object 
        try:
            async with async_timeout.timeout(10):
                async with session.get(url) as response:
                    return await response.text(), url
        #if timeout, return "TimeoutError" and url as tuple 
        except asyncio.exceptions.TimeoutError:
            return "Error: Timeout", url
        #if invalid url, return "InvalidURL" and url as tuple 
        except aiohttp.client_exceptions.InvalidURL:
            return "Error: InvaidURL", url 
        #if server disconnected, return "ServerDisconnected" and url as tuple
        except aiohttp.client_exceptions.ServerDisconnectedError:
            return 'Error: ServerDisconnected', url 
        except UnicodeDecodeError:
            return 'Error: UnicodeDecodeError', url
        except aiohttp.client_exceptions.ClientConnectorError:
            return 'Error: ClientConnectorError', url

    #define tasks for the urls 
    async def get_all(self,session, urls):
        tasks = []
        #for each url, create a task to get html for the defined session object and url 
        for url in urls:
            task = asyncio.create_task(self.get_html(session, url))
            tasks.append(task)
        #return all the tasks 
        results = await asyncio.gather(*tasks)
        return results 

    async def async_req(self,urls):
        #context manager for aiohttp session object 
        async with aiohttp.ClientSession() as session:
            #get data obtained from get_all with defined session object and urls 
            data = await self.get_all(session, urls)
            #return list of data, where each element is a tuple containing html, url 
            return data


if __name__ == '__main__':
    #define urls to scrape 
    urls = ['https://finance.yahoo.com/news/']
    #define web_scraper obj 
    ws = web_scraper(urls)
    #retrieve all links 
    links = ws.all_links()
    #perform URL filtering/validation 
    #<place in prefect flow or task>

    #async requests 
    
    
