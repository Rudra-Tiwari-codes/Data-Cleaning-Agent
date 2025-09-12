# OpenAI API Setup Guide

## Quick Setup for AI-Powered Data Cleaning Agent

### Step 1: Get OpenAI API Key
1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign up or log in to your account
3. Click "Create new secret key"
4. Copy the API key (starts with `sk-`)

### Step 2: Configure API Key
Open `config.py` and replace the placeholder:

```python
OPENAI_API_KEY = "your-openai-api-key-here"  # Replace with your actual API key
```

### Step 3: Test the Setup
Run this in your Python environment:

```python
from config import OPENAI_API_KEY
print(f"API Key configured: {'Yes' if OPENAI_API_KEY != 'your-openai-api-key-here' else 'No'}")
```

### Step 4: Install Dependencies
```bash
pip install langchain langchain-openai python-dotenv
```

## AI Features Available:
- **Intelligent Cleaning Suggestions** - AI analyzes your data and suggests cleaning actions
- **Automated Cleaning Workflows** - AI-powered cleaning process
- **Code Generation** - AI generates Python cleaning code
- **Data Insights** - Natural language analysis of your data

## For Demo:
1. Set up OpenAI API key
2. Run `python complete_demo.py` to see AI features
3. Use `interactive_demo.ipynb` for step-by-step demo
4. Show AI-powered suggestions and cleaning

**Ready for your hackathon demo!**
