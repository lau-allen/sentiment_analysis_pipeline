#libraries 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service 
import asyncio
import aiohttp
import async_timeout
from functools import reduce 

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
        #top-level URLs to scrape 
        self.data_sources = url_sources
        #dictionary containing top-level URL key and links values within top-level URL 
        self.url_to_links = {} 

    async def get_links(self,session:aiohttp.ClientSession, url:str) -> None:
        #define driver options 
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-dev-shm-usage')
        #define google chrome driver for selenium request 
        driver = webdriver.Chrome(service=Service('/usr/local/bin/chromedriver'),options=chrome_options)
        print('I am here')
        #sync access to shared dictionary property to avoid race conditions
        async with self.lock:
            #request data 
            driver.get(url)
            #create bs4 soup 
            soup = BeautifulSoup(driver.page_source,'lxml')
            #filter for links
            all_href = [x.get('href') for x in soup.find_all('a', href=True)]
            print(all_href)
            #add data into dict property 
            self.url_to_links[url] = all_href
        #quit driver 
        driver.quit()
        return 

    async def get_urls(self,session:aiohttp.ClientSession, urls:list) -> None:
        tasks = []
        #for each url, create a task to get links for the defined session object and url 
        for url in urls:
            task = asyncio.create_task(self.get_links(session, url))
            tasks.append(task)
        await asyncio.gather(*tasks)
        return  

    async def all_links_req(self,urls:list) -> None:
        #context manager for aiohttp session object 
        async with aiohttp.ClientSession() as session:
            #get data obtained from get_all with defined session object and urls 
            await self.get_urls(session, urls)
            return 

    def all_links(self) -> None:
        """
        Retrieve all links existing on a top-level webpage using headless chrome driver and selenium 
        to load JS webpage artifacts. 

        Set class url_to_links property with associated webpage:links data         
        """
        asyncio.run(self.all_links_req(self.url_to_links))
        return 

    #async get html from url 
    async def get_html(self,session:aiohttp.ClientSession, url:str) -> tuple:
        """
        Async request task for retriving HTML data from defined URL 

        Args:
            session (aiohttp.ClientSession): aiohttp ClientSession object for async workflow
            url (str): URL to request HTML data 

        Returns:
            tuple: HTML text, URL source ---OR--- Error message, URL Source 
        """
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
    async def get_all(self,session:aiohttp.ClientSession, urls:list) -> list:
        """
        Define tasks for async workflow to get HTML text from list of URL sources and 
        asynchronously requests HTML data. 

        Args:
            session (aiohttp.ClientSession): aiohttp ClientSession object for async workflow
            urls (list): URLs to request HTML data

        Returns:
            list: list of tuples (HTML data, URL Source)
        """
        tasks = []
        #for each url, create a task to get html for the defined session object and url 
        for url in urls:
            task = asyncio.create_task(self.get_html(session, url))
            tasks.append(task)
        #return all the tasks 
        results = await asyncio.gather(*tasks)
        return results 

    async def async_req(self,urls:list) -> list:
        """
        Definition of aiohttp Client Session object for async workflow and calls 
        to async functions to retrive HTML data from defined URLs 

        Args:
            urls (list): list of URLs to request HTML data 

        Returns:
            list: list of tuples (HTML data, URL source)
        """
        #context manager for aiohttp session object 
        async with aiohttp.ClientSession() as session:
            #get data obtained from get_all with defined session object and urls 
            data = await self.get_all(session, urls)
            #return list of data, where each element is a tuple containing html, url 
            return data

    def async_request(self,urls=None) -> list:
        """
        Wrapper function for self.async_req()

        Args:
            urls (list, optional): list of URLs to request HTML data from. Defaults to None.

        Returns:
            list: list of tuples (HTML data, URL source)
        """
        if urls == None:
            text_url_tup = asyncio.run(self.async_req(self.url_to_links.values()))
        else:
            text_url_tup = asyncio.run(self.async_req(urls))
        return text_url_tup

    def get_raw_text(self,html:str):
        """
        Function to retrieve paragraph text from news articles

        Args:
            text (str): raw HTML data 

        Returns:
            tuple: Tuple of paragraph text and title of article 
        """
        #define BS4 object with defined HTML data 
        soup = BeautifulSoup(html,'lxml')
        try: 
            #get article title if exists 
            title = soup.title.get_text()
        except AttributeError:
            title = "N/A"
        #loop through paragraph tags and extract string information
        for script in soup(['script','style','template','TemplateString','ProcessingInstruction','Declaration','Doctype']):
            script.extract()
        #perform additional preprocessing steps like removing white spaces and binary formatting
        text = [item.text.strip().replace(u'\xa0', u' ') for item in soup.find_all('p')]
        #return paragraph text
        return reduce(lambda x,y: x+' '+y,text,''), title 



if __name__ == '__main__':
    pass
