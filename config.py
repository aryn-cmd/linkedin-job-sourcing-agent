import os
from typing import Optional

class Config:
    """Configuration settings for the LinkedIn Recruitment Agent"""
    
    # RapidAPI LinkedIn Data API
    RAPIDAPI_KEY = "b33e8a9b34msh236c7d31bb49420p1b1a08jsn3c853752052e"
    RAPIDAPI_HOST = "linkedin-profile-data.p.rapidapi.com"  # Fresh LinkedIn Data API
    
    # OpenAI API for GPT-4
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')  # Set your OpenAI API key here or via environment
    
    # Anthropic API for Claude
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')  # Set your Anthropic API key here or via environment
    
    # Search settings
    DEFAULT_MAX_CANDIDATES = 20
    DEFAULT_SEARCH_PAGES = 2
    SEARCH_DELAY = 2  # seconds between requests
    
    # Scoring weights (matching your rubric)
    SCORING_WEIGHTS = {
        'education': 0.20,
        'trajectory': 0.20,
        'company': 0.15,
        'skills': 0.25,
        'location': 0.10,
        'tenure': 0.10
    }
    
    # Outreach settings
    OUTREACH_TEMPLATE = """
Hi {name},

I noticed your {headline} experience and thought you might be interested in a {job_title} position at {company} in {location}.

Your background in {skills_highlight} aligns perfectly with what we're looking for. Would you be open to a brief conversation about this opportunity?

Best regards,
{recruiter_name}
    """
    
    @classmethod
    def get_rapidapi_key(cls) -> str:
        """Get RapidAPI key from environment or config"""
        return os.getenv('RAPIDAPI_KEY', cls.RAPIDAPI_KEY)
    
    @classmethod
    def get_rapidapi_host(cls) -> str:
        """Get RapidAPI host"""
        return cls.RAPIDAPI_HOST
    
    @classmethod
    def get_openai_key(cls) -> str:
        """Get OpenAI API key from environment or config"""
        return os.getenv('OPENAI_API_KEY', cls.OPENAI_API_KEY)
    
    @classmethod
    def get_anthropic_key(cls) -> str:
        """Get Anthropic API key from environment or config"""
        return os.getenv('ANTHROPIC_API_KEY', cls.ANTHROPIC_API_KEY) 