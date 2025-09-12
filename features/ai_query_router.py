# AI Query Router for Health Crisis Prediction
# Uses OpenAI to process natural language health queries

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_TEMPERATURE
import traceback

def route_health_query(user_query: str, health_engine=None, df=None):
    """
    Route health queries using OpenAI to generate appropriate code
    """
    if not OPENAI_API_KEY:
        return "OpenAI API key not configured. Please set OPENAI_API_KEY in config.py"
    
    # Initialize OpenAI
    llm = ChatOpenAI(
        api_key=OPENAI_API_KEY,
        model=OPENAI_MODEL,
        temperature=OPENAI_TEMPERATURE
    )
    
    # Create system message
    messages = []
    messages.append(SystemMessage(content=f"""You are a health data analysis expert. 
    Generate Python code to answer health-related queries using the available data and health engine.
    
    Available objects:
    - health_engine: GlobalHealthEngine object with methods for health analysis
    - df: pandas DataFrame with country data (if available)
    
    Health Engine Methods:
    - health_engine.get_country_analysis(country_name): Get analysis for specific country
    - health_engine.display_health_insights(): Show global health insights
    - health_engine.get_immediate_threats(): Get countries at immediate risk
    - health_engine.get_emerging_risks(): Get countries with emerging risks
    - health_engine.get_global_trends(): Get global health trends
    - health_engine.get_regional_vulnerability(): Get regional vulnerability analysis
    
    Instructions:
    - Use the health_engine object for all health analysis operations
    - Return only executable Python code, no explanations, NO MARKDOWN BLOCKS
    - If query requires data analysis, use pandas operations on df if provided
    - For health-specific queries, use health_engine methods
    - Always include error handling with try-except blocks
    
    Examples:
    HEALTH QUERIES:
    - User: What countries are at highest risk?, Generated: try: high_risk = health_engine.get_country_analysis('India'); print(f'India Crisis Level: {high_risk["crisis_level"]}'); except Exception as e: print(f'Error: {e}')
    - User: Show me global health summary, Generated: try: health_engine.display_health_insights(); except Exception as e: print(f'Error: {e}')
    - User: Compare India and China health metrics, Generated: try: india = health_engine.get_country_analysis('India'); china = health_engine.get_country_analysis('China'); print(f'India: {india["country"]["crisis_probability"]:.1%}'); print(f'China: {china["country"]["crisis_probability"]:.1%}'); except Exception as e: print(f'Error: {e}')
    
    DATA ANALYSIS QUERIES:
    - User: What are the top 5 countries by population?, Generated: try: if df is not None: top_pop = df.nlargest(5, 'population')[['name', 'population']]; print(top_pop); else: print('No data available'); except Exception as e: print(f'Error: {e}')
    """))
    
    messages.append(HumanMessage(content=f"User health query: {user_query}"))
    
    # Call OpenAI
    try:
        response = llm.invoke(messages)
        return response.content
    except Exception as e:
        return f"Error generating query response: {e}"

def execute_health_query(user_query: str, health_engine=None, df=None):
    """
    Execute health query by routing to OpenAI and running generated code
    """
    print(f"Processing query: {user_query}")
    print("-" * 50)
    
    # Route query to get code
    code = route_health_query(user_query, health_engine, df)
    
    if code.startswith("Error") or code.startswith("OpenAI"):
        print(code)
        return None
    
    # Execute the generated code
    try:
        print("Generated code:")
        print(code)
        print("\nExecuting...")
        print("-" * 30)
        
        # Create execution environment
        exec_globals = {
            'health_engine': health_engine,
            'df': df,
            'print': print
        }
        
        exec(code, exec_globals)
        return True
        
    except Exception as e:
        print(f"Execution error: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return False

def get_ai_health_insights(health_engine=None, df=None):
    """
    Get AI-generated health insights using OpenAI
    """
    if not OPENAI_API_KEY:
        return "OpenAI API key not configured"
    
    # Initialize OpenAI
    llm = ChatOpenAI(
        api_key=OPENAI_API_KEY,
        model=OPENAI_MODEL,
        temperature=OPENAI_TEMPERATURE
    )
    
    # Create system message for insights
    messages = []
    messages.append(SystemMessage(content="""You are a global health expert. 
    Analyze the provided health data and generate comprehensive insights about global health trends, 
    crisis risks, and recommendations for health policy makers.
    
    Focus on:
    - Key health trends and patterns
    - Countries at highest risk
    - Regional health disparities
    - Actionable recommendations
    - Emerging health threats
    
    Provide a structured analysis with clear insights and recommendations."""))
    
    # Get health data summary
    health_summary = ""
    if health_engine and health_engine.data:
        try:
            # Get basic health insights
            immediate_threats = health_engine.get_immediate_threats()
            emerging_risks = health_engine.get_emerging_risks()
            global_trends = health_engine.get_global_trends()
            
            health_summary = f"""
            Health Data Summary:
            - Total countries analyzed: {len(health_engine.data)}
            - Immediate threats: {len(immediate_threats)} countries
            - Emerging risks: {len(emerging_risks)} countries
            - Global trends: {global_trends}
            """
        except Exception as e:
            health_summary = f"Error getting health summary: {e}"
    
    messages.append(HumanMessage(content=f"Analyze this health data and provide insights:\n{health_summary}"))
    
    try:
        response = llm.invoke(messages)
        return response.content
    except Exception as e:
        return f"Error generating health insights: {e}"