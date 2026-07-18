import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Cấu hình trang trang web của ứng dụng
st.set_page_config(
    page_title="Hệ thống Thẩm định Tín dụng Cá nhân Toàn diện",
    page_icon="🏦",
    layout="wide"
)

# Giao diện Tiêu đề chính
st.title("🏦 HỆ THỐNG THẨM ĐỊNH TÍN DỤNG KHÁCH HÀNG CÁ NHÂN")
st.markdown("---")

# Chia ứng dụng thành 2 cột: Cột 1 nhập liệu, Cột 2 hiển thị kết quả
col_input, col_result = st.columns([1.1, 1.2])

with col_input:
    st.header("📋 Hồ sơ Đề nghị Cấp tín dụng")
    
    # --- PHẦN 1: THÔNG TIN NHÂN THÂN & PHÁP LÝ ---
    with st.expander("👤 1. Thông tin Nhân thân & Pháp lý", expanded=True):
        customer_name = st.text_input("Họ và tên khách hàng", value="Nguyễn Văn A")
        col_ns, col_gt = st.columns(2)
        with col_ns:
            birth_year = st.number_input("Năm sinh", min_value=1950, max_value=2010, value=1995)
        with col_gt:
            gender = st.selectbox("Giới tính", ["Nam", "Nữ", "Khác"])
            
        marital_status = st.selectbox(
            "Tình trạng hôn nhân", 
            ["Độc thân", "Đã kết hôn (Có đồng ký nợ vợ/chồng)", "Ly hôn/Khác"]
        )
        resident_status = st.selectbox(
            "Tình trạng cư trú tại địa bàn kinh doanh của Ngân hàng",
            ["Thường trú (Hộ khẩu)", "Tạm trú dài hạn (KT3)", "Tạm trú dưới 6 tháng / Không cư trú"]
        )
        dependents = st.number_input("Số người phụ thuộc (Con nhỏ, bố mẹ già...)", min_value=0, max_value=10, value=1, step=1)

    # --- PHẦN 2: THÔNG TIN KHOẢN VAY VÀ MỤC ĐÍCH ---
    with st.expander("🎯 2. Phương án vay vốn & Mục đích Sử dụng", expanded=True):
        loan_purpose = st.selectbox(
            "Mục đích sử dụng vốn vay",
            ["Mua Bất động sản (Nhà/Đất)", "Xây dựng/Sửa chữa nhà cửa", "Mua xe ô tô tiêu dùng", "Vay tiêu dùng sinh hoạt (Tín chấp)", "Bổ sung vốn kinh doanh cá thể"]
        )
        loan_amount = st.number_input("Số tiền đề nghị vay (VND)", min_value=0, value=500000000, step=10000000, format="%d")
        loan_term_years = st.number_input("Thời gian vay đề nghị (Năm)", min_value=1, max_value=30, value=15, step=1)
        interest_rate_annual = st.slider("Lãi suất cho vay áp dụng (% / năm)", min_value=1.0, max_value=20.0, value=8.5, step=0.1)

    # --- PHẦN 3: THÔNG TIN TÀI CHÍNH CHI TIẾT (NGUỒN THU & NỢ) ---
    with st.expander("💰 3. Năng lực Tài chính & Nguồn thu nhập", expanded=True):
        st.markdown("**Các nguồn thu nhập chứng minh được (Hàng tháng):**")
        inc_salary = st.number_input("1. Thu nhập từ Lương (Sao kê/Bảng lương) (VND)", min_value=0, value=25000000, step=1000000, format="%d")
        inc_business = st.number_input("2. Thu nhập từ Hộ kinh doanh/Doanh nghiệp riêng (VND)", min_value=0, value=5000000, step=1000000, format="%d")
        inc_rent = st.number_input("3. Thu nhập từ Cho thuê Tài sản (Nhà, Đất, Ô tô) (VND)", min_value=0, value=0, step=1000000, format="%d")
        
        # Tổng thu nhập tự động tính toán
        total_income = inc_salary + inc_business + inc_rent
        st.info(f"👉 **Tổng thu nhập hàng tháng:** {total_income:,} VND")
        
        st.markdown("**Nghĩa vụ nợ và Chi phí:**")
        existing_monthly_debt = st.number_input("Dư nợ gốc + lãi đang trả tại TCTD khác hàng tháng (VND)", min_value=0, value=2000000, step=500000, format="%d")
        living_cost_per_person = 4000000 # Giả định chi phí sinh hoạt tối thiểu 4 triệu/người tại đô thị
        calculated_living_cost = (1 + dependents) * living_cost_per_person

    # --- PHẦN 4: BIỆN PHÁP BẢO ĐẢM TIỀN VAY ---
    with st.expander("🛡️ 4. Tài sản Đảm bảo (Collateral)", expanded=True):
        collateral_type = st.selectbox(
            "Loại Tài sản Đảm bảo",
            ["Bất động sản (Đất ở, nhà ở có sổ hồng/sổ đỏ)", "Phương tiện vận tải (Ô tô)", "Giấy tờ có giá (Sổ tiết kiệm, Trái phiếu Chính phủ)", "Không có TSĐB (Vay tín chấp)"]
        )
        collateral_value = st.number_input("Giá trị định giá của Tài sản Bảo đảm (VND)", min_value=0, value=1000000000, step=50000000, format="%d")

    # --- PHẦN 5: UY TÍN TÍN DỤNG (CIC) ---
    with st.expander("🔍 5. Kiểm tra Lịch sử Tín dụng (CIC)", expanded=True):
        cic_group = st.selectbox(
            "Nhóm nợ CIC hiện tại của Khách hàng",
            options=["Nhóm 1 (Nợ đủ tiêu chuẩn)", "Nhóm 2 (Nợ cần chú ý)", "Nhóm 3 (Nợ dưới tiêu chuẩn)", "Nhóm 4 (Nợ nghi ngờ)", "Nhóm 5 (Nợ có khả năng mất vốn)"]
        )
        has_credit_card_overdue = st.checkbox("Có lịch sử chậm thanh toán thẻ tín dụng trong 12 tháng qua")

