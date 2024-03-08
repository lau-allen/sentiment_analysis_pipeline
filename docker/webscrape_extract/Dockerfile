#base image 
FROM prefecthq/prefect:2-python3.10-conda

#dependencies
RUN apt-get update && apt-get install -y \
    git \
    wget \
    unzip 

# #install Azure CLI 
# RUN pip install azure-cli

#specify desired versions
ENV CHROME_VERSION=114.0.5735.90
ENV CHROMEDRIVER_VERSION=114.0.5735.90

#install Chrome and dependencies 
RUN wget https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_${CHROME_VERSION}-1_amd64.deb
RUN apt install -y ./google-chrome-stable_${CHROME_VERSION}-1_amd64.deb

#install ChromeDriver for Selenium Workflows 
RUN wget https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip -d /usr/local/bin/
RUN rm chromedriver_linux64.zip

#change working dir 
WORKDIR /opt 

#clone pipeline repo 
RUN git clone https://github.com/lau-allen/sentiment_analysis_pipeline.git
#change working dir 
WORKDIR /opt/sentiment_analysis_pipeline
#install dependencies for pipeline 
RUN pip install --trusted-host pypi.python.org -r ./docker/webscrape_extract/requirements.txt 

# #set up environment variable for Azure Key Vault URI
# ENV AZURE_KEY_VAULT_URI=https://prefectsentimentanalysis.vault.azure.net/

#ensure permissions to run entrypoint 
RUN chmod +x /opt/sentiment_analysis_pipeline/docker/webscrape_extract/entrypoint.sh
#run entry point script 
WORKDIR /opt/sentiment_analysis_pipeline
ENTRYPOINT ["/opt/sentiment_analysis_pipeline/docker/webscrape_extract/entrypoint.sh"]

