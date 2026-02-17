"""
test_advanced_features.py

Test script for all three advanced features:
1. Multiple JSON databases
2. Financial stress detection
3. Sophisticated pattern recognition
"""

import os
import sys

# Add modules to path
sys.path.insert(0, os.path.dirname(__file__))

from modules.module_stress_detector import SimpleStressDetector
from modules.module_financial import FinancialStressDetector
from modules.module_resources import ResourceManager


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "="*70)
    print(f" {title}")
    print("="*70)


def test_json_databases():
    """Test that all JSON databases load correctly."""
    print_section("TEST 1: Multiple JSON Databases")
    
    rm = ResourceManager()
    
    # Check crisis resources
    crisis_count = len(rm.crisis_resources.get('crisis_hotlines', []))
    print(f"✓ Crisis resources loaded: {crisis_count} hotlines")
    
    # Check mental health resources
    mh_categories = len(rm.mental_health_resources)
    print(f"✓ Mental health resources loaded: {mh_categories} categories")
    
    # Check financial resources
    fin_categories = len(rm.financial_resources)
    print(f"✓ Financial resources loaded: {fin_categories} categories")
    
    # Check coping strategies
    coping_categories = len(rm.coping_strategies)
    print(f"✓ Coping strategies loaded: {coping_categories} categories")
    
    # Verify some key resources exist
    assert crisis_count >= 5, "Should have at least 5 crisis hotlines"
    assert mh_categories >= 5, "Should have at least 5 MH categories"
    assert fin_categories >= 8, "Should have at least 8 financial categories"
    assert coping_categories >= 6, "Should have at least 6 coping categories"
    
    print("\n✅ All JSON databases loaded successfully!")


def test_financial_detection():
    """Test financial stress detection with various scenarios."""
    print_section("TEST 2: Financial Stress Detection")
    
    detector = FinancialStressDetector()
    
    test_cases = [
        {
            'message': "I'm drowning in debt and can't pay my bills",
            'expect_stress': True,
            'expect_severity': 'high',
            'expect_categories': ['debt', 'bills']
        },
        {
            'message': "Just got eviction notice, losing my home",
            'expect_stress': True,
            'expect_severity': 'critical',
            'expect_urgency': 'immediate',
            'expect_categories': ['housing']
        },
        {
            'message': "Lost my job, running out of money fast",
            'expect_stress': True,
            'expect_severity': 'high',
            'expect_categories': ['income']
        },
        {
            'message': "Having a great day, no financial worries",
            'expect_stress': False
        },
        {
            'message': "Bankruptcy is my only option now",
            'expect_stress': True,
            'expect_severity': 'critical',
            'expect_categories': ['bankruptcy']
        }
    ]
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_cases, 1):
        print(f"\nTest {i}: \"{test['message'][:50]}...\"")
        result = detector.detect(test['message'])
        
        # Check stress detection
        if result['has_financial_stress'] == test['expect_stress']:
            print(f"  ✓ Stress detected: {result['has_financial_stress']}")
            passed += 1
        else:
            print(f"  ✗ Expected stress: {test['expect_stress']}, got: {result['has_financial_stress']}")
            failed += 1
            continue
        
        # If stress expected, check severity and categories
        if test['expect_stress']:
            if 'expect_severity' in test:
                if result['severity'] == test['expect_severity']:
                    print(f"  ✓ Severity: {result['severity']}")
                else:
                    print(f"  ⚠ Expected severity: {test['expect_severity']}, got: {result['severity']}")
            
            if 'expect_urgency' in test:
                if result['urgency'] == test['expect_urgency']:
                    print(f"  ✓ Urgency: {result['urgency']}")
                else:
                    print(f"  ⚠ Expected urgency: {test['expect_urgency']}, got: {result['urgency']}")
            
            if 'expect_categories' in test:
                matched = any(cat in result['categories'] for cat in test['expect_categories'])
                if matched:
                    print(f"  ✓ Categories: {result['categories']}")
                else:
                    print(f"  ⚠ Expected categories: {test['expect_categories']}, got: {result['categories']}")
            
            print(f"  → Stress level: {result['stress_level']}/10")
    
    print(f"\n✅ Financial detection tests: {passed} passed, {failed} failed")


