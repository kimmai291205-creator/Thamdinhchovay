import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CẤU HÌNH GIAO DIỆN
st.set_page_config(
    page_title="Thẩm Định Cho Vay Khách Hàng Cá Nhân",
    page_icon="🏦",
    layout="wide"
)

# Tiêu đề tinh gọn
st.title("🏦 THẨM ĐỊNH CHO VAY KHÁCH HÀNG CÁ NHÂN")
st.markdown("---")

# HÀM ĐỔI SỐ THÀNH CHỮ TIẾNG VIỆT
def doc_so_tien(so_tien):
    if so_tien == 0:
        return "Không đồng"
    if so_tien >= 1000000000:
        ty = so_tien // 1000000000
        trieu = (so_tien % 1000000000) // 1000000
        if trieu > 0:
            return f"{ty} tỷ {trieu} triệu đồng"
        return f"{ty} tỷ đồng"
    elif so_tien >= 1000000:
        trieu = so_tien // 1000000
        return f"{trieu} triệu đồng"
    return f"{so_tien:,} đồng"

# CHIA GIAO DIỆN THÀNH 2 CỘT
col_input, col_result = st.columns([1, 1.2])

# --- CỘT TRÁI: NHẬP THÔNG TIN ---
with col_input:
    # CHÈN LOGO VÀ TIÊU ĐỀ PHỤ NẰM CẠNH NHAU TRÊN CỘT CHÍNH
    col_logo, col_title_sub = st.columns([1, 4])
    with col_logo:
        # Sử dụng file ảnh logo vay.webp của bạn, chỉnh width=80 để logo vừa vặn
        st.image("logo vay.webp", width=80) 
    with col_title_sub:
        st.subheader("📋 Thông tin nhập liệu")
    
    # 1. Số tiền vay (Đã bỏ toàn bộ hàng nút bấm tăng nhanh phía dưới)
    loan_amount = st.number_input("Số tiền đề nghị vay (VND)", min_value=0, step=1000000, format="%d", value=500000000)
    st.markdown(f"👉 *Số tiền nhập:* **{loan_amount:,} VND**")
    st.markdown(f"👉 *Bằng chữ:* **{doc_so_tien(loan_amount)}**")
    
    st.markdown("---")
    loan_term_years = st.number_input("Thời gian vay (Năm)", min_value=1, max_value=30, value=15, step=1)
    interest_rate_annual = st.slider("Lãi suất cho vay (%/năm)", min_value=1.0, max_value=20.0, value=8.5, step=0.1)
    
    st.markdown("---")
    # 2. Thu nhập hàng tháng
    monthly_income = st.number_input("Thu nhập hàng tháng của khách hàng (VND)", min_value=0, value=30000000, step=1000000, format="%d")
    st.markdown(f"👉 *Số tiền nhập:* **{monthly_income:,} VND**")
    st.markdown(f"👉 *Bằng chữ:* **{doc_so_tien(monthly_income)}**")
    
    dependents = st.number_input("Số người phụ thuộc", min_value=0, max_value=10, value=1, step=1)
    
    # 3. Dư nợ cũ hàng tháng
    existing_monthly_debt = st.number_input("Dư nợ khoản vay cũ hàng tháng (VND)", min_value=0, value=2000000, step=100000, format="%d")
    st.markdown(f"👉 *Số tiền nhập:* **{existing_monthly_debt:,} VND**")
    
    st.markdown("---")
    # 4. Giá trị tài sản đảm bảo
    collateral_value = st.number_input("Giá trị Tài sản Đảm bảo (TSĐB) (VND)", min_value=0, value=1000000000, step=10000000, format="%d")
    st.markdown(f"👉 *Số tiền nhập:* **{collateral_value:,} VND**")
    st.markdown(f"👉 *Bằng chữ:* **{doc_so_tien(collateral_value)}**")
    
    cic_group = st.selectbox(
        "Nhóm nợ CIC hiện tại",
        options=["Nhóm 1 (Nợ đủ tiêu chuẩn)", "Nhóm 2 (Nợ cần chú ý)", "Nhóm 3 (Nợ dưới tiêu chuẩn)", "Nhóm 4 (Nợ nghi ngờ)", "Nhóm 5 (Nợ có khả năng mất vốn)"]
    )
    overdue_days = st.number_input("Số ngày quá hạn giả định để tính phạt (Ngày)", min_value=0, max_value=365, value=30, step=1)

