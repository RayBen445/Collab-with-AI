#!/usr/bin/env python3
"""
Data Visualization Tools
Create charts, graphs, and visualizations from data
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from typing import Dict, List, Any, Optional
import json

class DataVisualizer:
    """Professional data visualization toolkit."""
    
    def __init__(self):
        self.style = 'seaborn'
        plt.style.use(self.style)
        sns.set_palette("husl")
    
    def create_line_chart(self, data: Dict[str, List], title: str = "Line Chart", 
                         x_label: str = "X", y_label: str = "Y") -> None:
        """Create a line chart from data."""
        plt.figure(figsize=(10, 6))
        
        for label, values in data.items():
            if label != 'x':
                plt.plot(data.get('x', range(len(values))), values, 
                        marker='o', linewidth=2, label=label)
        
        plt.title(title, fontsize=16, fontweight='bold')
        plt.xlabel(x_label, fontsize=12)
        plt.ylabel(y_label, fontsize=12)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    def create_bar_chart(self, categories: List[str], values: List[float], 
                        title: str = "Bar Chart") -> None:
        """Create a bar chart."""
        plt.figure(figsize=(10, 6))
        bars = plt.bar(categories, values, color=sns.color_palette("husl", len(categories)))
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values)*0.01,
                    f'{value:.1f}', ha='center', va='bottom', fontweight='bold')
        
        plt.title(title, fontsize=16, fontweight='bold')
        plt.xlabel('Categories', fontsize=12)
        plt.ylabel('Values', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
    
    def create_scatter_plot(self, x_data: List[float], y_data: List[float], 
                           title: str = "Scatter Plot", size_data: List[float] = None) -> None:
        """Create a scatter plot."""
        plt.figure(figsize=(10, 6))
        
        if size_data:
            plt.scatter(x_data, y_data, s=size_data, alpha=0.6, c=range(len(x_data)), 
                       cmap='viridis', edgecolors='black', linewidth=0.5)
        else:
            plt.scatter(x_data, y_data, alpha=0.6, edgecolors='black', linewidth=0.5)
        
        plt.title(title, fontsize=16, fontweight='bold')
        plt.xlabel('X Values', fontsize=12)
        plt.ylabel('Y Values', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    def create_pie_chart(self, labels: List[str], sizes: List[float], 
                        title: str = "Pie Chart") -> None:
        """Create a pie chart."""
        plt.figure(figsize=(8, 8))
        colors = sns.color_palette("husl", len(labels))
        
        wedges, texts, autotexts = plt.pie(sizes, labels=labels, autopct='%1.1f%%', 
                                          colors=colors, explode=[0.05]*len(labels),
                                          shadow=True, startangle=90)
        
        # Beautify text
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        plt.title(title, fontsize=16, fontweight='bold')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()
    
    def create_heatmap(self, data: List[List[float]], x_labels: List[str], 
                      y_labels: List[str], title: str = "Heatmap") -> None:
        """Create a heatmap."""
        plt.figure(figsize=(10, 8))
        sns.heatmap(data, xticklabels=x_labels, yticklabels=y_labels, 
                   annot=True, cmap='coolwarm', center=0, 
                   square=True, linewidths=0.5)
        
        plt.title(title, fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()
    
    def create_histogram(self, data: List[float], bins: int = 30, 
                        title: str = "Histogram") -> None:
        """Create a histogram."""
        plt.figure(figsize=(10, 6))
        n, bins_edge, patches = plt.hist(data, bins=bins, alpha=0.7, color='skyblue', 
                                        edgecolor='black', linewidth=0.5)
        
        # Color bars based on height
        cm = plt.cm.get_cmap('viridis')
        for i, p in enumerate(patches):
            p.set_facecolor(cm(n[i] / max(n)))
        
        plt.title(title, fontsize=16, fontweight='bold')
        plt.xlabel('Values', fontsize=12)
        plt.ylabel('Frequency', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

def demo_visualizations():
    """Demonstrate various visualization capabilities."""
    viz = DataVisualizer()
    
    print("🎨 Data Visualization Demo")
    print("=" * 40)
    
    # Sample data
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    sales = [150, 180, 165, 200, 190, 220]
    profits = [30, 45, 35, 60, 55, 75]
    
    # Line chart
    line_data = {'x': months, 'Sales': sales, 'Profits': profits}
    viz.create_line_chart(line_data, "Monthly Performance", "Month", "Amount ($)")
    
    # Bar chart
    viz.create_bar_chart(months, sales, "Monthly Sales")
    
    # Scatter plot
    x_vals = np.random.randn(100)
    y_vals = 2 * x_vals + np.random.randn(100) * 0.5
    viz.create_scatter_plot(x_vals.tolist(), y_vals.tolist(), "Correlation Example")
    
    # Pie chart
    categories = ['Product A', 'Product B', 'Product C', 'Product D']
    values = [35, 25, 25, 15]
    viz.create_pie_chart(categories, values, "Market Share")
    
    # Histogram
    random_data = np.random.normal(100, 15, 1000).tolist()
    viz.create_histogram(random_data, title="Normal Distribution")
    
    print("✅ Visualization demo completed!")

if __name__ == "__main__":
    demo_visualizations()