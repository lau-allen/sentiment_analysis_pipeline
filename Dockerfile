#base image 
FROM prefecthq/prefect:2-python3.11-conda

#dependencies
RUN apt-get update && apt-get install -y \
    git \
    azure-cli \
    wget \
    unzip 

#install Azure CLI 
RUN pip install azure-cli

#clone pipeline repo 
RUN git clone https://github.com/lau-allen/sentiment_analysis_pipeline.git

#install chrome and dependencies 
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt install -y ./google-chrome-stable_current_amd64.deb

#copy entry point script 
COPY entrypoint.sh /entrypoint.sh 

#set up environment variable for Azure Key Vault URI
ENV AZURE_KEY_VAULT_URI = https://prefectsentimentanalysis.vault.azure.net/

#run entry point script 
CMD ["/bin/bash", "/entrypoint.sh"]

