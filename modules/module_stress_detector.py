"""
module_stress_detector.py

Advanced stress detection system with sophisticated pattern recognition.
Features: phrase matching, context negation, intensity modifiers, temporal patterns.
"""

import re
from typing import Dict, List, Tuple
from collections import deque


class SimpleStressDetector:
    """
    Advanced stress detection using:
    - Keyword and phrase matching- Context-aware negation detection
    - Intensity modifiers
    - Pattern combination analysis
    - Conversation history trends
    """
    
    # Stress keyword database (single words)
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
    
    # Multi-word phrases (weighted higher than single keywords)
    STRESS_PHRASES = {
        'mental': [
            ('cant take it anymore', 9),
            ('cant handle this', 8),
            ('falling apart', 8),
            ('breaking down', 8),
            ('cant cope', 8),
            ('losing my mind', 9),
            ('going crazy', 7),
            ('cant breathe', 8),
            ('panic attack', 9),
            ('nervous breakdown', 9),
            ('mental breakdown', 9),
            ('completely overwhelmed', 8),
            ('nothing makes sense', 7),
            ('everything is falling apart', 9)
        ],
        'financial': [
            ('drowning in debt', 9),
            ('cant pay rent', 9),
            ('cant pay bills', 9),
            ('losing my home', 10),
            ('about to be evicted', 10),
            ('facing foreclosure', 10),
            ('living paycheck to paycheck', 7),
            ('maxed out', 8),
            ('debt collectors', 8),
            ('bills piling up', 8),
            ('cant afford', 7),
            ('running out of money', 8)
        ],
        'crisis': [
            ('want to die', 10),
            ('better off dead', 10),
            ('kill myself', 10),
            ('end my life', 10),
            ('end it all', 10),
            ('no reason to live', 10),
            ('ready to die', 10),
            ('planning my death', 10),
            ('suicide plan', 10),
            ('no point in living', 10)
        ]
    }
    
    # Intensity modifiers that increase severity
    INTENSITY_MODIFIERS = {
        'extreme': 2.0,
        'severe': 1.8,
        'really': 1.3,
        'very': 1.3,
        'extremely': 1.8,
        'incredibly': 1.5,
        'unbearably': 1.8,
        'constantly': 1.5,
        'always': 1.4,
        'completely': 1.5,
        'totally': 1.4,
        'absolutely': 1.5,
        'so much': 1.4,
        'too much': 1.5
    }
    
    # Negation words that might indicate user is NOT experiencing the stress
    NEGATION_WORDS = ['not', 'no', 'never', 'neither', 'none', 'nobody', 'nothing', 'nowhere', 'hardly', 'barely', 'scarcely']
    
    # Temporal trend tracking
    def __init__(self, history_size=10):
        """
        Initialize the stress detector.
        
        Args:
            history_size (int): Number of previous conversations to track for trend analysis
        """
        self.enabled = True
        self.conversation_history = deque(maxlen=history_size)
        self.stress_history = deque(maxlen=history_size)
    
    def detect(self, message: str, conversation_history: List = None) -> Dict:
        """
        Analyze a message for stress indicators with sophisticated pattern recognition.
        
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
                'phrases_found': list,
                'confidence': float (0.0-1.0),
                'intensity_multiplier': float,
                'trend': str ('improving', 'worsening', 'stable', 'unknown')
            }
        """
        if not message:
            return self._no_stress_result()
        
        message_lower = message.lower()
        
        # STEP 1: Check for crisis phrases (highest priority, most severe)
        crisis_result = self._check_crisis_patterns(message_lower)
        if crisis_result['is_crisis']:
            self._update_history(crisis_result)
            return crisis_result
        
        # STEP 2: Find multi-word phrases (more reliable than single keywords)
        phrase_matches = self._find_stress_phrases(message_lower)
        
        # STEP 3: Find single keywords
        keyword_matches = self._find_stress_keywords(message_lower)
        
        # STEP 4: Filter out negated stresses ("I'm not depressed" shouldn't trigger)
        filtered_keywords = self._filter_negations(message_lower, keyword_matches)
        filtered_phrases = self._filter_negations(message_lower, {k: v for k, v in phrase_matches.items()})
        
        # STEP 5: Calculate base stress level
        base_stress = self._calculate_base_stress(filtered_keywords, filtered_phrases)
        
        if base_stress == 0:
            result = self._no_stress_result()
            self._update_history(result)
            return result
        
        # STEP 6: Apply intensity modifiers ("really anxious" > "anxious")
        intensity = self._calculate_intensity(message_lower)
        adjusted_stress = min(10, int(base_stress * intensity))
        
        # STEP 7: Determine category
        category = self._determine_category_advanced(filtered_keywords, filtered_phrases)
        
        # STEP 8: Check for combination patterns (multiple symptoms = higher severity)
        combination_boost = self._check_combination_patterns(filtered_keywords, filtered_phrases)
        final_stress = min(10, adjusted_stress + combination_boost)
        
        # STEP 9: Analyze trend over conversation history
        trend = self._analyze_trend()
        
        # Collect all evidence
        all_keywords = []
        for cat_keywords in filtered_keywords.values():
            all_keywords.extend(cat_keywords)
        
        all_phrases = []
        for cat_phrases in filtered_phrases.values():
            all_phrases.extend([phrase for phrase, _ in cat_phrases])
        
        result = {
            'stress_detected': True,
            'stress_level': final_stress,
            'is_crisis': False,
            'category': category,
            'keywords_found': all_keywords[:10],  # Limit output
            'phrases_found': all_phrases[:5],
            'confidence': min(1.0, (len(all_keywords) + len(all_phrases) * 2) * 0.15),
            'intensity_multiplier': intensity,
            'trend': trend
        }
        
        self._update_history(result)
        return result
    
    def _check_crisis_patterns(self, text: str) -> Dict:
        """
        Check for crisis phrases and keywords using sophisticated matching.
        """
        # Check phrases first (more reliable)
        for phrase, severity in self.STRESS_PHRASES.get('crisis', []):
            if phrase in text:
                # Double-check it's not negated
                if not self._is_negated(text, phrase):
                    return {
                        'stress_detected': True,
                        'stress_level': 10,
                        'is_crisis': True,
                        'category': 'crisis',
                        'keywords_found': [],
                        'phrases_found': [phrase],
                        'confidence': 1.0,
                        'intensity_multiplier': 1.0,
                        'trend': 'unknown'
                    }
        
        # Check single keywords
        crisis_keywords = self._find_keywords(text, self.STRESS_KEYWORDS['crisis'])
        if crisis_keywords:
            # Verify not negated
            filtered = [kw for kw in crisis_keywords if not self._is_negated(text, kw)]
            if filtered:
                return {
                    'stress_detected': True,
                    'stress_level': 10,
                    'is_crisis': True,
                    'category': 'crisis',
                    'keywords_found': filtered,
                    'phrases_found': [],
                    'confidence': 1.0,
                    'intensity_multiplier': 1.0,
                    'trend': 'unknown'
                }
        
        return {'is_crisis': False}
    
    def _find_stress_phrases(self, text: str) -> Dict[str, List[Tuple[str, int]]]:
        """Find multi-word stress phrases in text."""
        found_phrases = {'mental': [], 'financial': [], 'physical': [], 'crisis': []}
        
        for category, phrases in self.STRESS_PHRASES.items():
            for phrase, weight in phrases:
                if phrase in text:
                    found_phrases[category].append((phrase, weight))
        
        return found_phrases
    
    def _find_stress_keywords(self, text: str) -> Dict[str, List[str]]:
        """Find stress keywords in each category."""
        found_keywords = {'mental': [], 'financial': [], 'physical': []}
        
        for category, keywords in self.STRESS_KEYWORDS.items():
            if category != 'crisis':  # Crisis handled separately
                found_keywords[category] = self._find_keywords(text, keywords)
        
        return found_keywords
    
    def _find_keywords(self, text: str, keyword_list: List[str]) -> List[str]:
        """Find which keywords from the list are present in the text."""
        found = []
        for keyword in keyword_list:
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, text):
                found.append(keyword)
        return found
    
    def _is_negated(self, text: str, phrase: str) -> bool:
        """
        Check if a phrase is negated in context.
        E.g., "I'm not depressed" should not trigger stress.
        """
        phrase_pos = text.find(phrase)
        if phrase_pos == -1:
            return False
        
        # Check 20 characters before the phrase for negation words
        before_text = text[max(0, phrase_pos - 20):phrase_pos]
        
        for neg_word in self.NEGATION_WORDS:
            if neg_word in before_text.split():
                return True
        
        return False
    
    def _filter_negations(self, text: str, matches: Dict) -> Dict:
        """Filter out negated matches from keywords or phrases."""
        filtered = {}
        
        for category, items in matches.items():
            filtered[category] = []
            for item in items:
                # For tuples (phrase, weight), check first element
                check_item = item[0] if isinstance(item, tuple) else item
                if not self._is_negated(text, check_item):
                    filtered[category].append(item)
        
        return filtered
    
    def _calculate_base_stress(self, keywords: Dict, phrases: Dict) -> int:
        """
        Calculate base stress level from keywords and phrases.
        Phrases weighted more heavily than keywords.
        """
        stress = 0
        
        # Count keywords (each worth 2 points)
        keyword_count = sum(len(kws) for kws in keywords.values())
        stress += keyword_count * 2
        
        # Count phrases (use their weight directly)
        for category_phrases in phrases.values():
            for phrase, weight in category_phrases:
                stress += weight
        
        # Base level of 3 if any stress detected
        if stress > 0:
            stress = max(3, stress)
        
        return min(10, stress)
    
    def _calculate_intensity(self, text: str) -> float:
        """
        Calculate intensity multiplier based on modifier words.
        E.g., "really anxious" gets higher multiplier than "anxious"
        """
        multiplier = 1.0
        
        for modifier, boost in self.INTENSITY_MODIFIERS.items():
            if modifier in text:
                multiplier = max(multiplier, boost)
        
        return multiplier
    
    def _check_combination_patterns(self, keywords: Dict, phrases: Dict) -> int:
        """
        Check for combination patterns that indicate higher severity.
        Multiple symptoms together = worse than single symptom.
        """
        boost = 0
        
        # Count how many categories have matches
        active_categories = sum(1 for cat in keywords.values() if len(cat) > 0)
        active_categories += sum(1 for cat in phrases.values() if len(cat) > 0)
        
        # Multiple categories = combination pattern
        if active_categories >= 3:
            boost += 2
        elif active_categories == 2:
            boost += 1
        
        # Multiple symptoms within same category
        for cat_keywords in keywords.values():
            if len(cat_keywords) >= 4:
                boost += 1
        
        return boost
    
    def _determine_category_advanced(self, keywords: Dict, phrases: Dict) -> str:
        """Determine primary stress category with phrase weighting."""
        scores = {'mental': 0, 'financial': 0, 'physical': 0}
        
        # Keywords worth 1 point each
        for cat, kws in keywords.items():
            if cat in scores:
                scores[cat] += len(kws)
        
        # Phrases worth 3 points each
        for cat, phr in phrases.items():
            if cat in scores:
                scores[cat] += len(phr) * 3
        
        # Check if both mental and financial are significant
        if scores['mental'] >= 2 and scores['financial'] >= 2:
            return 'both'
        
        # Return highest scoring category
        max_cat = max(scores, key=scores.get)
        return max_cat if scores[max_cat] > 0 else 'mental'
    
    def _analyze_trend(self) -> str:
        """
        Analyze stress trend over conversation history.
        Returns: 'improving', 'worsening', 'stable', or 'unknown'
        """
        if len(self.stress_history) < 3:
            return 'unknown'
        
        recent = list(self.stress_history)[-3:]
        levels = [s.get('stress_level', 0) for s in recent]
        
        # Simple trend analysis
        if levels[-1] < levels[0] - 1:
            return 'improving'
        elif levels[-1] > levels[0] + 1:
            return 'worsening'
        else:
            return 'stable'
    
    def _update_history(self, result: Dict):
        """Update conversation history for trend analysis."""
        self.stress_history.append(result)
    
    def _determine_category(self, mental: List, financial: List, physical: List) -> str:
        """Legacy method - kept for compatibility."""
        mental_count = len(mental)
        financial_count = len(financial)
        physical_count = len(physical)
        
        if mental_count > 0 and financial_count > 0:
            return 'both'
        
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
            'phrases_found': [],
            'confidence': 0.0,
            'intensity_multiplier': 1.0,
            'trend': 'stable'
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
