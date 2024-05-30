import os
import requests
import json
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta, timezone
import fitz

BLOB_CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
CONTAINER_NAME = os.getenv('AZURE_CONTAINER_NAME')
GPT4_KEY = os.getenv('GPT4_KEY')
GPT4_ENDPOINT = os.getenv('GPT4_ENDPOINT')

def convert_pdf_to_images_and_upload(pdf_document, current):
    """
    This function is used to convert a PDF document into images and upload them to Azure Blob Storage.

    Parameters:
    pdf_document (fitz.Document): The PDF document to be converted.
    current (str): A string used to name the images.

    Returns:
    list: A list of SAS URLs for the uploaded images.

    The function first creates a BlobServiceClient object using a connection string. 
    It then iterates over each page of the PDF document. 
    Each page is converted to an image with a zoom factor of 2.0 for increased resolution. 
    The image is then saved to Azure Blob Storage with a name based on the 'current' parameter and the page number. 
    A SAS URL is generated for the image with a 1-hour expiry time. 
    The SAS URL is appended to a list. 
    After all pages have been processed, the function returns the list of SAS URLs.
    """
    blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
    sas_urls = []
    # Convert each page to an image
    for page_number in range(len(pdf_document)):
        page = pdf_document[page_number]
        # Set the zoom factor to increase the resolution
        zoom_x = 2.0  # Horizontal zoom
        zoom_y = 2.0  # Vertical zoom
        matrix = fitz.Matrix(zoom_x, zoom_y)
        
        pix = page.get_pixmap(matrix=matrix)
        image_bytes = pix.tobytes('png')
        
        # Save the image to Azure Blob Storage
        image_blob_name = f'{current}_{page_number}.png'
        image_blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=image_blob_name)
        image_blob_client.upload_blob(image_bytes, blob_type="BlockBlob",overwrite=True)

        # generate sas url, with 1 hour expiry, then return to client
        sas_token = generate_blob_sas(
            blob_service_client.account_name,
            CONTAINER_NAME,
            image_blob_name,
            account_key=blob_service_client.credential.account_key,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.now(timezone.utc) + timedelta(minutes=60),
            start=datetime.now(timezone.utc)
        )

        sas_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{CONTAINER_NAME}/{image_blob_name}?{sas_token}"

        sas_urls.append(sas_url)
    return sas_urls

def process_with_gpt4(urls):
    """
    This function is used to process a list of URLs with the GPT-4 model.

    Parameters:
    urls (list): A list of URLs to be processed.

    Returns:
    None

    The function prints a message indicating the start of the processing. 
    It then sets the GPT4_KEY and GPT4_ENDPOINT variables, which are used for authentication and specifying the endpoint for the GPT-4 model respectively.
    The function sets up the headers for the HTTP request, which includes the Content-Type and the api-key.
    It also sets up the payload for the HTTP request, which includes a list of messages. Each message has a role and content. 
    The content is a list of dictionaries, where each dictionary represents a content item. 
    In this case, the content item is a text message that describes the role of the AI assistant.
    """

    print("Processing with GPT-4..")

    headers = {
        "Content-Type": "application/json",
        "api-key": GPT4_KEY
    }

    payload = {
        "messages":[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "You are an AI assistant that extract information from medical certificate. You only response as JSON."
                    
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": 
                        {
                            "url": url
                        }
                    } for url in urls
                ] + [
                    {
                        "type": "text",
                        "text": "extract patient name, NRIC, hospital name, leave date and duration. for NRIC, only keep the last 4 characters. reply in JSON. Sample response: {\"name\": \"name\", \"NRIC\": \"123D\", \"hospital\": \"hospital\", \"duration_day\": 3, \"from_date\": \"2024-01-01\", \"to_date\": \"2024-01-02\"}. "
                    }
                ]
            }
        ],
        "temperature": 0.7,
        "max_tokens": 800,
        "top_p": 0.95,
    }

    # Send the request to GPT-4
    try:
        response = requests.post(GPT4_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error processing with GPT-4: {e}")
    
    return process_json_response(response)


def process_json_response(response):
    """
    This function is used to process the JSON response from an HTTP request.

    Parameters:
    response (requests.Response): The response from an HTTP request.

    Returns:
    dict: The processed JSON content from the response.

    The function first prints the raw response. It then extracts the JSON content from the response and retrieves the message from the 'choices' field.
    The message, which is a dictionary, is converted to a JSON string.
    The function then cleans up the string by removing certain substrings ("```json", "```", and "\\n").
    Finally, the cleaned string is parsed as JSON and returned.
    """
    data = response.json()
    message = data['choices'][0]['message']['content']
    # Convert the dictionary to a JSON string
    message_str = json.dumps(message)
    
    # Clean up the string
    message_str = message_str.replace("```json", "")
    message_str = message_str.replace("```", "")
    message_str = message_str.replace("\\n", "")

    # Parse the cleaned string as JSON
    message_json = json.loads(message_str)
    
    return message_json