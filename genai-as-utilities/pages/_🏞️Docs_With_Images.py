import streamlit as st
import fitz
from datetime import datetime, timezone
from docs_with_images_helper import upload_pdf_extract_di, generate_docs_from_pdf, generate_docs_response

st.title('🏞️ Docs With Images')

st.subheader("Document Processing Details")
with st.expander("**With Document Intelligence Only**"):
    ocr_uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"], key="ocr")
    if ocr_uploaded_file is not None:
        file_bytes = ocr_uploaded_file.read()

        pdf_document = fitz.open(stream=file_bytes, filetype="pdf")
        current = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H-%M-%S")

        st.write(f'Processing {ocr_uploaded_file.name}...')
        content = upload_pdf_extract_di(pdf_document, current)
        st.write(content)

with st.expander("**With Generated Content from Azure Open AI + Document Intelligence**"):
    image_uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"], key="image")
    if image_uploaded_file is not None:
        file_bytes = image_uploaded_file.read()

        pdf_document = fitz.open(stream=file_bytes, filetype="pdf")
        current = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H-%M-%S")

        st.write(f'Processing {image_uploaded_file.name}...')
        content = generate_docs_from_pdf(pdf_document, current)

        st.markdown(content)

st.sidebar.subheader("Instruction to AI")

prompt = st.sidebar.text_area("System Prompt", "You are an AI assistant that generate knowledge base based on instruction manuals with images. You extract all text without summarizing them, as well as generate very descriptive caption for any images seen. Do not use markdown image syntax, only use description text for the images. Include tables if there's any as markdown. You generate markdown format, which is optimized for chucking in vector database and optimized for retrieval augmented generation application. You will be given content extracted via OCR as reference, prioritize the image content. OCR content:")

st.sidebar.subheader("How To Use")
st.sidebar.write("1. Upload a PDF document under **With Document Intelligence Only**.")
st.sidebar.write("2. Upload the same document for **With Generated Content from Azure Open AI + Document Intelligence**.")
st.sidebar.write("3. Compare the extracted results from both methods.")

st.sidebar.subheader("How It Works")
st.sidebar.write("1. **With Document Intelligence Only** is using Azure Document Intelligence to extract the content.")
st.sidebar.write("2. **With Generated Content from Azure Open AI + Document Intelligence** is using Azure Document Intelligence to extract the content, included in the prompt for Azure Open AI to generate content based on images.")
st.sidebar.write("3. The content generated from both method is ingested into different Azure Search index for retrieval.")



st.subheader("Chat With Docs With Images")

use_gen_index = st.toggle("Use Generated Document", False)

# Initialize session state messages if not already initialized
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("How can I help you today?"):

    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate assistant response
    print(st.session_state.messages)
    llm_result = generate_docs_response(st.session_state.messages, use_gen_index)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(llm_result)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": llm_result})
