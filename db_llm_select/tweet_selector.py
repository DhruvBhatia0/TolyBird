import tweepy
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from openai import OpenAI
from db_operations import DatabaseManager
from solathon.core.instructions import transfer
from solathon import Client, Transaction, PublicKey, Keypair
import numpy as np
import base58

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

# Initialize Solana client
solana_client = Client("https://api.mainnet-beta.solana.com")

# Add these constants at the top with other initializations
BUFFER_WALLET = "4cCV2NpYqjMeXzbTyPgnsw1azSuQCcvRtAM9GpTotUGk"
VAULT_WALLET = "9quG6nuCBGYabE3qRich4zbRDpNzGuSvSCPXLdCJHEDe"

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

    def calculate_reward(self, winner_bid: float, all_bids: List[float]) -> Tuple[float, float]:
        """
        Calculate reward based on bid percentile
        Returns (reward_amount, remaining_pool)
        """
        total_pool = sum(all_bids)
        
        # First remove winner's bid from pool (they get this back directly)
        adjusted_pool = total_pool - winner_bid
        
        # Calculate percentile of winner's bid
        percentile = np.percentile([bid for bid in all_bids], 
                                 [b for b in all_bids].index(winner_bid) * 100.0 / len(all_bids))
        
        # Scale percentile to reward percentage (30% to 70%)
        reward_percentage = 0.3 + (percentile / 100.0 * 0.4)  # Scales from 30% to 70%
        
        # Calculate reward from remaining pool
        reward_from_pool = adjusted_pool * reward_percentage
        
        # Total reward is their bid back plus their share of the pool
        total_reward = winner_bid + reward_from_pool
        
        # Remaining goes to vault
        remaining_pool = adjusted_pool - reward_from_pool
        
        return total_reward, remaining_pool

    def transfer_sol(self, private_key: str, to_address: str, amount: float) -> Optional[str]:
        """Transfer SOL and return transaction signature"""
        try:
            # Initialize Solana client (use devnet for testing, mainnet for production)
            client = Client("https://api.devnet.solana.com")
            
            # Create sender keypair from private key
            sender = Keypair.from_private_key(private_key)
            receiver = PublicKey(to_address)
            
            # Convert SOL to lamports (1 SOL = 1_000_000_000 lamports)
            amount_lamports = int(amount * 1_000_000_000)
            
            print(f"\nInitiating transfer:")
            print(f"From: {sender.public_key}")
            print(f"To: {to_address}")
            print(f"Amount: {amount} SOL ({amount_lamports} lamports)")
            
            # Create transfer instruction
            instruction = transfer(
                from_public_key=sender.public_key,
                to_public_key=receiver,
                lamports=amount_lamports
            )
            
            # Create and send transaction
            transaction = Transaction(instructions=[instruction], signers=[sender])
            result = client.send_transaction(transaction)
            
            print(f"Transfer successful!")
            print(f"Transaction ID: {result}")
            print(f"View transaction: https://explorer.solana.com/tx/{result}?cluster=devnet")
            return result
            
        except Exception as e:
            print(f"Error in transfer: {str(e)}")
            import traceback
            traceback.print_exc()
            return None

    def select_best_tweet(self) -> Optional[str]:
        """Main function to select the best tweet and handle rewards"""
        # Get recent submissions
        submissions = self.get_recent_submissions()
        
        if not submissions:
            print("No submissions in the last hour")
            return None

        # Get all bids for percentile calculation
        all_bids = [float(sub['bid_amount']) for sub in submissions]
        total_pool = sum(all_bids)
        
        print(f"\n=== Pool Information ===")
        print(f"Total submissions: {len(submissions)}")
        print(f"Total pool: {total_pool} SOL")
        print(f"Highest bid: {max(all_bids)} SOL")
        print(f"Lowest bid: {min(all_bids)} SOL")
        print(f"Average bid: {total_pool/len(all_bids):.4f} SOL")
        print(f"=====================\n")

        # Get recent tweets and their comments
        recent_tweets = self.get_recent_tweets_with_comments()
        
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
            selected_submission = None
            for line in llm_response.split('\n'):
                if line.startswith('SELECTED_TWEET:'):
                    selected_tweet = line.replace('SELECTED_TWEET:', '').strip()
                    # Find the submission that matches this tweet
                    for submission in submissions:
                        if submission['tweet_text'] == selected_tweet:
                            selected_submission = submission
                            break
                    break

            if not selected_tweet:
                print("No valid tweet selected by LLM")
                return None

            # Post tweet
            # tweet_response = twitter_client.create_tweet(text=selected_tweet)
            
            # Save tweet to database using existing create_tweet method
            self.db.create_tweet(selected_tweet, selected_submission['wallet_address'])

            print(f"Successfully posted tweet: {selected_tweet}")
            print(f"From wallet: {selected_submission['wallet_address']}")

            # After selecting the winning tweet
            if selected_submission:
                winner_bid = float(selected_submission['bid_amount'])
                winner_wallet = selected_submission['wallet_address']
                
                # Calculate rewards
                reward_amount, remaining_pool = self.calculate_reward(winner_bid, all_bids)
                
                print(f"\n=== Reward Distribution ===")
                print(f"Winner's wallet: {winner_wallet}")
                print(f"Original bid: {winner_bid} SOL")
                print(f"Additional reward: {reward_amount - winner_bid} SOL")
                print(f"Total reward: {reward_amount} SOL")
                print(f"Remaining pool: {remaining_pool} SOL")
                print(f"========================\n")

                try:
                    buffer_private_key = os.getenv('BUFFER_PRIVATE_KEY')
                    if not buffer_private_key:
                        raise ValueError("Buffer private key not found in environment variables")

                    print("\nStarting reward distribution process...")
                    
                    # Transfer reward to winner
                    winner_tx = self.transfer_sol(
                        buffer_private_key,
                        winner_wallet,
                        reward_amount
                    )

                    if winner_tx:
                        print(f"\nReward successfully sent to winner!")
                        print(f"Amount: {reward_amount} SOL")
                        print(f"Transaction: {winner_tx}")
                        
                        # Transfer remaining pool to vault
                        vault_tx = self.transfer_sol(
                            buffer_private_key,
                            VAULT_WALLET,
                            remaining_pool
                        )
                        
                        if vault_tx:
                            print(f"\nRemaining pool successfully sent to vault!")
                            print(f"Amount: {remaining_pool} SOL")
                            print(f"Transaction: {vault_tx}")
                        else:
                            print("\nFailed to transfer remaining pool to vault")
                    else:
                        print("\nFailed to send reward to winner")

                except Exception as e:
                    print(f"\nError in reward distribution: {str(e)}")
                    import traceback
                    traceback.print_exc()

            return selected_tweet

        except Exception as e:
            print(f"Error in tweet selection/posting: {str(e)}")
            import traceback
            traceback.print_exc()
            return None

async def run_hourly_selection():
    """Function to be called by the scheduler"""
    selector = TweetSelector()
    selected_tweet = await selector.select_best_tweet()
    if selected_tweet:
        print(f"Hourly tweet selected and posted: {selected_tweet}")
    else:
        print("No tweet selected this hour") 