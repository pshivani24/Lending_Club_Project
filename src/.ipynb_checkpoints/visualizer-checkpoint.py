"""
Visualization functions for Lending Club analysis.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Optional, Tuple, List
import os

# Set style and color palette
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

def setup_plot_style():
    """Configure matplotlib and seaborn for publication-quality plots."""
    plt.rcParams.update({
        'figure.figsize': (10, 6),
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'figure.titlesize': 16
    })

def plot_default_rate_by_grade(grade_metrics: pd.DataFrame, 
                              save_path: Optional[str] = None) -> None:
    """
    Create bar chart of default rates by loan grade.
    
    Args:
        grade_metrics: DataFrame with grade-level metrics
        save_path: Optional path to save the plot
    """
    setup_plot_style()
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create color map based on default rate
    colors = plt.cm.RdYlBu_r(grade_metrics['default_rate_pct'] / grade_metrics['default_rate_pct'].max())
    
    # Create bars
    bars = ax.bar(grade_metrics['grade'], 
                  grade_metrics['default_rate_pct'],
                  color=colors, 
                  alpha=0.8,
                  edgecolor='black',
                  linewidth=0.5)
    
    # Add value labels on bars
    for bar, rate in zip(bars, grade_metrics['default_rate_pct']):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + 0.5,
                f'{rate:.1f}%', 
                ha='center', va='bottom', 
                fontweight='bold', fontsize=11)
    
    # Styling
    ax.set_title('Loan Default Rate by Grade\n(Higher Risk Grades Show Elevated Default Rates)', 
                fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Loan Grade', fontsize=13, fontweight='bold')
    ax.set_ylabel('Default Rate (%)', fontsize=13, fontweight='bold')
    
    # Add risk threshold lines
    ax.axhline(y=15, color='orange', linestyle='--', alpha=0.7, 
               label='Medium Risk Threshold (15%)')
    ax.axhline(y=25, color='red', linestyle='--', alpha=0.7, 
               label='High Risk Threshold (25%)')
    
    ax.legend(loc='upper left')
    ax.grid(axis='y', alpha=0.3)
    ax.set_ylim(0, max(30, grade_metrics['default_rate_pct'].max() * 1.15))
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved plot to: {save_path}")
    
    plt.show()

def plot_risk_return_analysis(grade_metrics: pd.DataFrame, 
                             save_path: Optional[str] = None) -> None:
    """
    Create scatter plot showing risk-return relationship with volume indicators.
    
    Args:
        grade_metrics: DataFrame with grade-level metrics
        save_path: Optional path to save the plot
    """
    setup_plot_style()
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Normalize volume for bubble size
    max_volume = grade_metrics['total_volume'].max()
    sizes = (grade_metrics['total_volume'] / max_volume) * 1000 + 100
    
    # Create scatter plot
    scatter = ax.scatter(grade_metrics['default_rate_pct'], 
                        grade_metrics['avg_interest_rate'],
                        s=sizes,
                        c=grade_metrics['grade'].astype('category').cat.codes,
                        cmap='viridis', 
                        alpha=0.7,
                        edgecolors='black',
                        linewidth=1)
    
    # Add grade labels
    for idx, row in grade_metrics.iterrows():
        ax.annotate(f"Grade {row['grade']}", 
                   (row['default_rate_pct'], row['avg_interest_rate']),
                   xytext=(8, 8), 
                   textcoords='offset points',
                   fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
    
    # Add trend line
    z = np.polyfit(grade_metrics['default_rate_pct'], grade_metrics['avg_interest_rate'], 1)
    p = np.poly1d(z)
    ax.plot(grade_metrics['default_rate_pct'], p(grade_metrics['default_rate_pct']), 
            "r--", alpha=0.8, label=f'Trend line (R² = {np.corrcoef(grade_metrics["default_rate_pct"], grade_metrics["avg_interest_rate"])[0,1]**2:.3f})')
    
    ax.set_xlabel('Default Rate (%)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Average Interest Rate (%)', fontsize=13, fontweight='bold')
    ax.set_title('Risk-Return Profile by Loan Grade\n(Bubble size = Total loan volume)', 
                fontsize=16, fontweight='bold', pad=20)
    
    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Grade Rank', fontsize=12)
    
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved plot to: {save_path}")
    
    plt.show()

def plot_volume_distribution(grade_metrics: pd.DataFrame, 
                           save_path: Optional[str] = None) -> None:
    """
    Create pie chart showing loan volume distribution by grade.
    
    Args:
        grade_metrics: DataFrame with grade-level metrics
        save_path: Optional path to save the plot
    """
    setup_plot_style()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Create pie chart
    wedges, texts, autotexts = ax.pie(grade_metrics['volume_share_pct'],
                                      labels=grade_metrics['grade'],
                                      autopct='%1.1f%%',
                                      startangle=90,
                                      colors=plt.cm.Set3(np.linspace(0, 1, len(grade_metrics))))
    
    # Style the text
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(10)
    
    for text in texts:
        text.set_fontsize(12)
        text.set_fontweight('bold')
    
    ax.set_title('Loan Volume Distribution by Grade\n(Percentage of Total Portfolio)', 
                fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved plot to: {save_path}")
    
    plt.show()

def plot_grade_comparison_heatmap(grade_metrics: pd.DataFrame, 
                                 metrics_to_show: Optional[List[str]] = None,
                                 save_path: Optional[str] = None) -> None:
    """
    Make a heatmap to compare key metrics across grades. Shows how each grade stacks up for things like default rate, interest rate, loan amount, and volume share.
    """
    if metrics_to_show is None:
        metrics_to_show = ['default_rate_pct', 'avg_interest_rate', 'avg_loan_amount', 'volume_share_pct']
    setup_plot_style()
    heatmap_data = grade_metrics.set_index('grade')[metrics_to_show].T
    heatmap_data_norm = heatmap_data.div(heatmap_data.max(axis=1), axis=0)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(heatmap_data_norm, 
                annot=heatmap_data.round(1), 
                cmap='RdYlBu_r',
                center=0.5,
                fmt='g',
                cbar_kws={'label': 'Normalized Value'},
                ax=ax)
    ax.set_title('Grade Comparison Across Key Metrics', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Loan Grade', fontsize=13, fontweight='bold')
    ax.set_ylabel('Metrics', fontsize=13, fontweight='bold')
    metric_labels = {
        'default_rate_pct': 'Default Rate (%)',
        'avg_interest_rate': 'Avg Interest Rate (%)',
        'avg_loan_amount': 'Avg Loan Amount ($)',
        'volume_share_pct': 'Volume Share (%)'
    }
    ax.set_yticklabels([metric_labels.get(m, m) for m in metrics_to_show], rotation=0)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved plot to: {save_path}")
    plt.show()

def create_executive_dashboard(grade_metrics: pd.DataFrame, 
                              portfolio_metrics: dict,
                              save_path: Optional[str] = None) -> None:
    """
    Create a comprehensive executive dashboard with multiple subplots.
    
    Args:
        grade_metrics: DataFrame with grade-level metrics
        portfolio_metrics: Dictionary with portfolio-level metrics
        save_path: Optional path to save the plot
    """
    setup_plot_style()
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Default Rate Bar Chart
    colors = plt.cm.RdYlBu_r(grade_metrics['default_rate_pct'] / grade_metrics['default_rate_pct'].max())
    bars = ax1.bar(grade_metrics['grade'], grade_metrics['default_rate_pct'], color=colors, alpha=0.8)
    ax1.set_title('Default Rate by Grade', fontweight='bold')
    ax1.set_ylabel('Default Rate (%)')
    ax1.axhline(y=15, color='red', linestyle='--', alpha=0.7)
    
    # Add value labels
    for bar, rate in zip(bars, grade_metrics['default_rate_pct']):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{rate:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    # 2. Risk-Return Scatter
    sizes = (grade_metrics['total_volume'] / grade_metrics['total_volume'].max()) * 300 + 50
    scatter = ax2.scatter(grade_metrics['default_rate_pct'], grade_metrics['avg_interest_rate'],
                         s=sizes, c=grade_metrics['grade'].astype('category').cat.codes,
                         cmap='viridis', alpha=0.7)
    ax2.set_title('Risk vs Return (Size = Volume)', fontweight='bold')
    ax2.set_xlabel('Default Rate (%)')
    ax2.set_ylabel('Interest Rate (%)')
    
    # 3. Volume Distribution
    ax3.pie(grade_metrics['volume_share_pct'], labels=grade_metrics['grade'],
            autopct='%1.1f%%', startangle=90)
    ax3.set_title('Volume Distribution', fontweight='bold')
    
    # 4. Key Metrics Text Summary
    ax4.axis('off')
    summary_text = f"""
    PORTFOLIO SUMMARY
    
    Total Loans: {portfolio_metrics['total_loans']:,}
    Total Volume: ${portfolio_metrics['total_volume']:,.0f}
    
    Overall Default Rate: {portfolio_metrics['overall_default_rate_pct']:.2f}%
    Average Interest Rate: {portfolio_metrics['avg_interest_rate']:.2f}%
    
    High-Risk Exposure (F,G): {portfolio_metrics.get('high_risk_loans_pct', 0):.1f}%
    
    RISK ASSESSMENT:
    {'HIGH RISK EXPOSURE' if portfolio_metrics.get('high_risk_loans_pct', 0) > 20 else '✅ ACCEPTABLE RISK'}
    """
    
    ax4.text(0.1, 0.9, summary_text, transform=ax4.transAxes, fontsize=12,
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))
    
    plt.suptitle('Lending Club Portfolio Analysis - Executive Dashboard', 
                fontsize=18, fontweight='bold', y=0.98)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved dashboard to: {save_path}")
    
    plt.show()


def save_all_visualizations(grade_metrics: pd.DataFrame, 
                           portfolio_metrics: dict,
                           output_dir: str = 'outputs/visualizations') -> None:
    """
    Generate and save all visualizations to specified directory.
    
    Args:
        grade_metrics: DataFrame with grade-level metrics
        portfolio_metrics: Dictionary with portfolio-level metrics  
        output_dir: Directory to save plots
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Generating visualizations in: {output_dir}")
    
    # Generate all plots
    plot_default_rate_by_grade(grade_metrics, f"{output_dir}/default_rate_by_grade.png")
    plot_risk_return_analysis(grade_metrics, f"{output_dir}/risk_return_analysis.png")
    plot_volume_distribution(grade_metrics, f"{output_dir}/volume_distribution.png")
    plot_grade_comparison_heatmap(grade_metrics, save_path=f"{output_dir}/grade_comparison_heatmap.png")
    create_executive_dashboard(grade_metrics, portfolio_metrics, f"{output_dir}/executive_dashboard.png")
    
    print(" All visualizations saved successfully!")

# Utility function for consistent color schemes
def get_grade_colors(grades: List[str]) -> List[str]:
    """
    Return consistent colors for loan grades.
    
    Args:
        grades: List of grade strings
    
    Returns:
        List of color codes
    """
    color_map = {
        'A': '#2E8B57',  # Sea Green
        'B': '#32CD32',  # Lime Green  
        'C': '#FFD700',  # Gold
        'D': '#FFA500',  # Orange
        'E': '#FF6347',  # Tomato
        'F': '#FF4500',  # Orange Red
        'G': '#DC143C'   # Crimson
    }
    
    return [color_map.get(grade, '#808080') for grade in grades]