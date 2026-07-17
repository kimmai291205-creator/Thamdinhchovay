import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Cấu hình trang trang web của ứng dụng
st.set_page_config(
    page_title="Hệ thống Thẩm định & Ước tính Khoản vay",
    page_icon="🏦",
    layout="wide"
)

# Giao diện Tiêu đề chính
st.title("🏦 HỆ THỐNG THẨM ĐỊNH & ƯỚC TÍNH KHOẢN VAY CÁ NHÂN")
st.markdown("---")

# Chia ứng dụng thành 2 cột: Cột 1 nhập liệu, Cột 2 hiển thị kết quả
col_input, col_result = st.columns([1, 1.3])

with col_input:
    st.header("📋 Thông tin Đề nghị Vay & Khách hàng")
    
    # Khu vực 1: Thông tin khoản vay
    st.subheader("1. Thông tin Khoản vay")
    loan_amount = st.number_input("Số tiền đề nghị vay (VND)", min_value=0, value=500000000, step=10000000, format="%d")
    loan_term_years = st.number_input("Thời gian vay (Năm)", min_value=1, max_value=30, value=15, step=1)
    interest_rate_annual = st.slider("Lãi suất cho vay (% / năm)", min_value=1.0, max_value=20.0, value=8.5, step=0.1)
    
    # Khu vực 2: Thu nhập & Chi phí
    st.subheader("2. Thu nhập & Chi phí")
    monthly_income = st.number_input("Thu nhập hàng tháng của khách hàng (VND)", min_value=0, value=30000000, step=1000000, format="%d")
    existing_monthly_debt = st.number_input("Dư nợ/Trả gốc lãi cũ hàng tháng (VND)", min_value=0, value=2000000, step=500000, format="%d")
    
    # Khu vực 3: Tài sản đảm bảo & Uy tín tín dụng
    st.subheader("3. Tài sản đảm bảo (TSĐB) & CIC")
    collateral_value = st.number_input("Giá trị Tài sản Bảo đảm (VND)", min_value=0, value=1000000000, step=50000000, format="%d")
    
    cic_group = st.selectbox(
        "Nhóm nợ CIC hiện tại",
        options=["Nhóm 1 (Nợ đủ tiêu chuẩn)", "Nhóm 2 (Nợ cần chú ý)", "Nhóm 3 (Nợ dưới tiêu chuẩn)", "Nhóm 4 (Nợ nghi ngờ)", "Nhóm 5 (Nợ có khả năng mất vốn)"]
    )
    
    # TÍNH NĂNG MỚI: Cấu hình phạt Quá hạn
    st.subheader("🚨 Giả định Tình huống Quá hạn")
    overdue_days = st.number_input("Số ngày quá hạn giả định (Ngày)", min_value=0, max_value=365, value=30, step=1)
    # Lãi phạt quá hạn theo quy định thường bằng 150% lãi suất trong hạn
    penalty_rate_annual = interest_rate_annual * 1.5 

# --- XỬ LÝ LOGIC TOÁN HỌC ---
loan_term_months = loan_term_years * 12
monthly_interest_rate = (interest_rate_annual / 100) / 12

# Tính gốc lãi cố định hàng tháng (EMI)
if monthly_interest_rate > 0:
    monthly_emi = loan_amount * monthly_interest_rate * ((1 + monthly_interest_rate) ** loan_term_months) / (((1 + monthly_interest_rate) ** loan_term_months) - 1)
else:
    monthly_emi = loan_amount / loan_term_months

# Tính toán các chỉ số DTI, LTV
total_monthly_debt_obligation = monthly_emi + existing_monthly_debt
dti_ratio = (total_monthly_debt_obligation / monthly_income) * 100 if monthly_income > 0 else 100
ltv_ratio = (loan_amount / collateral_value) * 100 if collateral_value > 0 else 100

MAX_DTI = 55.0
MAX_LTV = 75.0

# Tạo bảng phân phối trả nợ chi tiết từng tháng (Amortization Schedule)
remaining_balance = loan_amount
schedule_data = []

