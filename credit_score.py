def calculate_cic_score (
    credit_history,
    income,
    dti,
    ltv,
    job_stability):
   score = 0
    # Lịch sử tín dụng (30 điểm)
    if credit_history == "Tốt":
        score += 30
    elif credit_history == "Trung bình":
        score += 20
    else:
        score += 5
    # Thu nhập (25 điểm)
    if income >= 30000000:
        score += 25
    elif income >= 15000000:
        score += 20
    else:
        score += 10
    # DTI (20 điểm)
    if dti < 30:
        score += 20
    elif dti <= 50:
        score += 15
    else:
        score += 5
    # LTV (15 điểm)
    if ltv < 50:
        score += 15
    elif ltv <= 70:
        score += 10
    else:
        score += 5
    # Ổn định nghề nghiệp (10 điểm)
    if job_stability >= 5:
        score += 10
    elif job_stability >= 2:
        score += 7
    else:
        score += 3
    return score
def credit_decision (score):
    if score >= 80:
        return "🟢 PHÊ DUYỆT"
    elif score >= 60:
        return "🟡 XEM XÉT"
    else:
        return "🔴 TỪ CHỐI"
