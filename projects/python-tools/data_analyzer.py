#!/usr/bin/env python3
"""
Data Analysis Pipeline
A collaborative tool for analyzing CSV data with visualizations and insights.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import argparse
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

class DataAnalyzer:
    """Comprehensive data analysis tool with automated insights."""
    
    def __init__(self, data_file: str):
        self.data_file = data_file
        self.df = None
        self.insights = {}
        self.visualizations = []
        
        # Set up plotting style
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
    def load_data(self) -> bool:
        """Load data from various file formats."""
        try:
            file_ext = Path(self.data_file).suffix.lower()
            
            if file_ext == '.csv':
                self.df = pd.read_csv(self.data_file)
            elif file_ext in ['.xls', '.xlsx']:
                self.df = pd.read_excel(self.data_file)
            elif file_ext == '.json':
                self.df = pd.read_json(self.data_file)
            else:
                print(f"❌ Unsupported file format: {file_ext}")
                return False
            
            print(f"✅ Successfully loaded data: {self.df.shape[0]} rows, {self.df.shape[1]} columns")
            return True
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return False
    
    def basic_analysis(self) -> Dict[str, Any]:
        """Perform basic data analysis."""
        print("\n📊 BASIC DATA ANALYSIS")
        print("=" * 50)
        
        analysis = {
            "shape": self.df.shape,
            "columns": list(self.df.columns),
            "dtypes": self.df.dtypes.to_dict(),
            "missing_values": self.df.isnull().sum().to_dict(),
            "memory_usage": f"{self.df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB"
        }
        
        print(f"📏 Dataset shape: {analysis['shape'][0]} rows × {analysis['shape'][1]} columns")
        print(f"💾 Memory usage: {analysis['memory_usage']}")
        print(f"📝 Columns: {', '.join(analysis['columns'])}")
        
        # Missing values
        missing = {k: v for k, v in analysis['missing_values'].items() if v > 0}
        if missing:
            print(f"❗ Missing values: {missing}")
        else:
            print("✅ No missing values found")
        
        self.insights['basic'] = analysis
        return analysis
    
    def statistical_summary(self):
        """Generate statistical summary."""
        print("\n📈 STATISTICAL SUMMARY")
        print("=" * 50)
        
        # Numerical columns
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            print("🔢 Numerical Columns:")
            summary = self.df[numeric_cols].describe()
            print(summary.round(2))
            
            # Correlation matrix for numeric columns
            if len(numeric_cols) > 1:
                corr_matrix = self.df[numeric_cols].corr()
                
                # Find high correlations
                high_corr = []
                for i in range(len(corr_matrix.columns)):
                    for j in range(i+1, len(corr_matrix.columns)):
                        corr_val = abs(corr_matrix.iloc[i, j])
                        if corr_val > 0.7:
                            high_corr.append((
                                corr_matrix.columns[i],
                                corr_matrix.columns[j],
                                corr_matrix.iloc[i, j]
                            ))
                
                if high_corr:
                    print(f"\n🔗 High correlations (>0.7):")
                    for col1, col2, corr in high_corr:
                        print(f"   {col1} ↔ {col2}: {corr:.3f}")
        
        # Categorical columns
        cat_cols = self.df.select_dtypes(include=['object']).columns
        if len(cat_cols) > 0:
            print(f"\n📝 Categorical Columns:")
            for col in cat_cols:
                unique_count = self.df[col].nunique()
                print(f"   {col}: {unique_count} unique values")
                if unique_count <= 10:
                    value_counts = self.df[col].value_counts().head()
                    print(f"      Top values: {dict(value_counts)}")
    
    def detect_outliers(self) -> Dict[str, List]:
        """Detect outliers in numerical columns."""
        print("\n🎯 OUTLIER DETECTION")
        print("=" * 50)
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        outliers = {}
        
        for col in numeric_cols:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outlier_mask = (self.df[col] < lower_bound) | (self.df[col] > upper_bound)
            outlier_count = outlier_mask.sum()
            
            if outlier_count > 0:
                outliers[col] = self.df[outlier_mask][col].tolist()
                print(f"📌 {col}: {outlier_count} outliers ({outlier_count/len(self.df)*100:.1f}%)")
            else:
                print(f"✅ {col}: No outliers detected")
        
        self.insights['outliers'] = outliers
        return outliers
    
    def create_visualizations(self, output_dir: str = "analysis_output"):
        """Create comprehensive visualizations."""
        print(f"\n🎨 CREATING VISUALIZATIONS")
        print("=" * 50)
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        cat_cols = self.df.select_dtypes(include=['object']).columns
        
        # 1. Distribution plots for numerical columns
        if len(numeric_cols) > 0:
            fig, axes = plt.subplots(2, 2, figsize=(15, 10))
            fig.suptitle('📊 Numerical Distributions', fontsize=16, fontweight='bold')
            
            for i, col in enumerate(numeric_cols[:4]):
                row, col_idx = i // 2, i % 2
                
                # Histogram with KDE
                axes[row, col_idx].hist(self.df[col].dropna(), bins=30, alpha=0.7, density=True)
                self.df[col].plot.kde(ax=axes[row, col_idx], color='red', linewidth=2)
                axes[row, col_idx].set_title(f'{col} Distribution')
                axes[row, col_idx].set_xlabel(col)
                axes[row, col_idx].set_ylabel('Density')
            
            # Hide empty subplots
            for i in range(len(numeric_cols), 4):
                row, col_idx = i // 2, i % 2
                axes[row, col_idx].set_visible(False)
            
            plt.tight_layout()
            plt.savefig(f"{output_dir}/distributions.png", dpi=300, bbox_inches='tight')
            plt.show()
            self.visualizations.append("distributions.png")
        
        # 2. Correlation heatmap
        if len(numeric_cols) > 1:
            plt.figure(figsize=(10, 8))
            corr_matrix = self.df[numeric_cols].corr()
            
            sns.heatmap(corr_matrix, annot=True, cmap='RdYlBu_r', center=0,
                       square=True, fmt='.2f', cbar_kws={'label': 'Correlation'})
            plt.title('🔗 Correlation Matrix', fontsize=16, fontweight='bold')
            plt.tight_layout()
            plt.savefig(f"{output_dir}/correlation_matrix.png", dpi=300, bbox_inches='tight')
            plt.show()
            self.visualizations.append("correlation_matrix.png")
        
        # 3. Box plots for outlier visualization
        if len(numeric_cols) > 0:
            fig, axes = plt.subplots(1, min(len(numeric_cols), 3), figsize=(15, 5))
            if len(numeric_cols) == 1:
                axes = [axes]
            
            fig.suptitle('📦 Box Plots (Outlier Detection)', fontsize=16, fontweight='bold')
            
            for i, col in enumerate(numeric_cols[:3]):
                if len(numeric_cols) > 1:
                    axes[i].boxplot(self.df[col].dropna())
                    axes[i].set_title(f'{col}')
                    axes[i].set_ylabel('Values')
                else:
                    axes[0].boxplot(self.df[col].dropna())
                    axes[0].set_title(f'{col}')
                    axes[0].set_ylabel('Values')
            
            plt.tight_layout()
            plt.savefig(f"{output_dir}/box_plots.png", dpi=300, bbox_inches='tight')
            plt.show()
            self.visualizations.append("box_plots.png")
        
        # 4. Categorical data visualization
        if len(cat_cols) > 0:
            fig, axes = plt.subplots(1, min(len(cat_cols), 2), figsize=(15, 6))
            if len(cat_cols) == 1:
                axes = [axes]
            
            fig.suptitle('📊 Categorical Data Distribution', fontsize=16, fontweight='bold')
            
            for i, col in enumerate(cat_cols[:2]):
                value_counts = self.df[col].value_counts().head(10)
                
                if len(cat_cols) > 1:
                    value_counts.plot(kind='bar', ax=axes[i])
                    axes[i].set_title(f'{col}')
                    axes[i].set_xlabel('Categories')
                    axes[i].set_ylabel('Count')
                    axes[i].tick_params(axis='x', rotation=45)
                else:
                    value_counts.plot(kind='bar', ax=axes[0])
                    axes[0].set_title(f'{col}')
                    axes[0].set_xlabel('Categories')
                    axes[0].set_ylabel('Count')
                    axes[0].tick_params(axis='x', rotation=45)
            
            plt.tight_layout()
            plt.savefig(f"{output_dir}/categorical_plots.png", dpi=300, bbox_inches='tight')
            plt.show()
            self.visualizations.append("categorical_plots.png")
        
        print(f"✅ Visualizations saved to: {output_dir}/")
    
    def generate_insights(self) -> Dict[str, Any]:
        """Generate automated insights and recommendations."""
        print("\n💡 AUTOMATED INSIGHTS")
        print("=" * 50)
        
        insights = {
            "data_quality": {},
            "patterns": {},
            "recommendations": []
        }
        
        # Data quality insights
        missing_percentage = (self.df.isnull().sum() / len(self.df) * 100)
        high_missing = missing_percentage[missing_percentage > 10].to_dict()
        
        if high_missing:
            insights["data_quality"]["high_missing_columns"] = high_missing
            print(f"⚠️  Columns with >10% missing data: {list(high_missing.keys())}")
            insights["recommendations"].append("Consider data imputation or removal of columns with high missing values")
        
        # Duplicate detection
        duplicates = self.df.duplicated().sum()
        if duplicates > 0:
            insights["data_quality"]["duplicate_rows"] = duplicates
            print(f"⚠️  Found {duplicates} duplicate rows ({duplicates/len(self.df)*100:.1f}%)")
            insights["recommendations"].append("Remove duplicate rows to improve data quality")
        
        # Numerical insights
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            # Skewness analysis
            skewed_cols = []
            for col in numeric_cols:
                skewness = self.df[col].skew()
                if abs(skewness) > 1:
                    skewed_cols.append((col, skewness))
            
            if skewed_cols:
                insights["patterns"]["skewed_distributions"] = skewed_cols
                print(f"📊 Highly skewed columns: {[col for col, _ in skewed_cols]}")
                insights["recommendations"].append("Consider log transformation for highly skewed numerical columns")
        
        # Categorical insights
        cat_cols = self.df.select_dtypes(include=['object']).columns
        high_cardinality = []
        for col in cat_cols:
            unique_ratio = self.df[col].nunique() / len(self.df)
            if unique_ratio > 0.5:
                high_cardinality.append((col, self.df[col].nunique()))
        
        if high_cardinality:
            insights["patterns"]["high_cardinality_categorical"] = high_cardinality
            print(f"🏷️  High cardinality categorical columns: {[col for col, _ in high_cardinality]}")
            insights["recommendations"].append("High cardinality categorical columns may need grouping or encoding")
        
        # Memory optimization suggestions
        memory_mb = self.df.memory_usage(deep=True).sum() / 1024 / 1024
        if memory_mb > 100:
            insights["recommendations"].append("Consider data type optimization for large datasets")
        
        self.insights['automated'] = insights
        return insights
    
    def export_report(self, output_dir: str = "analysis_output"):
        """Export comprehensive analysis report."""
        report_file = f"{output_dir}/analysis_report.json"
        
        report = {
            "analysis_timestamp": datetime.now().isoformat(),
            "data_file": self.data_file,
            "insights": self.insights,
            "visualizations": self.visualizations
        }
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"\n📋 Analysis report exported to: {report_file}")
        
        # Create summary markdown report
        md_file = f"{output_dir}/analysis_summary.md"
        with open(md_file, 'w') as f:
            f.write(f"# Data Analysis Report\n\n")
            f.write(f"**File:** {self.data_file}\n")
            f.write(f"**Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write(f"## Dataset Overview\n")
            f.write(f"- **Rows:** {self.df.shape[0]:,}\n")
            f.write(f"- **Columns:** {self.df.shape[1]}\n")
            f.write(f"- **Memory Usage:** {self.insights['basic']['memory_usage']}\n\n")
            
            if 'automated' in self.insights:
                f.write(f"## Key Insights\n")
                recommendations = self.insights['automated']['recommendations']
                for i, rec in enumerate(recommendations, 1):
                    f.write(f"{i}. {rec}\n")
                f.write("\n")
            
            f.write(f"## Visualizations\n")
            for viz in self.visualizations:
                f.write(f"- ![{viz}]({viz})\n")
        
        print(f"📄 Summary report exported to: {md_file}")
    
    def run_full_analysis(self, create_viz: bool = True, export_results: bool = True):
        """Run complete analysis pipeline."""
        print("🤖🤝👨‍💻 DATA ANALYSIS PIPELINE")
        print("=" * 60)
        print("Collaborative AI-Human Data Analysis Tool")
        print("=" * 60)
        
        if not self.load_data():
            return False
        
        # Run analysis steps
        self.basic_analysis()
        self.statistical_summary()
        self.detect_outliers()
        self.generate_insights()
        
        if create_viz:
            self.create_visualizations()
        
        if export_results:
            self.export_report()
        
        print("\n✅ Analysis completed successfully!")
        print("💡 Review the generated insights and visualizations for next steps.")
        return True

def main():
    """Main function with command-line interface."""
    parser = argparse.ArgumentParser(
        description="🤖 Data Analysis Pipeline - Collaborative AI-Human Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python data_analyzer.py sales_data.csv
  python data_analyzer.py --file data.xlsx --no-viz
  python data_analyzer.py data.csv --output results/
        """
    )
    
    parser.add_argument("file", help="Data file to analyze (CSV, Excel, JSON)")
    parser.add_argument("--output", "-o", default="analysis_output", help="Output directory")
    parser.add_argument("--no-viz", action="store_true", help="Skip visualization creation")
    parser.add_argument("--no-export", action="store_true", help="Skip report export")
    
    args = parser.parse_args()
    
    # Create analyzer and run analysis
    analyzer = DataAnalyzer(args.file)
    success = analyzer.run_full_analysis(
        create_viz=not args.no_viz,
        export_results=not args.no_export
    )
    
    if success:
        print(f"\n📂 All results saved to: {args.output}/")
    else:
        print("\n❌ Analysis failed. Please check your data file and try again.")

if __name__ == "__main__":
    main()