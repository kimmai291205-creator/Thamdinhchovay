import streamlit as st
st.title("🏦 Loan Approval App")
name = st.text_input("Tên khách hàng")
income = st.number_input("Thu nhập")
loan = st.number_input("Khoản vay")
if st.button("Đánh giá"):
    if income > loan/20:
        st.success("Đủ điều kiện vay")
    else:
        st.error("Không đủ điều kiện")
