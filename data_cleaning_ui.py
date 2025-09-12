#!/usr/bin/env python3
"""
Interactive Data Cleaning User Interface
Provides easy-to-use interface for data cleaning operations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Any, Optional
from data_cleaning_agent import DataCleaningAgent
from ai_data_cleaning import AIDataCleaningAgent
import ipywidgets as widgets
from IPython.display import display, clear_output
import warnings
warnings.filterwarnings('ignore')

class DataCleaningUI:
    """
    Interactive User Interface for Data Cleaning Agent
    """
    
    def __init__(self):
        self.agent = AIDataCleaningAgent()
        self.current_df = None
        self.cleaned_df = None
        self.cleaning_history = []
    
    def load_dataset(self, file_path: str) -> pd.DataFrame:
        """
        Load dataset from file (single sheet)
        """
        print(f"📁 Loading dataset from {file_path}...")
        
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
                df = pd.read_excel(file_path)
            elif file_path.endswith('.json'):
                df = pd.read_json(file_path)
            else:
                raise ValueError("Unsupported file format")
            
            self.current_df = df
            print(f"✅ Dataset loaded successfully: {df.shape[0]} rows, {df.shape[1]} columns")
            return df
            
        except Exception as e:
            print(f"❌ Error loading dataset: {e}")
            return None
    
    def load_excel_multi_sheet(self, file_path: str) -> Dict[str, pd.DataFrame]:
        """
        Load Excel file with multiple sheets
        """
        print(f"📁 Loading Excel file with multiple sheets: {file_path}")
        
        try:
            sheets = self.agent.load_excel_multi_sheet(file_path)
            if sheets:
                print(f"✅ Loaded {len(sheets)} sheets successfully!")
                return sheets
            else:
                print("❌ No sheets loaded")
                return {}
                
        except Exception as e:
            print(f"❌ Error loading Excel file: {e}")
            return {}
    
    def select_and_clean_sheet(self, sheets: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """
        Select a sheet and clean it
        """
        if not sheets:
            print("❌ No sheets available")
            return None
        
        # Select sheet
        sheet_name, selected_df = self.agent.select_sheet(sheets)
        
        # Set as current dataset
        self.current_df = selected_df
        
        # Clean the selected sheet
        print(f"\n🧹 Cleaning selected sheet: {sheet_name}")
        cleaned_df = self.agent.auto_clean(selected_df)
        
        return cleaned_df
    
    def clean_all_sheets_demo(self, file_path: str) -> None:
        """
        Demo: Clean all sheets in an Excel file
        """
        print("🎬 Multi-Sheet Excel Cleaning Demo")
        print("=" * 50)
        
        # Load all sheets
        sheets = self.load_excel_multi_sheet(file_path)
        if not sheets:
            return
        
        # Clean all sheets
        cleaned_sheets = self.agent.clean_all_sheets(sheets)
        
        # Compare results
        self.agent.compare_sheets(sheets, cleaned_sheets)
        
        # Save cleaned data
        output_path = file_path.replace('.xlsx', '_cleaned.xlsx')
        self.agent.save_cleaned_excel(cleaned_sheets, output_path)
        
        print("\n🎉 Multi-sheet cleaning demo complete!")
    
    def show_data_preview(self, df: Optional[pd.DataFrame] = None) -> None:
        """
        Show data preview with basic info
        """
        if df is None:
            df = self.current_df
        
        if df is None:
            print("❌ No dataset loaded")
            return
        
        print("📊 Dataset Preview:")
        print("=" * 50)
        print(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
        print(f"Memory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        print("\nFirst 5 rows:")
        print(df.head())
        print("\nData Types:")
        print(df.dtypes)
        print("\nBasic Statistics:")
        print(df.describe())
    
    def show_data_quality_report(self, df: Optional[pd.DataFrame] = None) -> None:
        """
        Show comprehensive data quality report
        """
        if df is None:
            df = self.current_df
        
        if df is None:
            print("❌ No dataset loaded")
            return
        
        print("🔍 Data Quality Report:")
        print("=" * 50)
        
        analysis = self.agent.analyze_data_quality(df)
        
        print(f"📊 Dataset Overview:")
        print(f"   Shape: {analysis['shape']}")
        print(f"   Memory Usage: {analysis['memory_usage'] / 1024**2:.2f} MB")
        
        print(f"\n❌ Missing Values:")
        for col, count in analysis['missing_values'].items():
            if count > 0:
                percentage = analysis['missing_percentage'][col]
                print(f"   {col}: {count} ({percentage:.1f}%)")
        
        print(f"\n🔄 Duplicates:")
        print(f"   Duplicate rows: {analysis['duplicate_rows']} ({analysis['duplicate_percentage']:.1f}%)")
        
        print(f"\n📋 Data Types:")
        print(f"   Numeric columns: {len(analysis['numeric_columns'])}")
        print(f"   Categorical columns: {len(analysis['categorical_columns'])}")
        print(f"   DateTime columns: {len(analysis['datetime_columns'])}")
        
        if analysis['issues']:
            print(f"\n⚠️ Issues Detected:")
            for issue in analysis['issues']:
                print(f"   - {issue}")
        else:
            print(f"\n✅ No major issues detected")
    
    def show_ai_suggestions(self, df: Optional[pd.DataFrame] = None) -> None:
        """
        Show AI-powered cleaning suggestions
        """
        if df is None:
            df = self.current_df
        
        if df is None:
            print("❌ No dataset loaded")
            return
        
        print("🤖 AI-Powered Cleaning Suggestions:")
        print("=" * 50)
        
        suggestions = self.agent.get_ai_cleaning_suggestions(df)
        
        for i, suggestion in enumerate(suggestions, 1):
            print(f"{i}. {suggestion}")
        
        print("\n" + "=" * 50)
    
    def show_cleaning_options(self) -> None:
        """
        Show interactive cleaning options
        """
        print("🧹 Data Cleaning Options:")
        print("=" * 50)
        print("1. 🤖 AI-Powered Auto Clean (Recommended)")
        print("2. 🧽 Clean Missing Values")
        print("3. 🔄 Remove Duplicates")
        print("4. 🔧 Standardize Data Types")
        print("5. 🎯 Detect & Clean Outliers")
        print("6. 📝 Standardize Text")
        print("7. 📊 Generate Cleaning Report")
        print("8. 💾 Save Cleaned Data")
        print("9. 🔄 Reset to Original")
        print("=" * 50)
    
    def perform_auto_clean(self, df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Perform automatic AI-powered cleaning
        """
        if df is None:
            df = self.current_df
        
        if df is None:
            print("❌ No dataset loaded")
            return None
        
        print("🤖 Starting AI-Powered Auto Cleaning...")
        print("=" * 50)
        
        # Perform intelligent cleaning
        cleaned_df = self.agent.intelligent_clean(df)
        
        # Store results
        self.cleaned_df = cleaned_df
        self.cleaning_history.append("AI Auto Clean")
        
        print("✅ Auto cleaning complete!")
        return cleaned_df
    
    def create_visualization_dashboard(self, df: Optional[pd.DataFrame] = None) -> None:
        """
        Create beautiful visualization dashboard
        """
        if df is None:
            df = self.current_df
        
        if df is None:
            print("❌ No dataset loaded")
            return
        
        print("📊 Creating Data Quality Visualization Dashboard...")
        
        # Create subplots
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Data Quality Analysis Dashboard', fontsize=16, fontweight='bold')
        
        # 1. Missing Values Heatmap
        missing_data = df.isnull().sum()
        if missing_data.sum() > 0:
            missing_data = missing_data[missing_data > 0]
            axes[0, 0].bar(range(len(missing_data)), missing_data.values)
            axes[0, 0].set_title('Missing Values by Column')
            axes[0, 0].set_xlabel('Columns')
            axes[0, 0].set_ylabel('Missing Count')
            axes[0, 0].set_xticks(range(len(missing_data)))
            axes[0, 0].set_xticklabels(missing_data.index, rotation=45)
        else:
            axes[0, 0].text(0.5, 0.5, 'No Missing Values', ha='center', va='center', fontsize=14)
            axes[0, 0].set_title('Missing Values by Column')
        
        # 2. Data Types Distribution
        dtype_counts = df.dtypes.value_counts()
        axes[0, 1].pie(dtype_counts.values, labels=dtype_counts.index, autopct='%1.1f%%')
        axes[0, 1].set_title('Data Types Distribution')
        
        # 3. Numeric Columns Correlation (if any)
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 1:
            corr_matrix = df[numeric_cols].corr()
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, ax=axes[1, 0])
            axes[1, 0].set_title('Numeric Columns Correlation')
        else:
            axes[1, 0].text(0.5, 0.5, 'Insufficient Numeric Data\nfor Correlation', 
                           ha='center', va='center', fontsize=12)
            axes[1, 0].set_title('Numeric Columns Correlation')
        
        # 4. Memory Usage by Column
        memory_usage = df.memory_usage(deep=True)
        memory_usage = memory_usage[memory_usage > 0].sort_values(ascending=True)
        axes[1, 1].barh(range(len(memory_usage)), memory_usage.values / 1024)
        axes[1, 1].set_title('Memory Usage by Column (KB)')
        axes[1, 1].set_xlabel('Memory Usage (KB)')
        axes[1, 1].set_yticks(range(len(memory_usage)))
        axes[1, 1].set_yticklabels(memory_usage.index)
        
        plt.tight_layout()
        plt.show()
        
        print("✅ Visualization dashboard created!")
    
    def compare_before_after(self, original_df: pd.DataFrame, cleaned_df: pd.DataFrame) -> None:
        """
        Compare original vs cleaned data
        """
        print("📊 Before vs After Cleaning Comparison:")
        print("=" * 60)
        
        # Basic stats comparison
        print(f"📏 Shape:")
        print(f"   Before: {original_df.shape[0]} rows × {original_df.shape[1]} columns")
        print(f"   After:  {cleaned_df.shape[0]} rows × {cleaned_df.shape[1]} columns")
        
        # Missing values comparison
        original_missing = original_df.isnull().sum().sum()
        cleaned_missing = cleaned_df.isnull().sum().sum()
        print(f"\n❌ Missing Values:")
        print(f"   Before: {original_missing}")
        print(f"   After:  {cleaned_missing}")
        print(f"   Improvement: {original_missing - cleaned_missing} values cleaned")
        
        # Duplicates comparison
        original_duplicates = original_df.duplicated().sum()
        cleaned_duplicates = cleaned_df.duplicated().sum()
        print(f"\n🔄 Duplicates:")
        print(f"   Before: {original_duplicates}")
        print(f"   After:  {cleaned_duplicates}")
        print(f"   Improvement: {original_duplicates - cleaned_duplicates} duplicates removed")
        
        # Memory usage comparison
        original_memory = original_df.memory_usage(deep=True).sum() / 1024**2
        cleaned_memory = cleaned_df.memory_usage(deep=True).sum() / 1024**2
        print(f"\n💾 Memory Usage:")
        print(f"   Before: {original_memory:.2f} MB")
        print(f"   After:  {cleaned_memory:.2f} MB")
        print(f"   Improvement: {original_memory - cleaned_memory:.2f} MB saved")
        
        print("=" * 60)
    
    def save_cleaned_data(self, df: pd.DataFrame, filename: str) -> None:
        """
        Save cleaned data to file
        """
        try:
            if filename.endswith('.csv'):
                df.to_csv(filename, index=False)
            elif filename.endswith('.xlsx'):
                df.to_excel(filename, index=False)
            else:
                df.to_csv(filename + '.csv', index=False)
            
            print(f"✅ Cleaned data saved to {filename}")
            
        except Exception as e:
            print(f"❌ Error saving data: {e}")
    
    def run_interactive_session(self) -> None:
        """
        Run interactive data cleaning session
        """
        print("🚀 Welcome to AI-Powered Data Cleaning Agent!")
        print("=" * 60)
        print("Built for UoM DSCubed x UWA DSC GenAI Competition")
        print("=" * 60)
        
        while True:
            print("\n📋 Available Commands:")
            print("1. Load dataset")
            print("2. Show data preview")
            print("3. Show data quality report")
            print("4. Show AI suggestions")
            print("5. Perform auto clean")
            print("6. Show cleaning options")
            print("7. Create visualization dashboard")
            print("8. Compare before/after")
            print("9. Save cleaned data")
            print("10. Exit")
            
            choice = input("\nEnter your choice (1-10): ").strip()
            
            if choice == '1':
                file_path = input("Enter file path: ").strip()
                self.load_dataset(file_path)
            
            elif choice == '2':
                self.show_data_preview()
            
            elif choice == '3':
                self.show_data_quality_report()
            
            elif choice == '4':
                self.show_ai_suggestions()
            
            elif choice == '5':
                self.perform_auto_clean()
            
            elif choice == '6':
                self.show_cleaning_options()
            
            elif choice == '7':
                self.create_visualization_dashboard()
            
            elif choice == '8':
                if self.current_df is not None and self.cleaned_df is not None:
                    self.compare_before_after(self.current_df, self.cleaned_df)
                else:
                    print("❌ Need both original and cleaned data for comparison")
            
            elif choice == '9':
                if self.cleaned_df is not None:
                    filename = input("Enter filename to save: ").strip()
                    self.save_cleaned_data(self.cleaned_df, filename)
                else:
                    print("❌ No cleaned data to save")
            
            elif choice == '10':
                print("👋 Thank you for using AI-Powered Data Cleaning Agent!")
                break
            
            else:
                print("❌ Invalid choice. Please try again.")
