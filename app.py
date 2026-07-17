import streamlit as st
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



    # Khả năng trả nợ

    if dti < 35:
        score += 10

    elif dti > 50:
        score -= 10



    # Tài sản đảm bảo

    if ltv < 70:
        score += 10

    elif ltv > 90:
        score -= 10



    # Thâm niên công việc

    if job_year >= 5:
        score += 5



    score = max(0, min(score, 100))


    return score



def credit_decision(score):

    if score >= 80:

        return "✅ Hồ sơ tốt - Đề xuất phê duyệt"

    elif score >= 60:

        return "⚠️ Cần xem xét thêm"

    else:

        return "❌ Rủi ro cao - Không đề xuất"



# ==========================
# TRANG CHỦ
# ==========================


st.title(
    "🏦 HỆ THỐNG HỖ TRỢ THẨM ĐỊNH CHO VAY"
)


st.write(
"""
Ứng dụng hỗ trợ đánh giá nhanh khả năng vay vốn
của khách hàng cá nhân.

Vui lòng nhập thông tin bên dưới.
"""
)



# ==========================
# THÔNG TIN KHÁCH HÀNG
# ==========================


st.subheader("👤 THÔNG TIN KHÁCH HÀNG")


col1, col2 = st.columns(2)



with col1:

    name = st.text_input(
        "Họ và tên",
        "Nguyễn Văn A"
    )


    income_input = st.number_input(
        "Thu nhập hàng tháng (triệu VNĐ)",
        min_value=0,
        value=25,
        step=1
    )


    job = st.text_input(
        "Nghề nghiệp",
        "Nhân viên văn phòng"
    )



with col2:

    job_year = st.number_input(
        "Số năm làm việc ổn định",
        min_value=0,
        value=3,
        step=1
    )


    credit_history = st.selectbox(
        "Lịch sử tín dụng",
        [
            "Tốt",
            "Trung bình",
            "Xấu"
        ]
    )



# Quy đổi thu nhập

income = income_input * 1_000_000



# ==========================
# THÔNG TIN KHOẢN VAY
# ==========================


st.subheader("💰 THÔNG TIN KHOẢN VAY")


loan_input = st.number_input(
    "Số tiền đề nghị vay (triệu VNĐ)",
    min_value=0,
    value=500,
    step=10
)



asset_input = st.number_input(
    "Giá trị tài sản đảm bảo (triệu VNĐ)",
    min_value=0,
    value=1500,
    step=50
)



loan_amount = loan_input * 1_000_000

asset_value = asset_input * 1_000_000



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



old_debt_input = st.number_input(
    "Khoản trả nợ hiện tại/tháng (triệu VNĐ)",
    min_value=0,
    value=2,
    step=1
)


old_debt = old_debt_input * 1_000_000



# ==========================
# NÚT THẨM ĐỊNH
# ==========================


st.divider()


if st.button(
    "🚀 BẮT ĐẦU THẨM ĐỊNH",
    use_container_width=True
):


    # Tính khoản trả hàng tháng

    r = interest / 100 / 12

    n = years * 12


    if r > 0:

        emi = (
            loan_amount * r * (1+r)**n
        ) / (
            (1+r)**n - 1
        )

    else:

        emi = loan_amount / n



    # Chỉ số tài chính

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



    # Điểm tín dụng

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
    # HIỂN THỊ KẾT QUẢ
    # ==========================


    st.divider()


    st.subheader(
        "📊 KẾT QUẢ THẨM ĐỊNH"
    )


    c1, c2, c3 = st.columns(3)



    c1.metric(
        "Điểm CIC",
        f"{cic_score}/100"
    )


    c2.metric(
        "Tỷ lệ nợ DTI",
        f"{dti:.1f}%"
    )


    c3.metric(
        "Đánh giá",
        decision
    )



    st.success(
f"""
👤 Khách hàng: {name}

💰 Khoản vay:
{loan_input:,.0f} triệu VNĐ

🏠 Tài sản đảm bảo:
{asset_input:,.0f} triệu VNĐ

📅 Số tiền trả hàng tháng:
{emi/1_000_000:,.2f} triệu VNĐ

📌 Tỷ lệ vay trên tài sản (LTV):
{ltv:.1f}%

"""
)



    # ==========================
    # BIỂU ĐỒ RỦI RO
    # ==========================


    st.subheader(
        "📈 PHÂN TÍCH RỦI RO"
    )


    risk_data = pd.DataFrame({

        "Chỉ số":
        [
            "Điểm CIC",
            "An toàn DTI",
            "An toàn LTV"
        ],


        "Điểm":
        [
            cic_score,
            max(0,100-dti),
            max(0,100-ltv)
        ]

    })


    st.bar_chart(
        risk_data.set_index("Chỉ số")
    )
