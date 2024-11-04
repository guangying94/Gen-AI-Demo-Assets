# Common Utilities Using Azure Open AI
This repository is a quick, sample code to use Azure Open AI as general purpose API such as classification and entity extraction from text. Primary model being used is GPT4o and GPT4o-mini.

The app is built based on Python streamlit as frontend, and developer can customize the backend and expose as API for external integration.

## Capability
1. Multi-level classification
2. Entity extraction from form (with options to leverage Azure Document Intelligence as enhancement)

## How to use this code
Create a python virtual environment and install the required packages.
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

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
