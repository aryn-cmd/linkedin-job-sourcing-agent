#  LinkedIn Recruitment Agent

> **Note:** By default, the system uses OpenAI's `gpt-3.5-turbo` for outreach messages. You can also use Anthropic Claude or switch to GPT-4 if you have access.

A comprehensive AI-powered tool for finding, scoring, and outreaching to LinkedIn candidates based on job postings. Features job parsing, profile search, AI scoring, and AI-powered personalized outreach messages using OpenAI GPT-4 or Anthropic Claude.

##  Features

- **Job Parsing**: Extract detailed job requirements from LinkedIn job postings
- **Profile Search**: Find relevant candidates using Google search and RapidAPI
- **AI Scoring**: Intelligent candidate scoring based on education, experience, skills, and fit
- **AI Outreach**: Generate personalized outreach messages using OpenAI GPT-4 or Anthropic Claude
- **Template Fallback**: Template-based messages when AI is unavailable
- **Export Results**: Export candidate data to JSON format
- **Demo Mode**: Test the system with sample data

##  Prerequisites

- Python 3.8+
- OpenAI API key (for GPT-4 messages) - **OR** - Anthropic API key (for Claude messages)
- RapidAPI key (for LinkedIn profile data)

##  Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd synapse-challenge-agent
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up API keys:**

### Option 1: OpenAI API Key Setup (for GPT-4 messages)

