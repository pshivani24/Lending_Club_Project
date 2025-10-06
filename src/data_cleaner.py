"""
Data cleaning functions for Lending Club analysis.
"""

import pandas as pd
import numpy as np
from typing import List, Tuple, Optional

# Define essential columns for the analysis
ESSENTIAL_COLUMNS = [
    'grade', 'sub_grade', 'loan_status', 'loan_amnt', 
    'int_rate', 'annual_inc', 'emp_length', 'purpose'
]

# Define completed loan statuses for default analysis
COMPLETED_STATUSES = ['Fully Paid', 'Charged Off', 'Default']

def clean_lending_club_data(df: pd.DataFrame, 
                           focus_columns: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Clean Lending Club data for default analysis.
    
    Args:
        df: Raw Lending Club DataFrame
        focus_columns: Columns to focus on (uses ESSENTIAL_COLUMNS if None)
    
    Returns:
        Cleaned DataFrame ready for analysis
    """
    if focus_columns is None:
        focus_columns = ESSENTIAL_COLUMNS
    
    print("Starting data cleaning...")
    print(f"Rows before cleaning: {df.shape[0]:,}")
    
    # Step 1: Select essential columns (if they exist)
    available_cols = [col for col in focus_columns if col in df.columns]
    missing_cols = [col for col in focus_columns if col not in df.columns]
    
    if missing_cols:
        print(f"Missing columns: {missing_cols}")
    
    df_clean = df[available_cols].copy()
    print(f"After column selection: {df_clean.shape[0]:,} rows × {df_clean.shape[1]} columns")
    
    # Step 2: Remove rows with missing critical values
    critical_cols = ['grade', 'loan_status']
    before_critical = len(df_clean)
    df_clean = df_clean.dropna(subset=critical_cols)
    print(f"After dropping missing grade/status: {df_clean.shape[0]:,} rows "
          f"(removed {before_critical - len(df_clean):,})")
    
    # Step 3: Focus on completed loans for default analysis
    before_status = len(df_clean)
    df_clean = df_clean[df_clean['loan_status'].isin(COMPLETED_STATUSES)]
    print(f"After filtering to completed loans: {df_clean.shape[0]:,} rows "
          f"(removed {before_status - len(df_clean):,})")
    
    # Step 4: Clean interest rate column
    if 'int_rate' in df_clean.columns:
        df_clean = clean_interest_rate(df_clean)
    
    # Step 5: Create default indicator
    df_clean = add_default_indicator(df_clean)
    
    # Step 6: Clean employment length
    if 'emp_length' in df_clean.columns:
        df_clean = clean_employment_length(df_clean)
    
    # Step 7: Handle remaining missing values
    df_clean = handle_missing_values(df_clean)
    
    print(f"Final cleaned dataset: {df_clean.shape[0]:,} rows × {df_clean.shape[1]} columns")
    print("Cleaning done.")
    
    return df_clean

def clean_interest_rate(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean interest rate column (remove % sign and convert to float).
    
    Args:
        df: DataFrame with int_rate column
    
    Returns:
        DataFrame with cleaned int_rate
    """
    df = df.copy()
    
    if df['int_rate'].dtype == 'object':
        # Remove % sign and convert to float
        df['int_rate'] = df['int_rate'].str.rstrip('%').astype(float)
        print("✓ Cleaned interest rate column (removed % signs)")
    
    return df

def add_default_indicator(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add binary default indicator column.
    
    Args:
        df: DataFrame with loan_status column
    
    Returns:
        DataFrame with is_default column added
    """
    df = df.copy()
    
    # Define default statuses
    default_statuses = ['Charged Off', 'Default']
    df['is_default'] = df['loan_status'].isin(default_statuses).astype(int)
    
    default_count = df['is_default'].sum()
    default_rate = (default_count / len(df)) * 100
    
    print(f"✓ Added default indicator: {default_count:,} defaults ({default_rate:.1f}%)")
    
    return df

def clean_employment_length(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean employment length column and convert to numeric years.
    
    Args:
        df: DataFrame with emp_length column
    
    Returns:
        DataFrame with cleaned emp_length_years column
    """
    df = df.copy()
    
    # Convert employment length to numeric years
    def parse_emp_length(emp_str):
        if pd.isna(emp_str):
            return np.nan
        if emp_str == '< 1 year':
            return 0.5
        elif emp_str == '10+ years':
            return 10
        elif 'year' in str(emp_str):
            return float(str(emp_str).split()[0])
        else:
            return np.nan
    
    df['emp_length_years'] = df['emp_length'].apply(parse_emp_length)
    print("✓ Converted employment length to numeric years")
    
    return df

def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing values in non-critical columns.
    
    Args:
        df: DataFrame to clean
    
    Returns:
        DataFrame with missing values handled
    """
    df = df.copy()
    
    # Fill missing annual income with median by grade
    if 'annual_inc' in df.columns:
        median_income_by_grade = df.groupby('grade')['annual_inc'].median()
        df['annual_inc'] = df.groupby('grade')['annual_inc'].transform(
            lambda x: x.fillna(x.median())
        )
    
    # Fill missing employment years with median
    if 'emp_length_years' in df.columns:
        median_emp = df['emp_length_years'].median()
        df['emp_length_years'] = df['emp_length_years'].fillna(median_emp)
    
    print("✓ Handled missing values in non-critical columns")
    
    return df

def get_cleaning_summary(df_original: pd.DataFrame, df_clean: pd.DataFrame) -> dict:
    """
    Generate summary of cleaning process.
    
    Args:
        df_original: Original DataFrame
        df_clean: Cleaned DataFrame
    
    Returns:
        Dictionary with cleaning summary statistics
    """
    summary = {
        'original_rows': len(df_original),
        'cleaned_rows': len(df_clean),
        'rows_removed': len(df_original) - len(df_clean),
        'removal_pct': ((len(df_original) - len(df_clean)) / len(df_original)) * 100,
        'original_cols': df_original.shape[1],
        'cleaned_cols': df_clean.shape[1],
        'default_rate': (df_clean['is_default'].sum() / len(df_clean)) * 100 if 'is_default' in df_clean.columns else 0
    }
    
    print("\nCleaning summary:")
    print(f"Rows: {summary['original_rows']:,} → {summary['cleaned_rows']:,} "
          f"({summary['removal_pct']:.1f}% removed)")
    print(f"Columns: {summary['original_cols']} → {summary['cleaned_cols']}")
    print(f"Overall default rate: {summary['default_rate']:.2f}%")
    
    return summary

def validate_cleaned_data(df: pd.DataFrame) -> bool:
    """
    Validate the cleaned dataset meets basic requirements.
    
    Args:
        df: Cleaned DataFrame
    
    Returns:
        True if validation passes, raises ValueError otherwise
    """
    checks = []
    
    # Check essential columns exist
    required = ['grade', 'loan_status', 'is_default']
    missing = [col for col in required if col not in df.columns]
    if missing:
        checks.append(f"Missing required columns: {missing}")
    
    # Check no missing values in critical columns
    critical_missing = df[['grade', 'loan_status', 'is_default']].isnull().sum()
    if critical_missing.sum() > 0:
        checks.append(f"Missing values in critical columns: {critical_missing[critical_missing > 0].to_dict()}")
    
    # Check default indicator is binary
    if 'is_default' in df.columns:
        unique_defaults = df['is_default'].unique()
        if not set(unique_defaults).issubset({0, 1}):
            checks.append(f"Default indicator not binary: {unique_defaults}")
    
    # Check reasonable number of rows remain
    if len(df) < 1000:
        checks.append(f"Very few rows remaining: {len(df)}")
    
    if checks:
        raise ValueError("Data validation failed:\n" + "\n".join(f"- {check}" for check in checks))
    
    print("Data validation passed.")
    return True