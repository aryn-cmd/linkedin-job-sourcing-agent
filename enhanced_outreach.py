import re
import random
from typing import Dict, List, Any
from config import Config

class EnhancedOutreachGenerator:
    def __init__(self):
        """Enhanced local outreach generator with multiple templates and personalization"""
        
        # Multiple template variations for different scenarios
        self.templates = {
            'senior_experienced': [
                """
Hi {name},

I was impressed by your {headline} experience and thought you'd be perfect for our {job_title} role at {company} in {location}.

Your expertise in {skills_highlight} aligns perfectly with what we're looking for. Given your background at {current_company}, I believe you'd bring valuable insights to our team.

Would you be interested in discussing this opportunity? I'd love to share more about the role and see if it's a good fit.

Best regards,
{recruiter_name}
                """,
                """
Hi {name},

I came across your profile and was struck by your {headline} experience. We're currently hiring for a {job_title} position at {company} in {location}, and your background seems like an excellent match.

Your skills in {skills_highlight} are exactly what we need, and your experience at {current_company} would be valuable to our team.

Would you be open to a brief conversation about this opportunity?

Best regards,
{recruiter_name}
                """
            ],
            
            'mid_level': [
                """
Hi {name},

I noticed your {headline} experience and thought you might be interested in a {job_title} position at {company} in {location}.

Your background in {skills_highlight} aligns well with our requirements. Would you be interested in learning more about this opportunity?

Best regards,
{recruiter_name}
                """,
                """
Hi {name},

I came across your profile and was impressed by your {headline} experience. We have a {job_title} opening at {company} in {location} that might be a great fit.

Your skills in {skills_highlight} are exactly what we're looking for. Would you be open to discussing this role?

Best regards,
{recruiter_name}
                """
            ],
            
            'junior_entry': [
                """
Hi {name},

I noticed your {headline} experience and thought you might be interested in a {job_title} position at {company} in {location}.

Your skills in {skills_highlight} show great potential. Would you be open to learning more about this opportunity?

Best regards,
{recruiter_name}
                """,
                """
Hi {name},

I came across your profile and was impressed by your {headline} background. We have a {job_title} opening at {company} in {location} that could be a great next step in your career.

Your experience with {skills_highlight} aligns well with what we're looking for. Would you be interested in discussing this role?

Best regards,
{recruiter_name}
                """
            ],
            
            'location_match': [
                """
Hi {name},

I noticed you're based in {candidate_location} and thought you might be interested in a {job_title} position at {company} in {location}.

Your {headline} experience and skills in {skills_highlight} make you a great candidate for this role. Would you be open to discussing this opportunity?

Best regards,
{recruiter_name}
                """
            ],
            
            'company_match': [
                """
Hi {name},

I was impressed by your {headline} experience at {current_company}. We have a {job_title} opening at {company} in {location} that could be a great next step.

Your expertise in {skills_highlight} is exactly what we need. Would you be interested in learning more about this opportunity?

Best regards,
{recruiter_name}
                """
            ]
        }
        
        # Personalization phrases
        self.personalization_phrases = {
            'opening': [
                "I was impressed by",
                "I came across your profile and was struck by",
                "I noticed your",
                "I was excited to see your",
                "Your profile caught my attention with your"
            ],
            'connection': [
                "and thought you'd be perfect for",
                "and believe you'd be an excellent fit for",
                "and think you might be interested in",
                "and wanted to reach out about",
                "and thought this could be a great opportunity for you"
            ],
            'closing': [
                "Would you be interested in discussing this opportunity?",
                "Would you be open to a brief conversation about this role?",
                "I'd love to share more about the position and see if it's a good fit.",
                "Would you be interested in learning more about this opportunity?",
                "I'd be happy to discuss this role in more detail if you're interested."
            ]
        }
    
    def generate_outreach_message(self, candidate: Dict[str, Any], job_details: Dict[str, Any], recruiter_name: str = "Recruitment Team") -> str:
        """
        Generate a personalized outreach message using enhanced local templates
        
        Args:
            candidate: Candidate data including name, headline, skills, etc.
            job_details: Job details including title, company, location, etc.
            recruiter_name: Name of the recruiter
            
        Returns:
            Personalized outreach message
        """
        # Determine the best template based on candidate profile
        template_key = self._determine_template_key(candidate, job_details)
        template_variations = self.templates[template_key]
        
        # Select a random template variation for variety
        template = random.choice(template_variations)
        
        # Extract and prepare data
        current_company = self._extract_current_company(candidate)
        skills_highlight = self._extract_skills_highlight(candidate, job_details)
        candidate_location = candidate.get('location', 'your area')
        
        # Prepare template variables
        template_vars = {
            'name': candidate.get('name', 'there'),
            'headline': candidate.get('headline', 'professional experience'),
            'job_title': job_details.get('title', 'this position'),
            'company': job_details.get('company', 'our company'),
            'location': job_details.get('location', 'our location'),
            'skills_highlight': skills_highlight,
            'current_company': current_company,
            'candidate_location': candidate_location,
            'recruiter_name': recruiter_name
        }
        
        # Generate message
        message = template.format(**template_vars)
        
        # Add personalization touches
        message = self._add_personalization(message, candidate, job_details)
        
        # Clean up the message
        message = self._clean_message(message)
        
        return message
    
    def _determine_template_key(self, candidate: Dict[str, Any], job_details: Dict[str, Any]) -> str:
        """Determine the best template based on candidate and job characteristics"""
        
        candidate_headline = candidate.get('headline', '').lower()
        job_title = job_details.get('title', '').lower()
        candidate_location = candidate.get('location', '').lower()
        job_location = job_details.get('location', '').lower()
        
        # Check for location match
        if self._is_location_match(candidate_location, job_location):
            return 'location_match'
        
        # Check for company match (if candidate has current company)
        if self._extract_current_company(candidate):
            return 'company_match'
        
        # Check for senior level
        senior_indicators = ['senior', 'lead', 'principal', 'staff', 'architect', 'director', 'manager', 'head']
        if any(indicator in candidate_headline for indicator in senior_indicators) or \
           any(indicator in job_title for indicator in senior_indicators):
            return 'senior_experienced'
        
        # Check for junior level
        junior_indicators = ['junior', 'entry', 'graduate', 'intern', 'associate', 'trainee']
        if any(indicator in candidate_headline for indicator in junior_indicators) or \
           any(indicator in job_title for indicator in junior_indicators):
            return 'junior_entry'
        
        # Default to mid-level
        return 'mid_level'
    
    def _extract_current_company(self, candidate: Dict[str, Any]) -> str:
        """Extract current company from candidate data"""
        headline = candidate.get('headline', '')
        
        # Look for "at Company" pattern
        if ' at ' in headline:
            company = headline.split(' at ')[-1]
            return company.strip()
        
        # Look in experience if available
        experience = candidate.get('experience', [])
        if experience:
            return experience[0].get('company', '')
        
        return ''
    
    def _extract_skills_highlight(self, candidate: Dict[str, Any], job_details: Dict[str, Any]) -> str:
        """Extract and format skills highlight for the message"""
        candidate_skills = set()
        job_skills = set()
        
        # Get candidate skills
        if 'skills' in candidate:
            candidate_skills.update(skill.lower() for skill in candidate['skills'])
        
        # Get job skills
        if 'skills' in job_details:
            job_skills.update(skill.lower() for skill in job_details['skills'])
        
        # Find matching skills
        matching_skills = candidate_skills.intersection(job_skills)
        
        if matching_skills:
            # Take top 3 matching skills
            top_skills = list(matching_skills)[:3]
            return ', '.join(skill.title() for skill in top_skills)
        elif candidate_skills:
            # Use top candidate skills if no match
            top_skills = list(candidate_skills)[:3]
            return ', '.join(skill.title() for skill in top_skills)
        else:
            return "relevant technical skills"
    
    def _is_location_match(self, candidate_location: str, job_location: str) -> bool:
        """Check if candidate and job locations match"""
        if not candidate_location or not job_location:
            return False
        
        # Extract city names
        candidate_city = candidate_location.split(',')[0].strip().lower()
        job_city = job_location.split(',')[0].strip().lower()
        
        return candidate_city == job_city
    
    def _add_personalization(self, message: str, candidate: Dict[str, Any], job_details: Dict[str, Any]) -> str:
        """Add personalization touches to the message"""
        
        # Add education mention if relevant
        education = candidate.get('education', [])
        if education:
            top_education = education[0]
            school = top_education.get('school', '')
            if school and any(prestigious in school.lower() for prestigious in ['stanford', 'mit', 'harvard', 'berkeley', 'caltech']):
                message = message.replace(
                    "Your expertise in",
                    f"Your background from {school} and expertise in"
                )
        
        # Add experience duration if available
        experience = candidate.get('experience', [])
        if experience:
            # Count years of experience (rough estimate)
            experience_count = len(experience)
            if experience_count >= 5:
                message = message.replace(
                    "Your expertise in",
                    "Your extensive experience and expertise in"
                )
        
        return message
    
    def _clean_message(self, message: str) -> str:
        """Clean and format the message"""
        # Remove extra whitespace
        message = re.sub(r'\n\s*\n', '\n\n', message)
        message = message.strip()
        
        return message
    
    def generate_bulk_outreach_messages(self, candidates: List[Dict[str, Any]], job_details: Dict[str, Any], recruiter_name: str = "Recruitment Team") -> List[Dict[str, Any]]:
        """
        Generate outreach messages for multiple candidates
        
        Args:
            candidates: List of candidate data
            job_details: Job details
            recruiter_name: Name of the recruiter
            
        Returns:
            List of candidates with outreach messages
        """
        results = []
        
        print(f"🎯 Generating enhanced local outreach messages for {len(candidates)} candidates...")
        
        for i, candidate in enumerate(candidates):
            print(f"   Generating message {i+1}/{len(candidates)}: {candidate.get('name', 'Unknown')}")
            
            message = self.generate_outreach_message(candidate, job_details, recruiter_name)
            
            candidate_with_message = {
                **candidate,
                'outreach_message': message,
                'message_source': 'enhanced_local'
            }
            
            results.append(candidate_with_message)
        
        return results

# Example usage
if __name__ == "__main__":
    generator = EnhancedOutreachGenerator()
    
    # Sample candidate
    candidate = {
        'name': 'Jane Smith',
        'headline': 'Senior Software Engineer at Google',
        'skills': ['Python', 'JavaScript', 'React', 'AWS', 'Docker'],
        'location': 'San Francisco, CA',
        'education': [{'school': 'Stanford University', 'degree': 'MS Computer Science'}],
        'experience': [
            {'title': 'Senior Software Engineer', 'company': 'Google', 'description': 'Python, JavaScript, AWS'},
            {'title': 'Software Engineer', 'company': 'Microsoft', 'description': 'C#, Azure'}
        ]
    }
    
    # Sample job
    job_details = {
        'title': 'Senior Software Engineer',
        'company': 'TechCorp',
        'location': 'San Francisco, CA',
        'skills': ['Python', 'JavaScript', 'React', 'AWS']
    }
    
    # Generate message
    message = generator.generate_outreach_message(candidate, job_details, "John Recruiter")
    
    print("Generated Enhanced Local Outreach Message:")
    print("=" * 60)
    print(message) 