import requests
from bs4 import BeautifulSoup
import re
import json
from urllib.parse import urlparse, parse_qs

class LinkedInJobParser:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
    
    def extract_job_id_from_url(self, job_url):
        """Extract job ID from LinkedIn job URL"""
        try:
            # Handle different LinkedIn job URL formats
            if "linkedin.com/jobs/view/" in job_url:
                job_id = job_url.split("linkedin.com/jobs/view/")[1].split("?")[0]
            elif "linkedin.com/jobs/collections/" in job_url:
                # Extract from collection URL
                parsed = urlparse(job_url)
                query_params = parse_qs(parsed.query)
                job_id = query_params.get('currentJobId', [None])[0]
            else:
                # Try to extract from any LinkedIn job URL
                match = re.search(r'linkedin\.com/jobs/[^/]+/(\d+)', job_url)
                job_id = match.group(1) if match else None
            
            return job_id
        except Exception as e:
            print(f"Error extracting job ID: {e}")
            return None
    
    def get_job_details(self, job_url):
        """Get job details from LinkedIn job posting"""
        try:
            job_id = self.extract_job_id_from_url(job_url)
            if not job_id:
                return None
            
            # LinkedIn job API endpoint (this is a simplified approach)
            api_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"
            
            response = requests.get(api_url, headers=self.headers)
            if response.status_code != 200:
                print(f"Failed to fetch job details: {response.status_code}")
                return None
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract job information
            job_data = {
                'job_id': job_id,
                'job_url': job_url,
                'title': self._extract_title(soup),
                'company': self._extract_company(soup),
                'location': self._extract_location(soup),
                'description': self._extract_description(soup),
                'requirements': self._extract_requirements(soup),
                'skills': self._extract_skills(soup),
                'industry': self._extract_industry(soup),
                'employment_type': self._extract_employment_type(soup),
                'seniority_level': self._extract_seniority_level(soup)
            }
            
            return job_data
            
        except Exception as e:
            print(f"Error getting job details: {e}")
            return None
    
    def _extract_title(self, soup):
        """Extract job title"""
        title_elem = soup.find('h1', class_='top-card-layout__title')
        if title_elem:
            return title_elem.get_text(strip=True)
        
        # Fallback selectors
        for selector in ['h1', '.job-details-jobs-unified-top-card__job-title']:
            elem = soup.select_one(selector)
            if elem:
                return elem.get_text(strip=True)
        return ""
    
    def _extract_company(self, soup):
        """Extract company name"""
        company_elem = soup.find('a', class_='topcard__org-name-link')
        if company_elem:
            return company_elem.get_text(strip=True)
        
        # Fallback selectors
        for selector in ['.topcard__org-name-link', '.job-details-jobs-unified-top-card__company-name']:
            elem = soup.select_one(selector)
            if elem:
                return elem.get_text(strip=True)
        return ""
    
    def _extract_location(self, soup):
        """Extract job location"""
        location_elem = soup.find('span', class_='topcard__flavor--bullet')
        if location_elem:
            return location_elem.get_text(strip=True)
        
        # Fallback selectors
        for selector in ['.topcard__flavor--bullet', '.job-details-jobs-unified-top-card__bullet']:
            elem = soup.select_one(selector)
            if elem:
                return elem.get_text(strip=True)
        return ""
    
    def _extract_description(self, soup):
        """Extract job description"""
        desc_elem = soup.find('div', class_='show-more-less-html__markup')
        if desc_elem:
            return desc_elem.get_text(strip=True)
        
        # Fallback selectors
        for selector in ['.show-more-less-html__markup', '.job-description']:
            elem = soup.select_one(selector)
            if elem:
                return elem.get_text(strip=True)
        return ""
    
    def _extract_requirements(self, soup):
        """Extract job requirements"""
        description = self._extract_description(soup)
        if not description:
            return []
        
        # Look for common requirement patterns
        requirements = []
        
        # Look for bullet points with requirements
        lines = description.split('\n')
        for line in lines:
            line = line.strip()
            if any(keyword in line.lower() for keyword in ['experience', 'years', 'degree', 'bachelor', 'master', 'phd', 'required', 'must have']):
                requirements.append(line)
        
        return requirements[:10]  # Limit to first 10 requirements
    
    def _extract_skills(self, soup):
        """Extract required skills"""
        description = self._extract_description(soup)
        if not description:
            return []
        
        # Common technical skills to look for
        common_skills = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node.js', 'sql', 'mongodb',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'git', 'agile', 'scrum', 'machine learning',
            'ai', 'data science', 'backend', 'frontend', 'full stack', 'devops', 'cloud', 'api',
            'rest', 'graphql', 'microservices', 'kubernetes', 'jenkins', 'ci/cd', 'testing'
        ]
        
        found_skills = []
        description_lower = description.lower()
        
        for skill in common_skills:
            if skill in description_lower:
                found_skills.append(skill)
        
        return found_skills
    
    def _extract_industry(self, soup):
        """Extract industry information"""
        # This is a simplified extraction - LinkedIn doesn't always expose this easily
        description = self._extract_description(soup)
        if not description:
            return ""
        
        # Look for industry keywords
        industries = [
            'technology', 'healthcare', 'finance', 'education', 'retail', 'manufacturing',
            'consulting', 'media', 'entertainment', 'real estate', 'transportation', 'energy'
        ]
        
        description_lower = description.lower()
        for industry in industries:
            if industry in description_lower:
                return industry
        
        return ""
    
    def _extract_employment_type(self, soup):
        """Extract employment type"""
        description = self._extract_description(soup)
        if not description:
            return ""
        
        description_lower = description.lower()
        
        if 'full-time' in description_lower or 'full time' in description_lower:
            return 'Full-time'
        elif 'part-time' in description_lower or 'part time' in description_lower:
            return 'Part-time'
        elif 'contract' in description_lower:
            return 'Contract'
        elif 'internship' in description_lower or 'intern' in description_lower:
            return 'Internship'
        
        return 'Full-time'  # Default assumption
    
    def _extract_seniority_level(self, soup):
        """Extract seniority level"""
        title = self._extract_title(soup)
        description = self._extract_description(soup)
        
        if not title and not description:
            return "Mid-level"
        
        text = f"{title} {description}".lower()
        
        if any(word in text for word in ['senior', 'lead', 'principal', 'staff', 'architect']):
            return 'Senior'
        elif any(word in text for word in ['junior', 'entry', 'graduate', 'intern']):
            return 'Entry-level'
        elif any(word in text for word in ['director', 'manager', 'head', 'vp', 'cto', 'ceo']):
            return 'Management'
        else:
            return 'Mid-level'

# Example usage
if __name__ == "__main__":
    parser = LinkedInJobParser()
    job_url = "https://www.linkedin.com/jobs/view/4256398535"
    job_details = parser.get_job_details(job_url)
    
    if job_details:
        print("Job Details:")
        print(json.dumps(job_details, indent=2))
    else:
        print("Failed to extract job details") 