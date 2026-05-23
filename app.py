import streamlit as st
import yfinance as yf
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="고급 범위 설정 스캐너", layout="wide")
st.title("🎯 실전형 가치투자 범위 설정 스캐너")

# 사이드바: 범위 필터 설정
st.sidebar.header("📊 범위 설정 필터")

# PER 범위
per_min, per_max = st.sidebar.slider("PER 범위", 0.0, 100.0, (0.0, 20.0))
# PBR 범위
pbr_min, pbr_max = st.sidebar.slider("PBR 범위", 0.0, 10.0, (0.0, 1.5))
# ROE 범위
roe_min, roe_max = st.sidebar.slider("ROE (%) 범위", 0.0, 50.0, (5.0, 30.0))
# 부채비율 범위
debt_min, debt_max = st.sidebar.slider("부채비율 (%) 범위", 0.0, 500.0, (0.0, 150.0))
# 시가총액 범위
cap_min, cap_max = st.sidebar.slider("시가총액 (억 원) 범위", 100, 10000, (500, 5000))

# 분석할 종목 리스트
tickers = ["005930.KS", "000660.KS", "035420.KS", "035720.KS", "005380.KS", "000270.KS", "055550.KS", "012330.KS", "005490.KS"]

if st.button("🚀 종합 범위 스캔 시작"):
    results = []
    with st.spinner("종목 데이터를 범위 조건에 맞춰 분석 중..."):
        for t in tickers:
            try:
                stock = yf.Ticker(t)
                info = stock.info
                
                # 데이터 추출
                name = info.get('shortName', '알 수 없음')
                per = info.get('trailingPE')
                pbr = info.get('priceToBook')
                roe = info.get('returnOnEquity', 0) * 100
                debt = info.get('debtToEquity', 0)
                cap = info.get('marketCap', 0) / 100_000_000
                
                # 범위 필터링
                if all([
                    per is not None and per_min <= per <= per_max,
                    pbr is not None and pbr_min <= pbr <= pbr_max,
                    roe_min <= roe <= roe_max,
                    debt_min <= debt <= debt_max,
                    cap_min <= cap <= cap_max
                ]):
                    results.append({
                        "종목명": name, "PER": round(per, 1), "PBR": round(pbr, 1),
                        "ROE(%)": round(roe, 1), "부채비율": round(debt, 1), "시총(억)": round(cap, 0)
                    })
            except Exception:
                continue

    if results:
        st.success(f"범위 내 종목 {len(results)}개를 찾았습니다!")
        st.dataframe(pd.DataFrame(results), use_container_width=True)
    else:
        st.warning("설정하신 범위 내에 맞는 종목이 없습니다. 범위를 더 넓혀보세요.")

# 지표 설명 (학습용)
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.write("**PER (주가수익비율)**: ")
with col2:
    st.write("**PBR (주가순자산비율)**: ")