import yfinance as yf
import pandas as pd

# 검색할 종목 리스트 (예: 삼성전자, 애플, 마이크로소프트)
stocks = ["005930.KQ", "AAPL", "MSFT"]

data = []

for ticker in stocks:
    stock = yf.Ticker(ticker)
    info = stock.info
    
    # 주요 지표 추출
    name = info.get("longName", ticker)
    price = info.get("currentPrice", None)
    pe_ratio = info.get("forwardPE", None)
    market_cap = info.get("marketCap", None)
    
    data.append([name, price, pe_ratio, market_cap])

# 데이터프레임으로 정리
df = pd.DataFrame(data, columns=["종목명", "현재가", "PER", "시가총액"])

# PER이 낮은 순으로 정렬
df_sorted = df.sort_values(by="PER", ascending=True)

print("저평가 우량주 후보:")
print(df_sorted)
