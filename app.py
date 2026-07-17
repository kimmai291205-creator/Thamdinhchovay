import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

from credit_score import calculate_cic_score, credit_decision
from report import export_excel
from pdf_report import create_pdf
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
# ================= DASHBOARD =================
st.divider()
st.subheader("📊 DASHBOARD PHÂN TÍCH RỦI RO")
# Biểu đồ cơ cấu vốn
chart_data = pd.DataFrame(
    {  "Nguồn vốn": [  "Khoản vay",  "Vốn tự có"     ],
        "Giá trị": [      loan_amount,  asset_value - loan_amount  ] })
fig, ax = plt.subplots()
ax.pie( chart_data["Giá trị"],
    labels=chart_data["Nguồn vốn"],
    autopct="%1.1f%%")
ax.axis("equal")
st.pyplot(fig)
# Biểu đồ chỉ số rủi ro
risk_data = pd.DataFrame(
    {  "Chỉ số": [    "CIC",  "DTI","LTV"    ],
        "Điểm": [   cic_score,  100-dti,100-lt ] })
st.bar_chart(  risk_data.set_index("Chỉ số"))
# ================= EXPORT EXCEL =================
st.divider()
st.subheader("📄 XUẤT BÁO CÁO")
report_data = {
    "Họ tên":[name],
    "Thu nhập":[income],
    "Khoản vay":[loan_amount],
    "EMI":[emi],
    "DTI":[dti],
    "LTV":[ltv],
    "Điểm CIC":[cic_score],
    "Kết quả":[decision]}
excel_file = export_excel( report_data)
st.download_button( label="📥 Tải báo cáo Excel", data=excel_file,  file_name="bao_cao_tham_dinh.xlsx",
                   mime= "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
# ================= PDF =================
pdf_data = {
"Họ tên":name,
"Khoản vay":loan_amount,
"EMI":emi,
"DTI":dti,
"LTV":ltv,
"CIC":cic_score,
"Quyết định":decision}
pdf_file = create_pdf(    pdf_data)
st.download_button(
label="📄 Tải báo cáo PDF",
data=pdf_file,
file_name="bao_cao_tham_dinh.pdf",
mime="application/pdf")
