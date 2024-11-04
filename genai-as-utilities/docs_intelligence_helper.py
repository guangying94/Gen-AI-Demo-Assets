import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

load_dotenv()

endpoint = os.environ["DOCS_INTELLIGENCE_ENDPOINT"]
key = os.environ["DOCS_INTELLIGENCE_KEY"]

def analyze_read(document_url):
    # Create a DocumentAnalysisClient with the given endpoint and credentials
    document_analysis_client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    
    # Start the analysis of the document from the URL using the "prebuilt-read" model
    poller = document_analysis_client.begin_analyze_document_from_url("prebuilt-read", document_url=document_url)

    # Retrieve the result of the analysis
    result = poller.result()

    # Initialize a string to accumulate the detected content
    detected_content = ''

    # If the result contains paragraphs
    if result.paragraphs:
        print(f"----Detected #{len(result.paragraphs)} paragraphs in the document----")
        # Loop through each paragraph in the result
        for paragraph in result.paragraphs:
            # Append the paragraph content to the detected_content string with a newline
            detected_content += paragraph.content + '\n'

    print("----------------------------------------")
    # Print all the detected content
    print(detected_content)
    # Return the detected content
    return detected_content