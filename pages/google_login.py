import os
import streamlit as st
from supabase import create_client, Client
from dotenv import find_dotenv, load_dotenv
from urllib.parse import urlencode
import re

load_dotenv(find_dotenv(), override=True)

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def extract_access_token_from_url():
    # JavaScript로 URL의 해시(#) 부분에서 access_token 추출
    st.markdown("""
        <script>
        function getAccessToken() {
            const url = window.location.href;
            const tokenMatch = url.match(/access_token=([^&]+)/);
            if (tokenMatch) {
                const accessToken = tokenMatch[1];
                // Streamlit에 전달
                window.parent.postMessage({isStreamlitToken: true, accessToken: accessToken}, "*");
            }
        }
        getAccessToken();
        </script>
    """, unsafe_allow_html=True)

# 메시지 리스너 설정
st.write("""
<script>
    window.addEventListener("message", (event) => {
        if (event.data.isStreamlitToken) {
            const accessToken = event.data.accessToken;
            Streamlit.setComponentValue(accessToken); // Streamlit의 세션에 저장
        }
    });
</script>
""", unsafe_allow_html=True)


def generate_login_url():
    # Supabase의 Google 로그인 URL 생성
    return f"{url}/auth/v1/authorize?provider=google&redirect_to=https://supaenter.streamlit.app/google_login"

st.title("Google 로그인 예제")

query_params = st.experimental_get_query_params()
access_token = query_params.get('access_token', [None])[0]

if access_token:
    st.session_state.access_token = access_token

    # 세션 상태 확인
if 'access_token' in st.session_state and st.session_state['access_token']:
    st.session_state['access_token'] = None

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

st.write(st.session_state.get('access_token', '토큰 없음'))

