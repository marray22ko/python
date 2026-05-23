import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import time

# -----------------------------
# 1. 종목 리스트 설정
# -----------------------------
stocks = ["005930.KQ", "035720.KQ", "AAPL", "MSFT", "GOOGL"]

# -----------------------------
# 2. 데이터 가져오기 함수
# -----------------------------
def get_stock_data(stocks):
    data = []
    for ticker in stocks:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        name = info.get("longName", ticker)
        price = info.get("currentPrice", None)
        pe_ratio = info.get("forwardPE", None)
        pb_ratio = info.get("priceToBook", None)
        dividend_yield = info.get("dividendYield", None)
        market_cap = info.get("marketCap", None)
        
        data.append([name, price, pe_ratio, pb_ratio, dividend_yield, market_cap])
    return pd.DataFrame(data, columns=["종목명", "현재가", "PER", "PBR", "배당수익률", "시가총액"])

# -----------------------------
# 3. Streamlit UI
# -----------------------------
st.title("📈 실시간 저평가 우량주 대시보드")
st.write("국내·해외 주요 종목의 PER, PBR, 배당수익률을 실시간으로 확인합니다.")

# 새로고침 주기 설정
refresh_rate = st.slider("새로고침 주기 (초)", 10, 300, 60)

# 자동 업데이트 루프
placeholder = st.empty()

while True:
    df = get_stock_data(stocks)
    
    # 필터 조건
    per_limit = 15
    pbr_limit = 2
    cap_limit = 10_000_000_000_000
    
    filtered = df[(df["PER"] < per_limit) & (df["PBR"] < pbr_limit) & (df["시가총액"] > cap_limit)]
    
    with placeholder.container():
        st.subheader("저평가 우량주 후보")
        st.dataframe(filtered)
        
        sns.set(style="whitegrid")
        
        # PER vs PBR 산점도
        st.subheader("PER vs PBR 산점도")
        fig1, ax1 = plt.subplots(figsize=(8,6))
        sns.scatterplot(data=df, x="PER", y="PBR", hue="종목명", size="시가총액", sizes=(50, 500), ax=ax1)
        ax1.set_title("PER vs PBR")
        st.pyplot(fig1)
        
        # 배당수익률 막대그래프
        st.subheader("배당수익률 비교")
        fig2, ax2 = plt.subplots(figsize=(8,6))
        sns.barplot(data=df, x="종목명", y="배당수익률", ax=ax2)
        ax2.set_title("종목별 배당수익률")
        st.pyplot(fig2)
    
    time.sleep(refresh_rate)