# --- XỬ LÝ LOGIC TOÁN HỌC ---
loan_term_months = loan_term_years * 12
monthly_interest_rate = (interest_rate_annual / 100) / 12

# Tính gốc lãi cố định hàng tháng (EMI)
if monthly_interest_rate > 0:
    monthly_emi = loan_amount * monthly_interest_rate * ((1 + monthly_interest_rate) ** loan_term_months) / (((1 + monthly_interest_rate) ** loan_term_months) - 1)
else:
    monthly_emi = loan_amount / loan_term_months

# Tính các tỷ lệ tài chính để thẩm định
total_monthly_debt_obligation = monthly_emi + existing_monthly_debt
dti_ratio = (total_monthly_debt_obligation / total_income) * 100 if total_income > 0 else 100
ltv_ratio = (loan_amount / collateral_value) * 100 if collateral_value > 0 else 100

# Thu nhập tích lũy còn lại sau khi trừ chi phí sinh hoạt gia đình và trả nợ vay
disposable_income = total_income - calculated_living_cost - total_monthly_debt_obligation

# Thiết lập các ngưỡng an toàn của Ngân hàng thương mại Việt Nam
MAX_DTI = 60.0  # DTI trần 60% cho khách hàng thu nhập trung bình khá
MAX_LTV = 70.0  # LTV tối đa 70% đối với tài sản đảm bảo là Bất động sản
if collateral_type == "Phương tiện vận tải (Ô tô)":
    MAX_LTV = 50.0 # Xe ô tô cũ/mới thường chỉ tài trợ 50-60%
elif collateral_type == "Giấy tờ có giá (Sổ tiết kiệm, Trái phiếu Chính phủ)":
    MAX_LTV = 85.0 # Sổ tiết kiệm độ an toàn cực cao, được tài trợ đến 85-90%

# Tự động tạo bảng lịch trình trả nợ
remaining_balance = loan_amount
schedule_data = []
for month in range(1, loan_term_months + 1):
    interest_payment = remaining_balance * monthly_interest_rate
    principal_payment = monthly_emi - interest_payment
    remaining_balance -= principal_payment
    if remaining_balance < 0: remaining_balance = 0
    
    schedule_data.append({
        "Tháng": month,
        "Gốc phải trả (VND)": round(principal_payment),
        "Lãi phải trả (VND)": round(interest_payment),
        "Tổng trả (VND)": round(monthly_emi),
        "Dư nợ còn lại (VND)": round(remaining_balance)
    })
df_schedule = pd.DataFrame(schedule_data)

