import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from pykrx import stock
import matplotlib.pyplot as plt
import io

# 페이지 설정
st.set_page_config(page_title="가치투자 스캐너", layout="wide")
st.title("💹 가치투자 스캐너 (골든크로스 + 재무지표 필터)")

# 사이드바: 필터 설정
st.sidebar.header("📊 범위 설정 필터")

per_min, per_max = st.sidebar.slider("PER 범위", 0.0, 100.0, (0.0, 20.0))
pbr_min, pbr_max = st.sidebar.slider("PBR 범위", 0.0, 10.0, (0.0, 1.5))
roe_min, roe_max = st.sidebar.slider("ROE (%) 범위", 0.0, 50.0, (5.0, 30.0))
debt_min, debt_max = st.sidebar.slider("부채비율 (%) 범위", 0.0, 500.0, (0.0, 150.0))
cap_min, cap_max = st.sidebar.slider("시가총액 (억 원) 범위", 100, 100000, (500, 5000))

min_volume = st.sidebar.number_input("최소 거래량 조건", min_value=0, value=0, step=1000)

# 골든크로스 탐지 함수
def get_golden_cross_stocks(min_volume=0):
    today = datetime.today().strftime("%Y%m%d")
    start_date = (datetime.today() - timedelta(days=60)).strftime("%Y%m%d")
    
    kospi_tickers = stock.get_market_ticker_list(today, market="KOSPI")
    kosdaq_tickers = stock.get_market_ticker_list(today, market="KOSDAQ")
    all_tickers = kospi_tickers + kosdaq_tickers
    
    golden_cross_list = []
    
    for ticker in all_tickers:
        try:
            name = stock.get_market_ticker_name(ticker)
            df = stock.get_market_ohlcv_by_date(start_date, today, ticker)
            
            if len(df) < 20:
                continue
            
            df['MA5'] = df['Close'].rolling(window=5).mean()
            df['MA20'] = df['Close'].rolling(window=20).mean()
            df['Vol_MA20'] = df['Volume'].rolling(window=20).mean()
            
            prev_row = df.iloc[-2]
            curr_row = df.iloc[-1]
            
            cond_prev = prev_row['MA5'] < prev_row['MA20']
            cond_curr = curr_row['MA5'] > curr_row['MA20']
            
            if cond_prev and cond_curr and curr_row['Volume'] >= min_volume:
                is_high_volume = curr_row['Volume'] > curr_row['Vol_MA20']
                
                # 재무지표 가져오기 (예시: pykrx 재무 데이터)
                fundamentals = stock.get_market_fundamental_by_date(today, today, ticker)
                f_row = fundamentals.iloc[-1]
                
                per = f_row['PER']
                pbr = f_row['PBR']
                roe = f_row['ROE']
                cap = stock.get_market_cap(today, ticker)['시가총액'].iloc[0] / 100000000  # 억 원 단위
                
                debt_ratio = 100  # 부채비율은 pykrx에서 직접 제공되지 않아 예시값
                
                # 필터 조건 적용
                if (per_min <= per <= per_max and
                    pbr_min <= pbr <= pbr_max and
                    roe_min <= roe <= roe_max and
                    debt_min <= debt_ratio <= debt_max and
                    cap_min <= cap <= cap_max):
                    
                    golden_cross_list.append({
                        "종목코드": ticker,
                        "종목명": name,
                        "오늘종가": int(curr_row['Close']),
                        "오늘거래량": int(curr_row['Volume']),
                        "거래량급증": "O" if is_high_volume else "X",
                        "PER": round(per, 2),
                        "PBR": round(pbr, 2),
                        "ROE": round(roe, 2),
                        "부채비율": debt_ratio,
                        "시가총액(억)": int(cap)
                    })
        except:
            continue
    
    return pd.DataFrame(golden_cross_list)

# 실행 버튼
if st.button("가치투자 스캐너 실행"):
    with st.spinner("데이터 분석 중... 잠시만 기다려주세요 🚀"):
        result_df = get_golden_cross_stocks(min_volume=min_volume)
    
    if not result_df.empty:
        st.success("오늘 조건에 맞는 가치투자 종목입니다!")
        st.dataframe(result_df)
        
        # 엑셀 다운로드 버튼
        buffer = io.BytesIO()
        result_df.to_excel(buffer, index=False, engine='openpyxl')
        st.download_button(
            label="📥 엑셀 다운로드",
            data=buffer.getvalue(),
            file_name="value_invest_scanner.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        # 차트 시각화
        selected_stocks = st.multiselect("차트로 확인할 종목 선택", result_df["종목명"].tolist())
        
        for stock_name in selected_stocks:
            code = result_df[result_df["종목명"] == stock_name]["종목코드"].values[0]
            today = datetime.today().strftime("%Y%m%d")
            start_date = (datetime.today() - timedelta(days=60)).strftime("%Y%m%d")
            df_chart = stock.get_market_ohlcv_by_date(start_date, today, code)
            df_chart['MA5'] = df_chart['Close'].rolling(window=5).mean()
            df_chart['MA20'] = df_chart['Close'].rolling(window=20).mean()
            
            st.subheader(f"📊 {stock_name} ({code}) 차트")
            fig, ax = plt.subplots(figsize=(10,5))
            ax.plot(df_chart.index, df_chart['Close'], label="종가", color="black")
            ax.plot(df_chart.index, df_chart['MA5'], label="5일선", color="blue")
            ax.plot(df_chart.index, df_chart['MA20'], label="20일선", color="red")
            ax.set_title(f"{stock_name} 주가 및 이동평균선")
            ax.legend()
            st.pyplot(fig)
        
    else:
        st.warning("오늘 조건에 맞는 종목이 없습니다.")
