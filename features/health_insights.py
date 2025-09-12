# Health Insights Feature
# Based on Data Cleaning Agent Workshop Framework

import pandas as pd
import numpy as np
from typing import Dict, Any, List

def analyze_country_risk(country_name: str, health_engine) -> Dict[str, Any]:
    """
    Analyze risk for a specific country using AI-powered insights
    """
    analysis = health_engine.get_country_analysis(country_name)
    if analysis:
        return {
            'country': country_name,
            'crisis_level': analysis['crisis_level'],
            'crisis_probability': analysis['country']['crisis_probability'],
            'vulnerability_index': analysis['country']['vulnerability_index'],
            'resilience_score': analysis['country']['resilience_score'],
            'recommendations': analysis['ai_recommendations']
        }
    return None

def get_global_summary(health_engine) -> Dict[str, Any]:
    """
    Get comprehensive global health crisis summary
    """
    if not health_engine.data:
        return {"error": "No data available"}
    
    analytics = health_engine.data['global_analytics']
    predictions = health_engine.data['crisis_predictions']
    
    return {
        'total_countries': analytics['total_countries'],
        'total_population': analytics['total_population'],
        'global_crisis_probability': analytics['avg_crisis_probability'],
        'high_risk_countries': analytics['high_risk_countries'],
        'immediate_threats': len(predictions['immediate_threats']),
        'emerging_risks': len(predictions['emerging_risks']),
        'population_at_risk': predictions['global_trends']['total_at_risk_population']
    }

def find_high_risk_countries(health_engine, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Find countries with highest crisis probability
    """
    if not health_engine.data:
        return []
    
    countries = health_engine.data['countries']
    high_risk = sorted(countries, key=lambda x: x['crisis_probability'], reverse=True)[:limit]
    
    return [{
        'name': country['name'],
        'crisis_probability': country['crisis_probability'],
        'vulnerability_index': country['vulnerability_index'],
        'population': country['population']
    } for country in high_risk]

def analyze_regional_trends(health_engine) -> Dict[str, Any]:
    """
    Analyze health trends by geographic region
    """
    if not health_engine.data:
        return {"error": "No data available"}
    
    countries = health_engine.data['countries']
    regional_data = {}
    
    for country in countries:
        region = country['region']
        if region not in regional_data:
            regional_data[region] = {
                'countries': 0,
                'total_population': 0,
                'avg_crisis_probability': 0,
                'total_crisis_probability': 0
            }
        
        regional_data[region]['countries'] += 1
        regional_data[region]['total_population'] += country['population']
        regional_data[region]['total_crisis_probability'] += country['crisis_probability']
    
    # Calculate averages
    for region in regional_data:
        regional_data[region]['avg_crisis_probability'] = (
            regional_data[region]['total_crisis_probability'] / 
            regional_data[region]['countries']
        )
    
    return regional_data

def get_crisis_recommendations(health_engine) -> List[str]:
    """
    Get AI-powered crisis response recommendations
    """
    if not health_engine.data:
        return ["No data available for recommendations"]
    
    predictions = health_engine.data['crisis_predictions']
    return predictions['recommendations']

def compare_countries(country1: str, country2: str, health_engine) -> Dict[str, Any]:
    """
    Compare health metrics between two countries
    """
    analysis1 = health_engine.get_country_analysis(country1)
    analysis2 = health_engine.get_country_analysis(country2)
    
    if not analysis1 or not analysis2:
        return {"error": "One or both countries not found"}
    
    return {
        'comparison': {
            country1: {
                'crisis_probability': analysis1['country']['crisis_probability'],
                'vulnerability_index': analysis1['country']['vulnerability_index'],
                'resilience_score': analysis1['country']['resilience_score'],
                'population': analysis1['country']['population']
            },
            country2: {
                'crisis_probability': analysis2['country']['crisis_probability'],
                'vulnerability_index': analysis2['country']['vulnerability_index'],
                'resilience_score': analysis2['country']['resilience_score'],
                'population': analysis2['country']['population']
            }
        },
        'higher_risk': country1 if analysis1['country']['crisis_probability'] > analysis2['country']['crisis_probability'] else country2
    }

def predict_crisis_timeline(health_engine) -> Dict[str, Any]:
    """
    Predict potential crisis timeline based on current data
    """
    if not health_engine.data:
        return {"error": "No data available"}
    
    analytics = health_engine.data['global_analytics']
    predictions = health_engine.data['crisis_predictions']
    
    # Simple prediction logic based on current metrics
    global_risk = analytics['avg_crisis_probability']
    high_risk_count = analytics['high_risk_countries']
    
    timeline = {
        'immediate_concern': high_risk_count > 10,
        'short_term_risk': global_risk > 0.3,
        'medium_term_risk': global_risk > 0.2,
        'long_term_monitoring': global_risk > 0.1,
        'recommended_actions': predictions['recommendations'][:3] if predictions['recommendations'] else []
    }
    
    return timeline
