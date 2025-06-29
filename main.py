#!/usr/bin/env python3
"""
LinkedIn Recruitment Agent
==========================

A comprehensive AI-powered tool for finding, scoring, and outreaching to LinkedIn candidates based on job postings.
Features job parsing, profile search, AI scoring, and GPT-4 powered personalized outreach messages.

Usage:
    python main.py <job_url>
    python main.py --demo
    python main.py --help
"""

import sys
import argparse
from job_orchestrator import JobOrchestrator

def main():
    parser = argparse.ArgumentParser(
        description="LinkedIn Recruitment Agent - Find, score, and outreach to candidates with GPT-4",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py https://www.linkedin.com/jobs/view/4256398535
  python main.py --demo
  python main.py --max-candidates 30 https://www.linkedin.com/jobs/view/4256398535
  python main.py --export --demo
  python main.py --templates --demo  # Use templates instead of GPT-4
        """
    )
    
    parser.add_argument(
        'job_url',
        nargs='?',
        help='LinkedIn job posting URL to analyze'
    )
    
    parser.add_argument(
        '--demo',
        action='store_true',
        help='Run with demo job data instead of scraping LinkedIn'
    )
    
    parser.add_argument(
        '--max-candidates',
        type=int,
        default=20,
        help='Maximum number of candidates to analyze (default: 20)'
    )
    
    parser.add_argument(
        '--export',
        action='store_true',
        help='Export results to JSON file'
    )
    
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress detailed output, show only summary'
    )
    
    parser.add_argument(
        '--recruiter-name',
        type=str,
        default='Recruitment Team',
        help='Name to use in outreach messages (default: "Recruitment Team")'
    )
    
    parser.add_argument(
        '--templates',
        action='store_true',
        help='Use template-based outreach messages instead of GPT-4 (fallback option)'
    )
    
    parser.add_argument(
        '--enhanced',
        action='store_true',
        help='Use enhanced local templates instead of GPT-4'
    )
    
    parser.add_argument(
        '--anthropic',
        action='store_true',
        help='Use Anthropic Claude instead of OpenAI GPT-4'
    )
    
    args = parser.parse_args()
    
    if not args.job_url and not args.demo:
        parser.print_help()
        return
    
    print("🚀 LinkedIn Recruitment Agent")
    print("=" * 60)
    print("Features: Job Parsing | Profile Search | AI Scoring | GPT-4/Claude Outreach")
    print("=" * 60)
    
    # Determine outreach method - GPT-4 is default unless specified otherwise
    use_gpt4 = not args.templates and not args.enhanced and not args.anthropic  # Default to GPT-4
    use_enhanced = args.enhanced
    use_anthropic = args.anthropic
    
    orchestrator = JobOrchestrator(use_gpt4=use_gpt4, use_enhanced=use_enhanced, use_anthropic=use_anthropic)
    
    try:
        if args.demo:
            # Run with demo data
            print("🎯 Running with demo data...")
            results = orchestrator.process_job_posting("demo", args.max_candidates)
        else:
            # Process actual job URL
            print(f"🔍 Processing job URL: {args.job_url}")
            results = orchestrator.process_job_posting(args.job_url, args.max_candidates)
        
        if 'error' in results:
            print(f"\n❌ Error: {results['error']}")
            return
        
        # Print results
        if not args.quiet:
            orchestrator.print_results(results, max_candidates=10)
        else:
            print_summary(results)
        
        # Export if requested
        if args.export:
            filename = orchestrator.export_results(results)
            print(f"\n💾 Results exported to: {filename}")
        
        print("\n✅ Process completed successfully!")
        print("\n📋 Next Steps:")
        print("   • Review the top candidates above")
        print("   • Use the outreach messages to contact candidates")
        print("   • Export results for further analysis")
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Operation cancelled by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("This might be due to LinkedIn's anti-scraping measures or network issues.")
        print("Try running with --demo to test the system with sample data.")

def print_summary(results):
    """Print a brief summary of results"""
    job_details = results.get('job_details', {})
    
    print(f"\n📊 SUMMARY")
    print(f"Job ID: {results.get('job_id', 'N/A')}")
    print(f"Position: {job_details.get('title', 'N/A')} at {job_details.get('company', 'N/A')}")
    print(f"Location: {job_details.get('location', 'N/A')}")
    print(f"Total Candidates Found: {results.get('candidates_found', 0)}")
    
    top_candidates = results.get('top_candidates', [])
    if top_candidates:
        print(f"\n🏆 Top 3 Candidates:")
        for i, candidate in enumerate(top_candidates[:3]):
            print(f"  {i+1}. {candidate['name']} - {candidate['fit_score']:.2f}/10")
            print(f"     {candidate['headline']}")
    else:
        print("No candidates found")

def run_demo_test():
    """Run a quick demo test to verify the system"""
    print("🧪 Running system test...")
    
    orchestrator = JobOrchestrator()
    results = orchestrator.process_job_posting("demo", max_candidates=3)
    
    if 'error' not in results:
        print("✅ System test passed!")
        print(f"Found {results.get('candidates_found', 0)} candidates")
        print(f"Top candidate: {results.get('top_candidates', [{}])[0].get('name', 'N/A')}")
    else:
        print(f"❌ System test failed: {results['error']}")

if __name__ == "__main__":
    main()
