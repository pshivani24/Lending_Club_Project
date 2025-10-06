-- BigQuery SQL for loan grade metrics view
-- This creates a materialized view for efficient default rate tracking

CREATE OR REPLACE VIEW `lending_club.loan_grade_metrics` AS
SELECT 
    grade,
    sub_grade,
    
    -- Core loan counts
    COUNT(*) as total_loans,
    COUNTIF(loan_status = 'Charged Off') as charged_off_loans,
    COUNTIF(loan_status = 'Fully Paid') as fully_paid_loans,
    COUNTIF(loan_status = 'Current') as current_loans,
    COUNTIF(loan_status = 'Default') as default_loans,
    
    -- Default rate calculation  
    SAFE_DIVIDE(
        COUNTIF(loan_status IN ('Charged Off', 'Default')), 
        COUNT(*)
    ) as default_rate,
    
    -- Financial metrics
    AVG(loan_amnt) as avg_loan_amount,
    PERCENTILE_CONT(loan_amnt, 0.5) OVER (PARTITION BY grade) as median_loan_amount,
    STDDEV(loan_amnt) as std_loan_amount,
    SUM(loan_amnt) as total_volume,
    
    -- Interest rate metrics
    AVG(int_rate) as avg_interest_rate,
    PERCENTILE_CONT(int_rate, 0.5) OVER (PARTITION BY grade) as median_interest_rate,
    MIN(int_rate) as min_interest_rate,
    MAX(int_rate) as max_interest_rate,
    
    -- Borrower profile metrics
    AVG(annual_inc) as avg_annual_income,
    PERCENTILE_CONT(annual_inc, 0.5) OVER (PARTITION BY grade) as median_annual_income,
    
    -- Risk metrics
    AVG(dti) as avg_debt_to_income,
    AVG(CASE WHEN emp_length = '10+ years' THEN 10
             WHEN emp_length = '< 1 year' THEN 0.5
             ELSE SAFE_CAST(REGEXP_EXTRACT(emp_length, r'(\d+)') AS FLOAT64)
        END) as avg_emp_length_years,
    
    -- Derived business metrics
    AVG(int_rate) * (1 - SAFE_DIVIDE(COUNTIF(loan_status IN ('Charged Off', 'Default')), COUNT(*))) as expected_return_rate,
    CURRENT_TIMESTAMP() as last_updated,
    COUNT(DISTINCT issue_d) as months_represented

FROM 
    `lending_club.raw_loan_data`
WHERE 
    grade IS NOT NULL 
    AND loan_status IS NOT NULL
    AND loan_status IN ('Charged Off', 'Fully Paid', 'Current', 'Default')
    AND loan_amnt > 0
    AND int_rate > 0
GROUP BY 
    grade, 
    sub_grade
ORDER BY 
    grade, 
    sub_grade;

-- Query to get default rates by grade 
SELECT 
    grade,
    SUM(charged_off_loans + default_loans) as num_defaults,
    SUM(total_loans) as total_loans,
    SAFE_DIVIDE(
        SUM(charged_off_loans + default_loans), 
        SUM(total_loans)
    ) as default_rate,
    ROUND(
        SAFE_DIVIDE(
            SUM(charged_off_loans + default_loans), 
            SUM(total_loans)
        ) * 100, 2
    ) as default_rate_pct
FROM 
    `lending_club.loan_grade_metrics`
GROUP BY 
    grade
ORDER BY 
    grade;

-- Monthly default rate trends by grade
SELECT 
    grade,
    EXTRACT(YEAR FROM issue_d) as year,
    EXTRACT(MONTH FROM issue_d) as month,
    COUNT(*) as loans_issued,
    COUNTIF(loan_status IN ('Charged Off', 'Default')) as defaults,
    SAFE_DIVIDE(
        COUNTIF(loan_status IN ('Charged Off', 'Default')), 
        COUNT(*)
    ) as monthly_default_rate
FROM 
    `lending_club.raw_loan_data`
WHERE 
    grade IS NOT NULL
    AND issue_d IS NOT NULL
GROUP BY 
    grade, year, month
ORDER BY 
    grade, year, month;

-- Portfolio concentration analysis
SELECT 
    grade,
    total_loans,
    total_volume,
    ROUND(total_loans / SUM(total_loans) OVER () * 100, 2) as loan_count_pct,
    ROUND(total_volume / SUM(total_volume) OVER () * 100, 2) as volume_pct,
    default_rate * 100 as default_rate_pct
FROM 
    `lending_club.loan_grade_metrics`
WHERE 
    grade IS NOT NULL
ORDER BY 
    grade;