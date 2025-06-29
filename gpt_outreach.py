import openai
import anthropic
from typing import Dict, List, Any
from config import Config
import time

class GPTOutreach:
    """Generate personalized outreach messages using OpenAI GPT-4 or Anthropic Claude"""
    
    def __init__(self):
        self.openai_client = None
        self.anthropic_client = None
        self.model = "gpt-3.5-turbo"  # Default to GPT-3.5 for cost efficiency
        
        # Initialize OpenAI client if API key is available
        openai_key = Config.get_openai_key()
        if openai_key:
            try:
                self.openai_client = openai.OpenAI(api_key=openai_key)
                print("✅ OpenAI client initialized")
            except Exception as e:
                print(f"⚠️ OpenAI client initialization failed: {e}")
        
        # Initialize Anthropic client if API key is available
        anthropic_key = Config.get_anthropic_key()
        if anthropic_key:
            try:
                self.anthropic_client = anthropic.Anthropic(api_key=anthropic_key)
                print("✅ Anthropic client initialized")
            except Exception as e:
                print(f"⚠️ Anthropic client initialization failed: {e}")
    
    def generate_message(self, candidate, job_details, recruiter_name="Recruitment Team", use_anthropic=False):
        """Generate personalized outreach message using AI"""
        
        if use_anthropic and self.anthropic_client:
            return self._generate_anthropic_message(candidate, job_details, recruiter_name)
        elif self.openai_client:
            return self._generate_openai_message(candidate, job_details, recruiter_name)
        else:
            return None, "no_ai_available"
    
    def _generate_anthropic_message(self, candidate, job_details, recruiter_name):
        """Generate message using Anthropic Claude"""
        try:
            prompt = self._build_prompt(candidate, job_details, recruiter_name)
            
            response = self.anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=500,
                temperature=0.7,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            message = response.content[0].text.strip()
            return message, "claude"
            
        except Exception as e:
            print(f"❌ Claude error: {e}")
            return None, "anthropic_error"
    
    def _generate_openai_message(self, candidate, job_details, recruiter_name):
        """Generate message using OpenAI GPT"""
        try:
            prompt = self._build_prompt(candidate, job_details, recruiter_name)
            
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional recruiter. Write personalized, friendly outreach messages."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            message = response.choices[0].message.content.strip()
            return message, "gpt-4"
            
        except Exception as e:
            print(f"❌ GPT-4 error: {e}")
            return None, "openai_error"
    
    def _build_prompt(self, candidate, job_details, recruiter_name):
        """Build the prompt for AI message generation"""
        
        # Extract candidate information
        name = candidate.get('name', 'there')
        headline = candidate.get('headline', 'professional experience')
        location = candidate.get('location', 'your area')
        skills = candidate.get('skills', [])
        experience = candidate.get('experience', [])
        
        # Extract job information
        job_title = job_details.get('title', 'this position')
        company = job_details.get('company', 'our company')
        job_location = job_details.get('location', 'our location')
        job_skills = job_details.get('skills', [])
        requirements = job_details.get('requirements', [])
        
        # Build skills highlight
        candidate_skills = ', '.join(skills[:3]) if skills else 'your technical background'
        job_skills_text = ', '.join(job_skills[:3]) if job_skills else 'various technologies'
        
        prompt = f"""
Write a personalized LinkedIn outreach message for a recruitment campaign.

CANDIDATE INFO:
- Name: {name}
- Current Role: {headline}
- Location: {location}
- Skills: {candidate_skills}
- Experience: {len(experience)} years

JOB OPPORTUNITY:
- Position: {job_title}
- Company: {company}
- Location: {job_location}
- Required Skills: {job_skills_text}
- Requirements: {', '.join(requirements[:2]) if requirements else 'Relevant experience'}

RECRUITER: {recruiter_name}

Write a friendly, professional message that:
1. Mentions their specific background/experience
2. Connects their skills to the job requirements
3. Is personalized and not generic
4. Invites them to have a conversation
5. Keeps it under 150 words
6. Uses their name and sounds human

Start with "Hi {name}," and end with "Best regards, {recruiter_name}"
"""
        
        return prompt

class GPT4OutreachGenerator:
    """Legacy class for backward compatibility"""
    
    def __init__(self, api_key: str = None, model: str = None):
        """Initialize GPT-4 outreach generator"""
        self.api_key = api_key or Config.get_openai_key()
        self.model = model or "gpt-3.5-turbo"
        if self.api_key:
            self.client = openai.OpenAI(api_key=self.api_key)
        else:
            print("⚠️ Warning: No OpenAI API key provided. Using fallback templates.")
    
    def generate_outreach_message(self, candidate: Dict[str, Any], job_details: Dict[str, Any], recruiter_name: str = "Recruitment Team") -> str:
        """Legacy method - now uses the new GPTOutreach class"""
        gpt_outreach = GPTOutreach()
        message, source = gpt_outreach.generate_message(candidate, job_details, recruiter_name)
        return message if message else self._fallback_message(candidate, job_details, recruiter_name)
    
    def _fallback_message(self, candidate: Dict[str, Any], job_details: Dict[str, Any], recruiter_name: str) -> str:
        """Generate fallback template message"""
        name = candidate.get('name', 'there')
        headline = candidate.get('headline', 'professional experience')
        job_title = job_details.get('title', 'this position')
        company = job_details.get('company', 'our company')
        location = job_details.get('location', 'our location')
        skills = candidate.get('skills', [])
        skills_highlight = ', '.join(skills[:2]) if skills else 'your technical background'
        
        return f"""Hi {name},

I noticed your {headline} experience and thought you might be interested in a {job_title} position at {company} in {location}.

Your background in {skills_highlight} aligns perfectly with what we're looking for. Would you be open to a brief conversation about this opportunity?

Best regards,
{recruiter_name}"""
    
    def generate_bulk_outreach_messages(self, candidates: List[Dict[str, Any]], job_details: Dict[str, Any], recruiter_name: str = "Recruitment Team") -> List[Dict[str, Any]]:
        """Generate outreach messages for multiple candidates"""
        gpt_outreach = GPTOutreach()
        results = []
        
        for i, candidate in enumerate(candidates, 1):
            print(f"   Generating message {i}/{len(candidates)}: {candidate.get('name', 'Unknown')}")
            
            message, source = gpt_outreach.generate_message(candidate, job_details, recruiter_name)
            
            if not message:
                message = self._fallback_message(candidate, job_details, recruiter_name)
                source = "template"
            
            candidate['outreach_message'] = message
            candidate['message_source'] = source
            results.append(candidate)
            
            # Small delay to avoid rate limiting
            time.sleep(0.5)
        
        return results

# Example usage
if __name__ == "__main__":
    # Test with sample data
    generator = GPT4OutreachGenerator()
    
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
    
    message = generator.generate_outreach_message(candidate, job_details, "John Recruiter")
    
    print("Generated GPT-4 Outreach Message:")
    print("=" * 50)
    print(message) 