import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

from credit_score import calculate_cic_score, credit_decision
from report import export_excel
from pdf_report import create_pdf


# ===============================
# CẤU HÌNH TRANG
# ===============================

st.set_page_config(
    page_title="Hệ thống thẩm định cho vay",
    page_icon="🏦",
    layout="wide"
)


# ===============================
# SESSION
# ===============================

if "submitted" not in st.session_state:
    st.session_state.submitted = False


# ===============================
# TRANG CHỦ
# ===============================

st.title("🏦 HỆ THỐNG HỖ TRỢ THẨM ĐỊNH CHO VAY")

st.write(
    """
    Hệ thống hỗ trợ đánh giá hồ sơ vay khách hàng cá nhân.
    
    Quy trình:
    
    1️⃣ Nhập thông tin khách hàng  
    2️⃣ Phân tích khả năng trả nợ  
    3️⃣ Chấm điểm tín dụng CIC  
    4️⃣ Đánh giá rủi ro khoản vay  
    5️⃣ Xuất báo cáo thẩm định
    """
)


# ===============================
# NHẬP THÔNG TIN KHÁCH HÀNG
# ===============================

st.divider()

st.subheader("📝 THÔNG TIN KHÁCH HÀNG & KHOẢN VAY")


col1, col2 = st.columns(2)


with col1:

    name = st.text_input(
        "Họ và tên khách hàng",
        value="Nguyễn Văn A"
    )

    loan_amount = st.number_input(
        "Số tiền đề nghị vay (VNĐ)",
        min_value=0.0,
        value=500000000.0,
        step=10000000.0
    )


    asset_value = st.number_input(
        "Giá trị tài sản đảm bảo (VNĐ)",
        min_value=1.0,
        value=1500000000.0,
        step=10000000.0
    )


    years = st.slider(
        "Thời hạn vay (năm)",
        1,
        30,
        20
    )


with col2:

    income = st.number_input(
        "Thu nhập hàng tháng (VNĐ)",
        min_value=1.0,
        value=25000000.0,
        step=1000000.0
    )


    old_debt = st.number_input(
        "Khoản trả nợ hiện tại (VNĐ)",
        min_value=0.0,
        value=2000000.0,
        step=500000.0
    )


    interest = st.slider(
        "Lãi suất (%/năm)",
        1.0,
        20.0,
        8.5
    )



# ===============================
# NÚT BẮT ĐẦU
# ===============================


st.divider()


if st.button(
    "🚀 BẮT ĐẦU THẨM ĐỊNH HỒ SƠ",
    use_container_width=True
):

    st.session_state.submitted = True



# ===============================
# PHÂN TÍCH HỒ SƠ
# ===============================


if st.session_state.submitted:


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

    dti = ((emi + old_debt) / income) * 100

    ltv = (loan_amount / asset_value) * 100



    # ===============================
    # CIC
    # ===============================


    st.divider()

    st.subheader("📈 CHẤM ĐIỂM CIC")


    c1, c2 = st.columns(2)


    with c1:

        credit_history = st.selectbox(
            "Lịch sử tín dụng",
            [
                "Tốt",
                "Trung bình",
                "Xấu"
            ]
        )


    with c2:

        job_stability = st.number_input(
            "Số năm làm việc ổn định",
            min_value=0,
            value=3
        )



    cic_score = calculate_cic_score(
        credit_history,
        income,
        dti,
        ltv,
        job_stability
    )


    decision = credit_decision(
        cic_score
    )



    # ===============================
    # KẾT QUẢ
    # ===============================


    st.divider()

    st.subheader(
        "📊 KẾT QUẢ THẨM ĐỊNH"
    )


    k1, k2, k3 = st.columns(3)


    with k1:

        st.metric(
            "Điểm CIC",
            f"{cic_score}/100"
        )


    with k2:

        st.metric(
            "DTI",
            f"{dti:.2f}%"
        )


    with k3:

        st.metric(
            "Quyết định",
            decision
        )



    # ===============================
    # DASHBOARD
    # ===============================


    st.divider()

    st.subheader(
        "📊 DASHBOARD PHÂN TÍCH RỦI RO"
    )


    d1, d2 = st.columns(2)



    with d1:

        st.write(
            "**Cơ cấu khoản vay**"
        )


        chart_data = pd.DataFrame({

            "Nguồn vốn":
            [
                "Khoản vay",
                "Vốn tự có"
            ],

            "Giá trị":
            [
                loan_amount,
                max(
                    0,
                    asset_value-loan_amount
                )
            ]

        })


        fig, ax = plt.subplots()


        ax.pie(
            chart_data["Giá trị"],
            labels=chart_data["Nguồn vốn"],
            autopct="%1.1f%%",
            startangle=90
        )


        ax.axis("equal")


        st.pyplot(fig)



    with d2:

        st.write(
            "**Chỉ số an toàn tín dụng**"
        )


        risk_data = pd.DataFrame({

            "Chỉ số":
            [
                "CIC Score",
                "DTI Safety",
                "LTV Safety"
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



    # ===============================
    # XUẤT BÁO CÁO
    # ===============================


    st.divider()

    st.subheader(
        "📄 XUẤT BÁO CÁO THẨM ĐỊNH"
    )



    report_data = {

        "Họ tên":
        [name],

        "Thu nhập":
        [income],

        "Khoản vay":
        [loan_amount],

        "EMI":
        [emi],

        "DTI":
        [dti],

        "LTV":
        [ltv],

        "Điểm CIC":
        [cic_score],

        "Kết quả":
        [decision]

    }



    e1, e2 = st.columns(2)



    with e1:

        excel_file = export_excel(
            report_data
        )


        st.download_button(

            "📥 Tải báo cáo Excel",

            excel_file,

            file_name=
            "bao_cao_tham_dinh.xlsx",

            mime=
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

        )



    with e2:


        pdf_data = {

            "Họ tên": name,
            "Khoản vay": loan_amount,
            "EMI": emi,
            "DTI": dti,
            "LTV": ltv,
            "CIC": cic_score,
            "Quyết định": decision

        }


        pdf_file = create_pdf(
            pdf_data
        )


        st.download_button(

            "📄 Tải báo cáo PDF",

            pdf_file,

            file_name=
            "bao_cao_tham_dinh.pdf",

            mime=
            "application/pdf"

        )
