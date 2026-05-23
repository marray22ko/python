import yfinance as yf
import pandas as pd
import streamlit as st

# 앱 제목
st.title("퀀트 투자 조건 검색기")

# 종목 입력
tickers = st.text_input("종목 티커 입력 (쉼표로 구분)", "AAPL, MSFT, GOOGL, TSLA, AMZN")
tickers = [t.strip() for t in tickers.split(",")]

# 조건 입력 (UI 요소)
per_max = st.number_input("최대 PER", value=20.0)
pbr_max = st.number_input("최대 PBR", value=3.0)
roe_min = st.number_input("최소 ROE", value=0.15)

# 데이터 수집
data = {}
for t in tickers:
    try:
        info = yf.Ticker(t).info
        data[t] = {
            "PER": info.get("trailingPE"),
            "PBR": info.get("priceToBook"),
            "ROE": info.get("returnOnEquity")
        }
    except Exception as e:
        st.warning(f"{t} 데이터 불러오기 실패: {e}")

df = pd.DataFrame(data).T

# 조건 필터링
filtered = df[
    (df["PER"] < per_max) &
    (df["PBR"] < pbr_max) &
    (df["ROE"] > roe_min)
]

# 결과 출력
st.subheader("조건을 만족하는 종목")
st.dataframe(filtered)

# 선택한 종목 주가 차트
if not filtered.empty:
    chosen = st.selectbox("차트 확인할 종목 선택", filtered.index)
    hist = yf.Ticker(chosen).history(period="6mo")
    st.line_chart(hist["Close"])
