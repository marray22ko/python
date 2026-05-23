import pandas as pd
import requests
from bs4 import BeautifulSoup

df = pd.read_csv(r"c:\python\상장종목.csv", encoding="cp949")
df["단축코드"] = df["단축코드"].apply(lambda x: str(x).zfill(6))

codes = df["단축코드"].tolist()
names = df["한글 종목명"].tolist()

results = []

for code, name in zip(codes[:50], names[:50]):  # 상위 50개만 테스트
    url = f"https://finance.naver.com/item/main.nhn?code={code}"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    
    try:
        finance_table = soup.select("table tbody tr")
        per = finance_table[3].select("td")[1].text.strip()
        pbr = finance_table[4].select("td")[1].text.strip()
        dividend = finance_table[5].select("td")[1].text.strip()
    except:
        per, pbr, dividend = None, None, None
    
    results.append([name, code, per, pbr, dividend])

df_result = pd.DataFrame(results, columns=["종목명", "종목코드", "PER", "PBR", "배당수익률"])

# 문자열 → 숫자 변환
df_result["PER"] = pd.to_numeric(df_result["PER"], errors="coerce")
df_result["PBR"] = pd.to_numeric(df_result["PBR"], errors="coerce")
df_result["배당수익률"] = pd.to_numeric(df_result["배당수익률"], errors="coerce")

# NaN 제거
df_result = df_result.dropna()

# 저평가 조건 적용
undervalued = df_result[(df_result["PER"] < 10) & (df_result["PBR"] < 1.5) & (df_result["배당수익률"] > 3)]

print("저평가 종목 후보:")
print(undervalued)

# ✅ 엑셀 파일로 저장
undervalued.to_excel(r"c:\python\undervalued.xlsx", index=False)
print("저평가 종목을 c:\\python\\undervalued.xlsx 파일로 저장했습니다.")
