import tweepy
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

client = tweepy.Client(
    bearer_token=os.getenv('TWITTER_BEARER_TOKEN'),
    consumer_key=os.getenv('TWITTER_API_KEY'),
    consumer_secret=os.getenv('TWITTER_API_SECRET_KEY'),
    access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
    access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
)

# response = client.create_tweet(text="test 1 2 3")

# print(response)

def get_tweet_replies(tweet_id):
    # Search for tweets that are replies to the specified tweet_id
    query = f"conversation_id:{tweet_id}"
    
    # Get replies using search_recent_tweets
    # Exclude the original tweet by filtering for only replies
    replies = client.search_recent_tweets(
        query=query,
        tweet_fields=['author_id', 'created_at'],
        max_results=100  # Adjust this number as needed
    )
    
    if replies.data:
        return replies.data
    return []

# Example usage:
tweet_id = "1863373173233975772"  # Replace with actual tweet ID
replies = get_tweet_replies(tweet_id)
for reply in replies:
    print(f"Reply: {reply.text}")
