import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta, timezone
import fitz
from docs_intelligence_helper import analyze_read
import io

load_dotenv()

AOAI_KEY = os.getenv('AOAI_KEY')
AOAI_ENDPOINT = os.getenv('AOAI_ENDPOINT')
GPT4O_MODEL_DEPLOYMENT_NAME = os.getenv('GPT4O_MODEL_DEPLOYMENT_NAME')
GPT4O_MINI_MODEL_DEPLOYMENT_NAME = os.getenv('GPT4O_MINI_MODEL_DEPLOYMENT_NAME')
BLOB_CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
STORAGE_ACCOUNT_NAME = os.getenv('AZURE_STORAGE_ACCOUNT_NAME')
CONTAINER_NAME = os.getenv('AZURE_STORAGE_CONTAINER_NAME')

def call_aoai(system_prompt, content):
    # Create an AzureOpenAI client with the provided API key, version, and endpoint
    client = AzureOpenAI(
        api_key=AOAI_KEY,
        api_version="2024-02-15-preview",
        azure_endpoint=AOAI_ENDPOINT,
    )
    
    # Prepare the messages for the chat completion request
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": content},
    ]
    
    # Request a chat completion from the Azure OpenAI service
    response = client.chat.completions.create(
        model=GPT4O_MINI_MODEL_DEPLOYMENT_NAME,
        messages=messages
    )
    
    try:
        # Extract the generated content from the response
        content = response.choices[0].message.content
        return content
    except (TypeError, KeyError, IndexError) as e:
        # Handle exceptions and print the error message
        print(f"Error: {e}")
        return None

def convert_pdf_to_images_and_upload(pdf_document, current, use_document_intelligence=False):
    # Initialize a list to store SAS URLs and a variable for Document Intelligence content
    sas_urls = []
    di_content = None

    # If Document Intelligence is enabled, process the PDF using Azure services
    if use_document_intelligence:
        # Upload the PDF to Azure Blob Storage and get its URL
        pdf_url = upload_pdf_to_blob(pdf_document, current)
        # Analyze the PDF content using Azure Document Intelligence
        di_content = analyze_read(pdf_url)

    # Create a BlobServiceClient using the connection string
    blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
    
    # Iterate over each page in the PDF document
    for page_number in range(len(pdf_document)):
        page = pdf_document[page_number]
        # Define zoom factors to increase image resolution
        zoom_x = 2.0  # Horizontal zoom
        zoom_y = 2.0  # Vertical zoom
        matrix = fitz.Matrix(zoom_x, zoom_y)
        
        # Render the page to a pixmap with the specified zoom
        pix = page.get_pixmap(matrix=matrix)
        # Convert the pixmap to PNG image bytes
        image_bytes = pix.tobytes('png')
        
        # Define the blob name for the image
        image_blob_name = f'{current}_{page_number}.png'
        # Get a blob client for the image
        image_blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=image_blob_name)
        # Upload the image to Azure Blob Storage, overwriting if it exists
        image_blob_client.upload_blob(image_bytes, blob_type="BlockBlob", overwrite=True)

        # Generate a SAS token with read permission, valid for 60 minutes
        sas_token = generate_blob_sas(
            blob_service_client.account_name,
            CONTAINER_NAME,
            image_blob_name,
            account_key=blob_service_client.credential.account_key,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.now(timezone.utc) + timedelta(minutes=60),
            start=datetime.now(timezone.utc)
        )

        # Construct the SAS URL for the uploaded image
        sas_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{CONTAINER_NAME}/{image_blob_name}?{sas_token}"

        # Add the SAS URL to the list
        sas_urls.append(sas_url)
    
    # Return the list of SAS URLs and any Document Intelligence content
    return sas_urls, di_content

def upload_pdf_to_blob(pdf_document, current):
    # Convert the PyMuPDF Document to bytes
    pdf_bytes = io.BytesIO()
    pdf_document.save(pdf_bytes)
    pdf_bytes.seek(0)  # Reset the buffer position to the beginning
    
    # Create a BlobServiceClient using the connection string
    blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
    
    # Define the PDF file name in the blob storage
    pdf_name = f'{current}-uploaded.pdf'
    # Get a blob client for the PDF file
    pdf_blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=pdf_name)
    # Upload the PDF bytes to Azure Blob Storage, overwriting if it exists
    pdf_blob_client.upload_blob(pdf_bytes, blob_type="BlockBlob", overwrite=True)
    
    # Generate a SAS token with read permission, valid for 60 minutes
    sas_token = generate_blob_sas(
        blob_service_client.account_name,
        CONTAINER_NAME,
        pdf_name,
        account_key=blob_service_client.credential.account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.now(timezone.utc) + timedelta(minutes=60),
        start=datetime.now(timezone.utc)
    )
    
    # Construct the SAS URL for the uploaded PDF
    blob_sas_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{CONTAINER_NAME}/{pdf_name}?{sas_token}"
    # Return the SAS URL
    return blob_sas_url

def extract_content_from_images(system_prompts, sas_urls, di_content=None):
    # Create an AzureOpenAI client using the API key, version, and endpoint
    client = AzureOpenAI(
        api_key=AOAI_KEY,
        api_version="2024-02-15-preview",
        azure_endpoint=AOAI_ENDPOINT,
    )

    # Prepare the messages for the chat completion request
    if di_content is None:
        # If no Document Intelligence content, build messages with image URLs only
        messages = [
            {"role": "system", "content": system_prompts},
            {"role": "user", "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": sas_url}
                } for sas_url in sas_urls
            ]},
        ]
    else:
        # Include extracted text from Document Intelligence along with image URLs
        messages = [
            {"role": "system", "content": system_prompts},
            {"role": "user", "content": [
                {
                    "type": "text",
                    "text": f"Extracted text from Azure Document Intelligence as additional data: {di_content}"
                }
            ] + [
                {
                    "type": "image_url",
                    "image_url": {"url": sas_url}
                } for sas_url in sas_urls
            ]},
        ]

    # Request a chat completion from the Azure OpenAI service
    response = client.chat.completions.create(
        model=GPT4O_MINI_MODEL_DEPLOYMENT_NAME,
        messages=messages
    )

    print(response)

    try:
        # Extract the generated content from the response
        content = response.choices[0].message.content
        return content
    except (TypeError, KeyError, IndexError) as e:
        # Handle exceptions and print the error message
        print(f"Error: {e}")
        return None