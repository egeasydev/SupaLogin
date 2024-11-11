import os
from supabase import create_client, Client
import streamlit as st
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(), override=True)

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

email = st.text_input("email")
password = st.text_input("password")

if st.button("Submit"):
    response = supabase.auth.sign_up(
        {"email": email, "password": password}
    )
    st.write(response)