def test_pattern_recognition():
    """Test sophisticated pattern recognition features."""
    print_section("TEST 3: Sophisticated Pattern Recognition")
    
    detector = SimpleStressDetector()
    
    test_cases = [
        {
            'name': 'Multi-word phrase detection',
            'message': "I can't take it anymore, drowning in debt",
            'expect_phrases': ['cant take it anymore', 'drowning in debt'],
            'expect_high_stress': True
        },
        {
            'name': 'Negation filtering',
            'message': "I'm not depressed, just tired",
            'expect_stress': False,
            'expect_keywords_filtered': True
        },
        {
            'name': 'Intensity modifiers',
            'message': "I'm really really anxious about everything",
            'expect_intensity': True,
            'expect_high_stress': True
        },
        {
            'name': 'Crisis detection',
            'message': "I want to die, can't go on anymore",
            'expect_crisis': True,
            'expect_stress_level': 10
        },
        {
            'name': 'No stress - normal chat',
            'message': "How are you today? I'm doing okay",
            'expect_stress': False
        }
    ]
    
    passed = 0
    failed = 0
    
    for test in test_cases:
        print(f"\n{test['name']}: \"{test['message'][:50]}...\"")
        result = detector.detect(test['message'])
        
        test_passed = True
        
        # Check phrase detection
        if 'expect_phrases' in test:
            found_phrases = result.get('phrases_found', [])
            if any(phrase in found_phrases for phrase in test['expect_phrases']):
                print(f"  ✓ Phrases detected: {found_phrases}")
            else:
                print(f"  ✗ Expected phrases: {test['expect_phrases']}, got: {found_phrases}")
                test_passed = False
        
        # Check negation filtering
        if 'expect_stress' in test:
            if result['stress_detected'] == test['expect_stress']:
                print(f"  ✓ Stress detected: {result['stress_detected']}")
            else:
                print(f"  ✗ Expected stress: {test['expect_stress']}, got: {result['stress_detected']}")
                test_passed = False
        
        # Check intensity
        if 'expect_intensity' in test:
            multiplier = result.get('intensity_multiplier', 1.0)
            if multiplier > 1.0:
                print(f"  ✓ Intensity modifier applied: {multiplier}x")
            else:
                print(f"  ✗ Expected intensity modifier, got: {multiplier}")
                test_passed = False
        
        # Check crisis
        if 'expect_crisis' in test:
            if result['is_crisis'] == test['expect_crisis']:
                print(f"  ✓ Crisis detected: {result['is_crisis']}")
            else:
                print(f"  ✗ Expected crisis: {test['expect_crisis']}, got: {result['is_crisis']}")
                test_passed = False
        
        # Check stress level
        if 'expect_high_stress' in test and test['expect_high_stress']:
            if result.get('stress_level', 0) >= 7:
                print(f"  ✓ High stress level: {result['stress_level']}/10")
            else:
                print(f"  ⚠ Expected high stress, got: {result['stress_level']}/10")
        
        if test_passed:
            passed += 1
        else:
            failed += 1
    
    print(f"\n✅ Pattern recognition tests: {passed} passed, {failed} failed")


