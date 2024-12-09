# Common Utilities Using Azure Open AI
This repository is a quick, sample code to use Azure Open AI as general purpose API such as classification and entity extraction from text. Primary model being used is GPT4o and GPT4o-mini.

The app is built based on Python streamlit as frontend, and developer can customize the backend and expose as API for external integration.

## Capability
1. Multi-level classification
2. Entity extraction from form (with options to leverage Azure Document Intelligence as enhancement)
3. Chat With Database - perform retrival augmented generation from database
4. Chat With Document With Images - perform retrival augmented generation from document with images

## How to use this code
Create a python virtual environment and install the required packages.
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

In addition, you will need to install **ODBC driver for SQL Server**. You can follow the instruction [here](https://learn.microsoft.com/en-us/sql/connect/odbc/microsoft-odbc-driver-for-sql-server?view=sql-server-ver16).

Create a .env file and set the following environment variables. Replace with your own values
```bash
AZURE_STORAGE_CONNECTION_STRING='DefaultEndpointsProtocol=https;AccountName=xxxx;AccountKey=xxxx;EndpointSuffix=core.windows.net'
AZURE_STORAGE_ACCOUNT_NAME=xxxx
AZURE_STORAGE_CONTAINER_NAME=mini-app
AOAI_KEY=xxxxx
AOAI_ENDPOINT=https://xxxxxx.openai.azure.com/
GPT4O_MODEL_DEPLOYMENT_NAME=gpt4o-global
GPT4O_MINI_MODEL_DEPLOYMENT_NAME=gpt-4o-mini-global
DOCS_INTELLIGENCE_ENDPOINT=https://xxxxxxxx.cognitiveservices.azure.com/
DOCS_INTELLIGENCE_KEY=xxxxxx
AI_SEARCH_ENDPOINT=https://xxxxx.search.windows.net
AI_SEARCH_KEY=xxxxx
AI_SEARCH_INDEX=xxxxx
AI_GEN_SEARCH_INDEX=xxxxx

```

Then, run the app using streamlit command.
```bash
streamlit run Home.py
```

A Dockerfile is prepared for containerization. You can build the docker image and run the container.
```bash
docker build -t genai-as-utilities .
docker run -p 8501:8501 genai-as-utilities
```
