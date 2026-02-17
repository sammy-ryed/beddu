"""
module_resources.py

Resource management system for mental health and financial stress support.
Loads and matches resources based on detected stress categories.
"""

import json
import os
from typing import Dict, List


class ResourceManager:
    """
    Manages mental health, financial, and crisis resources.
    Provides context-appropriate recommendations based on stress analysis.
    """
    
    def __init__(self, resources_path=None):
        """
        Initialize the resource manager.
        
        Args:
            resources_path (str, optional): Path to support_resources.json
        """
        if resources_path is None:
            # Default to resources/ folder relative to this module
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            resources_path = os.path.join(base_dir, 'resources', 'support_resources.json')
        
        self.resources_path = resources_path
        self.resources = self._load_resources()
    
    def _load_resources(self) -> Dict:
        """Load resources from JSON file."""
        try:
            with open(self.resources_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠ Warning: Resources file not found at {self.resources_path}")
            return self._get_default_resources()
        except json.JSONDecodeError as e:
            print(f"⚠ Warning: Error parsing resources file: {e}")
            return self._get_default_resources()
    
    def _get_default_resources(self) -> Dict:
        """Provide minimal default resources if file can't be loaded."""
        return {
            "crisis": [
                {"name": "988 Suicide & Crisis Lifeline", "contact": "Call or Text 988", "available": "24/7"}
            ],
            "mental_health": [
                {"name": "SAMHSA Helpline", "contact": "Call 800-662-4357", "cost": "Free"}
            ],
            "financial_help": [
                {"name": "211 Community Resources", "contact": "Dial 211", "cost": "Free"}
            ],
            "coping_strategies": [
                {"name": "4-7-8 Breathing", "instructions": "Breathe in 4 sec, hold 7 sec, exhale 8 sec"}
            ]
        }
    
    def get_resources(self, stress_data: Dict) -> Dict:
        """
        Get appropriate resources based on stress analysis.
        
        Args:
            stress_data (Dict): Results from stress detector
        
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
                'crisis': self.resources.get('crisis', []),
                'message': "🚨 IMMEDIATE HELP NEEDED: Please reach out to crisis services right now."
            }
        
        category = stress_data.get('category')
        stress_level = stress_data.get('stress_level', 0)
        
        result = {}
        
        # Always include coping strategies for any stress
        if stress_level > 3:
            result['coping_strategies'] = self._get_relevant_coping_strategies(stress_data)
        
        # Add category-specific resources
        if category == 'mental' or category == 'both':
            result['mental_health'] = self.resources.get('mental_health', [])[:3]  # Top 3
        
        if category == 'financial' or category == 'both':
            result['financial_help'] = self.resources.get('financial_help', [])[:3]  # Top 3
        
        # For moderate to high stress, emphasize professional help
        if stress_level >= 7:
            result['message'] = "Your stress level seems quite high. Professional support could really help."
        
        return result
    
    def _get_relevant_coping_strategies(self, stress_data: Dict) -> List[Dict]:
        """Select most relevant coping strategies based on stress type."""
        all_strategies = self.resources.get('coping_strategies', [])
        keywords = stress_data.get('keywords_found', [])
        
        # Match strategies to keywords when possible
        relevant = []
        for strategy in all_strategies:
            best_for = strategy.get('best_for', [])
            # Check if any stress keyword matches strategy's "best for" list
            if any(keyword in best_for for keyword in keywords):
                relevant.append(strategy)
        
        # If no specific matches, return general strategies
        if not relevant and all_strategies:
            # Default to breathing and grounding for anxiety/stress
            relevant = [s for s in all_strategies if 'breathing' in s.get('category', '').lower()][:2]
            if not relevant:
                relevant = all_strategies[:2]  # Just return first 2
        
        return relevant[:2]  # Max 2 strategies to avoid overwhelming user
    
    def get_crisis_response(self) -> str:
        """
        Get immediate crisis resources formatted as text response.
        
        Returns:
            str: Formatted crisis message with hotline information
        """
        crisis_resources = self.resources.get('crisis', [])
        
        message = "🚨 I'm really concerned about what you're sharing. Please reach out for help right now:\n\n"
        
        for resource in crisis_resources:
            message += f"• {resource['name']}: {resource['contact']}"
            if 'available' in resource:
                message += f" ({resource['available']})"
            message += "\n"
        
        message += "\nYou don't have to face this alone. These services are confidential and free. Please call or text now."
        
        return message
    
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
            for r in resources['crisis']:
                output.append(f"• {r['name']}: {r['contact']}")
        
        # Coping strategies
        if 'coping_strategies' in resources:
            output.append("\n💡 IMMEDIATE COPING STRATEGIES:")
            for strategy in resources['coping_strategies']:
                output.append(f"\n• {strategy['name']}")
                if 'instructions' in strategy:
                    output.append(f"  {strategy['instructions']}")
        
        # Mental health resources
        if 'mental_health' in resources:
            output.append("\n🧠 MENTAL HEALTH SUPPORT:")
            for r in resources['mental_health'][:2]:  # Show top 2
                desc = f"{r['name']} ({r.get('cost', 'Varies')})"
                if 'contact' in r:
                    desc += f" - {r['contact']}"
                output.append(f"• {desc}")
        
        # Financial resources
        if 'financial_help' in resources:
            output.append("\n💰 FINANCIAL ASSISTANCE:")
            for r in resources['financial_help'][:2]:  # Show top 2
                desc = f"{r['name']}"
                if 'contact' in r:
                    desc += f" - {r['contact']}"
                output.append(f"• {desc}")
        
        # Message if provided
        if 'message' in resources:
            output.append(f"\n{resources['message']}")
        
        return '\n'.join(output) if output else ""


# Quick test
if __name__ == '__main__':
    rm = ResourceManager()
    
    # Test crisis detection
    crisis_data = {
        'stress_detected': True,
        'is_crisis': True,
        'stress_level': 10,
        'category': 'crisis'
    }
    
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
