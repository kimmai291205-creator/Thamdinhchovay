import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Mini App Thẩm định Khoản vay", page_icon="💰", layout="wide")

st.title("🏦 MINI APP THẨM ĐỊNH CHO VAY KHÁCH HÀNG CÁ NHÂN")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:

    loan_amount = st.number_input(
        "Số tiền vay (VNĐ)",
        min_value=1000000,
        value=500000000,
        step=1000000
    )

    years = st.number_input(
        "Thời gian vay (Năm)",
        min_value=1,
        max_value=35,
        value=10
    )

    interest = st.number_input(
        "Lãi suất (%/năm)",
        min_value=1.0,
        max_value=30.0,
        value=9.0
    )

    income = st.number_input(
        "Thu nhập hàng tháng (VNĐ)",
        min_value=1000000,
        value=30000000,
        step=1000000
    )

    dependents = st.number_input(
        "Số người phụ thuộc",
        min_value=0,
        max_value=10,
        value=1
    )

with col2:

    old_debt = st.number_input(
        "Dư nợ khoản vay cũ (VNĐ/tháng)",
        min_value=0,
        value=2000000,
        step=500000
    )

    collateral = st.number_input(
        "Giá trị tài sản đảm bảo (VNĐ)",
        min_value=1000000,
        value=800000000,
        step=1000000
    )

    cic = st.slider(
        "Điểm CIC",
        min_value=300,
        max_value=900,
        value=750
    )

st.markdown("---")

if st.button("THẨM ĐỊNH"):

    monthly_rate = interest/100/12

    months = years*12

    emi = (loan_amount*monthly_rate*(1+monthly_rate)**months)/((1+monthly_rate)**months-1)

    dti = (emi + old_debt)/income*100

    ltv = loan_amount/collateral*100

    score = 100

    # DTI
    if dti > 50:
        score -= 40
    elif dti > 40:
        score -= 20

    # LTV
    if ltv > 90:
        score -= 30
    elif ltv > 80:
        score -= 15

    # CIC
    if cic < 600:
        score -= 40
    elif cic < 700:
        score -= 20

    # Người phụ thuộc
    if dependents >= 3:
        score -= 10

    st.subheader("📊 KẾT QUẢ THẨM ĐỊNH")

    df = pd.DataFrame({

        "Chỉ tiêu":[
            "Khoản trả hàng tháng",
            "DTI",
            "LTV",
            "Điểm CIC",
            "Điểm đánh giá"
        ],

        "Giá trị":[
            f"{emi:,.0f} VNĐ",
            f"{dti:.2f} %",
            f"{ltv:.2f} %",
            cic,
            score
        ]

    })

    st.table(df)

    st.markdown("---")

    if score >= 80:
        st.success("✅ KHOẢN VAY ĐƯỢC PHÊ DUYỆT")

    elif score >= 60:
        st.warning("🟡 CẦN THẨM ĐỊNH THÊM")

    else:
        st.error("❌ TỪ CHỐI KHOẢN VAY")

    st.markdown("---")

    st.subheader("Phân tích")

    if dti > 50:
        st.write("• DTI cao → Khả năng trả nợ thấp.")

    else:
        st.write("• DTI ở mức an toàn.")

    if ltv > 80:
        st.write("• Giá trị khoản vay cao so với tài sản đảm bảo.")

    else:
        st.write("• Tài sản đảm bảo đáp ứng yêu cầu.")

    if cic >= 750:
        st.write("• Lịch sử tín dụng rất tốt.")
    elif cic >=700:
        st.write("• Lịch sử tín dụng tốt.")
    else:
        st.write("• Lịch sử tín dụng chưa tốt.")
