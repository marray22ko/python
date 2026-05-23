import openai
import pandas as pd
import streamlit as st
import yfinance as yf

st.title("퀀트 투자 조건 검색기 (KOSPI 200 전체, OpenAI 버전)")

# 조건 입력
per_max = st.number_input("최대 PER", value=20.0)
pbr_max = st.number_input("최대 PBR", value=3.0)
roe_min = st.number_input("최소 ROE", value=0.15)

# 예시 데이터프레임 (실제로는 KRX/네이버 금융에서 가져오기)
data = {
    "005930.KS": {"PER": 15.2, "PBR": 2.1, "ROE": 0.18},  # 삼성전자
    "000660.KS": {"PER": 25.0, "PBR": 3.5, "ROE": 0.12},  # SK하이닉스
    "051910.KS": {"PER": 18.0, "PBR": 2.8, "ROE": 0.20},  # LG화학
}
df = pd.DataFrame(data).T

if st.button("조건에 맞는 종목 찾기"):
    # OpenAI API 호출
    prompt = f"""
    아래 데이터에서 PER<{per_max}, PBR<{pbr_max}, ROE>{roe_min} 조건을 만족하는 종목만 골라줘.
    데이터: {df.to_dict()}
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role":"user","content":prompt}]
    )
    result = response["choices"][0]["message"]["content"]

    st.subheader("조건을 만족하는 종목")
    st.write(result)

    # 선택한 종목 차트
    chosen = st.selectbox("차트 확인할 종목 선택", df.index)
    hist = yf.Ticker(chosen).history(period="6mo")
    st.line_chart(hist["Close"])
