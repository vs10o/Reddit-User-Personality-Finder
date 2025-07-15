"""
Configuration file for Reddit User Persona Analyzer

This file contains configuration settings and can be modified to customize
the behavior of the analyzer.
"""

import os
from typing import Dict, List

# Analysis Configuration
class AnalysisConfig:
    """Configuration settings for the analysis process"""
    
    # Number of posts/comments to analyze per user
    MAX_POSTS_TO_ANALYZE = 100
    
    # Number of posts to send to OpenAI (to avoid token limits)
    OPENAI_ANALYSIS_LIMIT = 50
    
    # Character limit for content preview in rule-based analysis
    CONTENT_PREVIEW_LIMIT = 200
    
    # Maximum number of subreddits to show in overview
    MAX_SUBREDDITS_DISPLAY = 10
    
    # OpenAI model configuration
    OPENAI_MODEL = "gpt-3.5-turbo"  # Change to "gpt-4" for better analysis
    OPENAI_MAX_TOKENS = 2000
    OPENAI_TEMPERATURE = 0.7

# Interest Detection Keywords
INTEREST_KEYWORDS: Dict[str, List[str]] = {
    "Technology": [
        "python", "programming", "code", "tech", "software", "AI", "ML", 
        "data", "javascript", "react", "web", "development", "API", "github"
    ],
    "Gaming": [
        "game", "gaming", "PC", "console", "steam", "xbox", "playstation", 
        "nintendo", "RPG", "FPS", "MMO", "twitch", "streamer"
    ],
    "Sports & Fitness": [
        "football", "basketball", "soccer", "sports", "team", "league", 
        "workout", "fitness", "health", "exercise", "gym", "diet", "training"
    ],
    "Finance": [
        "stock", "investment", "money", "crypto", "bitcoin", "trading", 
        "portfolio", "401k", "retirement", "savings", "budget"
    ],
    "Education": [
        "university", "college", "student", "study", "exam", "degree", 
        "learning", "course", "education", "school", "academic"
    ],
    "Arts & Creativity": [
        "art", "music", "drawing", "painting", "creative", "design", 
        "photography", "writing", "poetry", "literature", "film"
    ],
    "Science": [
        "science", "research", "physics", "chemistry", "biology", 
        "mathematics", "engineering", "medicine", "space", "astronomy"
    ]
}

# Personality Indicators
PERSONALITY_INDICATORS: Dict[str, List[str]] = {
    "Analytical": [
        "analyze", "data", "research", "study", "examine", "investigate", 
        "statistics", "logical", "systematic", "methodical"
    ],
    "Creative": [
        "creative", "artistic", "imaginative", "innovative", "original", 
        "design", "create", "inspiration", "aesthetic", "visual"
    ],
    "Social": [
        "community", "friends", "social", "group", "team", "collaboration", 
        "networking", "meeting", "party", "event"
    ],
    "Introverted": [
        "alone", "quiet", "introvert", "solitude", "private", "reserved", 
        "shy", "independent", "self-sufficient"
    ],
    "Helpful": [
        "help", "assist", "support", "advice", "guide", "mentor", 
        "teaching", "volunteer", "contribute", "share"
    ]
}

# Age Group Indicators
AGE_INDICATORS: Dict[str, List[str]] = {
    "Teen (13-19)": [
        "high school", "teenager", "parents", "allowance", "homework", 
        "prom", "senior year", "college applications"
    ],
    "Young Adult (20-29)": [
        "college", "university", "first job", "entry level", "student loans", 
        "internship", "graduation", "apartment", "dating"
    ],
    "Adult (30-45)": [
        "career", "mortgage", "marriage", "kids", "family", "promotion", 
        "professional", "experience", "established"
    ],
    "Middle Age (45-60)": [
        "midlife", "teenagers", "high schooler", "college tuition", 
        "retirement planning", "senior position", "management"
    ]
}

# Output Configuration
class OutputConfig:
    """Configuration for output formatting"""
    
    # File encoding
    FILE_ENCODING = 'utf-8'
    
    # Date format for timestamps
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    
    # Maximum length for content citations
    MAX_CITATION_LENGTH = 300
    
    # Number of example posts to include in persona
    MAX_EXAMPLE_POSTS = 5

# API Configuration
class APIConfig:
    """API-related configuration"""
    
    # Reddit API rate limiting (requests per minute)
    REDDIT_RATE_LIMIT = 60
    
    # OpenAI API timeout (seconds)
    OPENAI_TIMEOUT = 30
    
    # Retry attempts for failed API calls
    MAX_RETRY_ATTEMPTS = 3
    
    # Wait time between retries (seconds)
    RETRY_WAIT_TIME = 5

# Environment variable names
ENV_VARS = {
    'REDDIT_CLIENT_ID': 'Reddit API Client ID',
    'REDDIT_CLIENT_SECRET': 'Reddit API Client Secret', 
    'REDDIT_USER_AGENT': 'Reddit API User Agent',
    'OPENAI_API_KEY': 'OpenAI API Key (Optional)'
}

# Default user agent for Reddit API
DEFAULT_USER_AGENT = "PersonaAnalyzer/1.0 (Educational Project)"