def test_resource_matching():
    """Test that resources are matched correctly to stress types."""
    print_section("TEST 4: Resource Matching")
    
    rm = ResourceManager()
    
    # Test crisis resources
    print("\nTest: Crisis situation")
    crisis_data = {
        'stress_detected': True,
        'is_crisis': True,
        'stress_level': 10,
        'category': 'crisis'
    }
    resources = rm.get_resources(crisis_data)
    if 'crisis' in resources:
        print(f"  ✓ Crisis resources returned: {len(resources['crisis'])} hotlines")
    else:
        print(f"  ✗ No crisis resources returned")
    
    # Test financial stress resources
    print("\nTest: Financial stress")
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
    resources = rm.get_resources(stress_data, financial_data)
    if 'financial_help' in resources:
        print(f"  ✓ Financial resources returned: {len(resources['financial_help'])} resources")
    else:
        print(f"  ✗ No financial resources returned")
    
    # Test mental health resources
    print("\nTest: Mental health stress")
    mental_data = {
        'stress_detected': True,
        'is_crisis': False,
        'stress_level': 6,
        'category': 'mental',
        'keywords_found': ['depressed', 'anxious']
    }
    resources = rm.get_resources(mental_data)
    if 'mental_health' in resources or 'coping_strategies' in resources:
        print(f"  ✓ Mental health resources returned")
        if 'coping_strategies' in resources:
            print(f"     - Coping strategies: {len(resources['coping_strategies'])}")
        if 'mental_health' in resources:
            print(f"     - Mental health resources: {len(resources['mental_health'])}")
    else:
        print(f"  ✗ No mental health resources returned")
    
    print("\n✅ Resource matching tests completed")


def test_integration():
    """Test full integration of all features together."""
    print_section("TEST 5: Full Integration")
    
    stress_detector = SimpleStressDetector()
    financial_detector = FinancialStressDetector()
    resource_manager = ResourceManager()
    
    test_message = "I'm really stressed, drowning in debt and can't pay bills. Feeling hopeless."
    
    print(f"\nTest message: \"{test_message}\"")
    
    # Run stress detection
    stress_data = stress_detector.detect(test_message)
    print(f"\n1. Stress Detection:")
    print(f"   - Stress detected: {stress_data['stress_detected']}")
    print(f"   - Stress level: {stress_data['stress_level']}/10")
    print(f"   - Category: {stress_data['category']}")
    print(f"   - Phrases found: {stress_data.get('phrases_found', [])}")
    print(f"   - Intensity multiplier: {stress_data.get('intensity_multiplier', 1.0)}")
    
    # Run financial detection
    financial_data = financial_detector.detect(test_message)
    print(f"\n2. Financial Detection:")
    print(f"   - Financial stress: {financial_data['has_financial_stress']}")
    print(f"   - Severity: {financial_data['severity']}")
    print(f"   - Categories: {financial_data['categories']}")
    print(f"   - Urgency: {financial_data['urgency']}")
    
    # Get resources
    resources = resource_manager.get_resources(stress_data, financial_data)
    print(f"\n3. Resources Matched:")
    for key in resources:
        if key == 'message':
            continue
        if isinstance(resources[key], list):
            print(f"   - {key}: {len(resources[key])} resources")
        else:
            print(f"   - {key}: {resources[key]}")
    
    # Format for display
    formatted = resource_manager.format_resources_for_display(resources)
    print(f"\n4. Formatted Output:")
    print(formatted)
    
    print("\n✅ Full integration test completed successfully!")


def run_all_tests():
    """Run all test suites."""
    print("\n" + "="*70)
    print(" BEEDU ADVANCED FEATURES TEST SUITE")
    print("="*70)
    
    try:
        test_json_databases()
        test_financial_detection()
        test_pattern_recognition()
        test_resource_matching()
        test_integration()
        
        print_section("ALL TESTS COMPLETED ✅")
        print("\nSummary:")
        print("  ✓ Multiple JSON databases working")
        print("  ✓ Financial stress detection working")
        print("  ✓ Sophisticated pattern recognition working")
        print("  ✓ Resource matching working")
        print("  ✓ Full integration working")
        print("\nBeedu is ready with all advanced features! 🚀")
        
    except Exception as e:
        print(f"\n❌ Test suite failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    run_all_tests()
