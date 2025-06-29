# 🤖 OpenAI API Setup Guide

## Get Your Free OpenAI API Key

### Step 1: Create OpenAI Account
1. **Visit**: https://platform.openai.com/
2. **Click**: "Sign Up" in the top right
3. **Complete**: Registration with email and password
4. **Verify**: Your email address

### Step 2: Get Your API Key
1. **Login** to your OpenAI account
2. **Navigate** to "API Keys" in the left sidebar
3. **Click** "Create new secret key"
4. **Name** your key (e.g., "LinkedIn Recruitment Agent")
5. **Copy** the generated key (starts with `sk-`)
6. **Save** it securely - you won't see it again!

### Step 3: Set Your API Key

#### Option A: Environment Variable (Recommended)
```bash
# Windows PowerShell
$env:OPENAI_API_KEY="sk-your-actual-api-key-here"

# Windows Command Prompt
set OPENAI_API_KEY=sk-your-actual-api-key-here

# Linux/Mac
export OPENAI_API_KEY="sk-your-actual-api-key-here"
```

#### Option B: Edit config.py
```python
# Open config.py and change line 10:
OPENAI_API_KEY = "sk-your-actual-api-key-here"
```

### Step 4: Test Your Setup
```bash
python test_gpt4.py
```

## 💰 Free Tier Information

### What You Get:
- **$5 Free Credits** upon signup
- **Valid for 3 months** from signup date
- **No credit card required** for free tier

### Cost Breakdown:
- **GPT-4 Input**: ~$0.03 per 1K tokens
- **GPT-4 Output**: ~$0.06 per 1K tokens
- **Typical Message**: ~$0.01-0.05 per outreach message
- **50 Candidates**: ~$0.50-2.00 total cost

### Usage Examples:
- **1 outreach message**: ~$0.02
- **10 candidates**: ~$0.20
- **50 candidates**: ~$1.00
- **100 candidates**: ~$2.00

## 🧪 Testing Your Setup

### Quick Test:
```bash
python test_gpt4.py
```

### Expected Output:
```
✅ OpenAI API key found
✅ GPT-4 Integration Successful!
```

### Demo Test:
```bash
python main.py --demo --gpt4
```

## 🔧 Troubleshooting

### "No OpenAI API key found"
- Check if you set the environment variable correctly
- Verify the key in config.py
- Make sure the key starts with `sk-`

### "Invalid API key"
- Double-check your API key
- Make sure you copied the entire key
- Try regenerating a new key

### "Rate limit exceeded"
- Free tier has rate limits
- Wait a few minutes and try again
- Consider upgrading to paid plan

### "Insufficient credits"
- Check your usage at https://platform.openai.com/usage
- Free credits expire after 3 months
- Add payment method for continued use

## 📊 Monitor Your Usage

1. **Visit**: https://platform.openai.com/usage
2. **Check**: Current usage and remaining credits
3. **Monitor**: API calls and costs
4. **Set**: Usage alerts if needed

## 🎯 Best Practices

1. **Start Small**: Test with demo mode first
2. **Monitor Costs**: Check usage regularly
3. **Batch Process**: Process multiple candidates together
4. **Use Templates**: Fallback when GPT-4 is unavailable
5. **Export Results**: Save your work

## 🚀 Ready to Use!

Once your API key is set up:

```bash
# Test with demo data
python main.py --demo --gpt4

# Process real jobs
python main.py --gpt4 "https://www.linkedin.com/jobs/view/4256398535"

# Export results
python main.py --gpt4 --export "https://www.linkedin.com/jobs/view/4256398535"
```

## 💡 Pro Tips

- **Keep your API key secure** - don't share it publicly
- **Start with demo mode** to test before using real data
- **Monitor your usage** to avoid unexpected charges
- **Use templates as backup** when GPT-4 is unavailable
- **Export results** to save your candidate data

---

**Need Help?** Check the main README.md or run `python main.py --help` for more options. 