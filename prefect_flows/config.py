#set of urls to exclude from yahoo finance news results  
yahoo_fin_block_set = set(['https://www.yahoo.com/', 'https://mail.yahoo.com/', 'https://news.yahoo.com/',
                'https://finance.yahoo.com/', 'https://sports.yahoo.com/', 'https://www.yahoo.com/entertainment/',
                'https://search.yahoo.com/search/', 'https://mobile.yahoo.com/', 'https://www.yahoo.com/everything/', 
                'https://finance.yahoo.com', '#Nav-0-DesktopNav', '#market-summary', 
                '#Aside', 'https://login.yahoo.com/config/login?.src=finance&.intl=us&.lang=en-US&.done=https%3A%2F%2Ffinance.yahoo.com%2Fnews%2F&activity=uh-signin&pspid=1183300073',
                'https://help.yahoo.com/kb/finance-for-web/SLN2310.html?locale=en_US', 
                'https://help.yahoo.com/kb/finance-for-web', 'https://yahoo.uservoice.com/forums/382977', 
                'https://guce.yahoo.com/terms?locale=en-US', 'https://guce.yahoo.com/privacy-policy?locale=en-US', 
                'https://guce.yahoo.com/privacy-dashboard?locale=en-US', 'https://policies.oath.com/us/en/oath/privacy/adinfo/index.html', 
                'https://finance.yahoo.com/sitemap/', 'https://twitter.com/YahooFinance', 'https://facebook.com/yahoofinance', 
                'https://www.linkedin.com/company/yahoo-finance','/', '/watchlists/', '/portfolios/', '/calendar/', '/news/', '/videos/', 
                '/plus-dashboard?ncid=dcm_306158762_490172245_127172993', '/screener/', '/topic/personal-finance/', 
                '/crypto/', '/sectors', '/news/', '/topic/yahoo-finance-originals/', '/topic/stock-market-news/', 
                '/topic/earnings/', '/live/politics/', '/topic/economic-news/', '/topic/morning-brief/', '/topic/personal-finance-news/',
                '/topic/crypto/', '/bidenomics/', '/quote/ES%3DF', '/chart/ES%3DF', '/quote/YM%3DF', '/chart/YM%3DF', '/quote/NQ%3DF', '/chart/NQ%3DF', '/quote/RTY%3DF', '/chart/RTY%3DF', 
                '/quote/CL%3DF', '/chart/CL%3DF', '/quote/GC%3DF', '/chart/GC%3DF'])

#define list of top-level websites to scrape 
top_level_websites = ['https://finance.yahoo.com/news/','https://www.marketwatch.com/latest-news?mod=top_nav']

#define name of S3 bucket Prefect Block 
s3_block = 'sap-webscrape-extract-s3-bucket'

#define AWS region name 
aws_region = 'us-east-1'

#define AWS Redshift connection secret name 
redshift_secret = 'redshift_secret'