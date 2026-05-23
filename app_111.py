import yfinance as yf
import pandas as pd
import streamlit as st

st.title("퀀트 투자 조건 검색기 (NASDAQ 100)")

# 조건 입력
per_max = st.number_input("최대 PER", value=20.0)
pbr_max = st.number_input("최대 PBR", value=3.0)
roe_min = st.number_input("최소 ROE", value=0.15)

# 나스닥 100 종목 리스트 (대표 티커들)
nasdaq_100 = [
    "AAPL","MSFT","GOOGL","AMZN","TSLA","NVDA","META","NFLX","INTC","AMD",
    "ADBE","CSCO","PEP","COST","AVGO","TXN","QCOM","AMAT","PYPL","SBUX",
    "MDLZ","BKNG","LRCX","INTU","ISRG","VRTX","REGN","GILD","ADP","MU",
    "PANW","KDP","MAR","MRNA","FTNT","KLAC","SNPS","MELI","CTAS","NXPI",
    "ORLY","PDD","IDXX","CDNS","ROST","WDAY","TEAM","ODFL","ANSS","CHTR",
    "CSX","AEP","XEL","PCAR","KHC","EXC","EA","VRSK","PAYX","AZN","BIIB",
    "ALGN","DLTR","SIRI","FAST","VRSN","EBAY","SGEN","ZS","ABNB","LCID",
    "RIVN","DOCU","OKTA","CRWD","DDOG","NTES","BIDU","JD","BKR","CEG",
    "SPLK","MTCH","CTSH","MRVL","SWKS","EXPE","LULU","FANG","WBD","CHKP",
    "ON","TTD","CPRT","CDW","CSGP","ODP","TTWO","FOX","FOXA","SJM","WBA"
]

# 버튼 클릭 시 실행
if st.button("조건에 맞는 나스닥 100 종목 찾기"):
    data = {}
    for t in nasdaq_100:
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

    st.subheader("조건을 만족하는 나스닥 100 종목")
    st.dataframe(filtered)

    # 선택한 종목 차트
    if not filtered.empty:
        chosen = st.selectbox("차트 확인할 종목 선택", filtered.index)
        hist = yf.Ticker(chosen).history(period="6mo")
        st.line_chart(hist["Close"])
