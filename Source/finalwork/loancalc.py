def calculate_monthly_payment(loan_amount, annual_interest_rate, loan_term_years):
    # 年利率轉換成月利率
    monthly_interest_rate = annual_interest_rate / 12 / 100
    # 貸款期限轉換成月數
    loan_term_months = loan_term_years * 12
    # 計算每月還款金額
    if monthly_interest_rate == 0:  # 若利率為0，則直接平均分攤
        monthly_payment = loan_amount / loan_term_months
    else:
        monthly_payment = loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate) ** loan_term_months) / ((1 + monthly_interest_rate) ** loan_term_months - 1)
    
    return f'{monthly_payment}'
