"""
Data loading utilities for Lending Club analysis.
"""

import pandas as pd
import numpy as np
from typing import Tuple, List, Optional
import os

def load_lending_club_data(filepath: str, sample_frac: Optional[float] = None) -> pd.DataFrame:
    """
    Load Lending Club dataset with initial validation and optional sampling.
    
    Args:
        filepath: Path to the Lending Club CSV file
        sample_frac: Fraction of data to sample (for testing with large files)
    
    Returns:
        DataFrame with loaded data
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Data file not found: {filepath}")
    
    print(f"Loading data from: {filepath}")
    
    # Load with low_memory=False to avoid mixed type warnings
    df = pd.read_csv(filepath, low_memory=False)
    
    print(f"Rows: {df.shape[0]:,}, Columns: {df.shape[1]}")
    
    # Optional sampling for development/testing
    if sample_frac and 0 < sample_frac < 1:
        df = df.sample(frac=sample_frac, random_state=42)
        print(f"Sampled to: {df.shape[0]:,} rows ({sample_frac:.1%})")
    
    return df

def validate_required_columns(df: pd.DataFrame, required_cols: List[str]) -> bool:
    """
    Make sure all required columns are in the DataFrame.
    """
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    print(f"All required columns found: {required_cols}")
    return True

def get_basic_info(df: pd.DataFrame) -> dict:
    """
    Print basic info about the dataset.
    """
    info = {
        'shape': df.shape,
        'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2,
        'null_counts': df.isnull().sum().sum(),
        'duplicate_rows': df.duplicated().sum(),
        'numeric_columns': len(df.select_dtypes(include=[np.number]).columns),
        'object_columns': len(df.select_dtypes(include=['object']).columns)
    }
    
    print(f"\nDataset overview:")
    print(f"Rows: {info['shape'][0]:,}, Columns: {info['shape'][1]}")
    print(f"Memory usage: {info['memory_usage_mb']:.1f} MB")
    print(f"Null values: {info['null_counts']:,}")
    print(f"Duplicate rows: {info['duplicate_rows']:,}")
    print(f"Numeric columns: {info['numeric_columns']}")
    print(f"Object columns: {info['object_columns']}")
    
    return info

def preview_loan_statuses(df: pd.DataFrame) -> pd.Series:
    """
    Show the distribution of loan statuses.
    """
    if 'loan_status' not in df.columns:
        print("Warning: 'loan_status' column not found")
        return pd.Series(dtype=int)
    
    status_counts = df['loan_status'].value_counts(dropna=False)
    
    print("\nLoan status breakdown:")
    for status, count in status_counts.items():
        pct = (count / len(df)) * 100
        print(f"{status}: {count:,} ({pct:.1f}%)")
    
    return status_counts

def preview_grades(df: pd.DataFrame) -> pd.Series:
    """
    Show the distribution of loan grades.
    """
    if 'grade' not in df.columns:
        print("Warning: 'grade' column not found")
        return pd.Series(dtype=int)
    
    grade_counts = df['grade'].value_counts().sort_index()
    
    print("\nGrade breakdown:")
    for grade, count in grade_counts.items():
        pct = (count / len(df)) * 100
        print(f"Grade {grade}: {count:,} ({pct:.1f}%)")
    
    return grade_counts