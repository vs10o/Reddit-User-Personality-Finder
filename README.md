# Reddit User Persona Analyzer  
http://astonishing-beignet-55cd56.netlify.app/

A Python script that analyzes Reddit user profiles to create detailed personality personas using AI-powered content analysis.

## Features

- **Web Scraping**: Uses PRAW (Python Reddit API Wrapper) to efficiently scrape user posts and comments
- **AI Analysis**: Leverages OpenAI's GPT models for intelligent personality analysis
- **Fallback Analysis**: Rule-based analysis when AI is unavailable
- **Citation System**: Links specific posts/comments to personality traits
- **Export Functionality**: Saves detailed personas as text files

## Requirements

### API Keys Required

1. **Reddit API** (Required)
   - Go to [Reddit App Preferences](https://www.reddit.com/prefs/apps)
   - Click "Create App" or "Create Another App"
   - Choose "script" as application type
   - Note down `client_id` and `client_secret`

2. **OpenAI API** (Optional, but recommended)
   - Sign up at [OpenAI Platform](https://platform.openai.com/)
   - Generate an API key from your dashboard
   - Note: Requires credits/billing setup

### Python Version
- Python 3.7 or higher

##  Setup Instructions

### Step 1: Clone/Download the Project
```bash
# Download all files to a folder called 'reddit-persona-analyzer'
mkdir reddit-persona-analyzer
cd reddit-persona-analyzer
# Place all the provided files in this directory
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Set Environment Variables

#### Option A: Create a `.env` file (Recommended)
Create a file named `.env` in your project directory:

```env
# Reddit API Credentials (Required)
REDDIT_CLIENT_ID=your_reddit_client_id_here
REDDIT_CLIENT_SECRET=your_reddit_client_secret_here
REDDIT_USER_AGENT=PersonaAnalyzer/1.0

# OpenAI API Key (Optional but recommended)
OPENAI_API_KEY=your_openai_api_key_here
```

#### Option B: Set System Environment Variables

**Windows:**
```cmd
set REDDIT_CLIENT_ID=your_reddit_client_id_here
set REDDIT_CLIENT_SECRET=your_reddit_client_secret_here
set OPENAI_API_KEY=your_openai_api_key_here
```

**macOS/Linux:**
```bash
export REDDIT_CLIENT_ID=your_reddit_client_id_here
export REDDIT_CLIENT_SECRET=your_reddit_client_secret_here
export OPENAI_API_KEY=your_openai_api_key_here
```

### Step 4: Run the Script
```bash
python main.py
```

## Usage

1. Run the script: `python main.py`
2. Enter a Reddit profile URL when prompted:
   - Format: `https://www.reddit.com/user/username/`
   - Alternative: `https://www.reddit.com/u/username/`

3. The script will:
   - Scrape the user's posts and comments
   - Analyze content using AI (or rule-based analysis)
   - Generate a detailed persona
   - Save results to `{username}_persona.txt`

##  Project Structure

```
reddit-persona-analyzer/
├── main.py                    # Main script
├── requirements.txt           # Python dependencies
├── README.md                 # This file
├── .env                      # Environment variables (create this)
├── kojied_persona.txt        # Sample output 1
└── Hungry-Move-6603_persona.txt  # Sample output 2
```

## Configuration Options

You can modify these parameters in `main.py`:

- `limit` in `scrape_user_data()`: Number of posts/comments to analyze (default: 100)
- OpenAI model: Change `gpt-3.5-turbo` to `gpt-4` for better analysis (costs more)
- Analysis depth: Modify the prompt in `analyze_with_openai()` for different insights


