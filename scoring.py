import re
from typing import Dict, List, Any
from config import Config

class CandidateScorer:
    def __init__(self):
        # Elite schools list
        self.elite_schools = {
            'mit', 'stanford', 'harvard', 'caltech', 'princeton', 'yale', 'columbia',
            'university of pennsylvania', 'upenn', 'university of chicago', 'northwestern',
            'duke', 'johns hopkins', 'carnegie mellon', 'cmu', 'berkeley', 'ucla',
            'university of michigan', 'georgia tech', 'gatech', 'cornell', 'brown',
            'dartmouth', 'vanderbilt', 'rice', 'washington university', 'washu',
            'university of southern california', 'usc', 'new york university', 'nyu',
            'university of texas at austin', 'ut austin', 'university of illinois',
            'uiuc', 'purdue', 'university of wisconsin', 'university of maryland',
            'university of virginia', 'uva', 'university of north carolina', 'unc'
        }
        
        # Top tech companies
        self.top_tech_companies = {
            'google', 'alphabet', 'microsoft', 'apple', 'amazon', 'meta', 'facebook',
            'netflix', 'tesla', 'nvidia', 'intel', 'amd', 'oracle', 'salesforce',
            'adobe', 'cisco', 'ibm', 'dell', 'hp', 'hewlett-packard', 'vmware',
            'palantir', 'airbnb', 'uber', 'lyft', 'twitter', 'linkedin', 'dropbox',
            'slack', 'zoom', 'stripe', 'square', 'paypal', 'shopify', 'twilio',
            'databricks', 'snowflake', 'mongodb', 'elastic', 'atlassian', 'jira',
            'confluence', 'github', 'gitlab', 'docker', 'kubernetes', 'hashicorp'
        }
        
        # Common technical skills
        self.technical_skills = {
            'python', 'java', 'javascript', 'typescript', 'react', 'angular', 'vue',
            'node.js', 'express', 'django', 'flask', 'spring', 'sql', 'mysql',
            'postgresql', 'mongodb', 'redis', 'aws', 'azure', 'gcp', 'docker',
            'kubernetes', 'git', 'jenkins', 'ci/cd', 'agile', 'scrum', 'machine learning',
            'ai', 'data science', 'backend', 'frontend', 'full stack', 'devops',
            'cloud', 'api', 'rest', 'graphql', 'microservices', 'testing', 'tdd',
            'bdd', 'selenium', 'junit', 'pytest', 'jest', 'cypress', 'terraform',
            'ansible', 'chef', 'puppet', 'elasticsearch', 'kafka', 'rabbitmq',
            'nginx', 'apache', 'linux', 'unix', 'bash', 'shell scripting'
        }
    
    def calculate_fit_score(self, candidate_data: Dict[str, Any], job_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate comprehensive fit score for a candidate based on job requirements
        
        Args:
            candidate_data: Dictionary containing candidate information
            job_requirements: Dictionary containing job requirements
            
        Returns:
            Dictionary with detailed scoring breakdown matching required format
        """
        scores = {}
        
        # Education Score (20%)
        education_score = self._score_education(candidate_data.get('education', []))
        scores['education'] = education_score
        
        # Career Trajectory Score (20%)
        trajectory_score = self._score_career_trajectory(candidate_data.get('experience', []))
        scores['trajectory'] = trajectory_score
        
        # Company Relevance Score (15%)
        company_score = self._score_company_relevance(candidate_data.get('experience', []))
        scores['company'] = company_score
        
        # Experience Match Score (25%)
        skills_score = self._score_experience_match(candidate_data, job_requirements)
        scores['skills'] = skills_score
        
        # Location Match Score (10%)
        location_score = self._score_location_match(candidate_data.get('location', ''), job_requirements.get('location', ''))
        scores['location'] = location_score
        
        # Tenure Score (10%)
        tenure_score = self._score_tenure(candidate_data.get('experience', []))
        scores['tenure'] = tenure_score
        
        # Calculate total weighted score
        total_score = (
            education_score * Config.SCORING_WEIGHTS['education'] +
            trajectory_score * Config.SCORING_WEIGHTS['trajectory'] +
            company_score * Config.SCORING_WEIGHTS['company'] +
            skills_score * Config.SCORING_WEIGHTS['skills'] +
            location_score * Config.SCORING_WEIGHTS['location'] +
            tenure_score * Config.SCORING_WEIGHTS['tenure']
        )
        
        return {
            'fit_score': round(total_score, 2),
            'score_breakdown': scores,
            'overall_grade': self._get_grade(total_score),
            'recommendation': self._get_recommendation(total_score)
        }
    
    def _score_education(self, education: List[Dict]) -> float:
        """Score education based on school prestige and degree progression"""
        if not education:
            return 5.0  # Neutral score for no education data
        
        max_score = 0
        for edu in education:
            school = edu.get('school', '').lower()
            degree = edu.get('degree', '').lower()
            
            # Check for elite schools
            if any(elite in school for elite in self.elite_schools):
                score = 9.5
            elif any(keyword in school for keyword in ['university', 'college', 'institute']):
                score = 7.0
            else:
                score = 5.0
            
            # Check for degree progression
            if any(level in degree for level in ['phd', 'doctorate']):
                score += 1.0
            elif any(level in degree for level in ['master', 'mba', 'ms', 'ma']):
                score += 0.5
            
            max_score = max(max_score, min(score, 10.0))
        
        return max_score
    
    def _score_career_trajectory(self, experience: List[Dict]) -> float:
        """Score career trajectory based on progression and growth"""
        if not experience or len(experience) < 2:
            return 5.0  # Neutral score for insufficient data
        
        # Analyze progression patterns
        progression_score = 0
        total_experience = len(experience)
        
        for i in range(1, len(experience)):
            current = experience[i]
            previous = experience[i-1]
            
            # Check for title progression
            current_title = current.get('title', '').lower()
            previous_title = previous.get('title', '').lower()
            
            # Simple progression indicators
            if any(word in current_title for word in ['senior', 'lead', 'principal', 'staff']):
                if not any(word in previous_title for word in ['senior', 'lead', 'principal', 'staff']):
                    progression_score += 2
            elif any(word in current_title for word in ['manager', 'director', 'head']):
                if not any(word in previous_title for word in ['manager', 'director', 'head']):
                    progression_score += 3
        
        # Normalize score
        if total_experience > 1:
            avg_progression = progression_score / (total_experience - 1)
            return min(avg_progression + 5, 10.0)  # Base 5 + progression
        else:
            return 5.0
    
    def _score_company_relevance(self, experience: List[Dict]) -> float:
        """Score company relevance based on tech company experience"""
        if not experience:
            return 5.0
        
        relevant_companies = 0
        total_companies = len(experience)
        
        for exp in experience:
            company = exp.get('company', '').lower()
            
            if any(tech_company in company for tech_company in self.top_tech_companies):
                relevant_companies += 1
        
        if total_companies > 0:
            relevance_ratio = relevant_companies / total_companies
            if relevance_ratio >= 0.8:
                return 9.5
            elif relevance_ratio >= 0.6:
                return 8.0
            elif relevance_ratio >= 0.4:
                return 7.0
            elif relevance_ratio >= 0.2:
                return 6.0
            else:
                return 5.0
        
        return 5.0
    
    def _score_experience_match(self, candidate_data: Dict, job_requirements: Dict) -> float:
        """Score experience match based on skills and requirements"""
        candidate_skills = set()
        
        # Extract skills from various sources
        if 'skills' in candidate_data:
            candidate_skills.update(skill.lower() for skill in candidate_data['skills'])
        
        if 'experience' in candidate_data:
            for exp in candidate_data['experience']:
                title = exp.get('title', '').lower()
                description = exp.get('description', '').lower()
                
                # Extract skills from title and description
                for skill in self.technical_skills:
                    if skill in title or skill in description:
                        candidate_skills.add(skill)
        
        # Get job requirements
        job_skills = set()
        if 'skills' in job_requirements:
            job_skills.update(skill.lower() for skill in job_requirements['skills'])
        
        if 'requirements' in job_requirements:
            for req in job_requirements['requirements']:
                req_lower = req.lower()
                for skill in self.technical_skills:
                    if skill in req_lower:
                        job_skills.add(skill)
        
        # Calculate match
        if not job_skills:
            return 5.0  # Neutral if no job skills specified
        
        if candidate_skills and job_skills:
            match_ratio = len(candidate_skills.intersection(job_skills)) / len(job_skills)
            
            if match_ratio >= 0.8:
                return 9.5
            elif match_ratio >= 0.6:
                return 8.0
            elif match_ratio >= 0.4:
                return 7.0
            elif match_ratio >= 0.2:
                return 6.0
            else:
                return 5.0
        
        return 5.0
    
    def _score_location_match(self, candidate_location: str, job_location: str) -> float:
        """Score location match"""
        if not candidate_location or not job_location:
            return 6.0  # Neutral for remote-friendly positions
        
        candidate_loc = candidate_location.lower()
        job_loc = job_location.lower()
        
        # Exact city match
        if candidate_loc == job_loc:
            return 10.0
        
        # Same metro area (simplified)
        if any(city in candidate_loc for city in ['san francisco', 'san jose', 'oakland']) and \
           any(city in job_loc for city in ['san francisco', 'san jose', 'oakland']):
            return 8.0
        
        if any(city in candidate_loc for city in ['new york', 'brooklyn', 'queens']) and \
           any(city in job_loc for city in ['new york', 'brooklyn', 'queens']):
            return 8.0
        
        # Remote indicators
        if 'remote' in candidate_loc or 'remote' in job_loc:
            return 6.0
        
        # Same state
        if any(state in candidate_loc for state in ['california', 'ca']) and \
           any(state in job_loc for state in ['california', 'ca']):
            return 7.0
        
        return 4.0  # Different locations
    
    def _score_tenure(self, experience: List[Dict]) -> float:
        """Score tenure based on job stability"""
        if not experience:
            return 5.0
        
        # Calculate average tenure (simplified - assuming 2 years per role if no dates)
        avg_tenure = 2.0  # Default assumption
        
        if len(experience) > 1:
            # Simple heuristic: more roles = potentially shorter tenure
            avg_tenure = 2.0 / len(experience)
        
        if avg_tenure >= 2.0:
            return 9.5
        elif avg_tenure >= 1.5:
            return 8.0
        elif avg_tenure >= 1.0:
            return 6.0
        else:
            return 3.0  # Job hopping
    
    def _get_grade(self, total_score: float) -> str:
        """Convert score to letter grade"""
        if total_score >= 8.5:
            return 'A'
        elif total_score >= 7.5:
            return 'B+'
        elif total_score >= 6.5:
            return 'B'
        elif total_score >= 5.5:
            return 'C+'
        elif total_score >= 4.5:
            return 'C'
        else:
            return 'D'
    
    def _get_recommendation(self, total_score: float) -> str:
        """Get recommendation based on score"""
        if total_score >= 8.0:
            return "Strongly Recommend"
        elif total_score >= 7.0:
            return "Recommend"
        elif total_score >= 6.0:
            return "Consider"
        elif total_score >= 5.0:
            return "Weak Match"
        else:
            return "Not Recommended"

# Example usage
if __name__ == "__main__":
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
    
    # Calculate score
    score_result = scorer.calculate_fit_score(candidate_data, job_requirements)
    
    print("Candidate Scoring Results:")
    print(f"Total Score: {score_result['fit_score']}/10")
    print(f"Grade: {score_result['overall_grade']}")
    print(f"Recommendation: {score_result['recommendation']}")
    print("\nDetailed Breakdown:")
    
    for category, score in score_result['score_breakdown'].items():
        print(f"{category}: {score:.1f}/10")
