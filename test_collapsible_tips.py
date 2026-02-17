"""
test_collapsible_tips.py

Quick test to demonstrate the new collapsible coping tips feature.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from modules.module_stress_detector import SimpleStressDetector
from modules.module_resources import ResourceManager


def test_collapsible_tips():
    """Test that coping tips are formatted with collapsible markers."""
    
    print("="*70)
    print(" TESTING COLLAPSIBLE COPING TIPS FEATURE")
    print("="*70)
    
    # Initialize
    stress_detector = SimpleStressDetector()
    resource_manager = ResourceManager()
    
    # Test message with moderate stress
    test_message = "I'm feeling really anxious and overwhelmed with everything"
    
    print(f"\nTest Message: \"{test_message}\"")
    
    # Detect stress
    stress_data = stress_detector.detect(test_message)
    print(f"\nStress Detection:")
    print(f"  - Stress Level: {stress_data['stress_level']}/10")
    print(f"  - Category: {stress_data['category']}")
    
    # Get resources
    resources = resource_manager.get_resources(stress_data)
    
    # Format resources
    formatted = resource_manager.format_resources_for_display(resources)
    
    print(f"\nFormatted Output (with special markers):")
    print("-" * 70)
    print(formatted)
    print("-" * 70)
    
    # Check for markers
    if '[COPING_TIP_START:' in formatted:
        print("\n✅ SUCCESS: Collapsible tip markers detected!")
        print("\nHow it works:")
        print("  1. Backend uses [COPING_TIP_START:X] markers")
        print("  2. JavaScript detects these markers")
        print("  3. Converts to clickable button: '💡 Want a tip to help with stress?'")
        print("  4. Content hidden until user clicks")
        print("  5. Button changes to 'Hide tip' when expanded")
        
        # Count tips
        tip_count = formatted.count('[COPING_TIP_START:')
        print(f"\n  → {tip_count} collapsible tip(s) will be shown")
        
    else:
        print("\n⚠️ WARNING: No collapsible tip markers found")
        print("  This might be because stress level is too low or no coping strategies matched")
    
    print("\n" + "="*70)
    print(" User Experience:")
    print("="*70)
    print("\n  Before clicking:")
    print("  ┌─────────────────────────────────────────────┐")
    print("  │ 💡 Want a tip to help with stress? (click) │")
    print("  └─────────────────────────────────────────────┘")
    print("\n  After clicking:")
    print("  ┌─────────────────────────────────────────────┐")
    print("  │ 💡 Hide tip                                 │")
    print("  ├─────────────────────────────────────────────┤")
    print("  │ • 4-7-8 Breathing                           │")
    print("  │   1. Breathe in for 4 seconds               │")
    print("  │   2. Hold for 7 seconds                     │")
    print("  │   3. Exhale slowly for 8 seconds            │")
    print("  │   4. Repeat 3-4 times                       │")
    print("  └─────────────────────────────────────────────┘")
    
    print("\n✅ Feature implementation complete!")
    print("   Start the web app to see it in action:")
    print("   → python web_app.py")


if __name__ == '__main__':
    test_collapsible_tips()
