import os
from dotenv import load_dotenv
from helper import upload_pdf_to_blob, convert_pdf_to_images_and_upload, extract_content_from_images
from docs_intelligence_helper import analyze_read
from openai import AzureOpenAI

load_dotenv()

STORAGE_ACCOUNT_NAME = os.getenv('AZURE_STORAGE_ACCOUNT_NAME')
CONTAINER_NAME = os.getenv('AZURE_STORAGE_CONTAINER_NAME')
AOAI_KEY = os.getenv('AOAI_KEY')
AOAI_ENDPOINT = os.getenv('AOAI_ENDPOINT')
GPT4O_MINI_MODEL_DEPLOYMENT_NAME = os.getenv('GPT4O_MINI_MODEL_DEPLOYMENT_NAME')
SEARCH_ENDPOINT = os.getenv('AI_SEARCH_ENDPOINT')
SEARCH_KEY = os.getenv('AI_SEARCH_KEY')
SEARCH_INDEX = os.getenv('AI_SEARCH_INDEX')
GEN_SEARCH_INDEX = os.getenv('AI_GEN_SEARCH_INDEX')

def upload_pdf_extract_di(pdf_document, current):
    pdf_url = upload_pdf_to_blob(pdf_document, current)
    content = analyze_read(pdf_url)
    return content


def generate_docs_from_pdf(pdf_document, current):
    image_url, di_content = convert_pdf_to_images_and_upload(pdf_document, current, use_document_intelligence=True)
    system_prompt = "You are an AI assistant that generate knowledge base based on instruction manuals with images. You extract all text without summarizing them, as well as generate very descriptive caption for any images seen. Do not use markdown image syntax, only use description text for the images. Include tables if there's any as markdown. You generate markdown format, which is optimized for chucking in vector database and optimized for retrieval augmented generation application. You will be given content extracted via OCR as reference, prioritize the image content. OCR content: \n\n" + di_content

    content = extract_content_from_images(system_prompt, image_url)
    return content

def generate_docs_response(conversation, use_gen_index):
    client = AzureOpenAI(
        api_key=AOAI_KEY,
        api_version="2024-02-15-preview",
        azure_endpoint=AOAI_ENDPOINT,
    )

    messages = [
        {
            "role": "system",
            "content": "You are an AI assistant that help user to find information from a document. You only derive response based on document. Answer 'I don't have the information' if you don't have the information.",
        }
    ]

    messages.extend(conversation)

    index = GEN_SEARCH_INDEX if use_gen_index else SEARCH_INDEX

    completion = client.chat.completions.create(
        model=GPT4O_MINI_MODEL_DEPLOYMENT_NAME,
        messages=messages,
        max_tokens=800,
        temperature=0.7,
        top_p=0.95,
        stream=False,
        extra_body={
            "data_sources": [{
            "type": "azure_search",
            "parameters": {
            "endpoint": f"{SEARCH_ENDPOINT}",
            "index_name": f"{index}",
            "authentication": {
              "type": "api_key",
              "key": f"{SEARCH_KEY}"
            }
          }
        }]
        }
    )

    return completion.choices[0].message.content