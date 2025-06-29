import requests
from bs4 import BeautifulSoup
import re
import time
import json
from urllib.parse import quote_plus
from job_parser import LinkedInJobParser
from config import Config

class LinkedInProfileSearcher:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        self.rapidapi_headers = {
            "X-RapidAPI-Key": Config.get_rapidapi_key(),
            "X-RapidAPI-Host": Config.get_rapidapi_host()
        }
        self.job_parser = LinkedInJobParser()
    
    def search_profiles_for_job(self, job_details, num_pages=3, delay=2):
        """
        Search for LinkedIn profiles based on job details
        """
        print(f"Searching for profiles matching: {job_details.get('title', 'N/A')} at {job_details.get('company', 'N/A')}")
        
        # Generate search queries based on job details
        search_queries = self._generate_search_queries(job_details)
        
        all_profiles = []
        
        # Search using different methods
        for query_info in search_queries:
            print(f"Searching with query: {query_info['query']}")
            
            # Google search
            google_results = self._google_linkedin_search(
                query_info['query'], 
                num_pages=num_pages, 
                delay=delay
            )
            
            # Add source information
            for profile in google_results:
                profile['search_source'] = 'google'
                profile['search_query'] = query_info['query']
                profile['job_match_score'] = query_info['relevance_score']
            
            all_profiles.extend(google_results)
            time.sleep(delay)
        
        # Remove duplicates based on profile URL
        unique_profiles = self._remove_duplicates(all_profiles)
        
        # Sort by relevance
        unique_profiles.sort(key=lambda x: x.get('job_match_score', 0), reverse=True)
        
        return unique_profiles[:50]  # Return top 50 results
    
    def get_profile_details_via_api(self, profile_url: str) -> dict:
        """
        Fetch detailed profile information using RapidAPI LinkedIn Data API
        """
        try:
            # Extract username from LinkedIn URL
            username = self._extract_username_from_url(profile_url)
            if not username:
                return None
            
            # API endpoint for profile data
            url = "https://linkedin-profile-data.p.rapidapi.com/profile"
            
            querystring = {"linkedin_url": profile_url}
            
            response = requests.get(url, headers=self.rapidapi_headers, params=querystring, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_api_response(data)
            else:
                print(f"API request failed with status {response.status_code}: {response.text}")
                return None
                
        except Exception as e:
            print(f"Error fetching profile via API: {e}")
            return None
    
    def _extract_username_from_url(self, profile_url: str) -> str:
        """Extract username from LinkedIn profile URL"""
        try:
            # Handle different LinkedIn URL formats
            if "linkedin.com/in/" in profile_url:
                username = profile_url.split("linkedin.com/in/")[1].split("?")[0].split("/")[0]
                return username
            return None
        except:
            return None
    
    def _parse_api_response(self, api_data: dict) -> dict:
        """Parse RapidAPI response into our standard format"""
        try:
            profile_data = {
                'name': api_data.get('full_name', ''),
                'headline': api_data.get('headline', ''),
                'location': api_data.get('location', ''),
                'summary': api_data.get('summary', ''),
                'profile_url': api_data.get('linkedin_url', ''),
                'education': [],
                'experience': [],
                'skills': []
            }
            
            # Parse education
            if 'education' in api_data:
                for edu in api_data['education']:
                    profile_data['education'].append({
                        'school': edu.get('school', ''),
                        'degree': edu.get('degree', ''),
                        'field': edu.get('field_of_study', ''),
                        'start_date': edu.get('start_date', ''),
                        'end_date': edu.get('end_date', '')
                    })
            
            # Parse experience
            if 'experience' in api_data:
                for exp in api_data['experience']:
                    profile_data['experience'].append({
                        'title': exp.get('title', ''),
                        'company': exp.get('company', ''),
                        'description': exp.get('description', ''),
                        'start_date': exp.get('start_date', ''),
                        'end_date': exp.get('end_date', ''),
                        'location': exp.get('location', '')
                    })
            
            # Parse skills
            if 'skills' in api_data:
                profile_data['skills'] = [skill.get('name', '') for skill in api_data['skills']]
            
            return profile_data
            
        except Exception as e:
            print(f"Error parsing API response: {e}")
            return None
    
    def get_enhanced_profile_data(self, profile_url: str, basic_data: dict) -> dict:
        """
        Get enhanced profile data using API, with fallback to basic data
        """
        print(f"Fetching detailed data for: {profile_url}")
        
        # Try API first
        api_data = self.get_profile_details_via_api(profile_url)
        
        if api_data:
            print("✅ Successfully fetched data via API")
            return api_data
        else:
            print("⚠️ API failed, using basic data from search results")
            # Return enhanced basic data
            return {
                'name': basic_data.get('name', ''),
                'headline': basic_data.get('headline', ''),
                'location': basic_data.get('location', ''),
                'profile_url': profile_url,
                'education': [],  # Would need to be extracted from snippet
                'experience': [],  # Would need to be extracted from snippet
                'skills': [],  # Would need to be extracted from snippet
                'summary': basic_data.get('snippet', '')
            }
    
    def _generate_search_queries(self, job_details):
        """
        Generate multiple search queries based on job details
        """
        queries = []
        
        # Extract key information
        title = job_details.get('title', '')
        company = job_details.get('company', '')
        location = job_details.get('location', '')
        skills = job_details.get('skills', [])
        industry = job_details.get('industry', '')
        seniority = job_details.get('seniority_level', '')
        
        # Query 1: Exact title + company + location (highest relevance)
        if title and company and location:
            query = f'site:linkedin.com/in "{title}" "{company}" "{location}"'
            queries.append({
                'query': query,
                'relevance_score': 10
            })
        
        # Query 2: Title + location (high relevance)
        if title and location:
            query = f'site:linkedin.com/in "{title}" "{location}"'
            queries.append({
                'query': query,
                'relevance_score': 8
            })
        
        # Query 3: Title + company (high relevance)
        if title and company:
            query = f'site:linkedin.com/in "{title}" "{company}"'
            queries.append({
                'query': query,
                'relevance_score': 8
            })
        
        # Query 4: Skills + location (medium relevance)
        if skills and location:
            for skill in skills[:3]:  # Top 3 skills
                query = f'site:linkedin.com/in "{skill}" "{location}"'
                queries.append({
                    'query': query,
                    'relevance_score': 6
                })
        
        return queries
    
    def _google_linkedin_search(self, query, num_pages=2, delay=2):
        """
        Search Google for LinkedIn profiles matching the query.
        Returns a list of dicts: [{url, name, headline, location, snippet}]
        """
        results = []
        
        for page in range(num_pages):
            start = page * 10
            url = f"https://www.google.com/search?q={quote_plus(query)}&start={start}"
            
            try:
                resp = requests.get(url, headers=self.headers, timeout=10)
                if resp.status_code != 200:
                    print(f"Google search failed with status {resp.status_code}")
                    continue
                
                soup = BeautifulSoup(resp.text, "html.parser")
                
                # Find search results
                search_results = soup.find_all('div', class_='g')
                if not search_results:
                    # Try alternative selectors
                    search_results = soup.find_all('div', {'data-sokoban-container': True})
                
                for result in search_results:
                    profile_data = self._extract_profile_from_result(result)
                    if profile_data:
                        results.append(profile_data)
                
                time.sleep(delay)  # Rate limiting
                
            except Exception as e:
                print(f"Error in Google search: {e}")
                continue
        
        return results
    
    def _extract_profile_from_result(self, result_div):
        """
        Extract profile information from a Google search result
        """
        try:
            # Find the link
            link_elem = result_div.find('a', href=True)
            if not link_elem or "linkedin.com/in/" not in link_elem['href']:
                return None
            
            profile_url = link_elem['href']
            
            # Clean the URL (remove Google redirect) - Fixed error handling
            if 'google.com/url?' in profile_url:
                try:
                    from urllib.parse import urlparse, parse_qs
                    parsed = urlparse(profile_url)
                    query_params = parse_qs(parsed.query)
                    
                    # Try multiple possible parameter names for the actual URL
                    actual_url = None
                    for param in ['q', 'url', 'u', 'link']:
                        if param in query_params:
                            actual_url = query_params[param][0]
                            break
                    
                    if actual_url and "linkedin.com/in/" in actual_url:
                        profile_url = actual_url
                except Exception as e:
                    # If parsing fails, keep the original URL
                    print(f"Warning: Could not parse Google redirect URL: {e}")
                    pass
            
            # Get the snippet text
            snippet_elem = result_div.find('div', class_='VwiC3b')
            if not snippet_elem:
                snippet_elem = result_div.find('span', class_='aCOpRe')
            
            snippet = snippet_elem.get_text(separator=" ", strip=True) if snippet_elem else ""
            
            # Extract profile information
            name, headline, location = self._extract_profile_info_from_snippet(snippet)
            
            return {
                "url": profile_url,
                "name": name,
                "headline": headline,
                "location": location,
                "snippet": snippet,
                "extracted_at": time.time()
            }
            
        except Exception as e:
            print(f"Error extracting profile from result: {e}")
            return None
    
    def _extract_profile_info_from_snippet(self, snippet):
        """
        Extract name, headline, and location from LinkedIn snippet
        """
        if not snippet:
            return "", "", ""
        
        # LinkedIn snippets typically follow pattern: "Name - Title at Company - Location"
        parts = snippet.split(" - ")
        
        name = parts[0].strip() if len(parts) > 0 else ""
        headline = parts[1].strip() if len(parts) > 1 else ""
        location = ""
        
        # Try to extract location from the last part or using regex
        if len(parts) > 2:
            location = parts[2].strip()
        else:
            # Look for location patterns in the entire snippet
            location_patterns = [
                r'([A-Z][a-z]+(?:[\s,]+[A-Z][a-z]+)*\s*(?:City|County|State|Province|Country))',
                r'([A-Z][a-z]+(?:[\s,]+[A-Z][a-z]+)*)',
                r'(Remote|On-site|Hybrid)'
            ]
            
            for pattern in location_patterns:
                match = re.search(pattern, snippet)
                if match:
                    location = match.group(1)
                    break
        
        return name, headline, location
    
    def _remove_duplicates(self, profiles):
        """
        Remove duplicate profiles based on URL
        """
        seen_urls = set()
        unique_profiles = []
        
        for profile in profiles:
            url = profile.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_profiles.append(profile)
        
        return unique_profiles
    
    def search_with_rapidapi(self, query, api_key=None):
        """
        Search using RapidAPI LinkedIn Data API (requires API key)
        """
        if not api_key:
            print("RapidAPI key not provided, skipping RapidAPI search")
            return []
        
        # This is a placeholder for RapidAPI integration
        # You would need to implement the actual API calls here
        print("RapidAPI search not implemented yet")
        return []
    
    def extract_candidate_data(self, profile_url):
        """
        Extract detailed candidate data from a LinkedIn profile URL
        Note: This is a simplified version - full profile scraping requires authentication
        """
        try:
            response = requests.get(profile_url, headers=self.headers, timeout=10)
            if response.status_code != 200:
                return None
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Extract basic information (this is limited without authentication)
            candidate_data = {
                'profile_url': profile_url,
                'name': self._extract_name_from_profile(soup),
                'headline': self._extract_headline_from_profile(soup),
                'location': self._extract_location_from_profile(soup),
                'summary': self._extract_summary_from_profile(soup),
                'experience': self._extract_experience_from_profile(soup),
                'education': self._extract_education_from_profile(soup),
                'skills': self._extract_skills_from_profile(soup)
            }
            
            return candidate_data
            
        except Exception as e:
            print(f"Error extracting candidate data: {e}")
            return None
    
    def _extract_name_from_profile(self, soup):
        """Extract name from profile page"""
        name_elem = soup.find('h1', class_='text-heading-xlarge')
        if name_elem:
            return name_elem.get_text(strip=True)
        return ""
    
    def _extract_headline_from_profile(self, soup):
        """Extract headline from profile page"""
        headline_elem = soup.find('div', class_='text-body-medium')
        if headline_elem:
            return headline_elem.get_text(strip=True)
        return ""
    
    def _extract_location_from_profile(self, soup):
        """Extract location from profile page"""
        location_elem = soup.find('span', class_='text-body-small')
        if location_elem:
            return location_elem.get_text(strip=True)
        return ""
    
    def _extract_summary_from_profile(self, soup):
        """Extract summary from profile page"""
        summary_elem = soup.find('div', class_='pv-shared-text-with-see-more')
        if summary_elem:
            return summary_elem.get_text(strip=True)
        return ""
    
    def _extract_experience_from_profile(self, soup):
        """Extract experience from profile page"""
        # This is a simplified extraction
        experience_section = soup.find('section', {'id': 'experience'})
        if experience_section:
            experiences = []
            for exp in experience_section.find_all('li', class_='artdeco-list__item'):
                title_elem = exp.find('h3')
                company_elem = exp.find('p', class_='pv-entity__secondary-title')
                
                if title_elem and company_elem:
                    experiences.append({
                        'title': title_elem.get_text(strip=True),
                        'company': company_elem.get_text(strip=True)
                    })
            
            return experiences
        return []
    
    def _extract_education_from_profile(self, soup):
        """Extract education from profile page"""
        # This is a simplified extraction
        education_section = soup.find('section', {'id': 'education'})
        if education_section:
            education = []
            for edu in education_section.find_all('li', class_='artdeco-list__item'):
                school_elem = edu.find('h3')
                degree_elem = edu.find('p', class_='pv-entity__secondary-title')
                
                if school_elem and degree_elem:
                    education.append({
                        'school': school_elem.get_text(strip=True),
                        'degree': degree_elem.get_text(strip=True)
                    })
            
            return education
        return []
    
    def _extract_skills_from_profile(self, soup):
        """Extract skills from profile page"""
        # This is a simplified extraction
        skills_section = soup.find('section', {'id': 'skills'})
        if skills_section:
            skills = []
            for skill in skills_section.find_all('span', class_='pv-skill-category-entity__name-text'):
                skills.append(skill.get_text(strip=True))
            return skills
        return []

# Example usage
if __name__ == "__main__":
    # Test with sample job data
    sample_job = {
        'title': 'Software Engineer',
        'company': 'Google',
        'location': 'San Francisco',
        'skills': ['Python', 'JavaScript', 'React'],
        'industry': 'Technology',
        'seniority_level': 'Mid-level'
    }
    
    searcher = LinkedInProfileSearcher()
    profiles = searcher.search_profiles_for_job(sample_job, num_pages=1)
    
    print(f"Found {len(profiles)} profiles")
    for i, profile in enumerate(profiles[:3]):  # Show first 3
        print(f"\nProfile {i+1}:")
        print(f"Name: {profile.get('name', 'N/A')}")
        print(f"Headline: {profile.get('headline', 'N/A')}")
        print(f"Location: {profile.get('location', 'N/A')}")
        print(f"URL: {profile.get('url', 'N/A')}")
        print(f"Relevance Score: {profile.get('job_match_score', 'N/A')}")