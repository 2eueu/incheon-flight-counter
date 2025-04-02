import streamlit as st
from flight_scraper import get_flight_count

st.set_page_config(page_title="인천공항 항공편 수", layout="wide")

st.markdown("## ✈️ 인천공항 제2터미널 출발 항공편 수")
st.markdown("#### (00:00~23:59 기준, 공동운항 통합)")

if st.button("🛫 항공편 수 확인"):
    with st.spinner("크롤링 중... 잠시만 기다려주세요."):
        try:
            total_blocks, unique_count = get_flight_count()
            st.success(f"✅ 총 로딩된 항공편 블록 수: {total_blocks}편")
            st.success(f"✅ 오늘(제2터미널, 00:00~23:59) 출발 항공편 수 (공동운항 포함 묶음): {unique_count}편")
        except Exception as e:
            import traceback
            st.error("⚠️ 오류 발생:")
            st.code(traceback.format_exc(), language="python")
