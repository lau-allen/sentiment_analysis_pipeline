#libraries 
import requests
from bs4 import BeautifulSoup

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


    def url_soup_filter(self,soup) -> tuple:
        print(soup.find_all('li',{'class': 'story-item svelte-j82fdi'}))
        
        #find <a> tages used for links, where tags have href attribute from soup object
        #all_href = map(lambda x: x.get('href'),soup.find_all('a',href=True))

        #print(list(all_href))
        #filter to url links 
        #url = filter(lambda x: filter_function(x,config.block_list,config.ad_block_list), all_href)
        return 1,1
        
    def all_links(self) -> dict:
        #define dictionary of data 
        url_linkdata = {}
        #request HTML from url and store into a dictionary format
        for url in self.data_sources:
            #request site 
            r = requests.get(url, headers={'user-agent': 'my-app/0.0.1'})
            #create bs4 soup 
            soup = BeautifulSoup(r.text,'lxml')
            #filter for links and link titles 
            url_data = self.url_soup_filter(soup)

            #add data into dict 
            url_linkdata[url] = r 
        return url_linkdata
    



if __name__ == '__main__':
    urls = ['https://finance.yahoo.com/news/']
    ws = web_scraper(urls)
    test = ws.all_links()
    
