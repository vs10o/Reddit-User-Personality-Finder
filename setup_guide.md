# Quick Setup Guide for Reddit User Persona Analyzer

## 🚀 Getting Started in 5 Minutes

### Prerequisites
- Python 3.7+ installed on your computer
- A Reddit account
- (Optional) An OpenAI account for AI-powered analysis

### Step 1: Get Reddit API Credentials (Required)

1. **Go to Reddit App Preferences**
   - Visit: https://www.reddit.com/prefs/apps
   - Log in to your Reddit account

2. **Create a New App**
   - Scroll to the bottom and click "Create App" or "Create Another App"
   - Fill out the form:
     - **App name**: `PersonaAnalyzer` (or any name you prefer)
     - **App type**: Select `script`
     - **Description**: `Educational project for analyzing user personas`
     - **About URL**: Leave blank
     - **Redirect URI**: `http://localhost:8080` (required but not used)

3. **Save Your Credentials**
   - After creating the app, you'll see:
     - **Client ID**: The string under your app name (looks like: `dQw4w9WgXcQ`)
     - **Client Secret**: The "secret" field (looks like: `dQw4w9WgXcQ-dQw4w9WgXcQ`)
   - Write these down securely!

### Step 2: Get OpenAI API Key (Optional but Recommended)

1. **Sign up for OpenAI**
   - Go to: https://platform.openai.com/
   - Create an account or log in

2. **Generate API Key**
   - Navigate to: https://platform.openai.com/account/api-keys
   - Click "Create new secret key"
   - Copy the key (starts with `sk-`)
   - **Important**: You'll need to add billing information for usage

### Step 3: Install and Configure

1. **Download the Project**
   ```bash
   # Create project directory
   mkdir reddit-persona-analyzer
   cd reddit-persona-analyzer
   # Place all provided files here
   ```

2. **Install Requirements**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create Environment File**
   
   Create a file named `.env` in your project folder:
   ```env
   REDDIT_CLIENT_ID=your_client_id_here
   REDDIT_CLIENT_SECRET=your_client_secret_here
   REDDIT_USER_AGENT=PersonaAnalyzer/1.0
   OPENAI_API_KEY=your_openai_key_here
   ```

### Step 4: Run the Script

```bash
python main.py
```

When prompted, enter a Reddit profile URL like:
- `https://www.reddit.com/user/kojied/`
- `https://www.reddit.com/u/Hungry-Move-6603/`

### Example Run

```
🚀 Reddit User Persona Analyzer
==================================================
✅ Reddit API connected successfully
✅ OpenAI API connected successfully

🔗 Enter Reddit profile URL: https://www.reddit.com/user/kojied/

🎯 Analyzing user: kojied
🔍 Scraping data for user: kojied
📝 Collecting posts...
💬 Collecting comments...
✅ Collected 87 posts and comments
🧠 Generating AI-powered persona...
✅ Persona saved to: kojied_persona.txt

📄 Analysis complete! Check kojied_persona.txt for results.
```

## 🛠️ Troubleshooting

### "Reddit API setup failed"
- Double-check your `REDDIT_CLIENT_ID` and `REDDIT_CLIENT_SECRET`
- Make sure you selected "script" as the app type
- Verify the `.env` file is in the same directory as `main.py`

### "User not found"
- Check that the username exists and is spelled correctly
- Try a different user (some accounts may be private or suspended)

### "OpenAI API failed"
- Check your API key is correct
- Ensure you have credits in your OpenAI account
- The script will still work with rule-based analysis if OpenAI fails

### "Permission denied" or module errors
- Make sure you're in the correct directory
- Try: `pip install --user -r requirements.txt`
- Check Python version: `python --version` (should be 3.7+)

## 💡 Tips for Best Results

1. **Choose Active Users**: Users with more posts/comments provide better analysis
2. **Public Profiles Only**: Private or deleted accounts won't work
3. **Recent Activity**: Users active in the last few months give more current insights
4. **Diverse Content**: Users who post in multiple subreddits provide richer personas

## 📊 What You'll Get

The generated persona file includes:
- **Interests & Hobbies**: Based on subreddit activity
- **Communication Style**: Tone, formality, humor
- **Demographics**: Age estimates, profession guesses
- **Personality Traits**: Analytical, creative, social tendencies
- **Citations**: Specific posts supporting each conclusion

Enjoy analyzing Reddit personalities! 🎉