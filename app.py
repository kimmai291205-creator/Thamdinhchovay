from credit_score import calculate_cic_score, credit_decision
import streamlit as st
st.set_page_config(
    page_title="Hệ thống thẩm định cho vay",
    page_icon="🏦",
    layout="wide")
st.title("🏦 HỆ THỐNG HỖ TRỢ THẨM ĐỊNH CHO VAY")
st.info(
"""
👈 Chọn chức năng ở menu bên trái để bắt đầu sử dụng hệ thống.
""")
st.subheader("📈 CHẤM ĐIỂM CIC")
credit_history = st.selectbox(
    "Lịch sử tín dụng",
    [ "Tốt",  "Trung bình", "Xấu"  ])
job_stability = st.number_input(
    "Số năm làm việc ổn định",
    min_value=0,
    value=3)
cic_score = calculate_cic_score(
    credit_history,
    income,
    dti,
    ltv,
    job_stability)
decision = credit_decision(cic_score)
st.subheader("📊 KẾT QUẢ THẨM ĐỊNH")
col1, col2 = st.columns(2)
with col1:
    st.metric(
        "Điểm CIC",
        f"{cic_score}/100"   )
with col2:
    st.metric(
        "Quyết định",
        decision)
