#!/usr/bin/env python3
"""
Simplified Reddit User Persona Analyzer
Works without external Python dependencies
"""

import json
import re
import urllib.request
import urllib.parse
from datetime import datetime


class SimpleRedditAnalyzer:
    """Simplified analyzer using only Python standard library"""
    
    def __init__(self):
        self.user_agent = 'PersonaAnalyzer/1.0'
    
    def extract_username_from_url(self, profile_url: str) -> str:
        """Extract username from Reddit profile URL"""
        patterns = [
            r'reddit\.com/user/([^/]+)',
            r'reddit\.com/u/([^/]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, profile_url)
            if match:
                return match.group(1)
        
        raise ValueError(f"Could not extract username from URL: {profile_url}")
    
    def fetch_reddit_data(self, username: str):
        """Fetch Reddit data using public JSON API"""
        try:
            # Use Reddit's public JSON API
            url = f"https://www.reddit.com/user/{username}.json"
            
            req = urllib.request.Request(url)
            req.add_header('User-Agent', self.user_agent)
            
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                return data
                
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None
    
    def analyze_user_data(self, data, username: str) -> str:
        """Analyze user data and create persona"""
        if not data or 'data' not in data:
            return f"No data available for user {username}"
        
        posts = data['data']['children']
        
        # Basic analysis
        total_posts = len(posts)
        subreddits = set()
        all_text = ""
        
        for post in posts:
            post_data = post['data']
            subreddits.add(post_data.get('subreddit', 'unknown'))
            
            # Collect text content
            title = post_data.get('title', '')
            body = post_data.get('body', '') or post_data.get('selftext', '')
            all_text += f" {title} {body}"
        
        # Simple keyword analysis
        interests = self.detect_interests(all_text)
        
        # Generate persona
        persona = f"""# Reddit User Persona Analysis for u/{username}

## Analysis Overview
- **Analysis Date**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **Total Posts Analyzed**: {total_posts}
- **Active Subreddits**: {len(subreddits)}

## Detected Interests
{', '.join(interests) if interests else 'No clear patterns detected'}

## Active Communities
{', '.join(list(subreddits)[:10])}

## Sample Content Analysis
"""
        
        # Add sample posts
        for i, post in enumerate(posts[:5]):
            post_data = post['data']
            persona += f"\n**Sample {i+1}**:\n"
            persona += f"- Subreddit: r/{post_data.get('subreddit', 'unknown')}\n"
            persona += f"- Title: {post_data.get('title', 'N/A')[:100]}...\n"
            persona += f"- Score: {post_data.get('score', 0)}\n"
        
        return persona
    
    def detect_interests(self, text: str) -> list:
        """Simple keyword-based interest detection"""
        text_lower = text.lower()
        
        interest_keywords = {
            "Technology": ["python", "programming", "code", "tech", "software", "ai", "ml"],
            "Gaming": ["game", "gaming", "pc", "console", "steam"],
            "Sports": ["football", "basketball", "soccer", "sports"],
            "Finance": ["stock", "investment", "crypto", "bitcoin"],
            "Health": ["workout", "fitness", "health", "exercise"]
        }
        
        detected = []
        for category, keywords in interest_keywords.items():
            if sum(1 for keyword in keywords if keyword in text_lower) >= 2:
                detected.append(category)
        
        return detected
    
    def generate_persona(self, profile_url: str) -> str:
        """Generate user persona"""
        try:
            username = self.extract_username_from_url(profile_url)
            print(f"Analyzing user: {username}")
            
            data = self.fetch_reddit_data(username)
            if not data:
                return f"Could not fetch data for user {username}"
            
            persona = self.analyze_user_data(data, username)
            return persona
            
        except Exception as e:
            return f"Error: {e}"
    
    def save_persona(self, persona: str, username: str):
        """Save persona to file"""
        filename = f"{username}_persona.txt"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(persona)
            print(f"Persona saved to: {filename}")
            return filename
        except Exception as e:
            print(f"Error saving file: {e}")
            return None


def main():
    """Main function"""
    print("🚀 Simple Reddit User Persona Analyzer")
    print("=" * 50)
    
    analyzer = SimpleRedditAnalyzer()
    
    profile_url = input("Enter Reddit profile URL: ").strip()
    
    if not profile_url:
        print("No URL provided")
        return
    
    try:
        persona = analyzer.generate_persona(profile_url)
        username = analyzer.extract_username_from_url(profile_url)
        
        print("\nGenerated Persona:")
        print("-" * 30)
        print(persona)
        
        analyzer.save_persona(persona, username)
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()