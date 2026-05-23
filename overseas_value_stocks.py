import requests
import pandas as pd

url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
headers = {"User-Agent": "Mozilla/5.0"}  # 브라우저처럼 위장
response = requests.get(url, headers=headers)

# HTML에서 표 추출
sp500 = pd.read_html(response.text)[0]
stocks = sp500["Symbol"].tolist()

print("S&P500 종목 예시:", stocks[:10])


import yfinance as yf

data = []
for ticker in stocks[:50]:  # 속도 문제 때문에 50개만 테스트
    stock = yf.Ticker(ticker)
    info = stock.info
    data.append([
        info.get("longName", ticker),
        info.get("currentPrice", None),
        info.get("forwardPE", None),
        info.get("priceToBook", None),
        info.get("dividendYield", None),
        info.get("marketCap", None)
    ])

df = pd.DataFrame(data, columns=["종목명","현재가","PER","PBR","배당수익률","시가총액"])

# 저평가 조건 필터링
filtered = df[(df["PER"] < 15) & (df["PBR"] < 2) & (df["시가총액"] > 10_000_000_000)]
print("저평가 우량주 후보:")
print(filtered)
