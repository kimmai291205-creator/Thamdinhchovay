import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd


# ==========================
# CẤU HÌNH TRANG
# ==========================

st.set_page_config(
    page_title="Hệ thống thẩm định cho vay",
    page_icon="🏦",
    layout="wide"
)



# ==========================
# HÀM CHẤM ĐIỂM TÍN DỤNG
# ==========================

def calculate_cic_score(
    credit_history,
    income,
    dti,
    ltv,
    job_year
):

    score = 50


    # Lịch sử tín dụng

    if credit_history == "Tốt":
        score += 25

    elif credit_history == "Trung bình":
        score += 10

    else:
        score -= 20



    # Thu nhập

    if income >= 30000000:
        score += 10

    elif income >= 15000000:
        score += 5



    # DTI

    if dti < 35:
        score += 10

    elif dti > 50:
        score -= 10



    # LTV

    if ltv < 70:
        score += 10

    elif ltv > 90:
        score -= 10



    # Thời gian làm việc

    if job_year >= 5:
        score += 5



    score = max(
        0,
        min(100, score)
    )


    return score




def credit_decision(score):

    if score >= 80:
        return "✅ Hồ sơ tốt - Đề xuất phê duyệt"

    elif score >= 60:
        return "⚠️ Hồ sơ cần xem xét thêm"

    else:
        return "❌ Rủi ro cao - Không đề xuất"



# ==========================
# TRANG CHỦ
# ==========================


st.title(
    "🏦 HỆ THỐNG HỖ TRỢ THẨM ĐỊNH CHO VAY"
)


st.info(
"""
Nhập thông tin khách hàng để hệ thống
phân tích khả năng vay vốn.
"""
)



# ==========================
# NHẬP THÔNG TIN
# ==========================


st.subheader(
    "👤 Thông tin khách hàng"
)


col1, col2 = st.columns(2)


with col1:

    name = st.text_input(
        "Họ và tên",
        "Nguyễn Văn A"
    )


    income = st.number_input(
        "Thu nhập hàng tháng (VNĐ)",
        value=25000000
    )


    job_year = st.number_input(
        "Số năm làm việc",
        min_value=0,
        value=3
    )



with col2:

    credit_history = st.selectbox(
        "Lịch sử tín dụng",
        [
            "Tốt",
            "Trung bình",
            "Xấu"
        ]
    )


    job = st.text_input(
        "Nghề nghiệp",
        "Nhân viên văn phòng"
    )



st.subheader(
    "💰 Thông tin khoản vay"
)



loan_amount = st.number_input(
    "Số tiền đề nghị vay (VNĐ)",
    value=500000000
)



asset_value = st.number_input(
    "Giá trị tài sản đảm bảo (VNĐ)",
    value=1500000000
)



years = st.slider(
    "Thời hạn vay (năm)",
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



old_debt = st.number_input(
    "Khoản trả nợ hiện tại/tháng",
    value=2000000
)



# ==========================
# NÚT THẨM ĐỊNH
# ==========================


if st.button(
    "🚀 BẮT ĐẦU THẨM ĐỊNH",
    use_container_width=True
):


    # Tính EMI

    r = interest / 100 / 12

    n = years * 12


    if r > 0:

        emi = (
            loan_amount*r*(1+r)**n
        ) / (
            (1+r)**n - 1
        )

    else:

        emi = loan_amount/n



    # Chỉ số

    dti = (
        (emi + old_debt)
        /
        income
    ) * 100



    ltv = (
        loan_amount
        /
        asset_value
    ) * 100



    # CIC

    cic_score = calculate_cic_score(
        credit_history,
        income,
        dti,
        ltv,
        job_year
    )


    decision = credit_decision(
        cic_score
    )



    # ==========================
    # KẾT QUẢ
    # ==========================


    st.divider()


    st.subheader(
        "📊 KẾT QUẢ THẨM ĐỊNH"
    )



    c1,c2,c3 = st.columns(3)


    c1.metric(
        "Điểm CIC",
        f"{cic_score}/100"
    )


    c2.metric(
        "DTI",
        f"{dti:.1f}%"
    )


    c3.metric(
        "Kết quả",
        decision
    )



    # ==========================
    # BIỂU ĐỒ
    # ==========================


    st.subheader(
        "📈 PHÂN TÍCH RỦI RO"
    )


    risk = pd.DataFrame({

        "Chỉ số":
        [
            "CIC",
            "DTI an toàn",
            "LTV an toàn"
        ],


        "Điểm":
        [
            cic_score,
            max(0,100-dti),
            max(0,100-ltv)
        ]

    })


    st.bar_chart(
        risk.set_index("Chỉ số")
    )



    st.success(
        f"""
        Khách hàng: {name}

        Khoản vay:
        {loan_amount:,.0f} VNĐ

        Khoản trả hàng tháng:
        {emi:,.0f} VNĐ
        """
    )
