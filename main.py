#!/usr/bin/env python3
"""
Reddit User Persona Analyzer

A Python script that analyzes Reddit user profiles to create detailed personality personas
using web scraping and AI-powered content analysis.

Author: AI/LLM Engineer Intern
"""

import praw
import json
import os
import re
import time
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import openai
from openai import OpenAI


@dataclass
class RedditPost:
    """Data class to store Reddit post information"""
    title: str
    content: str
    subreddit: str
    score: int
    created_utc: float
    url: str
    post_type: str  # 'post' or 'comment'


class RedditUserAnalyzer:
    """Main class for analyzing Reddit user profiles and generating personas"""
    
    def __init__(self):
        """Initialize the analyzer with API credentials"""
        self.reddit = None
        self.openai_client = None
        self.setup_apis()
    
    def setup_apis(self):
        """Setup Reddit and OpenAI API connections"""
        # Reddit API Setup
        try:
            self.reddit = praw.Reddit(
                client_id=os.getenv('REDDIT_CLIENT_ID'),
                client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
                user_agent=os.getenv('REDDIT_USER_AGENT', 'PersonaAnalyzer/1.0')
            )
            print("✅ Reddit API connected successfully")
        except Exception as e:
            print(f"❌ Reddit API setup failed: {e}")
            print("Please check your Reddit API credentials in environment variables")
            return
        
        # OpenAI API Setup
        try:
            openai_api_key = os.getenv('OPENAI_API_KEY')
            if openai_api_key:
                self.openai_client = OpenAI(api_key=openai_api_key)
                print("✅ OpenAI API connected successfully")
            else:
                print("⚠️  OpenAI API key not found. Will use rule-based analysis.")
        except Exception as e:
            print(f"⚠️  OpenAI API setup failed: {e}. Will use rule-based analysis.")
    
    def extract_username_from_url(self, profile_url: str) -> str:
        """Extract username from Reddit profile URL"""
        # Handle various Reddit URL formats
        patterns = [
            r'reddit\.com/user/([^/]+)',
            r'reddit\.com/u/([^/]+)',
            r'reddit\.com/user/([^/]+)/',
            r'reddit\.com/u/([^/]+)/'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, profile_url)
            if match:
                return match.group(1)
        
        raise ValueError(f"Could not extract username from URL: {profile_url}")
    
    def scrape_user_data(self, username: str, limit: int = 100) -> List[RedditPost]:
        """Scrape posts and comments from a Reddit user profile"""
        if not self.reddit:
            raise Exception("Reddit API not initialized")
        
        print(f"🔍 Scraping data for user: {username}")
        user_data = []
        
        try:
            user = self.reddit.redditor(username)
            
            # Check if user exists
            try:
                user.id  # This will throw an exception if user doesn't exist
            except Exception:
                raise Exception(f"User '{username}' not found or may be suspended")
            
            print(f"📝 Collecting posts...")
            # Get user's posts
            post_count = 0
            for submission in user.submissions.new(limit=limit):
                if post_count >= limit:
                    break
                
                user_data.append(RedditPost(
                    title=submission.title,
                    content=submission.selftext if submission.selftext else "",
                    subreddit=str(submission.subreddit),
                    score=submission.score,
                    created_utc=submission.created_utc,
                    url=f"https://reddit.com{submission.permalink}",
                    post_type="post"
                ))
                post_count += 1
            
            print(f"💬 Collecting comments...")
            # Get user's comments
            comment_count = 0
            for comment in user.comments.new(limit=limit):
                if comment_count >= limit:
                    break
                
                user_data.append(RedditPost(
                    title=f"Comment in r/{comment.subreddit}",
                    content=comment.body if comment.body else "",
                    subreddit=str(comment.subreddit),
                    score=comment.score,
                    created_utc=comment.created_utc,
                    url=f"https://reddit.com{comment.permalink}",
                    post_type="comment"
                ))
                comment_count += 1
            
            print(f"✅ Collected {len(user_data)} posts and comments")
            return user_data
            
        except Exception as e:
            raise Exception(f"Error scraping user data: {e}")
    
    def analyze_with_openai(self, user_data: List[RedditPost], username: str) -> str:
        """Use OpenAI to analyze user data and generate persona"""
        if not self.openai_client:
            return None
        
        # Prepare content for analysis
        content_for_analysis = []
        for post in user_data[:50]:  # Limit to avoid token limits
            content_for_analysis.append(f"[{post.post_type.upper()}] in r/{post.subreddit}: {post.title}\n{post.content[:500]}")
        
        combined_content = "\n\n".join(content_for_analysis)
        
        prompt = f"""
        Analyze the following Reddit posts and comments from user '{username}' and create a detailed personality persona. 
        For each trait you identify, please cite specific examples from the content.

        Reddit Content:
        {combined_content}

        Please provide a comprehensive analysis including:
        1. **Interests and Hobbies**
        2. **Communication Style and Tone**
        3. **Estimated Age Group**
        4. **Possible Profession or Field**
        5. **Political Opinions** (if evident)
        6. **Personality Traits**
        7. **Community Involvement**
        8. **Overall Assessment**

        For each section, include specific quotes or examples from their posts/comments as evidence.
        Format your response in a clear, structured way.
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert in personality analysis and social media behavior. Provide detailed, evidence-based personality assessments."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"⚠️  OpenAI analysis failed: {e}")
            return None
    
    def analyze_with_rules(self, user_data: List[RedditPost], username: str) -> str:
        """Rule-based analysis as fallback"""
        print("🤖 Using rule-based analysis...")
        
        # Extract basic statistics
        total_posts = len([p for p in user_data if p.post_type == "post"])
        total_comments = len([p for p in user_data if p.post_type == "comment"])
        subreddits = list(set([p.subreddit for p in user_data]))
        
        # Analyze content
        all_text = " ".join([p.title + " " + p.content for p in user_data])
        word_count = len(all_text.split())
        
        # Simple keyword analysis for interests
        interest_keywords = {
            "Technology": ["python", "programming", "code", "tech", "software", "AI", "ML", "data"],
            "Gaming": ["game", "gaming", "PC", "console", "steam", "xbox", "playstation"],
            "Sports": ["football", "basketball", "soccer", "sports", "team", "league"],
            "Finance": ["stock", "investment", "money", "crypto", "bitcoin", "trading"],
            "Health": ["workout", "fitness", "health", "exercise", "gym", "diet"]
        }
        
        detected_interests = []
        for category, keywords in interest_keywords.items():
            matches = sum(1 for keyword in keywords if keyword.lower() in all_text.lower())
            if matches >= 3:
                detected_interests.append(category)
        
        # Generate rule-based persona
        persona = f"""
