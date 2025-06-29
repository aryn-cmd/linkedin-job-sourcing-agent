import re
from typing import Dict, List, Any
from config import Config

class OutreachGenerator:
    def __init__(self):
        self.templates = {
            'default': Config.OUTREACH_TEMPLATE,
            'senior': """
Hi {name},

I came across your impressive background as {headline} and thought you'd be perfect for a {job_title} role at {company} in {location}.

Your experience with {skills_highlight} is exactly what we're looking for. Would you be interested in discussing this opportunity?

Best regards,
{recruiter_name}
            """,
            'junior': """
Hi {name},

I noticed your {headline} experience and thought you might be interested in a {job_title} position at {company} in {location}.

Your skills in {skills_highlight} align well with our needs. Would you be open to a conversation about this role?

Best regards,
{recruiter_name}
            """
        }
    
    def generate_outreach_message(self, candidate: Dict[str, Any], job_details: Dict[str, Any], recruiter_name: str = "Recruitment Team") -> str:
        """
        Generate a personalized outreach message for a candidate
        
        Args:
            candidate: Candidate data including name, headline, skills, etc.
            job_details: Job details including title, company, location, etc.
            recruiter_name: Name of the recruiter (default: "Recruitment Team")
            
        Returns:
            Personalized outreach message
        """
        # Determine template based on candidate level
        template_key = self._determine_template(candidate, job_details)
        template = self.templates[template_key]
        
        # Extract skills highlight
        skills_highlight = self._extract_skills_highlight(candidate, job_details)
        
        # Prepare template variables
        template_vars = {
            'name': candidate.get('name', 'there'),
            'headline': candidate.get('headline', 'professional experience'),
            'job_title': job_details.get('title', 'this position'),
            'company': job_details.get('company', 'our company'),
            'location': job_details.get('location', 'our location'),
            'skills_highlight': skills_highlight,
            'recruiter_name': recruiter_name
        }
        
        # Generate message
        message = template.format(**template_vars)
        
        # Clean up the message
        message = self._clean_message(message)
        
        return message
    
    def _determine_template(self, candidate: Dict[str, Any], job_details: Dict[str, Any]) -> str:
        """Determine which template to use based on candidate and job level"""
        candidate_headline = candidate.get('headline', '').lower()
        job_title = job_details.get('title', '').lower()
        
        # Check for senior indicators
        senior_indicators = ['senior', 'lead', 'principal', 'staff', 'architect', 'director', 'manager']
        
        if any(indicator in candidate_headline for indicator in senior_indicators) or \
           any(indicator in job_title for indicator in senior_indicators):
            return 'senior'
        
        # Check for junior indicators
        junior_indicators = ['junior', 'entry', 'graduate', 'intern', 'associate']
        
        if any(indicator in candidate_headline for indicator in junior_indicators) or \
           any(indicator in job_title for indicator in junior_indicators):
            return 'junior'
        
        return 'default'
    
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
        
        for candidate in candidates:
            message = self.generate_outreach_message(candidate, job_details, recruiter_name)
            
            candidate_with_message = {
                **candidate,
                'outreach_message': message
            }
            
            results.append(candidate_with_message)
        
        return results

# Example usage
if __name__ == "__main__":
    generator = OutreachGenerator()
    
    # Sample candidate
    candidate = {
        'name': 'Jane Smith',
        'headline': 'Senior Software Engineer at Google',
        'skills': ['Python', 'JavaScript', 'React', 'AWS', 'Docker'],
        'location': 'San Francisco, CA'
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
    
    print("Generated Outreach Message:")
    print("=" * 50)
    print(message)
