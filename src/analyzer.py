"""
Statistical analysis functions for Lending Club data.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional

def calculate_grade_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate comprehensive metrics by loan grade.
    
    Args:
        df: Cleaned DataFrame with grade and is_default columns
    
    Returns:
        DataFrame with grade-level aggregations
    """
    print("Calculating metrics for each loan grade...")
    
    # Core aggregations by grade
    grade_agg = df.groupby('grade').agg({
        'is_default': ['count', 'sum', 'mean'],
        'loan_amnt': ['mean', 'median', 'std', 'sum'],
        'int_rate': ['mean', 'median', 'std'],
        'annual_inc': ['mean', 'median']
    }).round(4)
    
    # Flatten multi-level column names
    grade_agg.columns = ['_'.join(col) for col in grade_agg.columns]
    
    # Rename for clarity
    grade_metrics = grade_agg.rename(columns={
        'is_default_count': 'total_loans',
        'is_default_sum': 'num_defaults',
        'is_default_mean': 'default_rate',
        'loan_amnt_mean': 'avg_loan_amount',
        'loan_amnt_median': 'median_loan_amount',
        'loan_amnt_std': 'std_loan_amount',
        'loan_amnt_sum': 'total_volume',
        'int_rate_mean': 'avg_interest_rate',
        'int_rate_median': 'median_interest_rate',
        'int_rate_std': 'std_interest_rate',
        'annual_inc_mean': 'avg_annual_income',
        'annual_inc_median': 'median_annual_income'
    })
    
    # Add derived metrics
    grade_metrics['default_rate_pct'] = (grade_metrics['default_rate'] * 100).round(2)
    grade_metrics['volume_share_pct'] = (
        (grade_metrics['total_volume'] / grade_metrics['total_volume'].sum()) * 100
    ).round(2)
    
    # Calculate risk-adjusted return (simplified)
    grade_metrics['expected_return_pct'] = (
        grade_metrics['avg_interest_rate'] * (1 - grade_metrics['default_rate'])
    ).round(2)
    
    grade_metrics = grade_metrics.reset_index()
    
    print(f"Done. Metrics calculated for {len(grade_metrics)} grades.")
    return grade_metrics

