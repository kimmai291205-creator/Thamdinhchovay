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
        value=500.0
    )

    loan_unit = st.selectbox(
        "Đơn vị",
        [
            "Triệu",
            "Tỷ"
        ]
    )

    years = st.slider(
        "Thời gian vay (năm)",
        1,
        30,
        20
    )

with col2:

    interest = st.slider(
        "Lãi suất (%/năm)",
        1.0,
        20.0,
        8.5
    )

    income = st.number_input(
        "Thu nhập (Triệu/tháng)",
        value=25.0
    )

    old_debt = st.number_input(
        "Khoản trả nợ hiện tại (Triệu/tháng)",
        value=2.0
    )

st.markdown("---")

# ==========================
# Tài sản đảm bảo
# ==========================

st.subheader("Tài sản đảm bảo")

asset = st.number_input(
    "Giá trị tài sản",
    value=1.5
)

asset_unit = st.selectbox(
    "Đơn vị tài sản",
    [
        "Tỷ",
        "Triệu"
    ]
)

st.markdown("---")

# ==========================
# CIC
# ==========================

st.subheader("Thông tin tín dụng")

cic = st.slider(
    "Điểm CIC",
    300,
    900,
    750
)
