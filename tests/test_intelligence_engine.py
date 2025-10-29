"""
Test Intelligence Engine with Real JPMC Case
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from taminator.core.intelligence_engine import get_intelligence_engine


def test_jpmc_email():
    """Test with actual JPMC email"""
    
    # Read test email
    email_path = Path(__file__).parent / "test_jpmc_email.txt"
    email_text = email_path.read_text()
    
    print("=" * 80)
    print("TESTING INTELLIGENCE ENGINE - JPMC CASE")
    print("=" * 80)
    print()
    
    # Get engine
    engine = get_intelligence_engine()
    
    # Analyze
    intelligence = engine.analyze_email(email_text)
    
    # Display results
    print("📋 CASE NUMBER:")
    print(f"   {intelligence.case_number or 'NOT DETECTED'}")
    print()
    
    print("🏢 CUSTOMER:")
    if intelligence.customer:
        print(f"   Name: {intelligence.customer.name}")
        print(f"   Account: {intelligence.customer.account_number}")
        print(f"   Confidence: {intelligence.customer.confidence:.2f}")
    else:
        print("   NOT DETECTED")
    print()
    
    print("👥 CONTACTS:")
    for contact in intelligence.contacts:
        print(f"   • {contact.name}")
        if contact.email:
            print(f"     Email: {contact.email}")
        if contact.role:
            print(f"     Role: {contact.role}")
    print()
    
    print("🏷️  ISSUE CLASSIFICATION:")
    if intelligence.issue:
        print(f"   Type: {intelligence.issue.primary_type.value}")
        print(f"   Product: {intelligence.issue.product or 'N/A'}")
        print(f"   Confidence: {intelligence.issue.confidence:.2f}")
        print(f"   Reasoning: {intelligence.issue.reasoning}")
    else:
        print("   NOT CLASSIFIED")
    print()
    
    print("⏰ URGENCY:")
    if intelligence.urgency:
        print(f"   Level: {intelligence.urgency.level.value}")
        print(f"   Score: {intelligence.urgency.score:.2f}")
        if intelligence.urgency.deadline:
            print(f"   Deadline: {intelligence.urgency.deadline}")
            print(f"   Days Remaining: {intelligence.urgency.days_remaining}")
        print(f"   Indicators: {intelligence.urgency.indicators}")
    else:
        print("   NOT ASSESSED")
    print()
    
    print("💡 RECOMMENDED ACTIONS:")
    if intelligence.recommended_actions:
        print(f"   Primary: {intelligence.recommended_actions.primary_action}")
        print(f"   Reasoning: {intelligence.recommended_actions.reasoning}")
        print(f"   Escalate to: {intelligence.recommended_actions.escalation_targets}")
        print("\n   Immediate Actions:")
        for action in intelligence.recommended_actions.immediate_actions:
            print(f"   • {action}")
    else:
        print("   NONE")
    print()
    
    # Overall confidence
    confidence_level, confidence_score = intelligence.get_overall_confidence()
    print("=" * 80)
    print(f"OVERALL CONFIDENCE: {confidence_level.value.upper()} ({confidence_score:.2f})")
    print("=" * 80)
    print()
    
    # Validation
    print("VALIDATION:")
    print(f"✅ Case number extracted: {intelligence.case_number == '04293185'}")
    print(f"✅ Customer identified: {intelligence.customer and intelligence.customer.name == 'JP Morgan Chase'}")
    print(f"✅ Issue classified as licensing: {intelligence.issue and intelligence.issue.primary_type.value == 'licensing'}")
    print(f"✅ High urgency detected: {intelligence.urgency and intelligence.urgency.level.value == 'high'}")
    print(f"✅ Escalation recommended: {intelligence.recommended_actions and 'licensing' in intelligence.recommended_actions.primary_action.lower()}")
    print()
    
    return intelligence


if __name__ == "__main__":
    test_jpmc_email()

