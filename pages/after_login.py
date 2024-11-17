import os
import streamlit as st
from streamlit_url_fragment import get_fragment
from supabase import create_client
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# Supabase 클라이언트 설정
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

# 세션 상태 초기화
# if 'access_token' not in st.session_state:
#     st.session_state['access_token'] = None
#
# # JavaScript로 해시 프래그먼트에서 Access Token 추출 및 쿼리 파라미터로 변환
# st.markdown("""
# <script>
# (function() {
#     function extractToken() {
#         const hash = window.location.hash;
#         const tokenMatch = hash.match(/access_token=([^&]+)/);
#         if (tokenMatch) {
#             const accessToken = tokenMatch[1];
#             const currentUrl = window.location.href.split('#')[0]; // # 이전 부분만 남김
#             const newUrl = currentUrl + "?access_token=" + accessToken; // 쿼리 파라미터 추가
#             window.location.replace(newUrl); // 페이지 리로드
#         }
#     }
#     if (window.location.hash.includes("access_token")) {
#         extractToken();
#     }
# })();
# </script>
# """, unsafe_allow_html=True)
#
# # 쿼리 파라미터에서 Access Token 추출
# query_params = st.query_params
# access_token = query_params.get('access_token')
#
# if access_token:
#     st.session_state['access_token'] = access_token[0]
#
# # Access Token이 세션에 저장되어 있으면 사용자 정보 가져오기
# if st.session_state['access_token']:
#     try:
#         user_info = supabase.auth.get_user(st.session_state['access_token'])
#         if user_info:
#             st.write("로그인 상태입니다.")
#             st.write(f"사용자 정보: {user_info.user.email}")
#             if st.button("로그아웃"):
#                 st.session_state['access_token'] = None
#                 st.rerun()
#         else:
#             st.write("사용자 정보를 가져오지 못했습니다.")
#     except Exception as e:
#         st.session_state['access_token'] = None
#         st.write("로그인 세션이 만료되었습니다. 다시 로그인해주세요.")
# else:
#     st.write("로그인하지 않았습니다.")

current_value = get_fragment()
st.write("Current value: {!r}".format(st.session_state.get('access_token', None)), key="unique_key_debug_output")