# --- HIỂN THỊ KẾT QUẢ PHÍA CỘT PHẢI ---
with col_result:
    tab1, tab2, tab3 = st.tabs(["📊 Kết quả thẩm định", "📈 Kế hoạch trả nợ", "👤 Tóm tắt Hồ sơ KH"])
    
    # --- TAB 1: KẾT QUẢ THẨM ĐỊNH TÍN DỤNG ---
    with tab1:
        st.subheader(f"Khách hàng: {customer_name.upper()}")
        
        # Khối chỉ số tài chính chính
        kpi_col1, kpi_col2 = st.columns(2)
        kpi_col1.metric("Gốc lãi khoản vay mới / tháng", f"{int(monthly_emi):,} VND")
        kpi_col2.metric("Thu nhập tích lũy còn lại (Thặng dư)", f"{int(disposable_income):,} VND", 
                        delta="Đạt yêu cầu" if disposable_income > 0 else "Âm dòng tiền", 
                        delta_color="normal" if disposable_income > 0 else "inverse")
        
        st.markdown("### 🔍 Đánh giá các điều kiện Core Banking")
        
        # Đánh giá 1: DTI
        dti_pass = dti_ratio <= MAX_DTI
        if dti_pass: st.success(f"✅ **Tỷ lệ nợ/thu nhập (DTI):** {dti_ratio:.2f}% (Đạt tiêu chuẩn < {MAX_DTI}%)")
        else: st.error(f"❌ **Tỷ lệ nợ/thu nhập (DTI):** {dti_ratio:.2f}% (Vượt ngưỡng rủi ro > {MAX_DTI}%)")
            
        # Đánh giá 2: LTV
        if collateral_type == "Không có TSĐB (Vay tín chấp)":
            ltv_pass = loan_amount <= 500000000 # Giả định trần vay tín chấp là 500 triệu
            st.warning(f"⚠️ **Tỷ lệ tài trợ LTV/LAV:** Vay tín chấp không TSĐB (Hạn mức tối đa hệ thống: 500 triệu VND)")
        else:
            ltv_pass = ltv_ratio <= MAX_LTV
            if ltv_pass: st.success(f"✅ **Tỷ lệ tài trợ trên tài sản (LTV):** {ltv_ratio:.2f}% (Hợp lệ đối với {collateral_type} < {MAX_LTV}%)")
            else: st.error(f"❌ **Tỷ lệ tài trợ trên tài sản (LTV):** {ltv_ratio:.2f}% (Vượt mức cho phép của loại tài sản đảm bảo này > {MAX_LTV}%)")
            
        # Đánh giá 3: CIC & Pháp lý cư trú
        cic_pass = cic_group in ["Nhóm 1 (Nợ đủ tiêu chuẩn)"] and not has_credit_card_overdue
        resident_pass = resident_status in ["Thường trú (Hộ khẩu)", "Tạm trú dài hạn (KT3)"]
        
        if cic_pass: st.success(f"✅ **Lịch sử tín dụng (CIC):** Khách hàng uy tín tốt ({cic_group})")
        else: st.error(f"❌ **Lịch sử tín dụng (CIC):** Rủi ro cao! Khách hàng có nợ cần chú ý/nợ xấu hoặc trễ hạn thẻ tín dụng.")
            
        if resident_pass: st.success(f"✅ **Địa bàn cư trú:** Đạt điều kiện quản lý sau vay")
        else: st.warning(f"⚠️ **Địa bàn cư trú:** Khách hàng tạm trú ngắn hạn, cần thắt chặt biện pháp kiểm soát dòng tiền.")

        st.markdown("---")
        st.subheader("⚖️ QUYẾT ĐỊNH PHÊ DUYỆT SƠ BỘ")
        if dti_pass and ltv_pass and cic_pass and disposable_income > 0:
            st.balloons()
            st.markdown("<h2 style='color:green;text-align:center;'>PHÊ DUYỆT (APPROVED)</h2>", unsafe_allow_html=True)
            st.info("💡 **Gợi ý kiểm soát:** Chuyển hồ sơ sang bộ phận Kiểm soát tín dụng để soạn thảo hợp đồng vay.")
        elif disposable_income <= 0 or not dti_pass:
            st.markdown("<h2 style='color:orange;text-align:center;'>TỪ CHỐI DO NĂNG LỰC TÀI CHÍNH</h2>", unsafe_allow_html=True)
            st.warning("💡 **Giải pháp:** Khách hàng bị âm dòng tiền hoặc nợ quá nhiều. Đề xuất giảm số tiền vay hoặc kéo dài thời hạn vay để giảm áp lực trả nợ tháng.")
        else:
            st.markdown("<h2 style='color:red;text-align:center;'>TỪ CHỐI HỒ SƠ (REJECTED)</h2>", unsafe_allow_html=True)
            st.error("💡 **Lý do:** Hồ sơ bị vướng nợ xấu CIC hoặc tỷ lệ tài sản đảm bảo không đủ an toàn để cấp tín dụng.")

    # --- TAB 2: KẾ HOẠCH TRẢ NỢ VÀ BIỂU ĐỒ XU HƯỚNG ---
    with tab2:
        st.subheader("📈 Phân tích dòng tiền trả nợ theo thời gian")
        fig = px.area(df_schedule, x="Tháng", y="Dư nợ còn lại (VND)", title="Tiến độ giảm dư nợ gốc")
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("📋 Bảng phân bổ lịch gốc lãi chi tiết")
        df_format = df_schedule.copy()
        for col in df_format.columns:
            if col != "Tháng": df_format[col] = df_format[col].map('{:,.0f}'.format)
        st.dataframe(df_format, use_container_width=True, height=350)

    # --- TAB 3: TÓM TẮT THÔNG TIN IN BÁO CÁO ---
    with tab3:
        st.subheader("📄 Tờ trình thẩm định khách hàng cá nhân tóm tắt")
        st.markdown(f"""
        * **Tên khách hàng:** {customer_name}
        * **Tình trạng hôn nhân:** {marital_status}
        * **Mục đích cấp tín dụng:** {loan_purpose}
        * **Tổng thu nhập ghi nhận:** {total_income:,} VND/tháng
        * **Chi phí sinh hoạt gia đình dự tính:** {calculated_living_cost:,} VND/tháng
        * **Biện pháp bảo đảm:** {collateral_type} (Định giá: {collateral_value:,} VND)
        * **Trạng thái CIC:** {cic_group}
        ---
        *Báo cáo được trích xuất tự động từ Hệ thống mô phỏng Thẩm định Tín dụng.*
        """)
