import streamlit as st
import json
import helper

st.title('🗣️ Feedback Classification')

default_prompt = "You are an AI Assistant for a city council. You receive feedback from residents about various issues. You need to classify the feedback into different categories and subcategories based on given categories below. You need to classify the feedback into one of the categories and one of the subcategories. You only response in text, so you need to provide the category and subcategory in text format. For example, if the feedback is about a broken road, you need to classify it as Category: Infrastructure \n Sub-category: Roads."

default_list_of_categories = [
        {
            "Category": "Infrastructure",
            "Subcategories": [
                "Roads",
                "Public Transport"
            ]
        },
                {
            "Category": "Public Services",
            "Subcategories": [
                "Healthcare",
                "Education"
            ]
        },
                {
            "Category": "Safety",
            "Subcategories": [
                "Police",
                "Fire Department"
            ]
        },
                {
            "Category": "Environment",
            "Subcategories": [
                "Waste Management",
                "Parks and Recreation"
            ]
        },
                {
            "Category": "Utilities",
            "Subcategories": [
                "Water Supply",
                "Electricity"
            ]
        }
    ]

st.sidebar.subheader("Instruction To AI")

# Add a sidebar with a text box
prompt = st.sidebar.text_area("System Prompt", default_prompt)

st.sidebar.subheader("List of Categories")
list_of_categories = st.sidebar.text_area("Categories JSON", json.dumps(default_list_of_categories, indent=3))

st.sidebar.subheader("How To Use")
st.sidebar.write("1. Enter the feedback in the text area below.")
st.sidebar.write("2. Click the 'Submit' button.")
st.sidebar.write("3. The AI will classify the feedback into a category and subcategory based on the given categories.")

st.sidebar.subheader("How It Works")
st.sidebar.write("1. The list of categories is shared to Azure Open AI as prompt to perform classification.")
st.sidebar.write("2. This can be customized by changing the category and subcategory list in the json above.")

# Add a text area for the user to enter text
user_input = st.text_area("Feedback")

# Add a button to call helper.call_aoai
if st.button("Submit"):
    prompt = f"{prompt}\n\n List of available category: {list_of_categories}"
    response = helper.call_aoai(prompt, user_input)
    st.text_area("Category", response)