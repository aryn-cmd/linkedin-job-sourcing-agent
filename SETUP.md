# 🚀 Quick Setup Guide

## Get Started in 5 Minutes

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Test the System (No API Keys Required)
```bash
python main.py --demo
```

### 3. Get OpenAI API Key (Free)

#### Step-by-Step:
1. **Go to OpenAI**: https://platform.openai.com/
2. **Sign Up**: Create a free account
3. **Get API Key**: 
   - Click "API Keys" in the left sidebar
   - Click "Create new secret key"
   - Copy the key (starts with `sk-`)

#### Free Tier Details:
- **$5 Free Credits** upon signup
- **Expires in 3 months**
- **Cost per message**: ~$0.01-0.05
- **Typical usage**: $0.50-2.00 for 50 candidates

### 4. Set Your API Key

#### Option A: Environment Variable (Recommended)
```bash
# Windows PowerShell
$env:OPENAI_API_KEY="sk-your-api-key-here"

# Windows Command Prompt
set OPENAI_API_KEY=sk-your-api-key-here

# Linux/Mac
export OPENAI_API_KEY="sk-your-api-key-here"
```

#### Option B: Edit config.py
```python
# In config.py, line 10:
OPENAI_API_KEY = "sk-your-api-key-here"
```

### 5. Test GPT-4 Integration
```bash
python main.py --demo --gpt4
```

### 6. Process Real Jobs
```bash
python main.py --gpt4 "https://www.linkedin.com/jobs/view/4256398535"
```

## 🎯 Quick Commands Reference

| Command | Description |
|---------|-------------|
| `python main.py --demo` | Test with sample data |
| `python main.py --demo --gpt4` | Test with GPT-4 messages |
| `python main.py --demo --templates` | Test with template messages |
| `python main.py --demo --export` | Export results to JSON |
| `python main.py --gpt4 "JOB_URL"` | Process real job with GPT-4 |
| `python main.py --max-candidates 30 "JOB_URL"` | Limit candidates |
| `python main.py --quiet "JOB_URL"` | Summary only |

## 🔧 Troubleshooting

### "No OpenAI API key provided"
- Set your API key (see step 4 above)
- System will use template messages as fallback

### "ModuleNotFoundError: No module named 'openai'"
```bash
pip install openai
```

### "Failed to extract job details"
- Check if LinkedIn URL is valid
- Try with `--demo` first

## 💡 Pro Tips

1. **Start with demo mode** to test the system
2. **Use GPT-4 for personalized messages** when you have API key
3. **Export results** for further analysis
4. **Limit candidates** to control costs and processing time
5. **Use quiet mode** for batch processing

## 📊 Expected Output

After running successfully, you'll see:
- Job details and requirements
- List of scored candidates
- Personalized outreach messages
- Score breakdowns
- LinkedIn profile URLs

## 🎉 You're Ready!

The system is now fully configured and ready to find, score, and outreach to LinkedIn candidates automatically! 