# Reddit User Persona Analysis for u/{username}

## Overview
- **Total Posts**: {total_posts}
- **Total Comments**: {total_comments}
- **Active Subreddits**: {len(subreddits)}
- **Total Word Count**: {word_count}

## Detected Interests
{', '.join(detected_interests) if detected_interests else 'No clear patterns detected'}

## Active Communities
Top subreddits: {', '.join(subreddits[:10])}

## Communication Analysis
- Average words per post: {word_count // max(len(user_data), 1)}
- Most active in: {max(subreddits, key=lambda x: len([p for p in user_data if p.subreddit == x])) if subreddits else 'N/A'}

## Content Examples
"""
        
        # Add some example posts
        for i, post in enumerate(user_data[:5]):
            persona += f"\n**Example {i+1}** ({post.post_type} in r/{post.subreddit}):\n"
            persona += f"Title: {post.title}\n"
            persona += f"Content: {post.content[:200]}...\n"
            persona += f"Source: {post.url}\n"
        
        return persona
    
    def generate_persona(self, profile_url: str) -> str:
        """Main method to generate user persona"""
        try:
            # Extract username
            username = self.extract_username_from_url(profile_url)
            print(f"🎯 Analyzing user: {username}")
            
            # Scrape user data
            user_data = self.scrape_user_data(username)
            
            if not user_data:
                return f"No data found for user {username}"
            
            # Try OpenAI analysis first, fall back to rule-based
            persona = None
            if self.openai_client:
                print("🧠 Generating AI-powered persona...")
                persona = self.analyze_with_openai(user_data, username)
            
            if not persona:
                persona = self.analyze_with_rules(user_data, username)
            
            # Add metadata
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            header = f"""# Reddit User Persona Analysis
**User**: u/{username}
**Profile URL**: {profile_url}
**Analysis Date**: {timestamp}
**Data Points Analyzed**: {len(user_data)} posts and comments

---

"""
            
            return header + persona
            
        except Exception as e:
            return f"Error generating persona: {e}"
    
    def save_persona(self, persona: str, username: str) -> str:
        """Save persona to text file"""
        filename = f"{username}_persona.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(persona)
            print(f"✅ Persona saved to: {filename}")
            return filename
        except Exception as e:
            print(f"❌ Error saving file: {e}")
            return None


def main():
    """Main function to run the persona analyzer"""
    print("🚀 Reddit User Persona Analyzer")
    print("=" * 50)
    
    # Check for required environment variables
    required_vars = ['REDDIT_CLIENT_ID', 'REDDIT_CLIENT_SECRET']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set these variables and try again.")
        print("See README.md for setup instructions.")
        return
    
    analyzer = RedditUserAnalyzer()
    
    # Get user input
    profile_url = input("\n🔗 Enter Reddit profile URL: ").strip()
    
    if not profile_url:
        print("❌ No URL provided")
        return
    
    try:
        # Generate persona
        persona = analyzer.generate_persona(profile_url)
        
        # Extract username for filename
        username = analyzer.extract_username_from_url(profile_url)
        
        # Save to file
        filename = analyzer.save_persona(persona, username)
        
        if filename:
            print(f"\n📄 Analysis complete! Check {filename} for results.")
            
            # Show preview
            print("\n📋 Preview:")
            print("-" * 30)
            print(persona[:500] + "..." if len(persona) > 500 else persona)
            
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()