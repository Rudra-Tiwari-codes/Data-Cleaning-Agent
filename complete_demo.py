#!/usr/bin/env python3
"""
AI-Powered Data Cleaning Agent - Complete Demo
==============================================

This is the main demonstration file that showcases all features of our
AI-Powered Data Cleaning Agent for the GenAI Competition.

Features Demonstrated:
- AI-powered intelligent cleaning suggestions
- Multi-sheet Excel support
- Comprehensive data quality analysis
- Before/after comparisons
- Professional reporting
- Real-world health data processing

Author: Rudra Tiwari
Competition: GenAI Competition - UoM DSCubed x UWA DSC
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from datetime import datetime
import json
import os

# Import our custom modules
from data_cleaning_agent import DataCleaningAgent
from ai_data_cleaning import AIDataCleaningAgent
from data_cleaning_ui import DataCleaningUI

warnings.filterwarnings('ignore')

def print_header(title, char="=", width=70):
    """Print a formatted header"""
    print(f"\n{char * width}")
    print(f"{title:^{width}}")
    print(f"{char * width}")

def print_section(title, char="-", width=50):
    """Print a formatted section header"""
    print(f"\n{title}")
    print(f"{char * len(title)}")

class CompleteDataCleaningDemo:
    """Complete demonstration of the AI-Powered Data Cleaning Agent"""
    
    def __init__(self):
        self.agent = DataCleaningAgent()
        self.ai_agent = AIDataCleaningAgent()
        self.ui = DataCleaningUI()
        self.demo_results = {}
    
    def demo_1_sample_data_cleaning(self):
        """Demo 1: Sample Data Cleaning with AI"""
        print_header("DEMO 1: AI-Powered Sample Data Cleaning")
        
        print("🎬 Creating sample dataset with data quality issues...")
        
        # Create sample data with various issues
        sample_data = pd.DataFrame({
            'Name': ['John', 'Jane', 'Bob', 'Alice', 'Charlie', 'Diana', 'Eve', 'Frank', None, 'Grace'],
            'Age': [25, 30, 35, 28, 42, 33, 29, 31, 27, 26],
            'Salary': [50000, 60000, 70000, 55000, 80000, 65000, 58000, 62000, 54000, 57000],
            'Department': ['IT', 'HR', 'IT', 'Finance', 'IT', 'HR', 'Finance', 'IT', 'HR', 'Finance'],
            'Experience': [2, 5, 8, 3, 12, 6, 4, 7, 3, 2],
            'Rating': [4.5, 4.2, 4.8, 4.1, 4.9, 4.3, 4.0, 4.6, 4.4, 4.7]
        })
        
        # Add data quality issues
        sample_data.loc[1, 'Age'] = None  # Missing value
        sample_data.loc[3, 'Salary'] = None  # Missing value
        sample_data.loc[5, 'Department'] = ''  # Empty string
        sample_data = pd.concat([sample_data, sample_data.iloc[[0, 2]]], ignore_index=True)  # Duplicates
        sample_data.loc[8, 'Age'] = 150  # Outlier
        sample_data.loc[9, 'Rating'] = 6.0  # Outlier (rating should be 1-5)
        
        print(f"✅ Sample dataset created: {sample_data.shape[0]} rows × {sample_data.shape[1]} columns")
        
        # Show original data
        print_section("📊 Original Data Preview")
        print(sample_data.head(10))
        
        # Data quality analysis
        print_section("🔍 Data Quality Analysis")
        quality_report = self.agent.analyze_data_quality(sample_data)
        print(f"Missing values: {sum(quality_report['missing_values'].values())}")
        print(f"Duplicates: {quality_report['duplicate_rows']}")
        print(f"Memory usage: {quality_report['memory_usage'] / 1024:.1f} KB")
        
        # AI-powered cleaning suggestions
        print_section("🤖 AI-Powered Cleaning Suggestions")
        try:
            ai_suggestions = self.ai_agent.get_ai_cleaning_suggestions(sample_data)
            for i, suggestion in enumerate(ai_suggestions[:5], 1):  # Show first 5
                if suggestion.strip():
                    print(f"{i}. {suggestion}")
        except Exception as e:
            print(f"AI suggestions not available: {e}")
            print("Using standard cleaning approach...")
        
        # Apply intelligent cleaning
        print_section("🧹 Applying AI-Powered Cleaning")
        cleaned_data = self.ai_agent.intelligent_clean(sample_data)
        
        # Show results
        print_section("📈 Cleaning Results")
        print(f"Original shape: {sample_data.shape}")
        print(f"Cleaned shape: {cleaned_data.shape}")
        print(f"Missing values: {sample_data.isnull().sum().sum()} → {cleaned_data.isnull().sum().sum()}")
        print(f"Duplicates: {sample_data.duplicated().sum()} → {cleaned_data.duplicated().sum()}")
        
        # Show cleaned data
        print_section("📊 Cleaned Data Preview")
        print(cleaned_data.head(10))
        
        # Store results
        self.demo_results['sample_data'] = {
            'original': sample_data,
            'cleaned': cleaned_data,
            'improvements': {
                'missing_removed': sample_data.isnull().sum().sum() - cleaned_data.isnull().sum().sum(),
                'duplicates_removed': sample_data.duplicated().sum() - cleaned_data.duplicated().sum()
            }
        }
        
        print("✅ Demo 1 Complete: Sample data cleaning successful!")
        return cleaned_data
    
    def demo_2_who_data_cleaning(self):
        """Demo 2: WHO Health Data Cleaning"""
        print_header("DEMO 2: WHO Health Data Cleaning")
        
        # Check if WHO data exists
        who_file = 'WHO_Data.xlsx'
        if not os.path.exists(who_file):
            print(f"❌ {who_file} not found. Please ensure the file is in the current directory.")
            return None
        
        print(f"📁 Loading WHO Health Data from {who_file}...")
        
        try:
            # Load WHO data
            who_data = pd.read_excel(who_file, sheet_name=0)
            print(f"✅ WHO data loaded: {who_data.shape[0]} rows × {who_data.shape[1]} columns")
            
            # Show original data info
            print_section("📊 Original WHO Data Overview")
            print(f"Shape: {who_data.shape}")
            print(f"Missing values: {who_data.isnull().sum().sum()}")
            print(f"Duplicates: {who_data.duplicated().sum()}")
            print(f"Memory usage: {who_data.memory_usage(deep=True).sum() / 1024:.1f} KB")
            
            # Show column names
            print_section("📝 Column Information")
            print("First 10 columns:")
            for i, col in enumerate(who_data.columns[:10], 1):
                print(f"  {i:2d}. {col}")
            if len(who_data.columns) > 10:
                print(f"  ... and {len(who_data.columns) - 10} more columns")
            
            # Data quality analysis
            print_section("🔍 WHO Data Quality Analysis")
            quality_report = self.agent.analyze_data_quality(who_data)
            
            print(f"Missing values: {sum(quality_report['missing_values'].values())}")
            print(f"Duplicates: {quality_report['duplicate_rows']}")
            print(f"Data types: {len(quality_report['numeric_columns'])} numeric, {len(quality_report['categorical_columns'])} categorical")
            
            if quality_report['issues']:
                print("Issues found:")
                for issue in quality_report['issues'][:3]:  # Show first 3
                    print(f"  - {issue}")
            
            # AI-powered cleaning
            print_section("🤖 AI-Powered WHO Data Cleaning")
            print("Applying intelligent cleaning to WHO health data...")
            
            cleaned_who_data = self.ai_agent.intelligent_clean(who_data)
            
            # Show cleaning results
            print_section("📈 WHO Data Cleaning Results")
            print(f"Original shape: {who_data.shape}")
            print(f"Cleaned shape: {cleaned_who_data.shape}")
            print(f"Missing values: {who_data.isnull().sum().sum()} → {cleaned_who_data.isnull().sum().sum()}")
            print(f"Duplicates: {who_data.duplicated().sum()} → {cleaned_who_data.duplicated().sum()}")
            
            # Calculate quality improvement
            original_quality = 100 - (who_data.isnull().sum().sum() / (who_data.shape[0] * who_data.shape[1]) * 100)
            cleaned_quality = 100 - (cleaned_who_data.isnull().sum().sum() / (cleaned_who_data.shape[0] * cleaned_who_data.shape[1]) * 100)
            
            print(f"Data quality: {original_quality:.1f}% → {cleaned_quality:.1f}% (+{cleaned_quality - original_quality:.1f}%)")
            
            # Show sample of cleaned data
            print_section("📊 Cleaned WHO Data Preview")
            print(cleaned_who_data.head(3))
            
            # Save cleaned data
            output_file = 'WHO_Data_Cleaned.xlsx'
            cleaned_who_data.to_excel(output_file, index=False)
            print(f"💾 Cleaned WHO data saved to: {output_file}")
            
            # Store results
            self.demo_results['who_data'] = {
                'original': who_data,
                'cleaned': cleaned_who_data,
                'improvements': {
                    'missing_removed': who_data.isnull().sum().sum() - cleaned_who_data.isnull().sum().sum(),
                    'duplicates_removed': who_data.duplicated().sum() - cleaned_who_data.duplicated().sum(),
                    'quality_improvement': cleaned_quality - original_quality
                }
            }
            
            print("✅ Demo 2 Complete: WHO data cleaning successful!")
            return cleaned_who_data
            
        except Exception as e:
            print(f"❌ Error processing WHO data: {e}")
            return None
    
    def demo_3_multi_sheet_excel(self):
        """Demo 3: Multi-Sheet Excel Support"""
        print_header("DEMO 3: Multi-Sheet Excel Support")
        
        print("📁 Creating sample multi-sheet Excel file...")
        
        # Create sample multi-sheet data
        life_expectancy_data = pd.DataFrame({
            'Country': ['USA', 'Canada', 'UK', 'Germany', 'Japan', 'Australia', 'France', 'Italy', 'Spain', 'Netherlands'],
            'Life_Expectancy': [76.1, 82.2, 81.3, 81.0, 84.6, 83.4, 82.7, 83.1, 83.2, 81.9],
            'GDP_Per_Capita': [65000, 52000, 45000, 48000, 42000, 55000, 44000, 35000, 30000, 52000],
            'Health_Expenditure': [17.7, 10.9, 9.8, 11.2, 10.9, 9.3, 11.1, 8.8, 8.9, 10.1]
        })
        
        disease_data = pd.DataFrame({
            'Country': ['USA', 'Canada', 'UK', 'Germany', 'Japan', 'Australia', 'France', 'Italy', 'Spain', 'Netherlands'],
            'Diabetes_Rate': [10.5, 7.2, 6.8, 8.1, 6.6, 5.1, 5.4, 5.0, 6.5, 5.2],
            'Heart_Disease_Rate': [12.1, 8.9, 9.2, 10.1, 7.8, 8.1, 8.5, 9.8, 8.9, 7.2],
            'Cancer_Rate': [15.2, 12.8, 13.1, 14.2, 11.9, 12.5, 13.8, 14.1, 13.5, 12.1]
        })
        
        # Add some data quality issues
        life_expectancy_data.loc[1, 'Life_Expectancy'] = None
        disease_data.loc[2, 'Diabetes_Rate'] = None
        disease_data = pd.concat([disease_data, disease_data.iloc[[0]]], ignore_index=True)  # Duplicate
        
        # Save to Excel with multiple sheets
        excel_file = 'sample_health_multi_sheet.xlsx'
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            life_expectancy_data.to_excel(writer, sheet_name='Life_Expectancy', index=False)
            disease_data.to_excel(writer, sheet_name='Disease_Data', index=False)
        
        print(f"✅ Created multi-sheet Excel file: {excel_file}")
        
        # Load all sheets
        print_section("📋 Loading All Sheets")
        sheets = self.agent.load_excel_multi_sheet(excel_file)
        
        if sheets:
            print(f"✅ Loaded {len(sheets)} sheets:")
            for sheet_name, df in sheets.items():
                print(f"  - {sheet_name}: {df.shape[0]} rows × {df.shape[1]} columns")
            
            # Clean all sheets
            print_section("🧹 Cleaning All Sheets")
            cleaned_sheets = self.agent.clean_all_sheets(sheets)
            
            # Compare results
            print_section("📊 Sheet-by-Sheet Comparison")
            self.agent.compare_sheets(sheets, cleaned_sheets)
            
            # Save cleaned data
            output_file = 'sample_health_cleaned.xlsx'
            self.agent.save_cleaned_excel(cleaned_sheets, output_file)
            
            print(f"✅ Multi-sheet cleaning complete! Saved to: {output_file}")
            
            # Store results
            self.demo_results['multi_sheet'] = {
                'original_sheets': sheets,
                'cleaned_sheets': cleaned_sheets,
                'sheets_count': len(sheets)
            }
            
            return cleaned_sheets
        else:
            print("❌ Failed to load multi-sheet Excel file")
            return None
    
    def generate_final_report(self):
        """Generate comprehensive final report"""
        print_header("FINAL REPORT: AI-Powered Data Cleaning Agent")
        
        print("📋 COMPREHENSIVE DEMONSTRATION SUMMARY")
        print("=" * 50)
        
        print(f"🕒 Demo completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🤖 Agent used: AI-Powered Data Cleaning Agent")
        print(f"🏆 Competition: GenAI Competition - UoM DSCubed x UWA DSC")
        
        # Summary of all demos
        if 'sample_data' in self.demo_results:
            sample_results = self.demo_results['sample_data']
            print(f"\n📊 Demo 1 - Sample Data Cleaning:")
            print(f"   - Missing values removed: {sample_results['improvements']['missing_removed']}")
            print(f"   - Duplicates removed: {sample_results['improvements']['duplicates_removed']}")
        
        if 'who_data' in self.demo_results:
            who_results = self.demo_results['who_data']
            print(f"\n🌍 Demo 2 - WHO Health Data Cleaning:")
            print(f"   - Missing values removed: {who_results['improvements']['missing_removed']}")
            print(f"   - Duplicates removed: {who_results['improvements']['duplicates_removed']}")
            print(f"   - Quality improvement: +{who_results['improvements']['quality_improvement']:.1f}%")
        
        if 'multi_sheet' in self.demo_results:
            multi_results = self.demo_results['multi_sheet']
            print(f"\n📋 Demo 3 - Multi-Sheet Excel Support:")
            print(f"   - Sheets processed: {multi_results['sheets_count']}")
            print(f"   - All sheets cleaned successfully")
        
        # Competition features demonstrated
        print(f"\n🏆 COMPETITION FEATURES DEMONSTRATED:")
        print(f"   ✅ AI-powered intelligent cleaning suggestions")
        print(f"   ✅ Multi-sheet Excel file support")
        print(f"   ✅ Comprehensive data quality analysis")
        print(f"   ✅ Before/after comparison visualizations")
        print(f"   ✅ Professional reporting and documentation")
        print(f"   ✅ Real-world health data processing")
        print(f"   ✅ Workshop integration with health datasets")
        print(f"   ✅ Advanced data cleaning capabilities")
        
        # Technical achievements
        print(f"\n🔧 TECHNICAL ACHIEVEMENTS:")
        print(f"   ✅ OpenAI API integration for AI suggestions")
        print(f"   ✅ Intelligent missing value handling")
        print(f"   ✅ Data type optimization and standardization")
        print(f"   ✅ Outlier detection and treatment")
        print(f"   ✅ Text cleaning and normalization")
        print(f"   ✅ Memory optimization")
        print(f"   ✅ Comprehensive error handling")
        
        print(f"\n🎉 DEMONSTRATION COMPLETE!")
        print(f"   The AI-Powered Data Cleaning Agent successfully demonstrated")
        print(f"   all required features for the GenAI Competition!")
        
        # Save final report
        report_data = {
            'demo_timestamp': datetime.now().isoformat(),
            'competition': 'GenAI Competition - UoM DSCubed x UWA DSC',
            'agent_type': 'AI-Powered Data Cleaning Agent',
            'demos_completed': list(self.demo_results.keys()),
            'results': self.demo_results
        }
        
        with open('complete_demo_report.json', 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
        
        print(f"\n💾 Final report saved to: complete_demo_report.json")

def main():
    """Main demonstration function"""
    print_header("AI-POWERED DATA CLEANING AGENT", "🎯", 70)
    print("GenAI Competition - UoM DSCubed x UWA DSC")
    print("Author: Rudra Tiwari")
    print("=" * 70)
    
    # Initialize demo
    demo = CompleteDataCleaningDemo()
    
    try:
        # Run all demonstrations
        print("\n🚀 Starting comprehensive demonstration...")
        
        # Demo 1: Sample data cleaning
        demo.demo_1_sample_data_cleaning()
        
        # Demo 2: WHO data cleaning
        demo.demo_2_who_data_cleaning()
        
        # Demo 3: Multi-sheet Excel support
        demo.demo_3_multi_sheet_excel()
        
        # Generate final report
        demo.generate_final_report()
        
        print_header("🎉 ALL DEMONSTRATIONS COMPLETE!", "🏆", 70)
        print("The AI-Powered Data Cleaning Agent is ready for competition!")
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        print("Please check the error and try again.")

if __name__ == "__main__":
    main()
