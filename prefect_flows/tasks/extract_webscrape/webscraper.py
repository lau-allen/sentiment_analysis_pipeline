

class web_scraper:
    """
    web_scaper object encapsulates all logic for 
    web scraping HTML data sources
    """

    def __init__(self,url_sources:list) -> None:
        """Generator 

        Args:
            url_sources (list): list of URLs to scrape 
        """
        self.data_sources = url_sources
        self.length = len(self.data_sources)


if __name__ == '__main__':
    urls = ['https://finance.yahoo.com/news/']
    ws = web_scraper(urls)
    print(ws.length)
    
