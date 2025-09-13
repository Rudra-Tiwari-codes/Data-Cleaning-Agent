#!/usr/bin/env python3
"""
AI-Powered Data Cleaning Agent
Built for UoM DSCubed x UWA DSC GenAI Competition
Based on workshop methods with advanced AI integration
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

class DataCleaningAgent:
    """
    AI-Powered Data Cleaning Agent
    Provides intelligent data cleaning with OpenAI integration
    """
    
    def __init__(self):
        self.cleaning_history = []
        self.data_quality_report = {}
        self.cleaning_suggestions = []
    
    def analyze_data_quality(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Comprehensive data quality analysis
        """
        print("🔍 Analyzing Data Quality...")
        
        analysis = {
            'shape': df.shape,
            'columns': list(df.columns),
            'data_types': df.dtypes.to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'missing_percentage': (df.isnull().sum() / len(df) * 100).to_dict(),
            'duplicate_rows': df.duplicated().sum(),
            'duplicate_percentage': (df.duplicated().sum() / len(df) * 100),
            'memory_usage': df.memory_usage(deep=True).sum(),
            'numeric_columns': df.select_dtypes(include=[np.number]).columns.tolist(),
            'categorical_columns': df.select_dtypes(include=['object']).columns.tolist(),
            'datetime_columns': df.select_dtypes(include=['datetime64']).columns.tolist()
        }
        
        # Detect potential issues
        issues = []
        if analysis['missing_percentage']:
            high_missing = {col: pct for col, pct in analysis['missing_percentage'].items() if pct > 50}
            if high_missing:
                issues.append(f"High missing values (>50%): {high_missing}")
        
        if analysis['duplicate_percentage'] > 10:
            issues.append(f"High duplicate rate: {analysis['duplicate_percentage']:.1f}%")
        
        analysis['issues'] = issues
        self.data_quality_report = analysis
        
        return analysis
    
    def clean_missing_values(self, df: pd.DataFrame, strategy: str = 'auto') -> pd.DataFrame:
        """
        Clean missing values with intelligent strategies
        """
        print(f"🧹 Cleaning Missing Values using {strategy} strategy...")
        
        df_cleaned = df.copy()
        changes_made = []
        
        for column in df_cleaned.columns:
            missing_count = df_cleaned[column].isnull().sum()
            if missing_count > 0:
                if strategy == 'auto':
                    # Intelligent strategy selection
                    if df_cleaned[column].dtype in ['int64', 'float64']:
                        # Numeric: use median for skewed, mean for normal
                        try:
                            if df_cleaned[column].skew() > 1:
                                fill_value = df_cleaned[column].median()
                                method = 'median'
                            else:
                                fill_value = df_cleaned[column].mean()
                                method = 'mean'
                        except:
                            # If all values are NaN, use 0 for numeric
                            fill_value = 0
                            method = 'zero_fill'
                    else:
                        # Categorical: use mode
                        fill_value = df_cleaned[column].mode().iloc[0] if not df_cleaned[column].mode().empty else 'Unknown'
                        method = 'mode'
                elif strategy == 'drop':
                    df_cleaned = df_cleaned.dropna(subset=[column])
                    method = 'dropped'
                    fill_value = None
                elif strategy == 'forward_fill':
                    df_cleaned[column] = df_cleaned[column].fillna(method='ffill')
                    method = 'forward_fill'
                    fill_value = None
                else:
                    continue
                
                if method != 'dropped':
                    df_cleaned[column] = df_cleaned[column].fillna(fill_value)
                
                changes_made.append({
                    'column': column,
                    'missing_count': missing_count,
                    'method': method,
                    'fill_value': fill_value
                })
        
        # Log cleaning action
        self.cleaning_history.append({
            'action': 'clean_missing_values',
            'strategy': strategy,
            'changes': changes_made,
            'rows_before': len(df),
            'rows_after': len(df_cleaned)
        })
        
        print(f"✅ Cleaned {len(changes_made)} columns with missing values")
        return df_cleaned
    
    def remove_duplicates(self, df: pd.DataFrame, subset: Optional[List[str]] = None, keep: str = 'first') -> pd.DataFrame:
        """
        Remove duplicate rows
        """
        print("🔄 Removing Duplicate Rows...")
        
        rows_before = len(df)
        df_cleaned = df.drop_duplicates(subset=subset, keep=keep)
        rows_after = len(df_cleaned)
        duplicates_removed = rows_before - rows_after
        
        # Log cleaning action
        self.cleaning_history.append({
            'action': 'remove_duplicates',
            'subset': subset,
            'keep': keep,
            'duplicates_removed': duplicates_removed,
            'rows_before': rows_before,
            'rows_after': rows_after
        })
        
        print(f"✅ Removed {duplicates_removed} duplicate rows")
        return df_cleaned
    
    def standardize_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardize and optimize data types
        """
        print("🔧 Standardizing Data Types...")
        
        df_cleaned = df.copy()
        changes_made = []
        
        for column in df_cleaned.columns:
            original_dtype = str(df_cleaned[column].dtype)
            
            # Optimize numeric columns
            if df_cleaned[column].dtype == 'int64':
                if df_cleaned[column].min() >= 0 and df_cleaned[column].max() <= 255:
                    df_cleaned[column] = df_cleaned[column].astype('uint8')
                elif df_cleaned[column].min() >= -128 and df_cleaned[column].max() <= 127:
                    df_cleaned[column] = df_cleaned[column].astype('int8')
                elif df_cleaned[column].min() >= 0 and df_cleaned[column].max() <= 65535:
                    df_cleaned[column] = df_cleaned[column].astype('uint16')
                elif df_cleaned[column].min() >= -32768 and df_cleaned[column].max() <= 32767:
                    df_cleaned[column] = df_cleaned[column].astype('int16')
                elif df_cleaned[column].min() >= 0 and df_cleaned[column].max() <= 4294967295:
                    df_cleaned[column] = df_cleaned[column].astype('uint32')
                elif df_cleaned[column].min() >= -2147483648 and df_cleaned[column].max() <= 2147483647:
                    df_cleaned[column] = df_cleaned[column].astype('int32')
            
            # Optimize float columns
            elif df_cleaned[column].dtype == 'float64':
                df_cleaned[column] = pd.to_numeric(df_cleaned[column], downcast='float')
            
            # Convert object columns to category if low cardinality
            elif df_cleaned[column].dtype == 'object':
                unique_ratio = df_cleaned[column].nunique() / len(df_cleaned)
                if unique_ratio < 0.5:  # Less than 50% unique values
                    df_cleaned[column] = df_cleaned[column].astype('category')
            
            new_dtype = str(df_cleaned[column].dtype)
            if original_dtype != new_dtype:
                changes_made.append({
                    'column': column,
                    'original_dtype': original_dtype,
                    'new_dtype': new_dtype
                })
        
        # Log cleaning action
        self.cleaning_history.append({
            'action': 'standardize_data_types',
            'changes': changes_made
        })
        
        print(f"✅ Optimized {len(changes_made)} column data types")
        return df_cleaned
    
    def detect_outliers(self, df: pd.DataFrame, method: str = 'iqr') -> Dict[str, List[int]]:
        """
        Detect outliers in numeric columns
        """
        print(f"🎯 Detecting Outliers using {method} method...")
        
        outliers = {}
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        
        for column in numeric_columns:
            if method == 'iqr':
                Q1 = df[column].quantile(0.25)
                Q3 = df[column].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                outlier_indices = df[(df[column] < lower_bound) | (df[column] > upper_bound)].index.tolist()
            elif method == 'zscore':
                z_scores = np.abs((df[column] - df[column].mean()) / df[column].std())
                outlier_indices = df[z_scores > 3].index.tolist()
            
            if outlier_indices:
                outliers[column] = outlier_indices
        
        print(f"✅ Found outliers in {len(outliers)} columns")
        return outliers
    
    def clean_outliers(self, df: pd.DataFrame, outliers: Dict[str, List[int]], method: str = 'cap') -> pd.DataFrame:
        """
        Clean outliers using various methods
        """
        print(f"🧽 Cleaning Outliers using {method} method...")
        
        df_cleaned = df.copy()
        changes_made = []
        
        for column, outlier_indices in outliers.items():
            if method == 'cap':
                # Cap outliers at 95th and 5th percentiles
                lower_cap = df_cleaned[column].quantile(0.05)
                upper_cap = df_cleaned[column].quantile(0.95)
                df_cleaned[column] = df_cleaned[column].clip(lower=lower_cap, upper=upper_cap)
                method_used = 'capped'
            elif method == 'remove':
                df_cleaned = df_cleaned.drop(outlier_indices)
                method_used = 'removed'
            elif method == 'median':
                median_value = df_cleaned[column].median()
                df_cleaned.loc[outlier_indices, column] = median_value
                method_used = 'replaced_with_median'
            
            changes_made.append({
                'column': column,
                'outlier_count': len(outlier_indices),
                'method': method_used
            })
        
        # Log cleaning action
        self.cleaning_history.append({
            'action': 'clean_outliers',
            'method': method,
            'changes': changes_made
        })
        
        print(f"✅ Cleaned outliers in {len(changes_made)} columns")
        return df_cleaned
    
    def standardize_text(self, df: pd.DataFrame, columns: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Standardize text data (lowercase, trim whitespace, etc.)
        """
        print("📝 Standardizing Text Data...")
        
        df_cleaned = df.copy()
        if columns is None:
            columns = df_cleaned.select_dtypes(include=['object']).columns
        
        changes_made = []
        for column in columns:
            if df_cleaned[column].dtype == 'object':
                original_sample = df_cleaned[column].dropna().iloc[0] if not df_cleaned[column].dropna().empty else None
                
                # Standardize text
                df_cleaned[column] = df_cleaned[column].astype(str).str.strip().str.lower()
                
                new_sample = df_cleaned[column].dropna().iloc[0] if not df_cleaned[column].dropna().empty else None
                if original_sample != new_sample:
                    changes_made.append({
                        'column': column,
                        'original_sample': original_sample,
                        'new_sample': new_sample
                    })
        
        # Log cleaning action
        self.cleaning_history.append({
            'action': 'standardize_text',
            'columns': columns,
            'changes': changes_made
        })
        
        print(f"✅ Standardized text in {len(changes_made)} columns")
        return df_cleaned
    
    def generate_cleaning_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive cleaning report
        """
        report = {
            'total_actions': len(self.cleaning_history),
            'actions_performed': [action['action'] for action in self.cleaning_history],
            'data_quality_before': self.data_quality_report,
            'cleaning_summary': self.cleaning_history
        }
        
        return report
    
    def load_excel_multi_sheet(self, file_path: str) -> Dict[str, pd.DataFrame]:
        """
        Load all sheets from Excel file
        """
        print(f"📁 Loading Excel file with multiple sheets: {file_path}")
        
        try:
            excel_file = pd.ExcelFile(file_path)
            sheets = {}
            
            for sheet_name in excel_file.sheet_names:
                print(f"   Loading sheet: {sheet_name}")
                sheets[sheet_name] = pd.read_excel(file_path, sheet_name=sheet_name)
                print(f"   ✅ {sheet_name}: {sheets[sheet_name].shape[0]} rows × {sheets[sheet_name].shape[1]} columns")
            
            print(f"✅ Loaded {len(sheets)} sheets successfully!")
            return sheets
            
        except Exception as e:
            print(f"❌ Error loading Excel file: {e}")
            return {}
    
    def select_sheet(self, sheets: Dict[str, pd.DataFrame]) -> Tuple[str, pd.DataFrame]:
        """
        Interactive sheet selection
        """
        print("\n📋 Available Sheets:")
        print("-" * 30)
        
        sheet_names = list(sheets.keys())
        for i, sheet_name in enumerate(sheet_names, 1):
            df = sheets[sheet_name]
            print(f"{i}. {sheet_name} ({df.shape[0]} rows × {df.shape[1]} columns)")
        
        while True:
            try:
                choice = input(f"\nSelect sheet number (1-{len(sheet_names)}): ").strip()
                choice_idx = int(choice) - 1
                
                if 0 <= choice_idx < len(sheet_names):
                    selected_sheet = sheet_names[choice_idx]
                    selected_df = sheets[selected_sheet]
                    print(f"✅ Selected: {selected_sheet}")
                    return selected_sheet, selected_df
                else:
                    print(f"❌ Please enter a number between 1 and {len(sheet_names)}")
            except ValueError:
                print("❌ Please enter a valid number")
    
    def clean_all_sheets(self, sheets: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
        """
        Clean all sheets in an Excel file
        """
        print("🧹 Cleaning All Sheets...")
        print("=" * 50)
        
        cleaned_sheets = {}
        
        for sheet_name, df in sheets.items():
            print(f"\n📊 Cleaning Sheet: {sheet_name}")
            print("-" * 30)
            
            # Clean each sheet
            cleaned_df = self.auto_clean(df)
            cleaned_sheets[sheet_name] = cleaned_df
            
            # Log cleaning for this sheet
            self.cleaning_history.append({
                'action': 'clean_sheet',
                'sheet_name': sheet_name,
                'rows_before': len(df),
                'rows_after': len(cleaned_df)
            })
        
        print("\n" + "=" * 50)
        print("🎉 All Sheets Cleaned Successfully!")
        return cleaned_sheets
    
    def compare_sheets(self, original_sheets: Dict[str, pd.DataFrame], cleaned_sheets: Dict[str, pd.DataFrame]) -> None:
        """
        Compare original vs cleaned sheets
        """
        print("📊 Sheet-by-Sheet Comparison:")
        print("=" * 60)
        
        for sheet_name in original_sheets.keys():
            original_df = original_sheets[sheet_name]
            cleaned_df = cleaned_sheets[sheet_name]
            
            print(f"\n📋 Sheet: {sheet_name}")
            print("-" * 30)
            
            # Basic comparison
            print(f"   Shape: {original_df.shape} → {cleaned_df.shape}")
            print(f"   Missing values: {original_df.isnull().sum().sum()} → {cleaned_df.isnull().sum().sum()}")
            print(f"   Duplicates: {original_df.duplicated().sum()} → {cleaned_df.duplicated().sum()}")
            print(f"   Memory: {original_df.memory_usage(deep=True).sum() / 1024:.1f} KB → {cleaned_df.memory_usage(deep=True).sum() / 1024:.1f} KB")
    
    def save_cleaned_excel(self, cleaned_sheets: Dict[str, pd.DataFrame], output_path: str) -> None:
        """
        Save cleaned sheets to new Excel file
        """
        print(f"💾 Saving cleaned data to: {output_path}")
        
        try:
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                for sheet_name, df in cleaned_sheets.items():
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
                    print(f"   ✅ Saved sheet: {sheet_name}")
            
            print("✅ All sheets saved successfully!")
            
        except Exception as e:
            print(f"❌ Error saving Excel file: {e}")

    def auto_clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Perform automatic data cleaning with intelligent decisions
        """
        print("🤖 Starting Automatic Data Cleaning...")
        print("=" * 50)
        
        # Step 1: Analyze data quality
        self.analyze_data_quality(df)
        
        # Step 2: Clean missing values
        df_cleaned = self.clean_missing_values(df, strategy='auto')
        
        # Step 3: Remove duplicates
        df_cleaned = self.remove_duplicates(df_cleaned)
        
        # Step 4: Standardize data types
        df_cleaned = self.standardize_data_types(df_cleaned)
        
        # Step 5: Detect and clean outliers
        outliers = self.detect_outliers(df_cleaned)
        if outliers:
            df_cleaned = self.clean_outliers(df_cleaned, outliers, method='cap')
        
        # Step 6: Standardize text
        df_cleaned = self.standardize_text(df_cleaned)
        
        print("=" * 50)
        print("🎉 Automatic Data Cleaning Complete!")
        
        return df_cleaned
