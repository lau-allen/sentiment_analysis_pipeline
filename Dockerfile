#base image 
FROM prefecthq/prefect:2-python3.10-conda

#dependencies
RUN apt-get update && apt-get install -y \
    git \
    azure-cli \
    wget \
    unzip 

#install Azure CLI 
RUN pip install azure-cli

#install chrome and dependencies 
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt install -y ./google-chrome-stable_current_amd64.deb

#change working dir 
WORKDIR /opt 

#clone pipeline repo 
RUN git clone https://github.com/lau-allen/sentiment_analysis_pipeline.git
#change working dir 
WORKDIR /opt/sentiment_analysis_pipeline
#install dependencies for pipeline 
RUN pip install --trusted-host pypi.python.org -r requirements.txt 

#set up environment variable for Azure Key Vault URI
ENV AZURE_KEY_VAULT_URI=https://prefectsentimentanalysis.vault.azure.net/

#ensure permissions to run entrypoint 
RUN chmod +x /opt/sentiment_analysis_pipeline/entrypoint.sh
#run entry point script 
CMD ["/opt/sentiment_analysis_pipeline/entrypoint.sh"]

