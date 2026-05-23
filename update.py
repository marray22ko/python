import yfinance as yf
import pandas as pd

# 국내 + 해외 종목 리스트
stocks = ["005930.KQ", "035720.KQ", "AAPL", "MSFT", "GOOGL"]

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

# 데이터프레임으로 정리
df = pd.DataFrame(data, columns=["종목명", "현재가", "PER", "PBR", "배당수익률", "시가총액"])

# 필터링: PER < 15, PBR < 2, 시가총액 > 10조
filtered = df[(df["PER"] < 15) & (df["PBR"] < 2) & (df["시가총액"] > 10_000_000_000_000)]

print("저평가 우량주 후보:")
print(filtered)
