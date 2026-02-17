"""
module_resources.py

Advanced resource management system with multiple specialized databases.
Loads from: crisis_resources.json, mental_health_resources.json, 
financial_resources.json, coping_strategies.json
"""

import json
import os
from typing import Dict, List


class ResourceManager:
    """
    Manages multiple resource databases:
    - Crisis hotlines and emergency resources
    - Mental health therapy and support groups
    - Financial assistance and counseling
    - Coping strategies and techniques
    """
    
    def __init__(self, resources_dir=None):
        """
        Initialize the resource manager with multiple databases.
        
        Args:
            resources_dir (str, optional): Path to resources folder
        """
        if resources_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            resources_dir = os.path.join(base_dir, 'resources')
        
        self.resources_dir = resources_dir
        
        # Load all resource databases
        self.crisis_resources = self._load_json('crisis_resources.json')
        self.mental_health_resources = self._load_json('mental_health_resources.json')
        self.financial_resources = self._load_json('financial_resources.json')
        self.coping_strategies = self._load_json('coping_strategies.json')
        
        # Legacy support - combine into single dict like old version
        self.resources = {
            'crisis': self.crisis_resources.get('crisis_hotlines', []),
            'mental_health': self._flatten_mental_health(),
            'financial_help': self._flatten_financial(),
            'coping_strategies': self._flatten_coping()
        }
        
        print(f"✓ Loaded {len(self.crisis_resources.get('crisis_hotlines', []))} crisis resources")
        print(f"✓ Loaded {len(self.mental_health_resources)} mental health categories")
        print(f"✓ Loaded {len(self.financial_resources)} financial resource categories")
        print(f"✓ Loaded {len(self.coping_strategies)} coping technique categories")
    
    def _load_json(self, filename: str) -> Dict:
        """Load a JSON resource file."""
        filepath = os.path.join(self.resources_dir, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠ Warning: {filename} not found, using empty dict")
            return {}
        except json.JSONDecodeError as e:
            print(f"⚠ Warning: Error parsing {filename}: {e}")
            return {}
    
    def _flatten_mental_health(self) -> List[Dict]:
        """Flatten mental health resources for legacy compatibility."""
        resources = []
        for category in ['online_therapy', 'affordable_therapy', 'support_groups']:
            resources.extend(self.mental_health_resources.get(category, []))
        return resources[:10]  # Return top 10
    
    def _flatten_financial(self) -> List[Dict]:
        """Flatten financial resources for legacy compatibility."""
        resources = []
        for category in ['emergency_assistance', 'credit_counseling', 'employment_resources']:
            resources.extend(self.financial_resources.get(category, []))
        return resources[:10]
    
    def _flatten_coping(self) -> List[Dict]:
        """Flatten coping strategies for legacy compatibility."""
        strategies = []
        for category in ['breathing_techniques', 'grounding_techniques', 'quick_techniques']:
            strategies.extend(self.coping_strategies.get(category, []))
        return strategies[:15]
    
    def get_resources(self, stress_data: Dict, financial_data: Dict = None) -> Dict:
        """
        Get appropriate resources based on stress and financial analysis.
        
        Args:
            stress_data (Dict): Results from stress detector
            financial_data (Dict): Results from financial stress detector
        
        Returns:
            Dict: {
                'crisis': [...] if crisis detected,
                'mental_health': [...] if mental stress,
                'financial_help': [...] if financial stress,
                'coping_strategies': [...] immediate techniques
            }
        """
        if not stress_data or not stress_data.get('stress_detected'):
            return {}
        
        # Crisis takes absolute priority
        if stress_data.get('is_crisis'):
            return {
                'crisis': self.crisis_resources.get('crisis_hotlines', [])[:3],
                'crisis_online': self.crisis_resources.get('crisis_online_resources', [])[:2],
                'message': "🚨 IMMEDIATE HELP: Please reach out to crisis services right now."
            }
        
        result = {}
        stress_level = stress_data.get('stress_level', 0)
        category = stress_data.get('category')
        
        # Financial stress gets specialized resources
        if financial_data and financial_data.get('has_financial_stress'):
            severity = financial_data.get('severity', 'moderate')
            urgency = financial_data.get('urgency', 'none')
            categories = financial_data.get('categories', [])
            
            # Get targeted financial resources
            financial_help = []
            if urgency in ['immediate', 'urgent']:
                financial_help.extend(self.financial_resources.get('emergency_assistance', [])[:2])
            if 'debt' in categories:
                financial_help.extend(self.financial_resources.get('credit_counseling', [])[:1])
                financial_help.extend(self.financial_resources.get('debt_management', [])[:1])
            if 'housing' in categories:
                financial_help.extend(self.financial_resources.get('housing_assistance', [])[:2])
            if 'income' in categories or 'job_loss' in categories:
                financial_help.extend(self.financial_resources.get('employment_resources', [])[:2])
            
            # Add general financial help if nothing specific matched
            if not financial_help:
                financial_help.extend(self.financial_resources.get('emergency_assistance', [])[:2])
                financial_help.extend(self.financial_resources.get('financial_education', [])[:1])
            
            result['financial_help'] = financial_help[:4]  # Max 4 resources
        
        # Mental health resources for non-financial stress
        elif category in ['mental', 'both']:
            mental_help = []
            keywords = stress_data.get('keywords_found', [])
            
            # Severe stress gets therapy options
            if stress_level >= 6:
                mental_help.extend(self.mental_health_resources.get('affordable_therapy', [])[:2])
            
            # Depression/anxiety gets support groups
            if any(word in keywords for word in ['depress', 'anxious', 'lonely']):
                mental_help.extend(self.mental_health_resources.get('support_groups', [])[:2])
            
            # General mental health
            if not mental_help:
                mental_help.extend(self.mental_health_resources.get('helplines', [])[:2])
            
            result['mental_health'] = mental_help[:3]
        
        # Add coping strategies for moderate+ stress
        if stress_level >= 4:
            result['coping_strategies'] = self._get_relevant_coping_strategies(stress_data)
        
        # Add severity message
        if stress_level >= 7:
            result['message'] = "Your stress level seems high. Professional support could really help."
        
        return result
    
    def _get_relevant_coping_strategies(self, stress_data: Dict) -> List[Dict]:
        """Select most relevant coping strategies based on stress type."""
        keywords = stress_data.get('keywords_found', [])
        phrases = stress_data.get('phrases_found', [])
        
        selected = []
        
        # Anxiety/panic gets breathing + grounding
        if any(word in keywords for word in ['anxious', 'panic', 'overwhelm']):
            selected.extend(self.coping_strategies.get('breathing_techniques', [])[:1])
            selected.extend(self.coping_strategies.get('grounding_techniques', [])[:1])
        # Depression gets physical + cognitive
        elif any(word in keywords for word in ['depress', 'sad', 'hopeless']):
            selected.extend(self.coping_strategies.get('physical_techniques', [])[:1])
            selected.extend(self.coping_strategies.get('cognitive_techniques', [])[:1])
        # Sleep issues
        elif any(word in keywords for word in ['sleep', 'tired', 'exhaust']):
            selected.extend(self.coping_strategies.get('sleep_techniques', [])[:2])
        # General stress - quick techniques
        else:
            selected.extend(self.coping_strategies.get('quick_techniques', [])[:2])
        
        # If nothing matched, default to breathing
        if not selected:
            selected.extend(self.coping_strategies.get('breathing_techniques', [])[:2])
        
        return selected[:2]  # Max 2 to avoid overwhelming
    
    def get_crisis_response(self) -> str:
        """
        Get immediate crisis resources formatted as text response.
        
        Returns:
            str: Formatted crisis message with hotline information
        """
        crisis_hotlines = self.crisis_resources.get('crisis_hotlines', [])
        
        message = "🚨 I'm really concerned. Please reach out right now:\n\n"
        
        for resource in crisis_hotlines[:3]:  # Top 3 most critical
            message += f"• {resource['name']}: {resource['contact']}"
            if resource.get('available') == '24/7':
                message += " (24/7)"
            message += "\n"
        
        message += "\nYou don't have to face this alone. These are confidential and free."
        
        return message
    
    def get_crisis_header(self) -> str:
        """
        Get brief crisis header to prepend to AI response.
        
        Returns:
            str: Crisis hotline information (concise)
        """
        crisis_hotlines = self.crisis_resources.get('crisis_hotlines', [])
        message = "🚨 CRISIS RESOURCES:\n"
        
        # Show 988 and Crisis Text Line (most accessible)
        for resource in crisis_hotlines[:2]:
            message += f"• {resource['name']}: {resource['contact']}\n"
        
        return message.rstrip()
    
    def format_resources_for_display(self, resources: Dict) -> str:
        """
        Format resources as readable text for user.
        
        Args:
            resources (Dict): Resources from get_resources()
        
        Returns:
            str: Human-readable formatted text
        """
        if not resources:
            return ""
        
        output = []
        
        # Crisis resources
        if 'crisis' in resources:
            output.append("\n🚨 CRISIS RESOURCES:")
            for r in resources['crisis'][:2]:
                output.append(f"• {r['name']}: {r['contact']}")
        
        # Coping strategies (most immediate) - make them collapsible
        if 'coping_strategies' in resources:
            for i, strategy in enumerate(resources['coping_strategies']):
                # Use special markers for JavaScript to detect and make collapsible
                output.append(f"\n[COPING_TIP_START:{i}]")
                output.append(f"💡 Want a tip to help with stress? (click to reveal)")
                output.append(f"[COPING_TIP_CONTENT:{i}]")
                output.append(f"\n• {strategy['name']}")
                if 'instructions' in strategy:
                    output.append(f"  {strategy['instructions']}")
                output.append(f"[COPING_TIP_END:{i}]")
        
        # Mental health resources
        if 'mental_health' in resources:
            output.append("\n🧠 GET SUPPORT:")
            for r in resources['mental_health'][:2]:
                desc = f"{r['name']}"
                if 'cost' in r:
                    desc += f" ({r['cost']})"
                if 'contact' in r:
                    desc += f" - {r['contact']}"
                output.append(f"• {desc}")
        
        # Financial resources
        if 'financial_help' in resources:
            output.append("\n💰 FINANCIAL HELP:")
            for r in resources['financial_help'][:3]:
                desc = f"{r['name']}"
                if 'contact' in r:
                    desc += f": {r['contact']}"
                elif 'website' in r:
                    desc += f": {r['website']}"
                output.append(f"• {desc}")
        
        # Message if provided
        if 'message' in resources:
            output.append(f"\n💬 {resources['message']}")
        
        return '\n'.join(output) if output else ""


# Quick test
if __name__ == '__main__':
    rm = ResourceManager()
    
    # Test crisis detection
    print("\n=== CRISIS TEST ===")
    crisis_data = {
        'stress_detected': True,
        'is_crisis': True,
        'stress_level': 10,
        'category': 'crisis'
    }
    crisis_resources = rm.get_resources(crisis_data)
    print(rm.format_resources_for_display(crisis_resources))
    
    # Test financial stress
    print("\n=== FINANCIAL STRESS TEST ===")
    stress_data = {
        'stress_detected': True,
        'is_crisis': False,
        'stress_level': 7,
        'category': 'financial',
        'keywords_found': ['debt', 'bills']
    }
    financial_data = {
        'has_financial_stress': True,
        'stress_level': 8,
        'severity': 'high',
        'urgency': 'urgent',
        'categories': ['debt', 'bills']
    }
    financial_resources = rm.get_resources(stress_data, financial_data)
    print(rm.format_resources_for_display(financial_resources))
    
    print("Crisis Response:")
    print(rm.get_crisis_response())
    
    # Test regular stress
    stress_data = {
        'stress_detected': True,
        'is_crisis': False,
        'stress_level': 7,
        'category': 'both',
        'keywords_found': ['anxious', 'debt']
    }
    
    print("\n\nRegular Stress Resources:")
    resources = rm.get_resources(stress_data)
    print(rm.format_resources_for_display(resources))
