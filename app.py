import streamlit as st

st.title("내 Streamlit 앱 모음")
st.write("여기서 원하는 앱을 선택하세요.")

# 버튼으로 다른 앱으로 이동
if st.button("조건 필터형 퀀트 검색기 열기"):
    st.markdown('<a href="https://python-7qve9iqwvzj8n5kzezmvoq.streamlit.app/" target="_blank">👉 이동하기</a>', unsafe_allow_html=True)

if st.button("가치투자 분석 열기"):
    st.markdown('<a href="https://python-gmzcymqjhkdah3aamk2uaa.streamlit.app/" target="_blank">👉 이동하기</a>', unsafe_allow_html=True)
