import tkinter as tk
from tkinter import messagebox
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import threading

def run_analysis():
    start_time = time.time()
    results = []

    try:
        df = pd.read_csv(r"c:\python\상장종목.csv", encoding="cp949")
        df["단축코드"] = df["단축코드"].apply(lambda x: str(x).zfill(6))

        codes = df["단축코드"].tolist()
        names = df["한글 종목명"].tolist()
        total = len(codes)

        for i, (code, name) in enumerate(zip(codes, names), start=1):
            url = f"https://finance.naver.com/item/main.nhn?code={code}"
            headers = {"User-Agent": "Mozilla/5.0"}
            try:
                res = requests.get(url, headers=headers, timeout=5)
                soup = BeautifulSoup(res.text, "html.parser")

                finance_table = soup.select("table tbody tr")
                per = finance_table[3].select("td")[1].text.strip()
                pbr = finance_table[4].select("td")[1].text.strip()
                dividend = finance_table[5].select("td")[1].text.strip()
            except Exception:
                per, pbr, dividend = None, None, None

            results.append([name, code, per, pbr, dividend])
            time.sleep(1)  # 요청 간격을 1초로 늘려 안정성 확보

            # ✅ 진행률 + 예상 남은 시간 표시
            elapsed = int(time.time() - start_time)
            percent = int((i / total) * 100)
            remaining = int((elapsed / i) * (total - i))
            status_label.config(text=f"진행률: {percent}% | 경과: {elapsed}초 | 예상 남은: {remaining}초")
            root.update_idletasks()

            # ✅ 중간 저장 (100개마다)
            if i % 100 == 0:
                df_partial = pd.DataFrame(results, columns=["종목명", "종목코드", "PER", "PBR", "배당수익률"])
                df_partial.to_excel(r"c:\python\partial_result.xlsx", index=False)

        # 최종 결과 처리
        df_result = pd.DataFrame(results, columns=["종목명", "종목코드", "PER", "PBR", "배당수익률"])
        df_result["PER"] = pd.to_numeric(df_result["PER"], errors="coerce")
        df_result["PBR"] = pd.to_numeric(df_result["PBR"], errors="coerce")
        df_result["배당수익률"] = pd.to_numeric(df_result["배당수익률"], errors="coerce")
        df_result = df_result.dropna()

        undervalued = df_result[(df_result["PER"] < 15) & (df_result["PBR"] < 2) & (df_result["배당수익률"] > 3)]
        df_result.to_excel(r"c:\python\all_stocks.xlsx", index=False)
        undervalued.to_excel(r"c:\python\undervalued.xlsx", index=False)

        messagebox.showinfo("완료", "전체 분석이 끝났습니다!\n엑셀 파일을 확인하세요.")
    except Exception as e:
        messagebox.showerror("에러 발생", str(e))

root = tk.Tk()
root.title("저평가 종목 분석기")

btn = tk.Button(root, text="분석 실행", command=lambda: threading.Thread(target=run_analysis).start(), width=20, height=2)
btn.pack(pady=20)

status_label = tk.Label(root, text="대기 중...")
status_label.pack(pady=10)

root.mainloop()
