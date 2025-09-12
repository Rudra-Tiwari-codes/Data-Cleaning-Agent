# Configuration for Global Health Crisis Prediction Engine
# Based on Data Cleaning Agent Workshop Framework

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
REST_COUNTRIES_API_URL = "https://restcountries.com/v3.1"
API_TIMEOUT = 15

# Data Sources (Health Crisis Prediction Relevant Only)
DATASET_PATHS = {
    'life_expectancy': 'datasets/Life Expectancy Data.csv'  # Only relevant dataset for health crisis prediction
}

# Analysis Parameters
CRISIS_THRESHOLDS = {
    'high_risk': 0.7,
    'medium_risk': 0.4,
    'low_risk': 0.1
}

# OpenAI Configuration (from workshop)
OPENAI_API_KEY = "your-openai-api-key-here"  # Set your API key here
OPENAI_MODEL = "gpt-4o-mini"  # Cost-effective model for health analysis
OPENAI_TEMPERATURE = 0.0  # Deterministic responses for health analysis

# AI Query Configuration
AI_FEATURES = {
    'country_analysis': True,
    'global_summary': True,
    'risk_prediction': True,
    'regional_analysis': True,
    'crisis_recommendations': True,
    'country_comparison': True
}

# Project Configuration
PROJECT_NAME = "Global Health Crisis Prediction Engine"
VERSION = "1.0.0"
