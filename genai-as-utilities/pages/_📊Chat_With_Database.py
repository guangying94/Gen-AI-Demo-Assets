import streamlit as st
from helper import chat_with_azure_sql

st.title('📊 Chat With Database')

st.write("Please refer to sidebar on the instruction to connect to your database.")

st.sidebar.subheader("DB Configuration (Azure SQL)")
server = st.sidebar.text_input("Server", "guteegenaidemo.database.windows.net")
database = st.sidebar.text_input("Database", "BikeStores")

st.sidebar.subheader("How To Use")
st.sidebar.write("1. Provide the Azure SQL Database server and database name. Service Principal / managed identity is used to authenticate.")
st.sidebar.write("2. Enter the query in the text area below.")
st.sidebar.write("3. Click the 'Submit' button.")
st.sidebar.write("4. The AI will generate a T-SQL query based on the given query, and execute the query to database to formualate response.")

st.sidebar.subheader("How It Works")
st.sidebar.write("1. First, Azure Open AI is given the table schema, by querying the database for what table is available.")
st.sidebar.write("2. Based on the user query, the AI will generate a T-SQL query to fetch the data from the database.")
st.sidebar.write("3. The AI will execute the generated T-SQL query to fetch the data.")
st.sidebar.write("4. The AI will generate a response based on the fetched data.")


# Add a text area for the user to enter text
user_input = st.text_area("Your Question")

if st.button("Send"):
    response, t_sql = chat_with_azure_sql(user_input, server, database)
    st.markdown(response)
    with st.expander("Show T-SQL"):
        st.markdown(f"```sql\n{t_sql}\n```")