import tweepy
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from openai import OpenAI
from db_operations import DatabaseManager

# Load environment variables
load_dotenv()

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Initialize Twitter client
twitter_client = tweepy.Client(
    bearer_token=os.getenv('TWITTER_BEARER_TOKEN'),
    consumer_key=os.getenv('TWITTER_API_KEY'),
    consumer_secret=os.getenv('TWITTER_API_SECRET_KEY'),
    access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
    access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
)

class TweetSelector:
    def __init__(self):
        self.db = DatabaseManager()

    def get_recent_tweets_with_comments(self, limit: int = 10) -> List[Dict]:
        """Get the most recent tweets and their comments using existing db operations"""
        tweets = []
        try:
            # Get recent tweets using existing method
            self.db.cur.execute(
                "SELECT * FROM tweets ORDER BY created_at DESC LIMIT %s",
                (limit,)
            )
            recent_tweets = self.db.cur.fetchall()

            for tweet in recent_tweets:
                tweet_dict = dict(tweet)
                # Use existing get_tweet_comments method
                comments = self.db.get_tweet_comments(tweet_dict['tweet_id'])
                tweet_dict['comments'] = comments
                tweets.append(tweet_dict)

        except Exception as e:
            print(f"Error getting recent tweets: {e}")
            return []

        return tweets

    def get_recent_submissions(self) -> List[Dict]:
        """Get submissions from the last hour using existing db operations"""
        try:
            one_hour_ago = datetime.now() - timedelta(hours=1)
            self.db.cur.execute(
                "SELECT * FROM submissions WHERE created_at > %s ORDER BY bid_amount DESC",
                (one_hour_ago,)
            )
            return [dict(submission) for submission in self.db.cur.fetchall()]
        except Exception as e:
            print(f"Error getting recent submissions: {e}")
            return []

    def construct_llm_prompt(self, recent_tweets: List[Dict], submissions: List[Dict]) -> str:
        """Construct the prompt for the LLM"""
        prompt = """You are a social media expert tasked with selecting the most viral potential tweet. 

Rules:
1. NEVER select content that is racist, sexist, discriminatory, or harmful
2. Prefer content that is:
   - Humorous and relatable
   - Timely and relevant
   - Original and creative
   - Family-friendly
3. Consider the bid amounts as signals of confidence
4. Learn from the engagement patterns of previous tweets

Context of recent tweets and their engagement:
"""
        
        # Add recent tweets and their comments
        for tweet in recent_tweets:
            prompt += f"\nTweet: {tweet['tweet_text']}"
            prompt += f"\nEngagement: {len(tweet['comments'])} comments"
            if tweet['comments']:
                prompt += "\nSample comments:"
                for comment in tweet['comments'][:3]:  # Show up to 3 comments
                    prompt += f"\n- {comment['comment_text']}"
            prompt += "\n"

        prompt += "\nNew submissions to choose from:\n"
        for sub in submissions:
            prompt += f"- Text: {sub['tweet_text']} (Bid: {sub['bid_amount']} SOL)\n"

        prompt += "\nAnalyze the submissions and select the tweet with the highest viral potential. Provide your selection and reasoning in this format:\nSELECTED_TWEET: <tweet_text>\nREASONING: <your explanation>"

        return prompt

    def select_best_tweet(self) -> Optional[str]:
        """Main function to select the best tweet"""
        # Get recent tweets and their comments
        recent_tweets = self.get_recent_tweets_with_comments()
        
        # Get recent submissions
        submissions = self.get_recent_submissions()
        
        if not submissions:
            print("No submissions in the last hour")
            return None

        # Construct prompt
        prompt = self.construct_llm_prompt(recent_tweets, submissions)

        try:
            # Get LLM response
            response = openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "system", "content": prompt}],
                temperature=0.7,
                max_tokens=500
            )

            # Extract selected tweet
            llm_response = response.choices[0].message.content
            selected_tweet = None
            for line in llm_response.split('\n'):
                if line.startswith('SELECTED_TWEET:'):
                    selected_tweet = line.replace('SELECTED_TWEET:', '').strip()
                    break

            if not selected_tweet:
                print("No valid tweet selected by LLM")
                return None

            # Post tweet
            tweet_response = twitter_client.create_tweet(text=selected_tweet)
            
            # Save tweet to database using existing create_tweet method
            self.db.create_tweet(selected_tweet)

            print(f"Successfully posted tweet: {selected_tweet}")
            return selected_tweet

        except Exception as e:
            print(f"Error in tweet selection/posting: {e}")
            return None

def run_hourly_selection():
    """Function to be called by the scheduler"""
    selector = TweetSelector()
    selected_tweet = selector.select_best_tweet()
    if selected_tweet:
        print(f"Hourly tweet selected and posted: {selected_tweet}")
    else:
        print("No tweet selected this hour") 