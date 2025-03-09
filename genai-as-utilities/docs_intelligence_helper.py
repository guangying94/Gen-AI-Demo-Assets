import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, DocumentAnalysisFeature

load_dotenv()

endpoint = os.environ["DOCS_INTELLIGENCE_ENDPOINT"]
key = os.environ["DOCS_INTELLIGENCE_KEY"]

def analyze_read(document_url):
    docs_intelligence_client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    docs_request = AnalyzeDocumentRequest(url_source=document_url)

    # Add the feature to extract text
    docs_analysis_feature = [DocumentAnalysisFeature.OCR_HIGH_RESOLUTION, DocumentAnalysisFeature.LANGUAGES]

    # Start the analysis of the document from the URL using the "prebuilt-read" model
    poller = docs_intelligence_client.begin_analyze_document("prebuilt-read", docs_request, features=docs_analysis_feature)

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