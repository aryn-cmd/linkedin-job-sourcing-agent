#!/usr/bin/env python3
"""
Test Script for LinkedIn Recruitment Agent
==========================================

This script demonstrates how to use the system with visible output.
"""

import json
import time
from job_orchestrator import JobOrchestrator

def test_demo_mode():
    """Test the system with demo data"""
    print("🧪 TESTING LINKEDIN RECRUITMENT AGENT")
    print("=" * 60)
    
    # Initialize the orchestrator
    print("📋 Initializing system components...")
    orchestrator = JobOrchestrator()
    print("✅ System initialized successfully!")
    
    # Run demo
    print("\n🎯 Running demo with sample job data...")
    results = orchestrator.process_job_posting("demo", max_candidates=5)
    
    if 'error' in results:
        print(f"❌ Error: {results['error']}")
        return
    
    # Display results
    print("\n📊 RESULTS SUMMARY")
    print("-" * 40)
    
    job_details = results['job_details']
    print(f"Job Title: {job_details.get('title', 'N/A')}")
    print(f"Company: {job_details.get('company', 'N/A')}")
    print(f"Location: {job_details.get('location', 'N/A')}")
    print(f"Required Skills: {', '.join(job_details.get('skills', []))}")
    
    summary = results['summary']
    print(f"\nTotal Candidates Found: {summary['total_candidates']}")
    print(f"Average Score: {summary['average_score']:.2f}/10")
    
    print("\n🏆 TOP CANDIDATES:")
    print("-" * 40)
    
    for i, candidate in enumerate(summary['top_candidates'][:3]):
        print(f"\n{i+1}. {candidate['name']}")
        print(f"   📝 Headline: {candidate['headline']}")
        print(f"   📍 Location: {candidate.get('location', 'N/A')}")
        print(f"   ⭐ Score: {candidate['score']:.2f}/10 ({candidate['grade']})")
        print(f"   💡 Recommendation: {candidate['recommendation']}")
        print(f"   🔗 Profile: {candidate['profile_url']}")
    
    print("\n📈 SCORE DISTRIBUTION:")
    print("-" * 40)
    for range_name, count in summary['score_distribution'].items():
        if count > 0:
            print(f"   {range_name}: {count} candidates")
    
    print("\n💡 RECOMMENDATIONS:")
    print("-" * 40)
    for rec in summary['recommendations']:
        print(f"   • {rec}")
    
    # Export results
    filename = orchestrator.export_results(results)
    print(f"\n💾 Results exported to: {filename}")
    
    print("\n✅ Demo completed successfully!")
    return results

def test_scoring_system():
    """Test the scoring system with sample data"""
    print("\n🎯 TESTING SCORING SYSTEM")
    print("=" * 40)
    
    from scoring import CandidateScorer
    
    scorer = CandidateScorer()
    
    # Sample candidate data
    candidate_data = {
        'name': 'John Doe',
        'location': 'San Francisco, CA',
        'education': [
            {'school': 'Stanford University', 'degree': 'MS Computer Science'},
            {'school': 'UC Berkeley', 'degree': 'BS Computer Science'}
        ],
        'experience': [
            {'title': 'Software Engineer', 'company': 'Google', 'description': 'Backend development with Python and Java'},
            {'title': 'Senior Software Engineer', 'company': 'Microsoft', 'description': 'Full-stack development with React and Node.js'},
            {'title': 'Lead Engineer', 'company': 'Netflix', 'description': 'System architecture and microservices'}
        ],
        'skills': ['Python', 'Java', 'JavaScript', 'React', 'Node.js', 'AWS', 'Docker']
    }
    
    # Sample job requirements
    job_requirements = {
        'title': 'Senior Software Engineer',
        'location': 'San Francisco, CA',
        'skills': ['Python', 'JavaScript', 'React', 'AWS', 'Docker'],
        'requirements': [
            '5+ years of experience in software development',
            'Experience with Python and JavaScript',
            'Knowledge of cloud platforms like AWS'
        ]
    }
    
    print("📊 Calculating fit score...")
    score_result = scorer.calculate_fit_score(candidate_data, job_requirements)
    
    print(f"\n🎯 SCORING RESULTS:")
    print(f"Total Score: {score_result['total_score']}/10")
    print(f"Grade: {score_result['overall_grade']}")
    print(f"Recommendation: {score_result['recommendation']}")
    
    print(f"\n📋 DETAILED BREAKDOWN:")
    for category, details in score_result['score_breakdown'].items():
        print(f"   {category.replace('_', ' ').title()}: {details['score']:.1f}/10")
        print(f"     Details: {details['details']}")
    
    print("\n✅ Scoring test completed!")

def main():
    """Main test function"""
    print("🚀 LINKEDIN RECRUITMENT AGENT - SYSTEM TEST")
    print("=" * 60)
    
    try:
        # Test 1: Demo mode
        test_demo_mode()
        
        # Test 2: Scoring system
        test_scoring_system()
        
        print("\n🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
        print("\n📖 HOW TO USE THE SYSTEM:")
        print("1. Run demo: python main.py --demo")
        print("2. Process real job: python main.py <linkedin_job_url>")
        print("3. Export results: python main.py --export --demo")
        print("4. Get help: python main.py --help")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        print("Please check your internet connection and try again.")

if __name__ == "__main__":
    main() 