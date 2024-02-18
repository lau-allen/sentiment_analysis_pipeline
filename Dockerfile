#base image 
FROM prefecthq/prefect:2-python3.11-conda

#dependencies
RUN apt-get update && apt-get install -y \
    git \
    azure-cli \
    expect

#install Azure CLI 
RUN pip install azure-cli

RUN git clone https://github.com/lau-allen/sentiment_analysis_pipeline.git

#copy entry point script 
COPY entrypoint.sh /entrypoint.sh 

#set up environment variable for Azure Key Vault URI
ENV AZURE_KEY_VAULT_URI = https://prefectsentimentanalysis.vault.azure.net/

#run entry point script 
CMD ["/bin/bash", "/entrypoint.sh"]

