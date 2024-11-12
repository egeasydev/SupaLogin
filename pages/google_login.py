import os
import streamlit as st
from supabase import create_client, Client
from dotenv import find_dotenv, load_dotenv
from urllib.parse import urlencode

load_dotenv(find_dotenv(), override=True)

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def generate_login_url():
    params = {
        "provider": "google",
        "redirect_to": "https://fnucjhunzytgevnujnxs.supabase.co"
    }
    query_string = urlencode(params)
    return f"{url}/auth/v1/authorize?{query_string}"



st.title("Google 로그인 예제")
st.write(user_info)
query_params = st.experimental_get_query_params()

    # 세션 상태 확인
if 'access_token' in query_params:
    access_token = query_params['access_token'][0]
    user_info = supabase.auth.get_user(access_token)

    if user_info:
                st.write("로그인 상태입니다.")
                st.write(f"사용자 정보: {user_info.user.email}")
    else:
        st.write("사용자 정보를 가져오지 못했습니다.")
else:
    # 로그인 버튼 표시
    login_url = generate_login_url()
    st.markdown(f"[Google로 로그인하기]({login_url})", unsafe_allow_html=True)
    if st.button("Google로 로그인"):
        st.experimental_set_query_params(redirect="https://supaenter.streamlit.app")
        st.rerun()