for month in range(1, loan_term_months + 1):
    interest_payment = remaining_balance * monthly_interest_rate
    principal_payment = monthly_emi - interest_payment
    remaining_balance -= principal_payment
    # Đảm bảo số dư cuối cùng không bị âm do làm tròn số
    if remaining_balance < 0: remaining_balance = 0
    
    schedule_data.append({
        "Tháng": month,
        "Gốc phải trả (VND)": round(principal_payment),
        "Lãi phải trả (VND)": round(interest_payment),
        "Tổng trả (VND)": round(monthly_emi),
        "Dư nợ còn lại (VND)": round(remaining_balance)
    })

df_schedule = pd.DataFrame(schedule_data)

# Tính toán số tiền phạt quá hạn (Giả định khách hàng trễ hạn 1 kỳ thanh toán)
# Lãi phạt trên nợ gốc quá hạn = Gốc quá hạn * (Lãi suất phạt / 365) * Số ngày quá hạn
goc_mot_ky = df_schedule.loc[0, "Gốc phải trả (VND)"]
lai_mot_ky = df_schedule.loc[0, "Lãi phải trả (VND)"]
penalty_interest_goc = goc_mot_ky * (penalty_rate_annual / 100) / 365 * overdue_days
# Lãi phạt trên nợ lãi chậm trả (thường 10%/năm)
penalty_interest_lai = lai_mot_ky * (10 / 100) / 365 * overdue_days
total_overdue_payment = monthly_emi + penalty_interest_goc + penalty_interest_lai

