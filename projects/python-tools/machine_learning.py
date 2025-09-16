#!/usr/bin/env python3
"""
Machine Learning Toolkit
Comprehensive ML utilities for data science projects
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.svm import SVC, SVR
from sklearn.metrics import accuracy_score, mean_squared_error, classification_report
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Tuple, Dict, Any, List
import joblib

class MLToolkit:
    """Professional machine learning toolkit."""
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.encoders = {}
        
    def load_data(self, file_path: str) -> pd.DataFrame:
        """Load data from various file formats."""
        try:
            if file_path.endswith('.csv'):
                return pd.read_csv(file_path)
            elif file_path.endswith('.json'):
                return pd.read_json(file_path)
            elif file_path.endswith('.xlsx'):
                return pd.read_excel(file_path)
            else:
                raise ValueError("Unsupported file format")
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return None
    
    def explore_data(self, df: pd.DataFrame) -> None:
        """Comprehensive data exploration."""
        print("📊 Data Exploration Report")
        print("=" * 50)
        
        print(f"Dataset shape: {df.shape}")
        print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        
        print("\n📈 Data Types:")
        print(df.dtypes.value_counts())
        
        print("\n🔍 Missing Values:")
        missing = df.isnull().sum()
        if missing.sum() > 0:
            print(missing[missing > 0])
        else:
            print("No missing values found!")
        
        print("\n📊 Statistical Summary:")
        print(df.describe())
        
        # Correlation heatmap for numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 1:
            plt.figure(figsize=(10, 8))
            correlation_matrix = df[numeric_cols].corr()
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', 
                       center=0, square=True)
            plt.title('Feature Correlation Matrix')
            plt.tight_layout()
            plt.show()
    
    def preprocess_data(self, df: pd.DataFrame, target_column: str) -> Tuple[np.ndarray, np.ndarray]:
        """Preprocess data for machine learning."""
        print("🔧 Preprocessing data...")
        
        # Separate features and target
        X = df.drop(columns=[target_column])
        y = df[target_column]
        
        # Handle categorical variables
        categorical_cols = X.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
            self.encoders[col] = le
        
        # Handle missing values
        X = X.fillna(X.mean())
        
        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        self.scalers['features'] = scaler
        
        # Encode target if categorical
        if y.dtype == 'object':
            le_target = LabelEncoder()
            y = le_target.fit_transform(y)
            self.encoders['target'] = le_target
        
        print(f"✅ Preprocessing complete. Features shape: {X_scaled.shape}")
        return X_scaled, y
    
    def train_classification_models(self, X: np.ndarray, y: np.ndarray) -> Dict[str, float]:
        """Train multiple classification models."""
        print("🤖 Training classification models...")
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        models = {
            'Logistic Regression': LogisticRegression(random_state=42),
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'SVM': SVC(random_state=42)
        }
        
        results = {}
        
        for name, model in models.items():
            print(f"Training {name}...")
            model.fit(X_train, y_train)
            
            # Cross-validation
            cv_scores = cross_val_score(model, X_train, y_train, cv=5)
            
            # Test set performance
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            results[name] = {
                'cv_mean': cv_scores.mean(),
                'cv_std': cv_scores.std(),
                'test_accuracy': accuracy
            }
            
            self.models[name] = model
            
            print(f"  CV Score: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")
            print(f"  Test Accuracy: {accuracy:.3f}")
            print()
        
        return results
    
    def train_regression_models(self, X: np.ndarray, y: np.ndarray) -> Dict[str, float]:
        """Train multiple regression models."""
        print("📈 Training regression models...")
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        models = {
            'Linear Regression': LinearRegression(),
            'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
            'SVR': SVR()
        }
        
        results = {}
        
        for name, model in models.items():
            print(f"Training {name}...")
            model.fit(X_train, y_train)
            
            # Cross-validation (negative MSE)
            cv_scores = cross_val_score(model, X_train, y_train, cv=5, 
                                      scoring='neg_mean_squared_error')
            
            # Test set performance
            y_pred = model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)
            
            results[name] = {
                'cv_rmse': np.sqrt(-cv_scores.mean()),
                'cv_std': np.sqrt(cv_scores.std()),
                'test_rmse': rmse
            }
            
            self.models[name] = model
            
            print(f"  CV RMSE: {np.sqrt(-cv_scores.mean()):.3f}")
            print(f"  Test RMSE: {rmse:.3f}")
            print()
        
        return results
    
    def perform_clustering(self, X: np.ndarray, n_clusters: int = 3) -> np.ndarray:
        """Perform K-means clustering."""
        print(f"🎯 Performing K-means clustering with {n_clusters} clusters...")
        
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(X)
        
        self.models['kmeans'] = kmeans
        
        # Visualize clusters if 2D
        if X.shape[1] == 2:
            plt.figure(figsize=(10, 6))
            scatter = plt.scatter(X[:, 0], X[:, 1], c=clusters, cmap='viridis', alpha=0.6)
            plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], 
                       c='red', marker='x', s=200, linewidths=3)
            plt.title(f'K-means Clustering (k={n_clusters})')
            plt.colorbar(scatter)
            plt.show()
        
        print(f"✅ Clustering complete. Inertia: {kmeans.inertia_:.2f}")
        return clusters
    
    def save_model(self, model_name: str, file_path: str) -> None:
        """Save trained model to disk."""
        if model_name in self.models:
            joblib.dump(self.models[model_name], file_path)
            print(f"✅ Model '{model_name}' saved to {file_path}")
        else:
            print(f"❌ Model '{model_name}' not found")
    
    def load_model(self, file_path: str, model_name: str) -> None:
        """Load model from disk."""
        try:
            self.models[model_name] = joblib.load(file_path)
            print(f"✅ Model loaded as '{model_name}'")
        except Exception as e:
            print(f"❌ Error loading model: {e}")

def demo_ml_workflow():
    """Demonstrate complete ML workflow."""
    print("🤖 Machine Learning Toolkit Demo")
    print("=" * 50)
    
    # Create sample dataset
    from sklearn.datasets import make_classification, make_regression
    
    ml = MLToolkit()
    
    # Classification demo
    print("\n🎯 Classification Demo")
    X_class, y_class = make_classification(n_samples=1000, n_features=10, 
                                          n_informative=8, n_redundant=2, 
                                          random_state=42)
    
    class_results = ml.train_classification_models(X_class, y_class)
    
    # Regression demo
    print("\n📈 Regression Demo")
    X_reg, y_reg = make_regression(n_samples=1000, n_features=10, 
                                  noise=0.1, random_state=42)
    
    reg_results = ml.train_regression_models(X_reg, y_reg)
    
    # Clustering demo
    print("\n🎯 Clustering Demo")
    from sklearn.datasets import make_blobs
    X_cluster, _ = make_blobs(n_samples=300, centers=4, cluster_std=0.60, 
                             random_state=42)
    
    clusters = ml.perform_clustering(X_cluster, n_clusters=4)
    
    print("✅ ML workflow demo completed!")

if __name__ == "__main__":
    demo_ml_workflow()