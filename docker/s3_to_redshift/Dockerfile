#base image 
FROM prefecthq/prefect:2-python3.10-conda

#dependencies
RUN apt-get update && apt-get install -y \
    git

# #install Azure CLI 
# RUN pip install azure-cli

#change working dir 
WORKDIR /opt 

#clone pipeline repo 
RUN git clone https://github.com/lau-allen/sentiment_analysis_pipeline.git
#change working dir 
WORKDIR /opt/sentiment_analysis_pipeline
#install dependencies for pipeline 
RUN pip install --trusted-host pypi.python.org -r ./docker/s3_to_redshift/requirements.txt

# #set up environment variable for Azure Key Vault URI
# ENV AZURE_KEY_VAULT_URI=https://prefectsentimentanalysis.vault.azure.net/

#ensure permissions to run entrypoint 
RUN chmod +x /opt/sentiment_analysis_pipeline/docker/s3_to_redshift/entrypoint.sh
#run entry point script 
WORKDIR /opt/sentiment_analysis_pipeline
ENTRYPOINT ["/opt/sentiment_analysis_pipeline/docker/s3_to_redshift/entrypoint.sh"]