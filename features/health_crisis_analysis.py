#!/usr/bin/env python3
"""
Health Crisis Analysis Module
Specialized analysis for WHO health data and crisis prediction
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Any, Optional
import warnings

warnings.filterwarnings('ignore')

class HealthCrisisAnalyzer:
    """
    Specialized analyzer for health crisis data
    Works with WHO health datasets and life expectancy data
    """
    
    def __init__(self):
        self.crisis_thresholds = {
            'life_expectancy_low': 60,
            'life_expectancy_medium': 70,
            'gdp_low': 5000,
            'gdp_medium': 15000,
            'health_expenditure_low': 3,
            'health_expenditure_medium': 8
        }
    
    def analyze_health_crisis_risk(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze health crisis risk based on WHO health indicators
        
        Args:
            df: DataFrame with health data
            
        Returns:
            Dictionary with crisis analysis results
        """
        analysis = {
            'total_countries': len(df),
            'crisis_indicators': {},
            'risk_categories': {},
            'recommendations': []
        }
        
        # Analyze life expectancy crisis
        if 'Life expectancy at birth (years)' in df.columns:
            life_exp = df['Life expectancy at birth (years)'].dropna()
            low_life_exp = life_exp[life_exp < self.crisis_thresholds['life_expectancy_low']]
            medium_life_exp = life_exp[(life_exp >= self.crisis_thresholds['life_expectancy_low']) & 
                                     (life_exp < self.crisis_thresholds['life_expectancy_medium'])]
            
            analysis['crisis_indicators']['life_expectancy'] = {
                'low_risk_countries': len(low_life_exp),
                'medium_risk_countries': len(medium_life_exp),
                'high_risk_countries': len(life_exp) - len(low_life_exp) - len(medium_life_exp),
                'average_life_expectancy': life_exp.mean(),
                'min_life_expectancy': life_exp.min(),
                'max_life_expectancy': life_exp.max()
            }
        
        # Analyze GDP crisis
        if 'GDP' in df.columns:
            gdp = df['GDP'].dropna()
            low_gdp = gdp[gdp < self.crisis_thresholds['gdp_low']]
            medium_gdp = gdp[(gdp >= self.crisis_thresholds['gdp_low']) & 
                           (gdp < self.crisis_thresholds['gdp_medium'])]
            
            analysis['crisis_indicators']['gdp'] = {
                'low_income_countries': len(low_gdp),
                'medium_income_countries': len(medium_gdp),
                'high_income_countries': len(gdp) - len(low_gdp) - len(medium_gdp),
                'average_gdp': gdp.mean(),
                'min_gdp': gdp.min(),
                'max_gdp': gdp.max()
            }
        
        # Analyze health expenditure crisis
        if 'percentage expenditure' in df.columns:
            health_exp = df['percentage expenditure'].dropna()
            low_health_exp = health_exp[health_exp < self.crisis_thresholds['health_expenditure_low']]
            medium_health_exp = health_exp[(health_exp >= self.crisis_thresholds['health_expenditure_low']) & 
                                         (health_exp < self.crisis_thresholds['health_expenditure_medium'])]
            
            analysis['crisis_indicators']['health_expenditure'] = {
                'low_expenditure_countries': len(low_health_exp),
                'medium_expenditure_countries': len(medium_health_exp),
                'high_expenditure_countries': len(health_exp) - len(low_health_exp) - len(medium_health_exp),
                'average_expenditure': health_exp.mean(),
                'min_expenditure': health_exp.min(),
                'max_expenditure': health_exp.max()
            }
        
        # Generate recommendations
        analysis['recommendations'] = self._generate_crisis_recommendations(analysis)
        
        return analysis
    
    def _generate_crisis_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate crisis prevention recommendations"""
        recommendations = []
        
        if 'life_expectancy' in analysis['crisis_indicators']:
            life_data = analysis['crisis_indicators']['life_expectancy']
            if life_data['low_risk_countries'] > 0:
                recommendations.append(f"Focus on {life_data['low_risk_countries']} countries with life expectancy below 60 years")
                recommendations.append("Implement maternal and child health programs")
                recommendations.append("Strengthen healthcare infrastructure in low-income countries")
        
        if 'gdp' in analysis['crisis_indicators']:
            gdp_data = analysis['crisis_indicators']['gdp']
            if gdp_data['low_income_countries'] > 0:
                recommendations.append(f"Economic support needed for {gdp_data['low_income_countries']} low-income countries")
                recommendations.append("Invest in education and healthcare infrastructure")
        
        if 'health_expenditure' in analysis['crisis_indicators']:
            health_data = analysis['crisis_indicators']['health_expenditure']
            if health_data['low_expenditure_countries'] > 0:
                recommendations.append(f"Increase health expenditure in {health_data['low_expenditure_countries']} countries")
                recommendations.append("Implement universal health coverage programs")
        
        return recommendations
    
    def create_crisis_visualization(self, df: pd.DataFrame, analysis: Dict[str, Any]) -> None:
        """Create comprehensive crisis analysis visualization"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('WHO Health Crisis Analysis Dashboard', fontsize=16, fontweight='bold')
        
        # Life Expectancy Distribution
        if 'Life expectancy at birth (years)' in df.columns:
            life_exp = df['Life expectancy at birth (years)'].dropna()
            axes[0,0].hist(life_exp, bins=20, color='skyblue', alpha=0.7, edgecolor='black')
            axes[0,0].axvline(self.crisis_thresholds['life_expectancy_low'], color='red', linestyle='--', label='Crisis Threshold')
            axes[0,0].set_title('Life Expectancy Distribution')
            axes[0,0].set_xlabel('Life Expectancy (years)')
            axes[0,0].set_ylabel('Number of Countries')
            axes[0,0].legend()
        
        # GDP vs Life Expectancy
        if 'GDP' in df.columns and 'Life expectancy at birth (years)' in df.columns:
            gdp = df['GDP'].dropna()
            life_exp = df['Life expectancy at birth (years)'].dropna()
            common_countries = df.dropna(subset=['GDP', 'Life expectancy at birth (years)'])
            
            axes[0,1].scatter(common_countries['GDP'], common_countries['Life expectancy at birth (years)'], 
                            alpha=0.6, color='green')
            axes[0,1].set_title('GDP vs Life Expectancy')
            axes[0,1].set_xlabel('GDP per Capita')
            axes[0,1].set_ylabel('Life Expectancy (years)')
            axes[0,1].set_xscale('log')
        
        # Health Expenditure Analysis
        if 'percentage expenditure' in df.columns:
            health_exp = df['percentage expenditure'].dropna()
            axes[1,0].boxplot(health_exp, patch_artist=True, boxprops=dict(facecolor='orange', alpha=0.7))
            axes[1,0].set_title('Health Expenditure Distribution')
            axes[1,0].set_ylabel('Health Expenditure (%)')
            axes[1,0].set_xticklabels(['All Countries'])
        
        # Crisis Risk Summary
        risk_summary = []
        if 'life_expectancy' in analysis['crisis_indicators']:
            risk_summary.append(f"Low Life Expectancy: {analysis['crisis_indicators']['life_expectancy']['low_risk_countries']} countries")
        if 'gdp' in analysis['crisis_indicators']:
            risk_summary.append(f"Low GDP: {analysis['crisis_indicators']['gdp']['low_income_countries']} countries")
        if 'health_expenditure' in analysis['crisis_indicators']:
            risk_summary.append(f"Low Health Expenditure: {analysis['crisis_indicators']['health_expenditure']['low_expenditure_countries']} countries")
        
        axes[1,1].text(0.1, 0.8, 'CRISIS RISK SUMMARY', transform=axes[1,1].transAxes, 
                      fontsize=14, fontweight='bold')
        
        for i, risk in enumerate(risk_summary):
            axes[1,1].text(0.1, 0.6 - i*0.15, risk, transform=axes[1,1].transAxes, 
                          fontsize=12, color='red' if 'Low' in risk else 'black')
        
        axes[1,1].set_xlim(0, 1)
        axes[1,1].set_ylim(0, 1)
        axes[1,1].axis('off')
        
        plt.tight_layout()
        plt.show()
    
    def generate_crisis_report(self, analysis: Dict[str, Any]) -> str:
        """Generate comprehensive crisis analysis report"""
        report = []
        report.append("=" * 60)
        report.append("           WHO HEALTH CRISIS ANALYSIS REPORT")
        report.append("=" * 60)
        report.append(f"Total Countries Analyzed: {analysis['total_countries']}")
        report.append("")
        
        # Life Expectancy Analysis
        if 'life_expectancy' in analysis['crisis_indicators']:
            life_data = analysis['crisis_indicators']['life_expectancy']
            report.append("LIFE EXPECTANCY ANALYSIS:")
            report.append(f"  Average Life Expectancy: {life_data['average_life_expectancy']:.1f} years")
            report.append(f"  Countries with Low Life Expectancy (<60 years): {life_data['low_risk_countries']}")
            report.append(f"  Countries with Medium Life Expectancy (60-70 years): {life_data['medium_risk_countries']}")
            report.append(f"  Countries with High Life Expectancy (>70 years): {life_data['high_risk_countries']}")
            report.append("")
        
        # GDP Analysis
        if 'gdp' in analysis['crisis_indicators']:
            gdp_data = analysis['crisis_indicators']['gdp']
            report.append("GDP ANALYSIS:")
            report.append(f"  Average GDP per Capita: ${gdp_data['average_gdp']:,.0f}")
            report.append(f"  Low-Income Countries (<$5,000): {gdp_data['low_income_countries']}")
            report.append(f"  Medium-Income Countries ($5,000-$15,000): {gdp_data['medium_income_countries']}")
            report.append(f"  High-Income Countries (>$15,000): {gdp_data['high_income_countries']}")
            report.append("")
        
        # Health Expenditure Analysis
        if 'health_expenditure' in analysis['crisis_indicators']:
            health_data = analysis['crisis_indicators']['health_expenditure']
            report.append("HEALTH EXPENDITURE ANALYSIS:")
            report.append(f"  Average Health Expenditure: {health_data['average_expenditure']:.1f}% of GDP")
            report.append(f"  Low Expenditure Countries (<3%): {health_data['low_expenditure_countries']}")
            report.append(f"  Medium Expenditure Countries (3-8%): {health_data['medium_expenditure_countries']}")
            report.append(f"  High Expenditure Countries (>8%): {health_data['high_expenditure_countries']}")
            report.append("")
        
        # Recommendations
        if analysis['recommendations']:
            report.append("CRISIS PREVENTION RECOMMENDATIONS:")
            for i, rec in enumerate(analysis['recommendations'], 1):
                report.append(f"  {i}. {rec}")
            report.append("")
        
        report.append("=" * 60)
        report.append("           ANALYSIS COMPLETE")
        report.append("=" * 60)
        
        return "\n".join(report)

def analyze_health_data(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Main function to analyze health data for crisis prediction
    
    Args:
        df: DataFrame with WHO health data
        
    Returns:
        Dictionary with comprehensive health analysis
    """
    analyzer = HealthCrisisAnalyzer()
    
    # Perform crisis analysis
    analysis = analyzer.analyze_health_crisis_risk(df)
    
    # Create visualizations
    analyzer.create_crisis_visualization(df, analysis)
    
    # Generate report
    report = analyzer.generate_crisis_report(analysis)
    print(report)
    
    return analysis
