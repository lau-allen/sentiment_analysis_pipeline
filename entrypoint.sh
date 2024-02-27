#!/bin/bash
# This is the default entrypoint for the official Prefect Docker image
set -e

if [ -f ~/.bashrc ]; then
  . ~/.bashrc
fi

if [ ! -z "$EXTRA_PIP_PACKAGES" ]; then
  echo "+pip install $EXTRA_PIP_PACKAGES"
  pip install $EXTRA_PIP_PACKAGES
fi

if [ -z "$*" ]; then
  echo -e "\nSentiment Analysis Pipeline \n"
else
  "$@"
fi

# Below are additional entrypoint setup for the pipeline

#always get updated source code
cd /opt/sentiment_analysis_pipeline
git config pull.rebase false
git pull

#TESTING CODE TO CHECKOUT TO BRANCHES 
echo "Choose a branch to check out:"
echo "1. Main"
echo "2. Dev"

read -p "Enter your choice (1 or 2): " choice

case $choice in
    1)
        git checkout main
        ;;
    2)
        git checkout dev
        ;;
    *)
        echo "Invalid choice. Please enter 1 or 2."
        ;;
esac

#present options to either run Prefect Cloud Deployment Workflow or just enter command line 
echo "Enter 1 to run Prefect Cloud Deployment. Enter 2 to enter command line."
read -p "Enter Option (1 or 2): " choice 

case $choice in
  1) 
    echo "Running Prefect Cloud Deployment."

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

    Start an interactive shell at the end
    exec /bin/bash
    ;; 
  
  2) 
    echo "Entering Command Line." 
    # Start an interactive shell at the end
    exec /bin/bash
    ;; 
  
  *) 
    echo "Invalid Choice. Please enter 1 or 2."
    ;;

esac