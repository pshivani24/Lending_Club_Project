# Jack Henry Data Engineering Challenge: Lending Club Analysis

## Overview
This repo has everything for the Lending Club loan data analysis (2007-2015) as part of the Jack Henry Data Engineering challenge. The project shows how to model data, analyze it in Python, and communicate results to stakeholders—all in a clear, modular way.

## Repository Structure
```
lending-club-challenge/
├── README.md                           # You're here
├── requirements.txt                    # Python packages
├── notebooks/
│   └── lending_club_analysis.ipynb     # Main analysis notebook
├── src/
│   ├── __init__.py                     # Package setup
│   ├── data_loader.py                  # Data loading
│   ├── data_cleaner.py                 # Data cleaning
│   ├── analyzer.py                     # Analysis functions
│   └── visualizer.py                   # Visualization functions
├── sql/
│   └── loan_grade_metrics.sql          # BigQuery view
├── outputs/
│   ├── grade_metrics.csv               # Results
│   └── visualizations/                 # Charts
├── data/
│   └── .gitkeep                        # Loan data CSV files
└── docs/
    └── stakeholder_report.md           # Business summary
```

## Challenge Parts

### 1. Data Modeling & SQL
- **File**: `sql/loan_grade_metrics.sql`
- **Goal**: Schema for tracking default rates
- **Output**: BigQuery view with metrics

### 2. Python Analysis
- **File**: `notebooks/lending_club_analysis.ipynb`
- **Goal**: Modular analysis and charts
- **Metrics**: Default rates by grade, risk-return
- **Output**: CSV and charts

### 3. Stakeholder Communication
- **File**: `docs/stakeholder_report.md`
- **Goal**: Turn analysis into business insights
- **Focus**: Actionable recommendations

## Key Findings

1. **Risk Stratification**: Grades separate risk well (A: ~5% vs G: ~51%)
2. **Portfolio Concentration**: Most loans are C-E
3. **Risk-Return Alignment**: Interest rates generally match risk

## Business Recommendations

1. **Limit High-Risk Loans**: F-G grades capped at 15%
2. **Extra Checks**: More verification for lower grades
3. **Adjust Rates**: Use risk-based interest rates

## Technical Notes

- **Modular**: Each step (loading, cleaning, analysis, viz) is separate
- **Reproducible**: All dependencies listed, random seeds set
- **Scalable**: Handles big datasets
- **Documented**: Clear comments and docstrings

## Dependencies
- pandas >= 1.5.0
- numpy >= 1.21.0
- matplotlib >= 3.5.0
- seaborn >= 0.11.0
- jupyter >= 1.0.0

## Author
Submission for Jack Henry & Associates Data Engineering Challenge

This project is for assessment only.
