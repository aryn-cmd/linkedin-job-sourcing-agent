# 🤖 GPT-4 Setup Guide

## Get Your Free OpenAI API Key (5 Minutes)

### Step 1: Get Free API Key
1. **Go to**: https://platform.openai.com/
2. **Click**: "Sign Up" (top right)
3. **Create account** with email
4. **Verify email**
5. **Go to**: API Keys (left sidebar)
6. **Click**: "Create new secret key"
7. **Copy** the key (starts with `sk-`)

### Step 2: Set Your API Key
```bash
# Windows PowerShell
$env:OPENAI_API_KEY="sk-your-actual-key-here"

# Or edit config.py line 10:
OPENAI_API_KEY = "sk-your-actual-key-here"
```

### Step 3: Test GPT-4
```bash
python test_gpt4.py
```

## 💰 Free Tier Details
- **$5 Free Credits** (no credit card needed)
- **Valid for 3 months**
- **Cost per message**: ~$0.02
- **50 candidates**: ~$1.00

## 🚀 Usage Examples

### Demo with GPT-4 (Default)
```bash
python main.py --demo
```

### Real Job with GPT-4
```bash
python main.py "https://www.linkedin.com/jobs/view/4256398535"
```

### Fallback to Templates
```bash
python main.py --templates --demo
```

## 📊 Expected GPT-4 Output

Instead of basic templates, you'll get personalized messages like:

```
Hi Alice Johnson,

I was impressed by your Senior Software Engineer experience at Google and thought you'd be perfect for our Senior Software Engineer role at TechCorp in San Francisco, CA.

Your expertise in Python, JavaScript, React, AWS aligns perfectly with what we're looking for. Given your background at Google, I believe you'd bring valuable insights to our team.

Would you be interested in discussing this opportunity? I'd love to share more about the role and see if it's a good fit.

Best regards,
Recruitment Team
```

## 🔧 Troubleshooting

### "No OpenAI API key provided"
- Set your API key (see Step 2 above)
- System will use templates as fallback

### "Invalid API key"
- Check if key starts with `sk-`
- Make sure you copied the entire key

### "Rate limit exceeded"
- Wait a few minutes and try again
- Free tier has rate limits

## 🎯 Quick Test
```bash
# Test GPT-4 integration
python test_gpt4.py

# Test full system
python main.py --demo
```

---

**That's it!** Once you set your API key, the system will automatically use GPT-4 for personalized outreach messages. 