# --- XỬ LÝ LOGIC TOÁN HỌC ---
loan_term_months = loan_term_years * 12
monthly_interest_rate = (interest_rate_annual / 100) / 12

if monthly_interest_rate > 0:
    monthly_emi = loan_amount * monthly_interest_rate * ((1 + monthly_interest_rate) ** loan_term_months) / (((1 + monthly_interest_rate) ** loan_term_months) - 1)
else:
    monthly_emi = loan_amount / loan_term_months

total_monthly_debt = monthly_emi + existing_monthly_debt
dti_ratio = (total_monthly_debt / monthly_income) * 100 if monthly_income > 0 else 100
ltv_ratio = (loan_amount / collateral_value) * 100 if collateral_value > 0 else 100

MAX_DTI = 55.0
MAX_LTV = 70.0

penalty_rate_annual = interest_rate_annual * 1.5
penalty_interest = (monthly_emi) * (penalty_rate_annual / 100) / 365 * overdue_days
total_overdue_payment = monthly_emi + penalty_interest

# Tạo bảng lịch trả nợ 12 tháng đầu để minh họa
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
    
    kpi1, kpi2 = st.columns(2)
    kpi1.metric("Gốc lãi khoản vay mới/tháng", f"{int(monthly_emi):,} VND")
    kpi2.metric("Tổng nợ phải trả/tháng (gồm nợ cũ)", f"{int(total_monthly_debt):,} VND")
    
    st.markdown("### 🔍 Đánh giá các chỉ số cốt lõi")
    
    dti_pass = dti_ratio <= MAX_DTI
    if dti_pass: st.success(f"✅ **Tỷ lệ DTI đạt:** {dti_ratio:.2f}% (An toàn < {MAX_DTI}%)")
    else: st.error(f"❌ **Tỷ lệ DTI Quá cao:** {dti_ratio:.2f}% (Vượt ngưỡng {MAX_DTI}%)")
        
    ltv_pass = ltv_ratio <= MAX_LTV
    if ltv_pass: st.success(f"✅ **Tỷ lệ LTV/LAV đạt:** {ltv_ratio:.2f}% (An toàn < {MAX_LTV}%)")
    else: st.error(f"❌ **Tỷ lệ LTV/LAV Quá cao:** {ltv_ratio:.2f}% (Vượt ngưỡng {MAX_LTV}%)")
        
    cic_pass = cic_group == "Nhóm 1 (Nợ đủ tiêu chuẩn)"
    if cic_pass: st.success(f"✅ **Lịch sử tín dụng CIC:** Tốt ({cic_group})")
    else: st.warning(f"⚠️ **Cảnh báo CIC:** Khách hàng đang thuộc {cic_group}")

    st.markdown("### ⚖️ Quyết định phê duyệt sơ bộ")
    if dti_pass and ltv_pass and cic_pass:
        st.markdown("<h3 style='color:green;'>👉 ĐỦ ĐIỀU KIỆN PHÊ DUYỆT (PASSED)</h3>", unsafe_allow_html=True)
    else:
        st.markdown("<h3 style='color:red;'>👉 TỪ CHỐI CHO VAY (REJECTED)</h3>", unsafe_allow_html=True)
        
    st.markdown("---")
    st.subheader("🚨 Tình huống khách hàng quá hạn")
    if overdue_days > 0:
        st.error(f"Khách hàng trễ hạn **{overdue_days} ngày** sẽ chịu lãi phạt **{penalty_rate_annual:.1f}%/năm**.")
        st.write(f"• Số tiền phạt phát sinh thêm: **{int(penalty_interest):,} VND**")
        st.write(f"👉 **Tổng số tiền phải nộp kỳ này:** **{int(total_overdue_payment):,} VND**")
    else:
        st.info("Khách hàng đang thanh toán đúng hạn.")

    st.markdown("---")
    st.subheader("📈 Kế hoạch giảm dư nợ (Minh họa 12 tháng đầu)")
    fig = px.line(df_schedule, x="Tháng", y="Dư nợ còn lại", title="Xu hướng Dư nợ giảm dần")
    st.plotly_chart(fig, use_container_width=True)
    
    df_format = df_schedule.copy()
    for col in ["Gốc phải trả", "Lãi phải trả", "Dư nợ còn lại"]:
        df_format[col] = df_format[col].map('{:,.0f}'.format)
    st.dataframe(df_format, use_container_width=True)