#### Get Free OpenAI API Key:
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Click "Sign Up" and create an account
3. Navigate to [API Keys](https://platform.openai.com/api-keys)
4. Click "Create new secret key"
5. Copy your API key

#### Free Tier Information:
- **Free Credits**: $5 worth of API credits upon signup
- **GPT-4 Cost**: ~$0.03 per 1K tokens (roughly 750 words)
- **Typical Usage**: ~$0.01-0.05 per outreach message
- **Free Credits Duration**: Expires after 3 months

#### Set API Key:
```bash
# Option 1: Environment variable (recommended)
export OPENAI_API_KEY="your-openai-api-key-here"

# Option 2: Windows PowerShell
$env:OPENAI_API_KEY="your-openai-api-key-here"

# Option 3: Edit config.py directly
# Add your key to the OPENAI_API_KEY variable in config.py
```

### Option 2: Anthropic API Key Setup (for Claude messages) - **FREE TIER AVAILABLE**

#### Get Free Anthropic API Key:
1. Go to [Anthropic Console](https://console.anthropic.com/)
2. Sign up for a free account
3. Navigate to API Keys section
4. Create a new API key
5. Copy your API key

#### Free Tier Information:
- **Free Messages**: 5 messages per day with Claude 3.5 Sonnet
- **Cost**: Free tier available
- **Typical Usage**: Perfect for testing and small campaigns

#### Set API Key:
```bash
# Option 1: Environment variable (recommended)
export ANTHROPIC_API_KEY="your-anthropic-api-key-here"

# Option 2: Windows PowerShell
$env:ANTHROPIC_API_KEY="your-anthropic-api-key-here"

# Option 3: Edit config.py directly
# Add your key to the ANTHROPIC_API_KEY variable in config.py
```

### RapidAPI Key Setup (for LinkedIn profile data)

The system includes a RapidAPI key for LinkedIn profile data. If you need your own:

1. Go to [RapidAPI](https://rapidapi.com/)
2. Sign up and search for "LinkedIn Profile Data"
3. Subscribe to the API
4. Replace the key in `config.py`

##  Quick Start

### Demo Mode (No API Keys Required)
```bash
# Test with sample data
python main.py --demo

# Test with OpenAI GPT-4 (requires OpenAI API key)
python main.py --demo --gpt4

# Test with Anthropic Claude (requires Anthropic API key)
python main.py --demo --anthropic

# Export results
python main.py --demo --export
```

### Real Job Processing
```bash
# Process a LinkedIn job posting
python main.py "https://www.linkedin.com/jobs/view/4256398535"

# Use OpenAI GPT-4 for personalized messages
python main.py --gpt4 "https://www.linkedin.com/jobs/view/4256398535"

# Use Anthropic Claude for personalized messages
python main.py --anthropic "https://www.linkedin.com/jobs/view/4256398535"

# Limit candidates and export
python main.py --max-candidates 30 --export "https://www.linkedin.com/jobs/view/4256398535"
```

##  Usage Examples

### Basic Usage
```bash
# Process job with default settings (OpenAI GPT-3.5)
python main.py "https://www.linkedin.com/jobs/view/4256398535"
```

### Advanced Options
```bash
# Use OpenAI GPT-4 for personalized outreach
python main.py --gpt4 "https://www.linkedin.com/jobs/view/4256398535"

# Use Anthropic Claude for personalized outreach
python main.py --anthropic "https://www.linkedin.com/jobs/view/4256398535"

# Use template-based messages
python main.py --templates "https://www.linkedin.com/jobs/view/4256398535"

# Limit number of candidates
python main.py --max-candidates 50 "https://www.linkedin.com/jobs/view/4256398535"

# Export results to JSON
python main.py --export "https://www.linkedin.com/jobs/view/4256398535"

# Quiet mode (summary only)
python main.py --quiet "https://www.linkedin.com/jobs/view/4256398535"

# Custom recruiter name
python main.py --recruiter-name "John Smith" "https://www.linkedin.com/jobs/view/4256398535"
```

### Combined Options
```bash
# Full featured run with Claude, export, and custom settings
python main.py --anthropic --max-candidates 25 --export --recruiter-name "Sarah Johnson" "https://www.linkedin.com/jobs/view/4256398535"
```

##  Configuration

### API Keys
Edit `config.py` to set your API keys:

```python
# OpenAI API for GPT-4
OPENAI_API_KEY = "your-openai-api-key-here"

# Anthropic API for Claude
ANTHROPIC_API_KEY = "your-anthropic-api-key-here"

# RapidAPI LinkedIn Data API
RAPIDAPI_KEY = "your-rapidapi-key-here"
```

### Scoring Weights
Customize candidate scoring in `config.py`:

```python
SCORING_WEIGHTS = {
    'education': 0.20,    # Education background
    'trajectory': 0.20,   # Career progression
    'company': 0.15,      # Company reputation
    'skills': 0.25,       # Skills match
    'location': 0.10,     # Location match
    'tenure': 0.10        # Experience duration
}
```

##  Output Format

The system generates structured JSON output:

```json
{
  "job_id": "senior-software-engineer-techcorp-san-francisco-ca-1234567890",
  "candidates_found": 25,
  "job_details": {
    "title": "Senior Software Engineer",
    "company": "TechCorp",
    "location": "San Francisco, CA",
    "skills": ["Python", "JavaScript", "React", "AWS"],
    "requirements": ["5+ years experience", "Cloud platforms"]
  },
  "top_candidates": [
    {
      "name": "Alice Johnson",
      "linkedin_url": "https://linkedin.com/in/alice-johnson",
      "fit_score": 8.5,
      "headline": "Senior Software Engineer at Google",
      "location": "San Francisco, CA",
      "outreach_message": "Hi Alice Johnson,\n\nI was impressed by your experience...",
      "message_source": "claude",
      "score_breakdown": {
        "education": 10.0,
        "trajectory": 8.0,
        "company": 9.5,
        "skills": 8.0,
        "location": 10.0,
        "tenure": 9.5
      }
    }
  ],
  "processed_at": 1703123456.789
}
```

##  Architecture

```
Input Job → Search LinkedIn → Extract Profiles → Score Fit → Generate Messages
     ↓                              ↓                ↓              ↓
   Queue → RapidAPI/Scraping → Parse Data → Fit Algorithm → GPT-4/Claude
```

### Components:
- **`main.py`**: CLI interface and orchestration
- **`job_parser.py`**: LinkedIn job posting parser
- **`linkedin_search.py`**: Profile search with RapidAPI integration
- **`scoring.py`**: AI-like candidate scoring algorithm
- **`gpt_outreach.py`**: GPT-4 and Claude powered outreach message generator
- **`outreach.py`**: Template-based message generator (fallback)
- **`job_orchestrator.py`**: Main workflow coordinator
- **`config.py`**: Configuration and API keys

##  Cost Estimation

### OpenAI API Costs (GPT-4):
- **Per Message**: ~$0.01-0.05
- **Free Credits**: $5 worth (expires in 3 months)
- **Typical Campaign**: $0.50-2.00 for 50 candidates

### Anthropic API Costs (Claude):
- **Free Tier**: 5 messages per day
- **Cost**: Free tier available
- **Typical Usage**: Perfect for testing and small campaigns

### RapidAPI Costs:
- **LinkedIn Profile Data**: Included in free tier
- **Additional Queries**: May require subscription

##  Troubleshooting

### Common Issues:

1. **"No OpenAI API key provided"**
   - Set your OpenAI API key in environment or config.py
   - System will fallback to template messages

2. **"No Anthropic API key provided"**
   - Set your Anthropic API key in environment or config.py
   - System will fallback to template messages

3. **"ModuleNotFoundError: No module named 'openai'"**
   ```bash
   pip install openai
   ```

4. **"ModuleNotFoundError: No module named 'anthropic'"**
   ```bash
   pip install anthropic
   ```

5. **"Failed to extract job details"**
   - Check if LinkedIn job URL is valid
   - Try with --demo to test system

6. **"No profiles found"**
   - LinkedIn may have anti-scraping measures
   - Try different job postings
   - Check RapidAPI key validity

### Debug Mode:
```bash
# Run with verbose output
python main.py --demo --quiet
```

##  License

This project is for educational and research purposes. Please respect LinkedIn's terms of service and use responsibly.

##  Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

##  Support

For issues and questions:
1. Check the troubleshooting section
2. Review the demo mode output
3. Verify API key setup
4. Test with different job URLs

---

**Note**: This tool is designed for legitimate recruitment purposes. Please ensure compliance with LinkedIn's terms of service and applicable data protection regulations. 
