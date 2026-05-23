import yfinance as yf
import pandas as pd
import streamlit as st
import requests
import io
import time

st.title("퀀트 투자 조건 검색기 (KOSPI 200 전체, 캐싱 버전)")

per_max = st.number_input("최대 PER", value=20.0)
pbr_max = st.number_input("최대 PBR", value=3.0)
roe_min = st.number_input("최소 ROE", value=0.15)

# 🔹 KRX에서 KOSPI200 종목 리스트 가져오기
@st.cache_data  # Streamlit 캐싱: 데이터 재사용
def load_kospi200():
    url = "http://data.krx.co.kr/comm/fileDn/download_csv/download_csv.cmd?code=200"
    res = requests.get(url)
    kospi200_df = pd.read_csv(io.BytesIO(res.content), encoding="euc-kr")
    kospi200_df["종목코드"] = kospi200_df["종목코드"].apply(lambda x: str(x).zfill(6))
    return [code + ".KS" for code in kospi200_df["종목코드"]]

kospi200_tickers = load_kospi200()

# 🔹 종목 데이터 가져오기 (캐싱)
@st.cache_data
def fetch_data(tickers, delay=1):
    data = {}
    for t in tickers:
        try:
            info = yf.Ticker(t).info
            data[t] = {
                "PER": info.get("trailingPE", None),
                "PBR": info.get("priceToBook", None),
                "ROE": info.get("returnOnEquity", None)
            }
            time.sleep(delay)  # Rate limit 방지
        except Exception as e:
            data[t] = {"PER": None, "PBR": None, "ROE": None}
    return pd.DataFrame(data).T

if st.button("조건에 맞는 KOSPI200 종목 찾기"):
    df = fetch_data(kospi200_tickers, delay=0.5).dropna()

    if not df.empty:
        filtered = df[
            (df["PER"] < per_max) &
            (df["PBR"] < pbr_max) &
            (df["ROE"] > roe_min)
        ]
        st.subheader("조건을 만족하는 KOSPI200 종목")
        st.dataframe(filtered)

        if not filtered.empty:
            chosen = st.selectbox("차트 확인할 종목 선택", filtered.index)
            hist = yf.Ticker(chosen).history(period="6mo")
            st.line_chart(hist["Close"])
    else:
        st.error("데이터를 불러오지 못했습니다. 잠시 후 다시 시도해주세요.")