# --- HIỂN THỊ KẾT QUẢ PHÍA CỘT PHẢI ---
with col_result:
    # Tạo các Tab để phân tách thông tin cho khách hàng dễ nhìn
    tab1, tab2, tab3 = st.tabs(["📊 Thẩm định sơ bộ", "📅 Kế hoạch trả nợ & Biểu đồ", "⚠️ Rủi ro Quá hạn"])
    
    # --- TAB 1: THẨM ĐỊNH SƠ BỘ ---
    with tab1:
        st.subheader("💸 Nghĩa vụ tài chính hàng tháng")
        kpi1, kpi2 = st.columns(2)
        kpi1.metric("Tiền trả gốc + lãi / tháng", f"{int(monthly_emi):,}")
        kpi2.metric("Tổng nợ phải trả/tháng (gồm nợ cũ)", f"{int(total_monthly_debt_obligation):,}")
        
        st.markdown("### 🔍 Kiểm tra tiêu chuẩn phê duyệt")
        dti_pass = dti_ratio <= MAX_DTI
        ltv_pass = ltv_ratio <= MAX_LTV
        cic_pass = cic_group in ["Nhóm 1 (Nợ đủ tiêu chuẩn)"]
        
        if dti_pass: st.success(f"✅ **DTI Hợp lệ:** {dti_ratio:.2f}% (< {MAX_DTI}%)")
        else: st.error(f"❌ **DTI Quá cao:** {dti_ratio:.2f}% (> {MAX_DTI}%)")
            
        if ltv_pass: st.success(f"✅ **LTV/LAV Hợp lệ:** {ltv_ratio:.2f}% (< {MAX_LTV}%)")
        else: st.error(f"❌ **LTV/LAV Quá cao:** {ltv_ratio:.2f}% (> {MAX_LTV}%)")
            
        if cic_pass: st.success(f"✅ **CIC Tốt:** {cic_group}")
        else: st.warning(f"⚠️ **CIC Cần lưu ý:** {cic_group}")
        
        st.markdown("---")
        st.subheader("⚖️ Quyết định thẩm định sơ bộ")
        if dti_pass and ltv_pass and cic_pass:
            st.markdown("<h3 style='color:green;'>ĐỦ ĐIỀU KIỆN PHÊ DUYỆT (PASSED)</h3>", unsafe_allow_html=True)
        else:
            st.markdown("<h3 style='color:red;'>TỪ CHỐI HOẶC CẦN BỔ SUNG HỒ SƠ (REJECTED/PENDING)</h3>", unsafe_allow_html=True)

    # --- TAB 2: BIỂU ĐỒ & BẢNG PHÂN PHỐI ---
    with tab2:
        st.subheader("📈 Biểu đồ xu hướng dư nợ giảm dần")
        
        # Biểu đồ trực quan hóa quá trình trả nợ bằng Plotly
        fig = px.area(
            df_schedule, 
            x="Tháng", 
            y="Dư nợ còn lại (VND)", 
            title="Tốc độ giảm dư nợ gốc theo thời gian",
            labels={"Dư nợ còn lại (VND)": "Số tiền (VND)"}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Biểu đồ cột thể hiện tỷ trọng Gốc vs Lãi trong các năm đầu
        st.markdown("📊 **Tỷ trọng Gốc và Lãi trả hàng tháng:**")
        df_melted = pd.melt(df_schedule.head(12), id_vars=['Tháng'], value_vars=['Gốc phải trả (VND)', 'Lãi phải trả (VND)'],
                            var_name='Loại thanh toán', value_name='Số tiền (VND)')
        fig_bar = px.bar(df_melted, x='Tháng', y='Số tiền (VND)', color='Loại thanh toán', title="Chi tiết 12 tháng đầu tiên")
        st.plotly_chart(fig_bar, use_container_width=True)

        st.subheader("📋 Bảng phân phối chi tiết lịch trả nợ")
        # Định dạng hiển thị dấu phẩy phân cách phần nghìn cho bảng
        df_format = df_schedule.copy()
        for col in df_format.columns:
            if col != "Tháng":
                df_format[col] = df_format[col].map('{:,.0f}'.format)
        
        st.dataframe(df_format, use_container_width=True, height=300)

    # --- TAB 3: TÌNH HUỐNG QUÁ HẠN ---
    with tab3:
        st.subheader("🚨 Hệ quả pháp lý và tài chính khi Trễ hạn thanh toán")
        
        st.error(f"Nếu quá hạn **{overdue_days} ngày**, khoản nợ của bạn sẽ bị áp dụng mức lãi suất phạt bằng 150% trong hạn ({penalty_rate_annual}%/năm) đối với phần nợ gốc chậm trả.")
        
        st.markdown("### 💸 Chi tiết số tiền phải trả kỳ quá hạn:")
        
        col_p1, col_p2 = st.columns(2)
        col_p1.write(f"🔹 **Tiền gốc & lãi gốc một kỳ:**")
        col_p1.write(f"🔹 **Tiền phạt chậm trả nợ gốc:**")
        col_p1.write(f"🔹 **Tiền phạt chậm trả nợ lãi (10%):**")
        
        col_p2.write(f"{int(monthly_emi):,} VND")
        col_p2.write(f"{int(penalty_interest_goc):,} VND")
        col_p2.write(f"{int(penalty_interest_lai):,} VND")
        
        st.markdown("---")
        st.markdown(f"### 🧮 Tổng số tiền phải nộp để thanh lý kỳ quá hạn: <span style='color:red;'>{int(total_overdue_payment):,} VND</span>", unsafe_allow_html=True)
        
        # Đưa ra cảnh báo nhảy nhóm nợ CIC dựa trên số ngày trễ hạn thực tế ngân hàng Việt Nam
        st.subheader("📉 Dự báo ảnh hưởng đến Điểm tín dụng (CIC)")
        if overdue_days <= 10:
            st.warning("⚠️ **Nhóm 1 (Trễ hạn dưới 10 ngày):** Bạn bị phạt tiền nhưng chưa bị nhảy nhóm nợ xấu. Cần thanh toán ngay!")
        elif 10 < overdue_days <= 90:
            st.error("❌ **Nhóm 2 (Nợ cần chú ý - Từ 10 đến 90 ngày):** Lịch sử tín dụng của bạn bắt đầu bị ghi nhận vết xấu. Bạn sẽ rất khó vay thêm tại các ngân hàng khác trong vòng 12 tháng tới.")
        else:
            st.error("💀 **Nhóm 3 đến Nhóm 5 (NỢ XẤU - Trên 90 ngày):** Hồ sơ chuyển thành nợ xấu nhóm nghiêm trọng. Ngân hàng có quyền tiến hành thủ tục **Phát mại/Tịch thu Tài sản đảm bảo** để thu hồi nợ.")
