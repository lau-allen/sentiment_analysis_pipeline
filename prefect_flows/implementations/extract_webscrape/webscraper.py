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
    web_scraper object encapsulates all logic for 
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
        #dictionary containing links from top-level URL to its html data 
        self.links_to_data = {}
        #define async lock property to avoid race conditions
        self.lock = asyncio.Lock()

    async def get_links(self, url:str) -> None:
        """
        Define Chrome driver and perform Selenium requests for link data from specified URL

        Args:
            url (str): defined URL to scrape
        """
        try:
            #define driver options 
            chrome_options = Options()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-dev-shm-usage')
            #define google chrome driver for selenium request 
            driver = webdriver.Chrome(service=Service('/usr/local/bin/chromedriver'),options=chrome_options)
            #request data 
            driver.get(url)
            #create bs4 soup 
            soup = BeautifulSoup(driver.page_source,'lxml')
            #filter for links
            all_href = [x.get('href') for x in soup.find_all('a', href=True)]            
            #sync access to shared dictionary property to avoid race conditions
            async with self.lock:
                #add data into dict property 
                self.url_to_links[url] = all_href
        finally:
            #quit driver 
            driver.quit()
        return 

    async def get_urls(self, urls:list) -> None:
        """
        Define async tasks to get the URLs existing on a list of top-level URLs. Wait for all tasks to complete. 

        Args:
            urls (list): List of top-level URLs to scrape for links. 
        """
        tasks = []
        #for each url, create a task to get links for the defined session object and url 
        for url in urls:
            task = asyncio.create_task(self.get_links(url))
            tasks.append(task)
        #async tasks 
        await asyncio.gather(*tasks)
        return  

    def all_links(self) -> None:
        """
        Wrapper function for get_urls
        
        Retrieve all links existing on a top-level webpage using headless chrome driver and selenium 
        to load JS webpage artifacts. 

        Set class url_to_links property with associated webpage:links data         
        """
        asyncio.run(self.get_urls(self.data_sources))
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

    async def async_req(self,urls:list) -> dict:
        """
        Definition of aiohttp Client Session object for async workflow and calls 
        to async functions to retrive HTML data from defined URLs 

        Args:
            urls (list): list of URLs to request HTML data 

        Returns:
            dict: dictionary of link to data, where data is (text, title)
        """
        #context manager for aiohttp session object 
        async with aiohttp.ClientSession() as session:
            #get data obtained from get_all with defined session object and urls 
            data = await self.get_all(session, urls)
            #return dictionary of link to data, where data is (text, title)
            return {link:self.get_raw_text(html) for html,link in data} 

    def async_request(self,urls:list) -> dict:
        """
        Wrapper function for self.async_req()

        Args:
            urls (list, optional): list of URLs to request HTML data from. Defaults to None.

        Returns:
            dict: dictionary of link to data, where data is (text, title)
        """
        return asyncio.run(self.async_req(urls))

    def get_raw_text(self,html:str) -> tuple:
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
    # #define list of finance websites to scrape 
    # websites = ['https://finance.yahoo.com/news/','https://www.marketwatch.com/latest-news?mod=top_nav']
    # ws = web_scraper(websites)
    # #kickoff extract_urls_to_news links flow
    # ws.all_links()
    pass
