"""
test_india_resources.py

Test that all India-specific resources are loading correctly.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from modules.module_resources import ResourceManager
from modules.module_financial import FinancialStressDetector
from modules.module_stress_detector import SimpleStressDetector


def test_crisis_resources():
    """Test that Indian crisis resources are loaded."""
    print("\n" + "="*70)
    print(" TESTING INDIAN CRISIS RESOURCES")
    print("="*70)
    
    rm = ResourceManager()
    
    crisis_hotlines = rm.crisis_resources.get('crisis_hotlines', [])
    
    print(f"\n✓ Loaded {len(crisis_hotlines)} crisis hotlines")
    
    # Check for Indian helplines
    hotline_names = [h['name'] for h in crisis_hotlines]
    
    expected_indian = ['KIRAN', 'Vandrevala', 'iCall', 'Sumaitri', 'Aasra']
    found_indian = []
    
    for hotline in crisis_hotlines:
        name = hotline['name']
        print(f"\n  • {name}")
        print(f"    Contact: {hotline['contact']}")
        print(f"    Available: {hotline['available']}")
        if 'languages' in hotline:
            print(f"    Languages: {', '.join(hotline['languages'])}")
        
        for keyword in expected_indian:
            if keyword.lower() in name.lower():
                found_indian.append(keyword)
    
    if len(found_indian) >= 3:
        print(f"\n✅ Found {len(found_indian)} Indian crisis helplines!")
    else:
        print(f"\n⚠️ Only found {len(found_indian)} Indian helplines")
    
    # Check for 112 emergency
    emergency = [h for h in crisis_hotlines if '112' in h['contact']]
    if emergency:
        print("✓ Indian emergency number 112 included")
    
    return len(found_indian) >= 3


def test_mental_health_resources():
    """Test that Indian mental health resources are loaded."""
    print("\n" + "="*70)
    print(" TESTING INDIAN MENTAL HEALTH RESOURCES")
    print("="*70)
    
    rm = ResourceManager()
    
    # Check online therapy
    online = rm.mental_health_resources.get('online_therapy', [])
    print(f"\n✓ Online Therapy Platforms: {len(online)}")
    
    indian_platforms = ['Practo', 'YourDOST', 'BetterLYF', 'Amaha']
    found = []
    
    for platform in online:
        name = platform['name']
        cost = platform.get('cost', 'N/A')
        print(f"  • {name} - {cost}")
        
        for keyword in indian_platforms:
            if keyword.lower() in name.lower():
                found.append(keyword)
                break
    
    # Check helplines
    helplines = rm.mental_health_resources.get('helplines', [])
    print(f"\n✓ Mental Health Helplines: {len(helplines)}")
    
    for helpline in helplines:
        print(f"  • {helpline['name']}: {helpline['contact']}")
    
    # Check for NIMHANS
    nimhans_found = any('NIMHANS' in h['name'] for h in helplines)
    if nimhans_found:
        print("\n✅ NIMHANS helpline found!")
    
    if len(found) >= 2:
        print(f"✅ Found {len(found)} Indian online therapy platforms!")
        return True
    else:
        print(f"⚠️ Only found {len(found)} Indian platforms")
        return False


def test_financial_resources():
    """Test that Indian financial resources are loaded."""
    print("\n" + "="*70)
    print(" TESTING INDIAN FINANCIAL RESOURCES")
    print("="*70)
    
    rm = ResourceManager()
    
    # Check government schemes
    govt_schemes = rm.financial_resources.get('government_schemes', [])
    print(f"\n✓ Government Schemes: {len(govt_schemes)}")
    
    expected_schemes = ['PM Kisan', 'Atal Pension', 'Jan Dhan']
    found_schemes = []
    
    for scheme in govt_schemes:
        name = scheme['name']
        desc = scheme.get('description', '')
        print(f"  • {name}")
        print(f"    {desc[:60]}...")
        
        for keyword in expected_schemes:
            if keyword.lower() in name.lower():
                found_schemes.append(keyword)
    
    # Check employment resources
    employment = rm.financial_resources.get('employment_resources', [])
    print(f"\n✓ Employment Resources: {len(employment)}")
    
    for emp in employment[:3]:
        print(f"  • {emp['name']}: {emp.get('description', '')[:50]}...")
    
    # Check for MGNREGA
    mgnrega_found = any('MGNREGA' in e['name'] for e in employment)
    if mgnrega_found:
        print("\n✅ MGNREGA (employment guarantee) found!")
    
    # Check for PDS
    food = rm.financial_resources.get('food_assistance', [])
    pds_found = any('PDS' in f['name'] or 'Public Distribution' in f['name'] for f in food)
    if pds_found:
        print("✅ PDS (ration system) found!")
    
    if len(found_schemes) >= 2 and (mgnrega_found or pds_found):
        print(f"\n✅ Indian government schemes properly loaded!")
        return True
    else:
        print(f"\n⚠️ Some Indian schemes missing")
        return False


def test_financial_detector_indian_terms():
    """Test that financial detector recognizes Indian terms."""
    print("\n" + "="*70)
    print(" TESTING INDIAN FINANCIAL TERMS DETECTION")
    print("="*70)
    
    detector = FinancialStressDetector()
    
    test_cases = [
        ("Can't pay EMI this month", "EMI"),
        ("Need 5 lakh rupees urgently", "lakh rupees"),
        ("Lost my job, salary not paid for 3 months", "salary not paid"),
        ("Farm debt is crushing me", "farm debt"),
        ("School fees due, cant afford", "school fees"),
    ]
    
    passed = 0
    
    for message, expected_term in test_cases:
        result = detector.detect(message)
        
        if result['has_financial_stress']:
            print(f"\n✓ Detected: \"{message}\"")
            print(f"  → Stress Level: {result['stress_level']}/10")
            print(f"  → Categories: {result['categories']}")
            passed += 1
        else:
            print(f"\n✗ Failed: \"{message}\" (expected to detect {expected_term})")
    
    if passed >= 4:
        print(f"\n✅ Indian financial terms detection working! ({passed}/5 passed)")
        return True
    else:
        print(f"\n⚠️ Only {passed}/5 tests passed")
        return False


def test_character_india_aware():
    """Test that character persona is India-aware."""
    print("\n" + "="*70)
    print(" TESTING INDIA-AWARE CHARACTER PERSONA")
    print("="*70)
    
    import json
    
    with open('character/TARS/TARS.json', 'r', encoding='utf-8') as f:
        char = json.load(f)
    
    persona = char.get('char_persona', '')
    greeting = char.get('char_greeting', '')
    
    print(f"\nCharacter: {char['char_name']}")
    print(f"\nGreeting: {greeting}")
    
    # Check for Indian keywords
    india_keywords = ['India', 'Indian', 'EMI', 'family pressure', 'KIRAN']
    found_keywords = []
    
    combined_text = persona + ' ' + greeting
    
    for keyword in india_keywords:
        if keyword.lower() in combined_text.lower():
            found_keywords.append(keyword)
            print(f"✓ Found keyword: {keyword}")
    
    if len(found_keywords) >= 2:
        print(f"\n✅ Character is India-aware! ({len(found_keywords)} Indian references)")
        return True
    else:
        print(f"\n⚠️ Character may need more Indian context")
        return False


def run_all_tests():
    """Run all India-specific tests."""
    print("\n" + "="*70)
    print(" BEEDU INDIA RESOURCES TEST SUITE")
    print("="*70)
    
    results = []
    
    try:
        results.append(("Crisis Resources", test_crisis_resources()))
        results.append(("Mental Health Resources", test_mental_health_resources()))
        results.append(("Financial Resources", test_financial_resources()))
        results.append(("Indian Financial Terms", test_financial_detector_indian_terms()))
        results.append(("India-Aware Character", test_character_india_aware()))
        
        print("\n" + "="*70)
        print(" TEST SUMMARY")
        print("="*70)
        
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        for test_name, result in results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} - {test_name}")
        
        print(f"\n{passed}/{total} test suites passed")
        
        if passed == total:
            print("\n🎉 All Indian resources successfully loaded!")
            print("Beedu is ready to support users in India! 🇮🇳")
        else:
            print(f"\n⚠️ {total - passed} test(s) failed. Please review.")
        
    except Exception as e:
        print(f"\n❌ Test suite failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    run_all_tests()
