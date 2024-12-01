import tweepy
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

client = tweepy.Client(
    consumer_key=os.getenv('TWITTER_API_KEY'),
    consumer_secret=os.getenv('TWITTER_API_SECRET_KEY'),
    access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
    access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
)

response = client.create_tweet(text="test 1 2 3")

print(response)
