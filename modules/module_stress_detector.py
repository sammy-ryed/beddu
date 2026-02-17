"""
module_stress_detector.py

Simple keyword-based stress detection system.
Scans user messages for indicators of mental health stress, financial stress, and crisis situations.
"""

import re
from typing import Dict, List


class SimpleStressDetector:
    """
    Lightweight stress detection using keyword matching.
    Categorizes stress into: mental, financial, physical, or crisis.
    """
    
    # Stress keyword database
    STRESS_KEYWORDS = {
        'mental': [
            'anxious', 'anxiety', 'depressed', 'depression', 'panic', 'panicking',
            'overwhelmed', 'stressed', 'stress', 'worried', 'worry', 'scared',
            'afraid', 'hopeless', 'worthless', 'empty', 'numb', 'sad', 'crying',
            'lonely', 'alone', 'isolated', 'nervous', 'restless', 'uneasy',
            'dread', 'fear', 'frightened', 'helpless', 'miserable', 'unhappy',
            'struggling', 'suffering', 'hurting', 'pain', 'anguish'
        ],
        'financial': [
            'debt', 'debts', 'broke', 'bankrupt', 'bankruptcy', 'bills',
            'unemployed', 'unemployment', 'fired', 'laid off', 'layoff',
            'rent', 'eviction', 'evicted', 'foreclosure', 'loan', 'loans',
            'credit card', 'collections', 'paycheck', 'salary', 'income',
            'afford', 'expensive', 'money', 'financial', 'finances', 'budget',
            'poor', 'poverty', 'homeless', 'housing', 'food bank', 'struggling financially'
        ],
        'physical': [
            'exhausted', 'tired', 'fatigue', 'insomnia', 'sleep', 'sleeping',
            'headache', 'migraine', 'pain', 'ache', 'tense', 'tension',
            'chest pain', 'heart racing', 'shaking', 'trembling', 'nausea',
            'sick', 'ill', 'dizzy', 'weak', 'breathe', 'breathing'
        ],
        'crisis': [
            'suicide', 'suicidal', 'kill myself', 'end my life', 'end it all',
            'better off dead', 'want to die', 'ready to die', 'self harm',
            'self-harm', 'hurt myself', 'cut myself', 'overdose',
            'no reason to live', 'no point', 'give up on life', 'ending it'
        ]
    }
    
    def __init__(self):
        """Initialize the stress detector."""
        self.enabled = True
    
    def detect(self, message: str, conversation_history: List = None) -> Dict:
        """
        Analyze a message for stress indicators.
        
        Args:
            message (str): User's message to analyze
            conversation_history (List, optional): Previous messages for context
        
        Returns:
            Dict: {
                'stress_detected': bool,
                'stress_level': int (0-10),
                'is_crisis': bool,
                'category': str ('mental', 'financial', 'both', 'physical'),
                'keywords_found': list,
                'confidence': float (0.0-1.0)
            }
        """
        if not message:
            return self._no_stress_result()
        
        message_lower = message.lower()
        
        # First, check for crisis keywords (highest priority)
        crisis_check = self._check_crisis(message_lower)
        if crisis_check['is_crisis']:
            return crisis_check
        
        # Check for stress keywords in each category
        mental_matches = self._find_keywords(message_lower, self.STRESS_KEYWORDS['mental'])
        financial_matches = self._find_keywords(message_lower, self.STRESS_KEYWORDS['financial'])
        physical_matches = self._find_keywords(message_lower, self.STRESS_KEYWORDS['physical'])
        
        # Calculate stress level based on keyword matches
        total_matches = len(mental_matches) + len(financial_matches) + len(physical_matches)
        
        if total_matches == 0:
            return self._no_stress_result()
        
        # Determine primary category
        category = self._determine_category(mental_matches, financial_matches, physical_matches)
        
        # Calculate stress level (0-10 scale)
        stress_level = min(10, 3 + (total_matches * 2))  # Base 3, +2 per keyword, max 10
        
        # Boost stress level if multiple categories detected
        if len([m for m in [mental_matches, financial_matches, physical_matches] if m]) > 1:
            stress_level = min(10, stress_level + 1)
        
        all_keywords = mental_matches + financial_matches + physical_matches
        
        return {
            'stress_detected': True,
            'stress_level': stress_level,
            'is_crisis': False,
            'category': category,
            'keywords_found': all_keywords,
            'confidence': min(1.0, total_matches * 0.2)  # Confidence increases with matches
        }
    
    def _check_crisis(self, message_lower: str) -> Dict:
        """Check for crisis keywords that require immediate intervention."""
        crisis_keywords = self._find_keywords(message_lower, self.STRESS_KEYWORDS['crisis'])
        
        if crisis_keywords:
            return {
                'stress_detected': True,
                'stress_level': 10,
                'is_crisis': True,
                'category': 'crisis',
                'keywords_found': crisis_keywords,
                'confidence': 1.0
            }
        
        return {'is_crisis': False}
    
    def _find_keywords(self, text: str, keyword_list: List[str]) -> List[str]:
        """Find which keywords from the list are present in the text."""
        found = []
        for keyword in keyword_list:
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, text):
                found.append(keyword)
        return found
    
    def _determine_category(self, mental: List, financial: List, physical: List) -> str:
        """Determine the primary stress category based on matches."""
        mental_count = len(mental)
        financial_count = len(financial)
        physical_count = len(physical)
        
        # If both mental and financial are significant
        if mental_count > 0 and financial_count > 0:
            return 'both'
        
        # Return the category with most matches
        if mental_count >= financial_count and mental_count >= physical_count:
            return 'mental'
        elif financial_count > mental_count and financial_count >= physical_count:
            return 'financial'
        else:
            return 'physical'
    
    def _no_stress_result(self) -> Dict:
        """Return result indicating no stress detected."""
        return {
            'stress_detected': False,
            'stress_level': 0,
            'is_crisis': False,
            'category': None,
            'keywords_found': [],
            'confidence': 0.0
        }


# Quick test function
if __name__ == '__main__':
    detector = SimpleStressDetector()
    
    test_messages = [
        "I'm feeling really anxious about my debt",
        "Can't sleep, feeling hopeless",
        "I want to end it all",
        "Just checking in, how are you?",
        "I'm overwhelmed with bills and worried about rent"
    ]
    
    for msg in test_messages:
        result = detector.detect(msg)
        print(f"\nMessage: {msg}")
        print(f"Result: {result}")
