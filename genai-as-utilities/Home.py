import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.title('Generative AI Mini Apps')


st.write('This app contains a collection of mini apps that demonstrate the capabilities of Generative AI models. Select a mini app from the sidebar to get started.')

content_extraction = st.button('📄 Information Extraction')
if content_extraction:
    switch_page('Extraction')

feedback_classification = st.button('🗣️ Feedback Classification')
if feedback_classification:
    switch_page('Feedback')
