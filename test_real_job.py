#!/usr/bin/env python3
"""
Test Real Job Workflow with Macquarie Apprenticeship Program
"""

import time
from job_parser import LinkedInJobParser
from linkedin_search import LinkedInProfileSearcher
from scoring import CandidateScorer
from enhanced_outreach import EnhancedOutreachGenerator

def test_real_job_workflow():
    """Test complete workflow with real Macquarie job"""
    
    print("🔍 Testing Real Job: Macquarie Apprenticeship Program")
    print("=" * 60)
    
    job_url = "https://www.linkedin.com/jobs/view/4025320877"
    
    # Step 1: Parse Job
    print("Step 1: Parsing Job Details...")
    parser = LinkedInJobParser()
    job_details = parser.get_job_details(job_url)
    
    if not job_details:
        print("❌ Failed to parse job")
        return
    
    # Fix the job title if it's empty
    if not job_details.get('title'):
        job_details['title'] = "Apprenticeship Program"
    
    print(f"✅ Job Parsed Successfully!")
    print(f"   Company: {job_details.get('company')}")
    print(f"   Location: {job_details.get('location')}")
    print(f"   Title: {job_details.get('title')}")
    print(f"   Skills: {', '.join(job_details.get('skills', []))}")
    print()
    
    # Create sample profiles for demonstration
    print("Step 2: Creating Sample Profiles (for demonstration)...")
    sample_profiles = create_sample_profiles(job_details)
    
    # Step 3: Score Candidates
    print(f"\nStep 3: Scoring Candidates...")
    scorer = CandidateScorer()
    scored_candidates = []
    
    for i, profile in enumerate(sample_profiles):
        print(f"   Scoring candidate {i+1}/{len(sample_profiles)}: {profile.get('name', 'Unknown')}")
        
        score_result = scorer.calculate_fit_score(profile, job_details)
        
        scored_candidate = {
            'name': profile.get('name', ''),
            'linkedin_url': profile.get('url', ''),
            'fit_score': score_result['fit_score'],
            'score_breakdown': score_result['score_breakdown'],
            'headline': profile.get('headline', ''),
            'location': profile.get('location', ''),
            'education': profile.get('education', []),
            'experience': profile.get('experience', []),
            'skills': profile.get('skills', []),
            'processed_at': time.time()
        }
        
        scored_candidates.append(scored_candidate)
    
    # Sort by score
    scored_candidates.sort(key=lambda x: x['fit_score'], reverse=True)
    
    # Step 4: Generate Outreach Messages
    print(f"\nStep 4: Generating Outreach Messages...")
    outreach_generator = EnhancedOutreachGenerator()
    
    candidates_with_outreach = outreach_generator.generate_bulk_outreach_messages(
        scored_candidates, 
        job_details, 
        "Recruitment Team"
    )
    
    # Display Results
    print(f"\n📊 FINAL RESULTS")
    print("=" * 60)
    print(f"Job: {job_details.get('title')} at {job_details.get('company')}")
    print(f"Location: {job_details.get('location')}")
    print(f"Total Candidates Found: {len(candidates_with_outreach)}")
    print()
    
    print("🏆 TOP CANDIDATES:")
    print("-" * 60)
    
    for i, candidate in enumerate(candidates_with_outreach):
        print(f"{i+1}. {candidate['name']}")
        print(f"   📝 Headline: {candidate['headline']}")
        print(f"   📍 Location: {candidate['location']}")
        print(f"   ⭐ Fit Score: {candidate['fit_score']:.2f}/10")
        print(f"   🔗 LinkedIn: {candidate['linkedin_url']}")
        
        # Score breakdown
        breakdown = candidate['score_breakdown']
        print(f"   📊 Score Breakdown:")
        print(f"      Education: {breakdown.get('education', 0):.1f}/10")
        print(f"      Trajectory: {breakdown.get('trajectory', 0):.1f}/10")
        print(f"      Company: {breakdown.get('company', 0):.1f}/10")
        print(f"      Skills: {breakdown.get('skills', 0):.1f}/10")
        print(f"      Location: {breakdown.get('location', 0):.1f}/10")
        print(f"      Tenure: {breakdown.get('tenure', 0):.1f}/10")
        
        # Outreach message preview
        message = candidate.get('outreach_message', '')
        print(f"   💬 Outreach Preview: {message[:100]}...")
        print()
    
    return candidates_with_outreach

def create_sample_profiles(job_details):
    """Create sample profiles for demonstration"""
    
    sample_profiles = [
        {
            'name': 'Priya Sharma',
            'headline': 'Recent Graduate - Computer Science',
            'location': 'Gurugram, Haryana, India',
            'url': 'https://linkedin.com/in/demo-priya',
            'education': [{'school': 'Delhi University', 'degree': 'BS Computer Science'}],
            'experience': [{'title': 'Student', 'company': 'Delhi University', 'description': 'Computer Science'}],
            'skills': ['Python', 'Java', 'SQL', 'AI', 'Testing']
        },
        {
            'name': 'Rahul Kumar',
            'headline': 'Entry Level Developer',
            'location': 'Gurugram, Haryana, India',
            'url': 'https://linkedin.com/in/demo-rahul',
            'education': [{'school': 'IIT Delhi', 'degree': 'BS Engineering'}],
            'experience': [{'title': 'Intern', 'company': 'Tech Startup', 'description': 'Software Development'}],
            'skills': ['JavaScript', 'React', 'Node.js', 'Testing', 'AI']
        },
        {
            'name': 'Anjali Patel',
            'headline': 'Graduate Student - Data Science',
            'location': 'Delhi, India',
            'url': 'https://linkedin.com/in/demo-anjali',
            'education': [{'school': 'IISc Bangalore', 'degree': 'MS Data Science'}],
            'experience': [{'title': 'Research Assistant', 'company': 'IISc', 'description': 'Machine Learning'}],
            'skills': ['Python', 'Machine Learning', 'AI', 'Data Analysis', 'Testing']
        },
        {
            'name': 'Vikram Singh',
            'headline': 'Junior Software Engineer',
            'location': 'Gurugram, Haryana, India',
            'url': 'https://linkedin.com/in/demo-vikram',
            'education': [{'school': 'BITS Pilani', 'degree': 'BS Computer Science'}],
            'experience': [{'title': 'Junior Developer', 'company': 'IT Company', 'description': 'Full Stack Development'}],
            'skills': ['Java', 'Spring Boot', 'React', 'Testing', 'AWS']
        },
        {
            'name': 'Meera Reddy',
            'headline': 'Fresh Graduate - Information Technology',
            'location': 'Gurugram, Haryana, India',
            'url': 'https://linkedin.com/in/demo-meera',
            'education': [{'school': 'VIT University', 'degree': 'BS Information Technology'}],
            'experience': [{'title': 'Student', 'company': 'VIT University', 'description': 'IT Projects'}],
            'skills': ['Python', 'Database', 'Web Development', 'Testing', 'AI Basics']
        }
    ]
    
    return sample_profiles

if __name__ == "__main__":
    results = test_real_job_workflow()
    
    if results:
        print("✅ Workflow completed successfully!")
        print(f"📋 Generated {len(results)} candidate profiles with outreach messages")
        print("\n💡 Next Steps:")
        print("   • Review the top candidates above")
        print("   • Use the outreach messages to contact candidates")
        print("   • Export results for further analysis")
    else:
        print("❌ Workflow failed") 