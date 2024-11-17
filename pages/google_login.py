import os
import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# Supabase 클라이언트 설정
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

# 세션 상태에 access_token 초기화
if 'access_token' not in st.session_state:
    st.session_state['access_token'] = None

# JavaScript를 사용하여 해시 부분에서 access_token 추출 및 Streamlit에 전달
st.markdown("""
    <script>
    (function() {
        function getAccessToken() {
            const hash = window.location.hash;
            const tokenMatch = hash.match(/access_token=([^&]+)/);
            if (tokenMatch) {
                const accessToken = tokenMatch[1];
                // Streamlit에 전달
                const streamlitEvent = new CustomEvent("accessToken", {detail: accessToken});
                window.dispatchEvent(streamlitEvent);
            }
        }
        window.addEventListener("load", getAccessToken);
    })();
    </script>
""", unsafe_allow_html=True)

# JavaScript 이벤트 리스너 설정
st.write("""
    <script>
    window.addEventListener("accessToken", (event) => {
        const token = event.detail;
        if (token) {
            // Streamlit의 세션 상태에 access_token 저장
            fetch('/?access_token=' + token)
                .then(() => {
                    // 페이지 다시 로드
                    window.location.href = window.location.pathname;
                });
        }
    });
    </script>
""", unsafe_allow_html=True)

# 쿼리 파라미터에서 access_token 추출
query_params = st.query_params
access_token = query_params.get('access_token')

if access_token:
    st.session_state['access_token'] = access_token[0]  # 리스트의 첫 번째 요소 선택

# 세션 상태에서 access_token 확인 및 사용자 정보 가져오기
if st.session_state['access_token']:
    user_info = supabase.auth.get_user(st.session_state['access_token'])
    if user_info:
        st.write("로그인 상태입니다.")
        st.write(f"사용자 정보: {user_info.user.email}")
    else:
        st.write("사용자 정보를 가져오지 못했습니다.")
else:
    # 로그인 버튼 표시
    login_url = f"{url}/auth/v1/authorize?provider=google&redirect_to=https://supaenter.streamlit.app/"
    st.markdown(f"[Google로 로그인하기]({login_url})", unsafe_allow_html=True)
