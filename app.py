import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CẤU HÌNH GIAO DIỆN
st.set_page_config(
    page_title="Thẩm Định Cho Vay Khách Hàng Cá Nhân",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 THẨM ĐỊNH CHO VAY KHÁCH HÀNG CÁ NHÂN")
st.markdown("---")

# 2. CHIA GIAO DIỆN THÀNH 2 CỘT PHẲNG (DỄ THAO TÁC)
col_input, col_result = st.columns([1, 1.2])

# --- CỘT TRÁI: NHẬP THÔNG TIN (Đúng và đủ theo yêu cầu của đề tài) ---
with col_input:
    st.subheader("📋 Thông tin nhập liệu")
    
    # Thông tin khoản vay đề nghị
    loan_amount = st.number_input("Số tiền đề nghị vay (VND)", min_value=0, value=500000000, step=10000000, format="%d")
    loan_term_years = st.number_input("Thời gian vay (Năm)", min_value=1, max_value=30, value=15, step=1)
    interest_rate_annual = st.slider("Lãi suất cho vay (%/năm)", min_value=1.0, max_value=20.0, value=8.5, step=0.1)
    
    st.markdown("---")
    # Thông tin tài chính khách hàng
    monthly_income = st.number_input("Thu nhập hàng tháng của khách hàng (VND)", min_value=0, value=30000000, step=1000000, format="%d")
    dependents = st.number_input("Số người phụ thuộc", min_value=0, max_value=10, value=1, step=1)
    existing_monthly_debt = st.number_input("Dư nợ khoản vay cũ hàng tháng (VND)", min_value=0, value=2000000, step=500000, format="%d")
    
    st.markdown("---")
    # Tài sản bảo đảm và Uy tín tín dụng
    collateral_value = st.number_input("Giá trị Tài sản Đảm bảo (TSĐB) (VND)", min_value=0, value=1000000000, step=50000000, format="%d")
    cic_group = st.selectbox(
        "Nhóm nợ CIC hiện tại",
        options=["Nhóm 1 (Nợ đủ tiêu chuẩn)", "Nhóm 2 (Nợ cần chú ý)", "Nhóm 3 (Nợ dưới tiêu chuẩn)", "Nhóm 4 (Nợ nghi ngờ)", "Nhóm 5 (Nợ có khả năng mất vốn)"]
    )
    overdue_days = st.number_input("Số ngày quá hạn giả định để tính phạt (Ngày)", min_value=0, max_value=365, value=30, step=1)

# --- XỬ LÝ LOGIC TOÁN HỌC ---
loan_term_months = loan_term_years * 12
monthly_interest_rate = (interest_rate_annual / 100) / 12

# Tính gốc lãi hàng tháng (EMI)
if monthly_interest_rate > 0:
    monthly_emi = loan_amount * monthly_interest_rate * ((1 + monthly_interest_rate) ** loan_term_months) / (((1 + monthly_interest_rate) ** loan_term_months) - 1)
else:
    monthly_emi = loan_amount / loan_term_months

# 1. Tính chỉ số DTI (Nợ cũ + Nợ mới) / Thu nhập
total_monthly_debt = monthly_emi + existing_monthly_debt
dti_ratio = (total_monthly_debt / monthly_income) * 100 if monthly_income > 0 else 100

# 2. Tính chỉ số LTV/LAV (Số tiền vay / Giá trị TSĐB)
ltv_ratio = (loan_amount / collateral_value) * 100 if collateral_value > 0 else 100

# Ngưỡng an toàn quy định của Ngân hàng
MAX_DTI = 55.0
MAX_LTV = 70.0

# Tính toán số tiền phạt quá hạn (Lãi phạt = 150% lãi trong hạn)
penalty_rate_annual = interest_rate_annual * 1.5
penalty_interest = (monthly_emi) * (penalty_rate_annual / 100) / 365 * overdue_days
total_overdue_payment = monthly_emi + penalty_interest

# Tạo bảng lịch trả nợ rút gọn (12 tháng đầu để minh họa)
remaining_balance = loan_amount
schedule_data = []
for month in range(1, 13):
    interest_payment = remaining_balance * monthly_interest_rate
    principal_payment = monthly_emi - interest_payment
    remaining_balance -= principal_payment
    schedule_data.append({
        "Tháng": month,
        "Gốc phải trả": round(principal_payment),
        "Lãi phải trả": round(interest_payment),
        "Dư nợ còn lại": round(remaining_balance) if remaining_balance > 0 else 0
    })
df_schedule = pd.DataFrame(schedule_data)

# --- CỘT PHẢI: HIỂN THỊ KẾT QUẢ VÀ BIỂU ĐỒ ---
with col_result:
    st.subheader("📊 Kết quả Thẩm định & Ước tính")
    
    # Khối hiển thị số tiền lớn, rõ ràng
    kpi1, kpi2 = st.columns(2)
    kpi1.metric("Gốc lãi khoản vay mới/tháng", f"{int(monthly_emi):,} VND")
    kpi2.metric("Tổng nợ phải trả/tháng (gồm nợ cũ)", f"{int(total_monthly_debt):,} VND")
    
    st.markdown("### 🔍 Đánh giá các chỉ số cốt lõi")
    
    # Kiểm tra DTI
    dti_pass = dti_ratio <= MAX_DTI
    if dti_pass:
        st.success(f"✅ **Tỷ lệ DTI đạt:** {dti_ratio:.2f}% (An toàn < {MAX_DTI}%)")
    else:
        st.error(f"❌ **Tỷ lệ DTI Quá cao:** {dti_ratio:.2f}% (Vượt ngưỡng {MAX_DTI}%)")
        
    # Kiểm tra LTV/LAV
    ltv_pass = ltv_ratio <= MAX_LTV
    if ltv_pass:
        st.success(f"✅ **Tỷ lệ LTV/LAV đạt:** {ltv_ratio:.2f}% (An toàn < {MAX_LTV}%)")
    else:
        st.error(f"❌ **Tỷ lệ LTV/LAV Quá cao:** {ltv_ratio:.2f}% (Vượt ngưỡng {MAX_LTV}%)")
        
    # Kiểm tra CIC
    cic_pass = cic_group == "Nhóm 1 (Nợ đủ tiêu chuẩn)"
    if cic_pass:
        st.success(f"✅ **Lịch sử tín dụng CIC:** Tốt ({cic_group})")
    else:
        st.warning(f"⚠️ **Cảnh báo CIC:** Khách hàng đang thuộc {cic_group}")

    # QUYẾT ĐỊNH CUỐI CÙNG
    st.markdown("### ⚖️ Quyết định phê duyệt sơ bộ")
    if dti_pass and ltv_pass and cic_pass:
        st.markdown("<h3 style='color:green;'>👉 ĐỦ ĐIỀU KIỆN PHÊ DUYỆT (PASSED)</h3>", unsafe_allow_html=True)
    else:
        st.markdown("<h3 style='color:red;'>👉 TỪ CHỐI CHO VAY (REJECTED)</h3>", unsafe_allow_html=True)
        
    st.markdown("---")
    
    # TÍNH NĂNG ƯỚC TÍNH SỐ TIỀN PHẢI TRẢ KHI QUÁ HẠN
    st.subheader("🚨 Tình huống khách hàng quá hạn")
    if overdue_days > 0:
        st.error(f"Khách hàng trễ hạn **{overdue_days} ngày** sẽ chịu lãi phạt **{penalty_rate_annual:.1f}%/năm**.")
        st.write(f"• Số tiền phạt phát sinh thêm: **{int(penalty_interest):,} VND**")
        st.write(f"👉 **Tổng số tiền phải nộp kỳ này:** **{int(total_overdue_payment):,} VND**")
    else:
        st.info("Khách hàng đang thanh toán đúng hạn.")

    st.markdown("---")
    
    # BIỂU ĐỒ VÀ BẢNG PHÂN PHỐI 12 THÁNG ĐẦU
    st.subheader("📈 Kế hoạch giảm dư nợ (Minh họa 12 tháng đầu)")
    fig = px.line(df_schedule, x="Tháng", y="Dư nợ còn lại", title="Xu hướng Dư nợ giảm dần")
    st.plotly_chart(fig, use_container_width=True)
    
    # Định dạng dấu phẩy cho bảng số liệu
    df_format = df_schedule.copy()
    for col in ["Gốc phải trả", "Lãi phải trả", "Dư nợ còn lại"]:
        df_format[col] = df_format[col].map('{:,.0f}'.format)
    st.dataframe(df_format, use_container_width=True)
