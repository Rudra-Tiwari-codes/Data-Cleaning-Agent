#!/usr/bin/env python3
"""
AI-Powered Data Cleaning with OpenAI Integration
Provides intelligent cleaning suggestions and automated cleaning
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from data_cleaning_agent import DataCleaningAgent
from config import OPENAI_API_KEY
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

class AIDataCleaningAgent(DataCleaningAgent):
    """
    AI-Enhanced Data Cleaning Agent
    Uses OpenAI to provide intelligent cleaning suggestions
    """
    
    def __init__(self):
        super().__init__()
        self.llm = None
        if OPENAI_API_KEY:
            self.llm = ChatOpenAI(
                api_key=OPENAI_API_KEY,
                model="gpt-4o-mini",
                temperature=0.0
            )
    
    def get_ai_cleaning_suggestions(self, df: pd.DataFrame) -> List[str]:
        """
        Get AI-powered cleaning suggestions
        """
        if not self.llm:
            return ["OpenAI API not configured. Please set OPENAI_API_KEY in config.py"]
        
        print("🤖 Getting AI Cleaning Suggestions...")
        
        # Analyze data first
        analysis = self.analyze_data_quality(df)
        
        # Create prompt for AI
        prompt = f"""
        You are a data cleaning expert. Analyze this dataset and provide specific cleaning recommendations.
        
        Dataset Info:
        - Shape: {analysis['shape']}
        - Columns: {analysis['columns']}
        - Missing values: {analysis['missing_values']}
        - Duplicate rows: {analysis['duplicate_rows']}
        - Data types: {analysis['data_types']}
        - Issues detected: {analysis['issues']}
        
        Provide 5-7 specific, actionable cleaning recommendations. Focus on:
        1. Missing value handling strategies
        2. Data type optimizations
        3. Outlier treatment
        4. Text standardization
        5. Duplicate handling
        
        Format each recommendation as a clear, actionable step.
        """
        
        try:
            messages = [
                SystemMessage(content="You are a data cleaning expert. Provide specific, actionable recommendations for cleaning datasets."),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm.invoke(messages)
            suggestions = response.content.split('\n')
            
            # Filter and clean suggestions
            cleaned_suggestions = []
            for suggestion in suggestions:
                if suggestion.strip() and not suggestion.strip().startswith('#'):
                    cleaned_suggestions.append(suggestion.strip())
            
            self.cleaning_suggestions = cleaned_suggestions
            return cleaned_suggestions
            
        except Exception as e:
            return [f"Error getting AI suggestions: {e}"]
    
    def get_ai_data_insights(self, df: pd.DataFrame) -> str:
        """
        Get AI-powered data insights and recommendations
        """
        if not self.llm:
            return "OpenAI API not configured. Please set OPENAI_API_KEY in config.py"
        
        print("🤖 Getting AI Data Insights...")
        
        # Analyze data
        analysis = self.analyze_data_quality(df)
        
        # Create prompt
        prompt = f"""
        You are a data analysis expert. Provide insights about this dataset and cleaning recommendations.
        
        Dataset Analysis:
        - Shape: {analysis['shape']}
        - Missing values: {analysis['missing_values']}
        - Duplicate rows: {analysis['duplicate_rows']}
        - Data types: {analysis['data_types']}
        - Issues: {analysis['issues']}
        
        Provide comprehensive insights about:
        1. Data quality assessment
        2. Potential data issues
        3. Cleaning priorities
        4. Best practices for this type of data
        5. Recommendations for analysis readiness
        
        Be specific and actionable.
        """
        
        try:
            messages = [
                SystemMessage(content="You are a data analysis expert. Provide comprehensive insights about dataset quality and cleaning recommendations."),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm.invoke(messages)
            return response.content
            
        except Exception as e:
            return f"Error getting AI insights: {e}"
    
    def intelligent_clean(self, df: pd.DataFrame, user_preferences: Optional[Dict] = None) -> pd.DataFrame:
        """
        Perform intelligent cleaning based on AI suggestions
        """
        print("🧠 Starting AI-Powered Intelligent Cleaning...")
        print("=" * 50)
        
        # Get AI suggestions
        suggestions = self.get_ai_cleaning_suggestions(df)
        
        print("🤖 AI Cleaning Suggestions:")
        for i, suggestion in enumerate(suggestions[:5], 1):
            print(f"   {i}. {suggestion}")
        
        # Perform intelligent cleaning
        df_cleaned = df.copy()
        
        # Apply AI-informed cleaning strategies
        for suggestion in suggestions:
            if "missing" in suggestion.lower() or "null" in suggestion.lower():
                df_cleaned = self.clean_missing_values(df_cleaned, strategy='auto')
            elif "duplicate" in suggestion.lower():
                df_cleaned = self.remove_duplicates(df_cleaned)
            elif "outlier" in suggestion.lower():
                outliers = self.detect_outliers(df_cleaned)
                if outliers:
                    df_cleaned = self.clean_outliers(df_cleaned, outliers, method='cap')
            elif "text" in suggestion.lower() or "standardize" in suggestion.lower():
                df_cleaned = self.standardize_text(df_cleaned)
            elif "type" in suggestion.lower() or "dtype" in suggestion.lower():
                df_cleaned = self.standardize_data_types(df_cleaned)
        
        print("=" * 50)
        print("🎉 AI-Powered Cleaning Complete!")
        
        return df_cleaned
    
    def generate_cleaning_code(self, df: pd.DataFrame, cleaning_steps: List[str]) -> str:
        """
        Generate Python code for cleaning steps
        """
        if not self.llm:
            return "# OpenAI API not configured"
        
        print("🤖 Generating Cleaning Code...")
        
        prompt = f"""
        Generate Python code for the following data cleaning steps:
        
        Dataset info:
        - Shape: {df.shape}
        - Columns: {list(df.columns)}
        
        Cleaning steps requested:
        {cleaning_steps}
        
        Generate clean, efficient Python code using pandas. Include:
        1. Import statements
        2. Data loading (assume df is already loaded)
        3. Each cleaning step with comments
        4. Data quality checks
        5. Final validation
        
        Return only the Python code, no explanations.
        """
        
        try:
            messages = [
                SystemMessage(content="You are a Python expert. Generate clean, efficient pandas code for data cleaning."),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm.invoke(messages)
            return response.content
            
        except Exception as e:
            return f"# Error generating code: {e}"
    
    def explain_cleaning_action(self, action: str, df: pd.DataFrame) -> str:
        """
        Get AI explanation of a cleaning action
        """
        if not self.llm:
            return "OpenAI API not configured"
        
        prompt = f"""
        Explain this data cleaning action in simple terms:
        
        Action: {action}
        Dataset: {df.shape[0]} rows, {df.shape[1]} columns
        
        Explain:
        1. What this action does
        2. Why it's important
        3. How it affects the data
        4. When to use it
        
        Keep it simple and educational.
        """
        
        try:
            messages = [
                SystemMessage(content="You are a data cleaning educator. Explain cleaning actions in simple, clear terms."),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm.invoke(messages)
            return response.content
            
        except Exception as e:
            return f"Error getting explanation: {e}"
