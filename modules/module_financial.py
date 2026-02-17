"""
module_financial.py

Advanced Financial Stress Detection and Resource Management Module.
Provides specialized analysis for financial distress patterns, debt situations,
and employment concerns with targeted resource recommendations.
"""

import re
from typing import Dict, List, Tuple
import json
import os


class FinancialStressDetector:
    """
    Specialized detector for financial stress patterns.
    More sophisticated than general stress detection.
    """
    
    # Financial stress categories with severity weights
    DEBT_KEYWORDS = {
        # Severity 10 - Critical
        'bankruptcy': 10, 'foreclosure': 10, 'eviction': 10, 'repossession': 10,
        'garnishment': 10, 'collections lawsuit': 10,
        
        # Severity 8-9 - Severe
        'defaulting': 9, 'cant pay rent': 9, 'cant pay mortgage': 9,
        'losing home': 9, 'losing house': 9, 'losing apartment': 9,
        'debt collectors': 8, 'collection agency': 8, 'skip payments': 8,
        'maxed out': 8, 'drowning in debt': 9,
        
        # Severity 6-7 - High
        'overwhelming debt': 7, 'behind on payments': 7, 'late payments': 6,
        'collection calls': 7, 'creditors calling': 7, 'debt spiral': 8,
        'payday loan': 7, 'title loan': 7,
        
        # Severity 4-5 - Moderate
        'credit card debt': 5, 'student loans': 4, 'medical debt': 6,
        'car payment': 4, 'payment plan': 4, 'minimum payment': 5,
        
        # India-specific debt terms
        'emi': 5, 'emis': 5, 'loan emi': 6, 'home loan': 5, 'personal loan': 5,
        'gold loan': 6, 'education loan': 4, 'vehicle loan': 5,
        'money lender': 8, 'private lender': 8, 'lakh rupees': 6, 'lakhs debt': 7,
        'crore debt': 9, 'recovery agent': 8, 'loan recovery': 8
    }
    
    INCOME_KEYWORDS = {
        # Severity 10 - Critical
        'no income': 10, 'zero income': 10, 'lost job': 9, 'fired': 8,
        'laid off': 9, 'terminated': 8, 'unemployment running out': 10,
        
        # Severity 7-9 - Severe
        'cant find work': 8, 'no job': 9, 'unemployed': 8,
        'hours cut': 7, 'reduced hours': 7, 'pay cut': 8,
        
        # Severity 4-6 - Moderate
        'underpaid': 5, 'minimum wage': 4, 'barely making ends meet': 7,
        'living paycheck to paycheck': 6, 'tight budget': 5,
        
        # India-specific income terms
        'salary delay': 7, 'salary not paid': 9, 'no salary': 9,
        'pending salary': 7, 'gratuity': 5, 'pf withdrawal': 6,
        'no work': 8, 'business loss': 8, 'shop closed': 8,
        'crop failure': 9, 'harvest loss': 8, 'farm debt': 8
    }
    
    BILLS_KEYWORDS = {
        # Severity 9-10 - Critical
        'cant afford food': 10, 'cant afford medicine': 10,
        'utility shutoff': 9, 'water shutoff': 9, 'electricity shutoff': 9,
        'cant afford heat': 9, 'choosing between': 10,
        
        # Severity 7-8 - Severe
        'bills piling up': 8, 'overdue bills': 7, 'past due': 7,
        'disconnection notice': 8, 'cant pay bills': 8,
        
        # Severity 5-6 - Moderate
        'tight month': 5, 'struggling with bills': 6, 'expensive bills': 5,
        'unexpected expense': 6, 'emergency expense': 7,
        
        # India-specific bill terms
        'electricity bill': 5, 'phone bill': 4, 'internet bill': 4,
        'school fees': 6, 'tuition fees': 6, 'medical bills': 7,
        'hospital bills': 8, 'treatment cost': 7, 'surgery cost': 8,
        'rent due': 7, 'maintenance charges': 5, 'society dues': 5,
        'no ration': 8, 'ration card': 6
    }
    
    BANKRUPTCY_INDICATORS = {
        'bankruptcy': 10, 'chapter 7': 10, 'chapter 13': 10,
        'filing bankruptcy': 10, 'declaring bankruptcy': 10,
        'bankruptcy attorney': 9, 'bankruptcy lawyer': 9
    }
    
    HOUSING_CRISIS = {
        'eviction': 10, 'eviction notice': 10, '30 day notice': 9,
        'foreclosure': 10, 'losing home': 10, 'losing house': 10,
        'homeless': 10, 'homelessness': 10, 'living in car': 10,
        'couch surfing': 8, 'hotel living': 7
    }
    
    # Context modifiers
    URGENCY_WORDS = ['today', 'tomorrow', 'this week', 'immediate', 'urgent', 'asap', 'emergency']
    DESPERATION_WORDS = ['desperate', 'hopeless', 'helpless', 'dont know what to do', 'nowhere to turn', 'last resort']
    
    def __init__(self):
        """Initialize the financial stress detector."""
        # Combine all keywords for quick checking
        self.all_keywords = {
            **self.DEBT_KEYWORDS,
            **self.INCOME_KEYWORDS,
            **self.BILLS_KEYWORDS,
            **self.BANKRUPTCY_INDICATORS,
            **self.HOUSING_CRISIS
        }
    
    def detect(self, text: str) -> Dict:
        """
        Analyze text for financial stress indicators.
        
        Args:
            text (str): User's message
        
        Returns:
            Dict: {
                'has_financial_stress': bool,
                'stress_level': int (0-10),
                'categories': list of str,
                'severity': str (critical/severe/high/moderate/low),
                'urgency': str (immediate/urgent/soon/none),
                'specific_issues': list of detected issues,
                'recommended_resources': list of resource types needed
            }
        """
        if not text:
            return self._empty_result()
        
        text_lower = text.lower()
        
        # Find all matches
        detected_issues = []
        max_severity = 0
        categories = set()
        
        # Check each keyword category
        for keyword, severity in self.all_keywords.items():
            if keyword in text_lower:
                detected_issues.append({
                    'keyword': keyword,
                    'severity': severity,
                    'category': self._categorize_keyword(keyword)
                })
                max_severity = max(max_severity, severity)
                categories.add(self._categorize_keyword(keyword))
        
        # Check for urgency indicators
        urgency = self._assess_urgency(text_lower)
        
        # Check for desperation indicators
        desperation_level = self._assess_desperation(text_lower)
        
        # Adjust severity based on context
        if urgency == 'immediate':
            max_severity = min(10, max_severity + 2)
        if desperation_level == 'high':
            max_severity = min(10, max_severity + 1)
        
        # Determine if financial stress is present
        has_financial_stress = len(detected_issues) > 0
        
        # Get recommended resources
        recommended_resources = self._recommend_resources(categories, max_severity, detected_issues)
        
        return {
            'has_financial_stress': has_financial_stress,
            'stress_level': max_severity,
            'categories': list(categories),
            'severity': self._severity_label(max_severity),
            'urgency': urgency,
            'specific_issues': detected_issues,
            'recommended_resources': recommended_resources,
            'desperation_level': desperation_level
        }
    
    def _categorize_keyword(self, keyword: str) -> str:
        """Determine which category a keyword belongs to."""
        if keyword in self.DEBT_KEYWORDS:
            return 'debt'
        elif keyword in self.INCOME_KEYWORDS:
            return 'income_loss'
        elif keyword in self.BILLS_KEYWORDS:
            return 'bills'
        elif keyword in self.BANKRUPTCY_INDICATORS:
            return 'bankruptcy'
        elif keyword in self.HOUSING_CRISIS:
            return 'housing_crisis'
        return 'general_financial'
    
    def _assess_urgency(self, text: str) -> str:
        """Assess urgency from text."""
        for word in self.URGENCY_WORDS:
            if word in text:
                return 'immediate'
        
        # Check for time-based indicators
        if any(phrase in text for phrase in ['this month', 'next week', 'few days']):
            return 'urgent'
        if any(phrase in text for phrase in ['soon', 'coming up', 'next month']):
            return 'soon'
        
        return 'none'
    
    def _assess_desperation(self, text: str) -> str:
        """Assess desperation level."""
        desperation_count = sum(1 for word in self.DESPERATION_WORDS if word in text)
        if desperation_count >= 2:
            return 'high'
        elif desperation_count == 1:
            return 'moderate'
        return 'low'
    
    def _severity_label(self, level: int) -> str:
        """Convert numeric severity to label."""
        if level >= 9:
            return 'critical'
        elif level >= 7:
            return 'severe'
        elif level >= 5:
            return 'high'
        elif level >= 3:
            return 'moderate'
        elif level > 0:
            return 'low'
        return 'none'
    
    def _recommend_resources(self, categories: set, severity: int, issues: List[Dict]) -> List[str]:
        """Recommend specific resource types based on detected issues."""
        resources = []
        
        # Critical situations always get emergency assistance
        if severity >= 9:
            resources.append('emergency_assistance')
        
        # Category-specific resources
        if 'housing_crisis' in categories:
            resources.extend(['emergency_assistance', 'housing_assistance'])
        
        if 'bankruptcy' in categories:
            resources.append('bankruptcy_resources')
        
        if 'debt' in categories:
            if severity >= 7:
                resources.extend(['credit_counseling', 'debt_management'])
            else:
                resources.append('credit_counseling')
        
        if 'income_loss' in categories:
            resources.extend(['employment_resources', 'emergency_assistance'])
        
        if 'bills' in categories:
            if any('utility' in str(issue) or 'food' in str(issue) for issue in issues):
                resources.extend(['utility_assistance', 'food_assistance'])
            resources.append('emergency_assistance')
        
        # Always include education for less severe cases
        if severity < 7:
            resources.append('financial_education')
        
        # Remove duplicates while preserving order
        seen = set()
        return [r for r in resources if not (r in seen or seen.add(r))]
    
    def _empty_result(self) -> Dict:
        """Return empty result for no financial stress."""
        return {
            'has_financial_stress': False,
            'stress_level': 0,
            'categories': [],
            'severity': 'none',
            'urgency': 'none',
            'specific_issues': [],
            'recommended_resources': [],
            'desperation_level': 'low'
        }


