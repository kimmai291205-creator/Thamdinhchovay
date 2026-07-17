import streamlit as st

# ==========================
# Cấu hình trang
# ==========================
st.set_page_config(
    page_title="Mini App Thẩm định cho vay",
    page_icon="🏦",
    layout="wide"
)

# ==========================
# Tiêu đề
# ==========================

st.title("🏦 MINI APP THẨM ĐỊNH CHO VAY KHÁCH HÀNG CÁ NHÂN")

st.markdown("---")

# ==========================
# Chia thành 2 cột
# ==========================

col1, col2 = st.columns(2)

# ==========================
# Cột trái
# ==========================

with col1:

    st.subheader("👤 Thông tin khách hàng")

    name = st.text_input("Họ và tên")

    age = st.number_input(
        "Tuổi",
        min_value=18,
        max_value=70,
        value=25
    )

    job = st.text_input("Nghề nghiệp")

    income = st.number_input(
        "Thu nhập (Triệu đồng/tháng)",
        min_value=1.0,
        value=20.0
    )

    dependents = st.number_input(
        "Số người phụ thuộc",
        min_value=0,
        value=0
    )

# ==========================
# Cột phải
# ==========================

with col2:

    st.subheader("💰 Thông tin khoản vay")

    loan = st.number_input(
        "Số tiền vay",
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
        "Thời gian vay",
        1,
        30,
        20
    )

    interest = st.slider(
        "Lãi suất (%/năm)",
        1.0,
        20.0,
        8.5
    )

st.markdown("---")

st.subheader("🏠 Tài sản đảm bảo")

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

st.subheader("📈 Thông tin tín dụng")

cic = st.slider(
    "Điểm CIC",
    300,
    900,
    750
)

old_debt = st.number_input(
    "Khoản trả nợ hiện tại (Triệu/tháng)",
    value=2.0
)

st.markdown("---")

st.button("🔍 THẨM ĐỊNH")
