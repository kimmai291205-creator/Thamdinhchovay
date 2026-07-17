import streamlit as st

st.title("👤 Hồ sơ khách hàng")

st.subheader("Thông tin cá nhân")

col1, col2 = st.columns(2)

with col1:

    st.text_input("Họ và tên")

    st.number_input(
        "Tuổi",
        18,
        70,
        25
    )

    st.selectbox(
        "Giới tính",
        [
            "Nam",
            "Nữ"
        ]
    )

with col2:

    st.text_input("Nghề nghiệp")

    st.number_input(
        "Thu nhập (Triệu/tháng)",
        value=20.0
    )

    st.number_input(
        "Số người phụ thuộc",
        value=0
    )
