import streamlit as st
import math
st.title("💰 Thẩm định khoản vay")
st.markdown("---")
# ==========================
# Khoản vay
# ==========================
st.subheader("Thông tin khoản vay")
col1, col2 = st.columns(2)
with col1:
    loan = st.number_input(
        "Số tiền vay",
        min_value=1.0,
        value=500.0  )
    loan_unit = st.selectbox( "Đơn vị",   [ "Triệu", "Tỷ" ] )
    years = st.slider(
        "Thời gian vay (năm)",   1,  30,  20 )
with col2:
    interest = st.slider(
        "Lãi suất (%/năm)",
        1.0,
        20.0,
        8.5  )
    income = st.number_input(
        "Thu nhập (Triệu/tháng)",
        value=25.0 )
    old_debt = st.number_input(
        "Khoản trả nợ hiện tại (Triệu/tháng)",
        value=2.0  )
st.markdown("---")
# ==========================
# Tài sản đảm bảo
# ==========================
st.subheader("Tài sản đảm bảo")
asset = st.number_input(
    "Giá trị tài sản",
    value=1.5)
asset_unit = st.selectbox(
    "Đơn vị tài sản",
    [    "Tỷ",     "Triệu"  ])
st.markdown("---")
# ==========================
# CIC
# ==========================
st.subheader("Thông tin tín dụng")
cic = st.slider(
    "Điểm CIC",   300,    900,    750)
if st.button("🔍 THẨM ĐỊNH"):
    # ======================
    # Quy đổi đơn vị
    # ======================
    if loan_unit == "Triệu":
        loan_amount = loan * 1_000_000
    else:
        loan_amount = loan * 1_000_000_000
    if asset_unit == "Triệu":
        asset_value = asset * 1_000_000
    else:
        asset_value = asset * 1_000_000_000
    income_vnd = income * 1_000_000
    old_debt_vnd = old_debt * 1_000_000
    # ======================
    # EMI
    # ======================
    r = interest / 100 / 12
    n = years * 12
    emi = (loan_amount * r * (1 + r) ** n) / ((1 + r) ** n - 1)
    # ======================
    # DTI
    # ======================
    dti = ((emi + old_debt_vnd) / income_vnd) * 100
    # ======================
    # LTV
    # ======================
    ltv = (loan_amount / asset_value) * 100
        st.markdown("---")
    st.subheader("📊 Kết quả tính toán")
    c1, c2, c3 = st.columns(3)
    c1.metric(  "EMI",  f"{emi:,.0f} VNĐ/tháng"  )
    c2.metric(    "DTI",   f"{dti:.2f}%"  )
    c3.metric(   "LTV",  f"{ltv:.2f}%" )
    st.markdown("---")
    score = 0
    # DTI
    if dti <= 40:
        score += 40
    elif dti <= 50:
        score += 25
    else:
        score += 10
    # LTV
    if ltv <= 70:
        score += 30
    elif ltv <= 80:
        score += 20
    else:
        score += 10
    # CIC
    if cic >= 750:
        score += 30
    elif cic >= 650:
        score += 20
    else: score += 10
            st.subheader("🏦 Kết quả thẩm định")
    st.metric(
        "Điểm đánh giá",
        score   )
    if score >= 85:
        st.success("✅ KẾT QUẢ: PHÊ DUYỆT KHOẢN VAY")
    elif score >= 70:
        st.warning("🟡 KẾT QUẢ: CẦN XEM XÉT THÊM")
    else:
        st.error("❌ KẾT QUẢ: TỪ CHỐI KHOẢN VAY")