class FinancialResourceManager:
    """
    Manages financial resources from financial_resources.json.
    Provides smart matching based on detected financial stress.
    """
    
    def __init__(self, resources_path=None):
        """Initialize with path to financial resources JSON."""
        if resources_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            resources_path = os.path.join(base_dir, 'resources', 'financial_resources.json')
        
        self.resources_path = resources_path
        self.resources = self._load_resources()
    
    def _load_resources(self) -> Dict:
        """Load financial resources from JSON."""
        try:
            with open(self.resources_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠ Warning: Financial resources file not found at {self.resources_path}")
            return {}
        except json.JSONDecodeError as e:
            print(f"⚠ Warning: Error parsing financial resources: {e}")
            return {}
    
    def get_resources(self, financial_data: Dict) -> Dict:
        """
        Get appropriate financial resources based on detection results.
        
        Args:
            financial_data: Results from FinancialStressDetector
        
        Returns:
            Dict of categorized resources
        """
        if not financial_data.get('has_financial_stress'):
            return {}
        
        result = {}
        recommended = financial_data.get('recommended_resources', [])
        severity = financial_data.get('severity', 'low')
        
        # Get resources for each recommended category
        for resource_type in recommended:
            if resource_type in self.resources:
                # Limit resources based on severity
                if severity in ['critical', 'severe']:
                    result[resource_type] = self.resources[resource_type][:2]  # Top 2
                else:
                    result[resource_type] = self.resources[resource_type][:3]  # Top 3
        
        return result
    
    def format_resources(self, resources: Dict, financial_data: Dict) -> str:
        """
        Format financial resources for display.
        
        Args:
            resources: Resources from get_resources()
            financial_data: Detection results
        
        Returns:
            Formatted string
        """
        if not resources:
            return ""
        
        severity = financial_data.get('severity', 'low')
        urgency = financial_data.get('urgency', 'none')
        
        output = []
        
        # Add severity/urgency header
        if urgency == 'immediate' or severity == 'critical':
            output.append("\n🚨 URGENT FINANCIAL HELP:")
        else:
            output.append("\n💰 FINANCIAL RESOURCES:")
        
        # Format each resource category
        for category, items in resources.items():
            category_name = category.replace('_', ' ').title()
            output.append(f"\n**{category_name}:**")
            
            for resource in items:
                name = resource.get('name', 'Unknown')
                contact = resource.get('contact', '')
                cost = resource.get('cost', '')
                website = resource.get('website', '')
                
                output.append(f"• {name}")
                if contact:
                    output.append(f"  Contact: {contact}")
                if cost:
                    output.append(f"  Cost: {cost}")
                if website and len(output) < 40:  # Don't overdo it
                    output.append(f"  {website}")
        
        return "\n".join(output)
