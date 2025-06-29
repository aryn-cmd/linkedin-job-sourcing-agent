#!/usr/bin/env python3
"""
Test script for Anthropic Claude integration
"""

from gpt_outreach import GPTOutreach
from config import Config

def test_anthropic_integration():
    """Test Anthropic Claude integration"""
    print("🧪 Testing Anthropic Claude Integration")
    print("=" * 50)
    
    # Check if API key is available
    anthropic_key = Config.get_anthropic_key()
    if not anthropic_key:
        print("❌ No Anthropic API key found")
        print("Please set ANTHROPIC_API_KEY environment variable or add it to config.py")
        return False
    
    # Initialize GPTOutreach
    gpt_outreach = GPTOutreach()
    
    # Test data
    candidate = {
        'name': 'Alice Johnson',
        'headline': 'Senior Software Engineer at Google',
        'location': 'San Francisco, CA',
        'skills': ['Python', 'JavaScript', 'React', 'AWS'],
        'experience': [
            {'title': 'Senior Software Engineer', 'company': 'Google'},
            {'title': 'Software Engineer', 'company': 'Microsoft'}
        ]
    }
    
    job_details = {
        'title': 'Senior Software Engineer',
        'company': 'TechCorp',
        'location': 'San Francisco, CA',
        'skills': ['Python', 'JavaScript', 'React', 'AWS'],
        'requirements': ['5+ years experience', 'Cloud platforms']
    }
    
    print("📝 Testing message generation...")
    
    # Test Anthropic message generation
    message, source = gpt_outreach.generate_message(
        candidate, job_details, "Recruitment Team", use_anthropic=True
    )
    
    if message:
        print("✅ Anthropic Claude message generated successfully!")
        print(f"Source: {source}")
        print("\n📄 Generated Message:")
        print("-" * 40)
        print(message)
        print("-" * 40)
        return True
    else:
        print("❌ Failed to generate Anthropic message")
        print(f"Error source: {source}")
        return False

if __name__ == "__main__":
    test_anthropic_integration() 