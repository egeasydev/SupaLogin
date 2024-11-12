import os
import streamlit as st
from supabase import create_client, Client
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(), override=True)

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def generate_auth_url():
    from urllib.parse import urlencode
    params = {
        "provider": "google",
        "redirect_to": st.experimental_get_url()  # Streamlit 앱의 URL
    }
    query_string = urlencode(params)
    return f"https://{url}/auth/v1/authorize?{query_string}"


st.title("Google 로그인 예제")

# 로그인 상태 확인
session = supabase.auth.session()
    if session:
        user = session['user']
        if user:
            st.write("로그인 상태입니다.")
            st.write(f"사용자 정보: {user['email']}")
        else:
            st.write("로그인 상태가 아닙니다.")
    else:
        st.write("로그인 상태가 아닙니다.")
