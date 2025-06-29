import json
import time
import uuid
from typing import Dict, List, Any
from job_parser import LinkedInJobParser
from linkedin_search import LinkedInProfileSearcher
from scoring import CandidateScorer
from outreach import OutreachGenerator
from gpt_outreach import GPT4OutreachGenerator, GPTOutreach
from enhanced_outreach import EnhancedOutreachGenerator
from config import Config

class JobOrchestrator:
    def __init__(self, use_gpt4: bool = True, use_enhanced: bool = False, use_anthropic: bool = False):
        self.job_parser = LinkedInJobParser()
        self.profile_searcher = LinkedInProfileSearcher()
        self.candidate_scorer = CandidateScorer()
        self.use_gpt4 = use_gpt4
        self.use_enhanced = use_enhanced
        self.use_anthropic = use_anthropic
        
        # Choose outreach generator based on preference
        if use_anthropic:
            self.outreach_generator = GPTOutreach()
            print("🤖 Using Anthropic Claude for outreach message generation")
        elif use_gpt4:
            self.outreach_generator = GPT4OutreachGenerator()
            print("🤖 Using OpenAI GPT-4 for outreach message generation")
        elif use_enhanced:
            self.outreach_generator = EnhancedOutreachGenerator()
            print("🎯 Using enhanced local templates for outreach message generation")
        else:
            self.outreach_generator = OutreachGenerator()
            print("📝 Using basic template-based outreach message generation")
    
    def process_job_posting(self, job_url: str, max_candidates: int = 20) -> Dict[str, Any]:
        """
        Complete workflow: Parse job -> Search profiles -> Score candidates -> Generate outreach
        
        Args:
            job_url: LinkedIn job posting URL to analyze
            max_candidates: Maximum number of candidates to return
            
        Returns:
            Dictionary with job details and scored candidates in required format
        """
        print(f"Processing job posting: {job_url}")
        
        # Handle demo mode
        if job_url == "demo":
            return self._run_demo_mode(max_candidates)
        
        # Step 1: Parse job details
        print("Step 1: Extracting job details...")
        job_details = self.job_parser.get_job_details(job_url)
        if not job_details:
            return {
                'error': 'Failed to extract job details',
                'job_url': job_url
            }
        
        print(f"Job Title: {job_details.get('title', 'N/A')}")
        print(f"Company: {job_details.get('company', 'N/A')}")
        print(f"Location: {job_details.get('location', 'N/A')}")
        print(f"Skills: {', '.join(job_details.get('skills', []))}")
        
        # Step 2: Search for relevant profiles
        print("\nStep 2: Searching for relevant LinkedIn profiles...")
        profiles = self.profile_searcher.search_profiles_for_job(job_details, num_pages=2)
        
        if not profiles:
            return {
                'error': 'No profiles found',
                'job_details': job_details,
                'candidates': []
            }
        
        print(f"Found {len(profiles)} profiles")
        
        # Step 3: Enhance profile data with API
        print("\nStep 3: Enhancing profile data with RapidAPI...")
        enhanced_profiles = []
        
        for i, profile in enumerate(profiles[:max_candidates]):
            print(f"Enhancing profile {i+1}/{min(len(profiles), max_candidates)}: {profile.get('name', 'Unknown')}")
            
            # Get enhanced profile data
            enhanced_data = self.profile_searcher.get_enhanced_profile_data(
                profile.get('url', ''), 
                profile
            )
            
            if enhanced_data:
                enhanced_profiles.append(enhanced_data)
            
            # Rate limiting between API calls
            time.sleep(1)
        
        # Step 4: Score candidates
        print("\nStep 4: Scoring candidates...")
        scored_candidates = []
        
        for i, profile in enumerate(enhanced_profiles):
            print(f"Scoring candidate {i+1}/{len(enhanced_profiles)}: {profile.get('name', 'Unknown')}")
            
            # Calculate fit score
            score_result = self.candidate_scorer.calculate_fit_score(profile, job_details)
            
            # Combine profile data with scoring results
            scored_candidate = {
                'name': profile.get('name', ''),
                'linkedin_url': profile.get('profile_url', profile.get('url', '')),
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
        
        # Sort candidates by fit score
        scored_candidates.sort(key=lambda x: x['fit_score'], reverse=True)
        
        # Step 5: Generate outreach messages (GPT-4, Claude, or templates)
        ai_type = "Claude" if self.use_anthropic else ("GPT-4" if self.use_gpt4 else "templates")
        print(f"\nStep 5: Generating outreach messages using {ai_type}...")
        
        if self.use_anthropic:
            # Handle Anthropic Claude case
            candidates_with_outreach = []
            for i, candidate in enumerate(scored_candidates, 1):
                print(f"   Generating message {i}/{len(scored_candidates)}: {candidate.get('name', 'Unknown')}")
                
                message, source = self.outreach_generator.generate_message(
                    candidate, job_details, "Recruitment Team", use_anthropic=True
                )
                
                if not message:
                    # Fallback to template
                    from outreach import OutreachGenerator
                    template_gen = OutreachGenerator()
                    message = template_gen.generate_outreach_message(candidate, job_details, "Recruitment Team")
                    source = "template"
                
                candidate['outreach_message'] = message
                candidate['message_source'] = source
                candidates_with_outreach.append(candidate)
                
                # Small delay to avoid rate limiting
                time.sleep(0.5)
        else:
            # Handle OpenAI GPT-4 and templates
            candidates_with_outreach = self.outreach_generator.generate_bulk_outreach_messages(
                scored_candidates, 
                job_details, 
                "Recruitment Team"
            )
        
        # Step 6: Format final output
        print("\nStep 6: Formatting final output...")
        final_output = self._format_final_output(job_details, candidates_with_outreach)
        
        return final_output
    
    def _format_final_output(self, job_details: Dict[str, Any], candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Format the final output according to the required structure"""
        
        # Generate job ID
        job_id = self._generate_job_id(job_details)
        
        # Get top candidates (top 10)
        top_candidates = candidates[:10]
        
        return {
            'job_id': job_id,
            'candidates_found': len(candidates),
            'job_details': {
                'title': job_details.get('title', ''),
                'company': job_details.get('company', ''),
                'location': job_details.get('location', ''),
                'skills': job_details.get('skills', []),
                'requirements': job_details.get('requirements', [])
            },
            'top_candidates': top_candidates,
            'processed_at': time.time()
        }
    
    def _generate_job_id(self, job_details: Dict[str, Any]) -> str:
        """Generate a unique job ID based on job details"""
        title = job_details.get('title', '').lower().replace(' ', '-')
        company = job_details.get('company', '').lower().replace(' ', '-')
        location = job_details.get('location', '').lower().replace(' ', '-').replace(',', '')
        
        # Clean up the ID
        job_id = f"{title}-{company}-{location}".replace('--', '-').strip('-')
        
        # Add timestamp for uniqueness
        timestamp = int(time.time())
        
        return f"{job_id}-{timestamp}"
    
    def _run_demo_mode(self, max_candidates: int) -> Dict[str, Any]:
        """Run the system with demo data"""
        # Demo job data
        demo_job = {
            'job_id': 'demo_123',
            'job_url': 'https://www.linkedin.com/jobs/view/demo',
            'title': 'Senior Software Engineer',
            'company': 'TechCorp',
            'location': 'San Francisco, CA',
            'description': 'We are looking for a Senior Software Engineer with experience in Python, JavaScript, and cloud technologies.',
            'requirements': [
                '5+ years of experience in software development',
                'Experience with Python and JavaScript',
                'Knowledge of cloud platforms like AWS',
                'Experience with React and Node.js'
            ],
            'skills': ['Python', 'JavaScript', 'React', 'Node.js', 'AWS', 'Docker'],
            'industry': 'Technology',
            'employment_type': 'Full-time',
            'seniority_level': 'Senior'
        }
        
        # Demo candidate profiles with enhanced data
        demo_profiles = [
            {
                'name': 'Alice Johnson',
                'headline': 'Senior Software Engineer at Google',
                'location': 'San Francisco, CA',
                'profile_url': 'https://linkedin.com/in/demo1',
                'education': [
                    {'school': 'Stanford University', 'degree': 'MS Computer Science'}
                ],
                'experience': [
                    {'title': 'Senior Software Engineer', 'company': 'Google', 'description': 'Python, JavaScript, AWS'}
                ],
                'skills': ['Python', 'JavaScript', 'React', 'AWS', 'Docker']
            },
            {
                'name': 'Bob Smith',
                'headline': 'Lead Developer at Microsoft',
                'location': 'Seattle, WA',
                'profile_url': 'https://linkedin.com/in/demo2',
                'education': [
                    {'school': 'UC Berkeley', 'degree': 'BS Computer Science'}
                ],
                'experience': [
                    {'title': 'Lead Developer', 'company': 'Microsoft', 'description': 'C#, .NET, Azure'}
                ],
                'skills': ['C#', '.NET', 'Azure', 'JavaScript']
            },
            {
                'name': 'Carol Davis',
                'headline': 'Full Stack Engineer at Netflix',
                'location': 'Los Gatos, CA',
                'profile_url': 'https://linkedin.com/in/demo3',
                'education': [
                    {'school': 'MIT', 'degree': 'BS Computer Science'}
                ],
                'experience': [
                    {'title': 'Full Stack Engineer', 'company': 'Netflix', 'description': 'React, Node.js, AWS'}
                ],
                'skills': ['React', 'Node.js', 'JavaScript', 'AWS']
            },
            {
                'name': 'David Wilson',
                'headline': 'Software Engineer at StartupXYZ',
                'location': 'San Francisco, CA',
                'profile_url': 'https://linkedin.com/in/demo4',
                'education': [
                    {'school': 'University of Washington', 'degree': 'BS Computer Science'}
                ],
                'experience': [
                    {'title': 'Software Engineer', 'company': 'StartupXYZ', 'description': 'Python, JavaScript'}
                ],
                'skills': ['Python', 'JavaScript', 'React']
            },
            {
                'name': 'Eva Brown',
                'headline': 'Junior Developer at TechCorp',
                'location': 'Oakland, CA',
                'profile_url': 'https://linkedin.com/in/demo5',
                'education': [
                    {'school': 'San Francisco State University', 'degree': 'BS Computer Science'}
                ],
                'experience': [
                    {'title': 'Junior Developer', 'company': 'TechCorp', 'description': 'JavaScript, HTML, CSS'}
                ],
                'skills': ['JavaScript', 'HTML', 'CSS']
            }
        ]
        
        # Score the demo candidates
        scored_candidates = []
        for profile in demo_profiles[:max_candidates]:
            score_result = self.candidate_scorer.calculate_fit_score(profile, demo_job)
            
            scored_candidate = {
                'name': profile.get('name', ''),
                'linkedin_url': profile.get('profile_url', ''),
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
        
        # Generate outreach messages
        candidates_with_outreach = self.outreach_generator.generate_bulk_outreach_messages(
            scored_candidates, 
            demo_job, 
            "Recruitment Team"
        )
        
        # Format final output
        return self._format_final_output(demo_job, candidates_with_outreach)
    
    def export_results(self, results: Dict[str, Any], filename: str = None) -> str:
        """Export results to JSON file"""
        if not filename:
            job_id = results.get('job_id', 'job')
            timestamp = int(time.time())
            filename = f"candidate_search_{job_id}_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        return filename
    
    def print_results(self, results: Dict[str, Any], max_candidates: int = 10):
        """Print formatted results to console"""
        if 'error' in results:
            print(f"Error: {results['error']}")
            return
        
        job_details = results.get('job_details', {})
        candidates = results.get('top_candidates', [])
        
        print("\n" + "="*80)
        print("LINKEDIN RECRUITMENT AGENT - RESULTS")
        print("="*80)
        
        print(f"\nJob ID: {results.get('job_id', 'N/A')}")
        print(f"Job: {job_details.get('title', 'N/A')}")
        print(f"Company: {job_details.get('company', 'N/A')}")
        print(f"Location: {job_details.get('location', 'N/A')}")
        print(f"Skills: {', '.join(job_details.get('skills', []))}")
        
        print(f"\nTotal Candidates Found: {results.get('candidates_found', 0)}")
        
        print("\n🏆 TOP CANDIDATES:")
        print("-" * 80)
        
        for i, candidate in enumerate(candidates[:max_candidates]):
            print(f"\n{i+1}. {candidate['name']}")
            print(f"   📝 Headline: {candidate['headline']}")
            print(f"   📍 Location: {candidate.get('location', 'N/A')}")
            print(f"   ⭐ Fit Score: {candidate['fit_score']:.2f}/10")
            print(f"   🔗 LinkedIn: {candidate['linkedin_url']}")
            
            # Show score breakdown
            breakdown = candidate['score_breakdown']
            print(f"   📊 Score Breakdown:")
            print(f"      Education: {breakdown.get('education', 0):.1f}/10")
            print(f"      Trajectory: {breakdown.get('trajectory', 0):.1f}/10")
            print(f"      Company: {breakdown.get('company', 0):.1f}/10")
            print(f"      Skills: {breakdown.get('skills', 0):.1f}/10")
            print(f"      Location: {breakdown.get('location', 0):.1f}/10")
            print(f"      Tenure: {breakdown.get('tenure', 0):.1f}/10")
            
            # Show outreach message preview
            if 'outreach_message' in candidate:
                message_preview = candidate['outreach_message'][:100] + "..." if len(candidate['outreach_message']) > 100 else candidate['outreach_message']
                print(f"   💬 Outreach: {message_preview}")
        
        print("\n" + "="*80)

# Example usage
if __name__ == "__main__":
    orchestrator = JobOrchestrator()
    
    # Test with demo data
    results = orchestrator.process_job_posting("demo", max_candidates=5)
    
    # Print results
    orchestrator.print_results(results, max_candidates=3)
    
    # Export results
    filename = orchestrator.export_results(results)
    print(f"\nResults exported to: {filename}")
