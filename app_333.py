import yfinance as yf
import pandas as pd
import streamlit as st
import time
import requests

st.title("퀀트 투자 조건 검색기 (KOSPI 200 전체)")

per_max = st.number_input("최대 PER", value=20.0)
pbr_max = st.number_input("최대 PBR", value=3.0)
roe_min = st.number_input("최소 ROE", value=0.15)

# 🔹 KRX에서 KOSPI200 종목 리스트 가져오기
url = "https://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13"
kospi200_df = pd.read_html(requests.get(url).text)[0]
kospi200_df["종목코드"] = kospi200_df["종목코드"].apply(lambda x: str(x).zfill(6))
kospi200_tickers = kospi200_df["종목코드"].tolist()
kospi200_tickers = [code + ".KS" for code in kospi200_tickers]  # 코스피 종목은 .KS

if st.button("조건에 맞는 KOSPI200 종목 찾기"):
    data = {}
    for t in kospi200_tickers:
        try:
            info = yf.Ticker(t).info
            data[t] = {
                "PER": info.get("trailingPE", None),
                "PBR": info.get("priceToBook", None),
                "ROE": info.get("returnOnEquity", None)
            }
            time.sleep(1)  # 요청 간격 두기 (Rate limit 방지)
        except Exception as e:
            st.warning(f"{t} 데이터 불러오기 실패: {e}")

    df = pd.DataFrame(data).T.dropna()

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
