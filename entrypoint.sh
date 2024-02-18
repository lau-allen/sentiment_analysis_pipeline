#!/bin/bash

#azure account login 
az login

#get Prefect cloud API key from Azure Key Vault 
export PREFECT__CLOUD__API_KEY=$(az keyvault secret show --vault-name prefectsentimentanalysis --name prefect-key --query value -o tsv)

#check if secrete retrieval was successful 
if [ $? -ne 0 ]; then
    echo "Error retrieving Prefect Cloud API key from Azure Key Vault"
    exit 1
fi

#log message for successful key retrieval 
echo "Prefect Cloud API key retrieved successfully."

#login to prefect cloud
prefect cloud login -k $PREFECT__CLOUD__API_KEY

#run defined deployment 
prefect deployment run webscrape-extract/webscrape-extract

#start default agent 
prefect agent start -q 'default' --run-once
