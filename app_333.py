import yfinance as yf
import pandas as pd
import streamlit as st

st.title("퀀트 투자 조건 검색기 (KOSPI 200 전체)")

# 조건 입력
per_max = st.number_input("최대 PER", value=20.0)
pbr_max = st.number_input("최대 PBR", value=3.0)
roe_min = st.number_input("최소 ROE", value=0.15)

# 코스피 200 종목 리스트 (예시: 주요 티커, 실제로는 전체 리스트를 넣어야 함)
kospi200 = [
    "005930.KQ",  # 삼성전자
    "000660.KQ",  # SK하이닉스
    "035420.KQ",  # NAVER
    "051910.KQ",  # LG화학
    "207940.KQ",  # 삼성바이오로직스
    "006400.KQ",  # 삼성SDI
    "068270.KQ",  # 셀트리온
    "012330.KQ",  # 현대모비스
    "005380.KQ",  # 현대차
    "000270.KQ",  # 기아
    "090430.KQ",  # 아모레퍼시픽
    "034730.KQ",  # SK
    "017670.KQ",  # SK텔레콤
    "036570.KQ",  # 엔씨소프트
    "105560.KQ",  # KB금융
    "055550.KQ",  # 신한지주
    "033780.KQ",  # KT&G
    "003550.KQ",  # LG
    "251270.KQ",  # 넷마블
    "086790.KQ",  # 하나금융지주
    # … 실제로는 KOSPI 200 전체 티커를 리스트에 추가해야 함
]

# 버튼 클릭 시 실행
if st.button("조건에 맞는 코스피 200 종목 찾기"):
    data = {}
    for t in kospi200:
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

    st.subheader("조건을 만족하는 코스피 200 종목")
    st.dataframe(filtered)

    # 선택한 종목 차트
    if not filtered.empty:
        chosen = st.selectbox("차트 확인할 종목 선택", filtered.index)
        hist = yf.Ticker(chosen).history(period="6mo")
        st.line_chart(hist["Close"])
