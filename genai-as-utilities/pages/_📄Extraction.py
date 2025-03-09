import streamlit as st
import helper
import fitz  # PyMuPDF
from datetime import datetime, timezone

default_field_extraction = 'Field 1, Field 2, Field 3'
default_prompt = "You are an AI Assistant that extract content from a PDF document. You response in json. You only extract the required fields given by the user."

st.title('📄 Information Extraction')


field_extraction = st.text_area('Field(s) to extract', default_field_extraction)

st.sidebar.subheader("Instruction To AI")

# Add a sidebar with a text box
prompt = st.sidebar.text_area("System Prompt", default_prompt)

use_di = st.sidebar.toggle("Enhance with Azure Document Intelligence")

st.sidebar.subheader("How To Use")
st.sidebar.write("1. Define the fields required for extraction.")
st.sidebar.write("2. Optionally, enable Azure Document Intelligence for enhanced extraction.")
st.sidebar.write("3. Upload a PDF document.")
st.sidebar.write("4. The AI will extract the content based on the given fields.")

st.sidebar.subheader("How It Works")
st.sidebar.write("1. The uploaded PDF is converted into images and stored in Azure Blob Storage. SAS url is generated for each image, and sent to Azure Open AI as input. The AI will extract the content based on the given fields.")
st.sidebar.write("2. Optionally, by enabling Azure Document Intelligence, the AI will use the extracted content from Azure Document Intelligence / Form Recognizer as additional input.")

uploaded_file = st.file_uploader("Choose a file", type=["pdf","jpg","png","jpeg"])

if uploaded_file is not None:
    # Read the uploaded file as a binary stream
    file_bytes = uploaded_file.read()

    # Check the file extension
    file_extension = uploaded_file.name.split(".")[-1]

    if(file_extension == "pdf"):
    
        # Open the PDF file with fitz
        uploaded = fitz.open(stream=file_bytes, filetype="pdf")
        current = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H-%M-%S")

        st.write(f'Processing {uploaded_file.name}...')

        list_of_images, ocr_content = helper.convert_pdf_to_images_and_upload(uploaded, current, use_di)
        print(list_of_images)
        print(ocr_content)

        if use_di:
            final_prompt = f"{prompt} You will given the extracted output from Azure Document Intelligence / Form Recognizer, as well as images. Prioritize the image as primary data source.\n\nFields to extract: {field_extraction} \n\n OCR content from Azure Document Intelligence: {ocr_content}"
        else:
            final_prompt = f"{prompt}\n\n Fields to extract: {field_extraction}"

        print(final_prompt)
        response = helper.extract_content_from_images(final_prompt, list_of_images)

        st.write(response)

    else:
        st.write(f'Processing {uploaded_file.name}...')
        current = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H-%M-%S")
        img_sas_url = helper.upload_image_to_blob(uploaded_file.name, file_bytes, current)
        urls = []
        urls.append(img_sas_url)
        st.write(f'Uploaded image to Azure Blob Storage: {img_sas_url}')

        if use_di:
            final_prompt = f"{prompt} You will given the extracted output from Azure Document Intelligence / Form Recognizer, as well as images. Prioritize the image as primary data source.\n\nFields to extract: {field_extraction} \n\n OCR content from Azure Document Intelligence: {ocr_content}"
        else:
            final_prompt = f"{prompt}\n\n Fields to extract: {field_extraction}"

        response = helper.extract_content_from_images(final_prompt, urls)
        st.write(response)
        
