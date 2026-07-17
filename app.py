import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from credit_score import calculate_cic_score, credit_decision
from report import export_excel
from pdf_report import create_pdf

# Đảm bảo set_page_config là câu lệnh Streamlit đầu tiên được chạy
st.set_page_config(
    page_title="Hệ thống thẩm định cho vay",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 HỆ THỐNG HỖ TRỢ THẨM ĐỊNH CHO VAY")
st.info("👈 Chọn chức năng ở menu bên trái để bắt đầu sử dụng hệ thống.")

# ==========================================
# PHẦN NHẬP THÔNG TIN (ĐỂ KHẮC PHỤC LỖI THIẾU BIẾN)
# ==========================================
st.subheader("📝 THÔNG TIN KHÁCH HÀNG & KHOẢN VAY")
col_info1, col_info2 = st.columns(2)

with col_info1:
    name = st.text_input("Họ và tên khách hàng", value="Nguyễn Văn A")
    loan_amount = st.number_input("Số tiền đề nghị vay (VNĐ)", min_value=0.0, value=500000000.0, step=10000000.0)
    asset_value = st.number_input("Giá trị tài sản đảm bảo (VNĐ)", min_value=1.0, value=1500000000.0, step=10000000.0)
    years = st.slider("Thời hạn vay (năm)", 1, 30, 20)

with col_info2:
    income = st.number_input("Thu nhập hàng tháng (VNĐ)", min_value=1.0, value=25000000.0, step=1000000.0)
    old_debt = st.number_input("Khoản trả nợ hiện tại (VNĐ)", min_value=0.0, value=2000000.0, step=500000.0)
    interest = st.slider("Lãi suất (%/năm)", 1.0, 20.0, 8.5)

# Tự động tính toán các chỉ số tài chính cần thiết
r = interest / 100 / 12
n = years * 12
if r > 0:
    emi = (loan_amount * r * (1 + r) ** n) / ((1 + r) ** n - 1)
else:
    emi = loan_amount / n

dti = ((emi + old_debt) / income) * 100
ltv = (loan_amount / asset_value) * 100

st.markdown("---")

# ==========================
# CIC
# ==========================
st.subheader("📈 CHẤM ĐIỂM CIC")

col_cic1, col_cic2 = st.columns(2)
with col_cic1:
    credit_history = st.selectbox(
        "Lịch sử tín dụng",
        ["Tốt", "Trung bình", "Xấu"]
    )
with col_cic2:
    job_stability = st.number_input(
        "Số năm làm việc ổn định",
        min_value=0,
        value=3
    )

# Gọi hàm tính điểm CIC từ file credit_score.py
cic_score = calculate_cic_score(
    credit_history,
    income,
    dti,
    ltv,
    job_stability
)
decision = credit_decision(cic_score)

st.subheader("📊 KẾT QUẢ THẨM ĐỊNH TÍN DỤNG")
col1, col2 = st.columns(2)
with col1:
    st.metric(
        "Điểm đánh giá CIC",
        f"{cic_score}/100"
    )
with col2:
    st.metric(
        "Quyết định sơ bộ",
        decision
    )

# ================= DASHBOARD =================
st.divider()
st.subheader("📊 DASHBOARD PHÂN TÍCH RỦI RO")

col_dash1, col_dash2 = st.columns(2)

with col_dash1:
    st.write("**Cơ cấu nguồn vốn thực hiện dự án**")
    # Biểu đồ cơ cấu vốn
    chart_data = pd.DataFrame({
        "Nguồn vốn": ["Khoản vay", "Vốn tự có"],
        "Giá trị": [loan_amount, max(0.0, asset_value - loan_amount)]
    })
    fig, ax = plt.subplots()
    ax.pie(
        chart_data["Giá trị"],
        labels=chart_data["Nguồn vốn"],
        autopct="%1.1f%%",
        startangle=90
    )
    ax.axis("equal")
    st.pyplot(fig)

with col_dash2:
    st.write("**Biểu đồ phân tích chỉ số rủi ro**")
    # Biểu đồ chỉ số rủi ro (đã sửa lỗi chữ 'lt' thiếu chữ v thành 'ltv')
    risk_data = pd.DataFrame({
        "Chỉ số": ["CIC Score", "DTI Safety (100-DTI)", "LTV Safety (100-LTV)"],
        "Điểm": [cic_score, max(0.0, 100 - dti), max(0.0, 100 - ltv)]
    })
    st.bar_chart(risk_data.set_index("Chỉ số"))

# ================= EXPORT EXCEL =================
st.divider()
st.subheader("📄 XUẤT BÁO CÁO CHI TIẾT")

report_data = {
    "Họ tên": [name],
    "Thu nhập": [income],
    "Khoản vay": [loan_amount],
    "EMI": [emi],
    "DTI": [dti],
    "LTV": [ltv],
    "Điểm CIC": [cic_score],
    "Kết quả": [decision]
}

col_dl1, col_dl2 = st.columns(2)

with col_dl1:
    excel_file = export_excel(report_data)
    st.download_button(
        label="📥 Tải báo cáo Excel (.xlsx)",
        data=excel_file,
        file_name="bao_cao_tham_dinh.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# ================= PDF =================
with col_dl2:
    pdf_data = {
        "Họ tên": name,
        "Khoản vay": loan_amount,
        "EMI": emi,
        "DTI": dti,
        "LTV": ltv,
        "CIC": cic_score,
        "Quyết định": decision
    }
    pdf_file = create_pdf(pdf_data)
    st.download_button(
        label="📄 Tải báo cáo PDF (.pdf)",
        data=pdf_file,
        file_name="bao_cao_tham_dinh.pdf",
        mime="application/pdf"
    )