def calculate_subgrade_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate metrics by sub-grade for more granular analysis.
    
    Args:
        df: Cleaned DataFrame with sub_grade column
    
    Returns:
        DataFrame with sub-grade level metrics
    """
    if 'sub_grade' not in df.columns:
        print("Warning: sub_grade column not available")
        return pd.DataFrame()
    
    print("Calculating metrics for each sub-grade...")
    
    subgrade_metrics = df.groupby(['grade', 'sub_grade']).agg({
        'is_default': ['count', 'sum', 'mean'],
        'loan_amnt': ['mean', 'sum'],
        'int_rate': 'mean'
    }).round(4)
    
    # Flatten columns
    subgrade_metrics.columns = ['_'.join(col) for col in subgrade_metrics.columns]
    subgrade_metrics = subgrade_metrics.rename(columns={
        'is_default_count': 'total_loans',
        'is_default_sum': 'num_defaults', 
        'is_default_mean': 'default_rate',
        'loan_amnt_mean': 'avg_loan_amount',
        'loan_amnt_sum': 'total_volume',
        'int_rate_mean': 'avg_interest_rate'
    })
    
    subgrade_metrics['default_rate_pct'] = (subgrade_metrics['default_rate'] * 100).round(2)
    subgrade_metrics = subgrade_metrics.reset_index()
    
    print(f"Done. Metrics calculated for {len(subgrade_metrics)} sub-grades.")
    return subgrade_metrics

def calculate_portfolio_metrics(df: pd.DataFrame) -> Dict:
    """
    Calculate overall portfolio-level metrics.
    
    Args:
        df: Cleaned DataFrame
    
    Returns:
        Dictionary with portfolio statistics
    """
    portfolio = {
        'total_loans': len(df),
        'total_volume': df['loan_amnt'].sum(),
        'avg_loan_size': df['loan_amnt'].mean(),
        'overall_default_rate': df['is_default'].mean(),
        'overall_default_rate_pct': (df['is_default'].mean() * 100),
        'avg_interest_rate': df['int_rate'].mean(),
        'total_defaults': df['is_default'].sum(),
        'default_volume': df[df['is_default'] == 1]['loan_amnt'].sum()
    }
    
    # Risk concentration metrics
    grade_concentration = df['grade'].value_counts(normalize=True).max()
    portfolio['max_grade_concentration_pct'] = (grade_concentration * 100)
    
    # High-risk exposure (grades F, G)
    high_risk_grades = ['F', 'G']
    high_risk_mask = df['grade'].isin(high_risk_grades)
    portfolio['high_risk_loans_pct'] = (high_risk_mask.mean() * 100)
    portfolio['high_risk_volume_pct'] = (
        df[high_risk_mask]['loan_amnt'].sum() / df['loan_amnt'].sum() * 100
    )
    
    print("Portfolio Overview:")
    print(f"Total loans: {portfolio['total_loans']:,}")
    print(f"Total volume: ${portfolio['total_volume']:,.0f}")
    print(f"Overall default rate: {portfolio['overall_default_rate_pct']:.2f}%")
    print(f"Average interest rate: {portfolio['avg_interest_rate']:.2f}%")
    print(f"High-risk exposure (F,G): {portfolio['high_risk_loans_pct']:.1f}% of loans")
    
    return portfolio

def analyze_risk_return_relationship(grade_metrics: pd.DataFrame) -> Dict:
    """
    Analyze the relationship between risk (default rate) and return (interest rate).
    
    Args:
        grade_metrics: DataFrame with grade-level metrics
    
    Returns:
        Dictionary with risk-return analysis
    """
    # Calculate correlation between default rate and interest rate
    correlation = grade_metrics['default_rate'].corr(grade_metrics['avg_interest_rate'])
    
    # Find grades with poor risk-return tradeoff
    # (high default rate but not proportionally high interest rate)
    grade_metrics['risk_premium'] = grade_metrics['avg_interest_rate'] - grade_metrics['default_rate_pct']
    
    analysis = {
        'risk_return_correlation': correlation,
        'avg_risk_premium': grade_metrics['risk_premium'].mean(),
        'worst_risk_return_grade': grade_metrics.loc[grade_metrics['risk_premium'].idxmin(), 'grade'],
        'best_risk_return_grade': grade_metrics.loc[grade_metrics['risk_premium'].idxmax(), 'grade']
    }
    
    print("Risk-Return Analysis:")
    print(f"Risk-return correlation: {correlation:.3f}")
    print(f"Average risk premium: {analysis['avg_risk_premium']:.2f}%")
    print(f"Best risk-return grade: {analysis['best_risk_return_grade']}")
    print(f"Worst risk-return grade: {analysis['worst_risk_return_grade']}")
    
    return analysis

def identify_risk_thresholds(grade_metrics: pd.DataFrame, 
                           acceptable_default_rate: float = 15.0) -> Dict:
    """
    Identify which grades exceed acceptable risk thresholds.
    
    Args:
        grade_metrics: DataFrame with grade metrics
        acceptable_default_rate: Maximum acceptable default rate (%)
    
    Returns:
        Dictionary with risk threshold analysis
    """
    high_risk_grades = grade_metrics[
        grade_metrics['default_rate_pct'] > acceptable_default_rate
    ]['grade'].tolist()
    
    acceptable_grades = grade_metrics[
        grade_metrics['default_rate_pct'] <= acceptable_default_rate
    ]['grade'].tolist()
    
    # Calculate exposure to high-risk grades
    high_risk_volume = grade_metrics[
        grade_metrics['grade'].isin(high_risk_grades)
    ]['total_volume'].sum()
    
    total_volume = grade_metrics['total_volume'].sum()
    high_risk_exposure_pct = (high_risk_volume / total_volume) * 100
    
    analysis = {
        'acceptable_default_rate': acceptable_default_rate,
        'high_risk_grades': high_risk_grades,
        'acceptable_grades': acceptable_grades,
        'high_risk_exposure_pct': high_risk_exposure_pct,
        'num_high_risk_grades': len(high_risk_grades),
        'recommendation': 'REVIEW_EXPOSURE' if high_risk_exposure_pct > 20 else 'ACCEPTABLE'
    }
    
    print(f"Risk Threshold Analysis (>{acceptable_default_rate}% default rate):")
    print(f"High-risk grades: {high_risk_grades}")
    print(f"High-risk exposure: {high_risk_exposure_pct:.1f}% of volume")
    print(f"Recommendation: {analysis['recommendation']}")
    
    return analysis

def calculate_business_impact(df: pd.DataFrame, grade_metrics: pd.DataFrame) -> Dict:
    """
    Calculate business impact metrics for stakeholder communication.
    
    Args:
        df: Full cleaned dataset
        grade_metrics: Grade-level metrics
    
    Returns:
        Dictionary with business impact calculations
    """
    # Calculate potential loss reduction from eliminating high-risk grades
    high_risk_grades = ['F', 'G']
    high_risk_defaults = df[
        (df['grade'].isin(high_risk_grades)) & (df['is_default'] == 1)
    ]['loan_amnt'].sum()
    
    total_defaults_value = df[df['is_default'] == 1]['loan_amnt'].sum()
    
    # Revenue impact of different strategies
    total_interest_revenue = (df['loan_amnt'] * df['int_rate'] / 100).sum()
    
    impact = {
        'total_default_losses': total_defaults_value,
        'high_risk_default_losses': high_risk_defaults,
        'potential_loss_reduction_pct': (high_risk_defaults / total_defaults_value) * 100,
        'total_interest_revenue': total_interest_revenue,
        'loss_to_revenue_ratio': (total_defaults_value / total_interest_revenue) * 100
    }
    
    print("Business Impact Analysis:")
    print(f"Total default losses: ${impact['total_default_losses']:,.0f}")
    print(f"High-risk grade losses: ${impact['high_risk_default_losses']:,.0f}")
    print(f"Potential loss reduction: {impact['potential_loss_reduction_pct']:.1f}%")
    print(f"Loss-to-revenue ratio: {impact['loss_to_revenue_ratio']:.2f}%")
    
    return impact