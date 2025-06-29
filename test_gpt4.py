#!/usr/bin/env python3
"""
Test GPT-4 Integration
======================

Simple test script to verify GPT-4 outreach message generation.
"""

from gpt_outreach import GPT4OutreachGenerator
from config import Config

def test_gpt4_integration():
    """Test GPT-4 integration with sample data"""
    
    print("🧪 Testing GPT-4 Integration")
    print("=" * 50)
    
    # Check if API key is available
    api_key = Config.get_openai_key()
    if not api_key:
        print("❌ No OpenAI API key found!")
        print("\nTo get a free API key:")
        print("1. Go to https://platform.openai.com/")
        print("2. Sign up for a free account")
        print("3. Get your API key from the API Keys section")
        print("4. Set it in config.py or as environment variable")
        return False
    
    print("✅ OpenAI API key found")
    
    # Test data
    candidate = {
        'name': 'Jane Smith',
        'headline': 'Senior Software Engineer at Google',
        'skills': ['Python', 'JavaScript', 'React', 'AWS', 'Docker'],
        'location': 'San Francisco, CA',
        'education': [{'school': 'Stanford University', 'degree': 'MS Computer Science'}],
        'experience': [{'title': 'Senior Software Engineer', 'company': 'Google', 'description': 'Python, JavaScript, AWS'}],
        'fit_score': 8.5
    }
    
    job_details = {
        'title': 'Senior Software Engineer',
        'company': 'TechCorp',
        'location': 'San Francisco, CA',
        'skills': ['Python', 'JavaScript', 'React', 'AWS'],
        'requirements': ['5+ years experience', 'Cloud platforms', 'Full-stack development']
    }
    
    # Test GPT-4 generation
    try:
        generator = GPT4OutreachGenerator()
        message = generator.generate_outreach_message(candidate, job_details, "John Recruiter")
        
        print("\n✅ GPT-4 Integration Successful!")
        print("\nGenerated Message:")
        print("-" * 50)
        print(message)
        print("-" * 50)
        
        return True
        
    except Exception as e:
        print(f"\n❌ GPT-4 Integration Failed: {e}")
        print("\nThis might be due to:")
        print("- Invalid API key")
        print("- Network issues")
        print("- OpenAI service issues")
        return False

def test_template_fallback():
    """Test template fallback when GPT-4 is not available"""
    
    print("\n🧪 Testing Template Fallback")
    print("=" * 50)
    
    # Test without API key
    generator = GPT4OutreachGenerator(api_key=None)
    
    candidate = {
        'name': 'Alice Johnson',
        'headline': 'Software Engineer at Microsoft',
        'skills': ['Python', 'C#', 'Azure'],
        'location': 'Seattle, WA',
        'fit_score': 7.5
    }
    
    job_details = {
        'title': 'Senior Software Engineer',
        'company': 'TechCorp',
        'location': 'San Francisco, CA',
        'skills': ['Python', 'JavaScript', 'React']
    }
    
    message = generator.generate_outreach_message(candidate, job_details, "Recruitment Team")
    
    print("✅ Template Fallback Working!")
    print("\nGenerated Template Message:")
    print("-" * 50)
    print(message)
    print("-" * 50)

if __name__ == "__main__":
    print("🚀 LinkedIn Recruitment Agent - GPT-4 Test")
    print("=" * 60)
    
    # Test GPT-4 integration
    gpt4_success = test_gpt4_integration()
    
    # Test template fallback
    test_template_fallback()
    
    print("\n📋 Summary:")
    if gpt4_success:
        print("✅ GPT-4 integration is working!")
        print("✅ Template fallback is working!")
        print("\n🎉 Your system is ready for both GPT-4 and template messages!")
    else:
        print("⚠️ GPT-4 integration needs API key setup")
        print("✅ Template fallback is working!")
        print("\n💡 You can still use the system with template messages")
        print("   Run: python main.py --demo --templates") 