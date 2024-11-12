import os
import streamlit as st
from supabase import create_client, Client
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(), override=True)

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def generate_login_url():
    redirect_uri = st.experimental_get_query_params().get('redirect_uri', [''])[0]
    if not redirect_uri:
        redirect_uri = st.experimental_get_url()
    return f"{url}/auth/v1/authorize?provider=google&redirect_to={redirect_uri}"


st.title("Google 로그인 예제")

# 로그인 상태 확인
st.title("Google 로그인 예제")

    # 세션 상태 확인
if 'access_token' not in st.session_state:
    st.session_state['access_token'] = None

# 로그인 상태 확인
if st.session_state['access_token']:
    # 액세스 토큰을 사용하여 사용자 정보 가져오기
    user_info = supabase.auth.get_user(st.session_state['access_token'])
    if user_info:
        st.write("로그인 상태입니다.")
        st.write(f"사용자 정보: {user_info.user.email}")
    else:
        st.write("사용자 정보를 가져오지 못했습니다.")
else:
    # 로그인 버튼 표시
    login_url = generate_login_url()
    st.markdown(f"[Google로 로그인하기]({login_url})", unsafe_allow_html=True)