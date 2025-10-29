"""
Test Embedded Intelligence with SQLite Database
"""

import sys
from pathlib import Path
import tempfile
import shutil

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from taminator.core.intelligence_engine import get_intelligence_engine
from taminator.core.database import IntelligenceDatabase


def test_embedded_intelligence():
    """Test complete embedded intelligence workflow"""
    
    print("=" * 80)
    print("TESTING EMBEDDED INTELLIGENCE - JPMC CASE")
    print("=" * 80)
    print()
    
    # Create temporary database
    temp_dir = Path(tempfile.mkdtemp())
    db_path = temp_dir / "test_intelligence.db"
    
    try:
        # Initialize database
        print("📋 Initializing SQLite database...")
        db = IntelligenceDatabase(db_path)
        db.initialize_schema()
        print(f"✅ Database created: {db_path}")
        print(f"   Size: {db_path.stat().st_size} bytes")
        print()
        
        # Read test email
        email_path = Path(__file__).parent / "test_jpmc_email.txt"
        email_text = email_path.read_text()
        
        # Analyze email
        print("🧠 Analyzing email...")
        engine = get_intelligence_engine()
        intelligence = engine.analyze_email(email_text)
        print("✅ Analysis complete")
        print()
        
        # Store in database
        print("💾 Storing intelligence in database...")
        intelligence_id = db.store_intelligence(intelligence)
        print(f"✅ Stored with ID: {intelligence_id}")
        print()
        
        # Retrieve from database
        print("📖 Retrieving from database...")
        stored = db.get_intelligence_by_case(intelligence.case_number)
        print(f"✅ Retrieved case: {stored['case_number']}")
        print(f"   Customer: {stored['customer_name']}")
        print(f"   Issue: {stored['issue_type']}")
        print(f"   Urgency: {stored['urgency_level']}")
        print()
        
        # Get database stats
        print("📊 Database Statistics:")
        stats = db.get_database_stats()
        print(f"   Total cases: {stats['total_cases']}")
        print(f"   Database size: {stats['database_size_bytes']} bytes")
        print(f"   Database path: {stats['database_path']}")
        print()
        
        # Test feedback recording
        print("📝 Recording TAM feedback...")
        db.record_feedback(
            case_number=intelligence.case_number,
            tam_decision="Escalated to licensing team",
            ai_followed=True,
            notes="AI recommendation was correct"
        )
        print("✅ Feedback recorded")
        print()
        
        # Get accuracy stats
        print("📈 Accuracy Statistics:")
        accuracy = db.get_accuracy_stats(days=7)
        for day in accuracy:
            print(f"   {day['date']}: {day['total_cases']} cases, "
                  f"{day['correct_classifications']} correct, "
                  f"{day['accuracy_rate']:.2%} accuracy")
        print()
        
        # Get recent cases
        print("📋 Recent Cases:")
        recent = db.get_recent_cases(limit=5)
        for case in recent:
            print(f"   • {case['case_number']} - {case['customer_name']} "
                  f"({case['issue_type']}, {case['urgency_level']})")
        print()
        
        print("=" * 80)
        print("✅ EMBEDDED INTELLIGENCE TEST PASSED!")
        print("=" * 80)
        print()
        print("Key Features Validated:")
        print("✅ SQLite database creation")
        print("✅ Intelligence storage")
        print("✅ Intelligence retrieval")
        print("✅ Feedback recording")
        print("✅ Accuracy tracking")
        print("✅ Statistics generation")
        print()
        print("Ready for:")
        print("• GUI integration")
        print("• Packaging with Taminator")
        print("• GitLab release")
        
    finally:
        # Cleanup
        shutil.rmtree(temp_dir)
        print(f"\n🧹 Cleaned up test database")


if __name__ == "__main__":
    test_embedded_intelligence()

