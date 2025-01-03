from flask import Flask, request, jsonify
from db_operations import DatabaseManager
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import time
from tweet_selector import TweetSelector
import numpy as np

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Accept"],
        "expose_headers": ["Content-Type"]
    }
})

# Initialize database manager
db = DatabaseManager()

# Error handler for generic exceptions
@app.errorhandler(Exception)
def handle_error(error):
    return jsonify({
        "error": str(error),
        "status": "error"
    }), 500

# User endpoints
@app.route('/users', methods=['POST'])
def create_user():
    print("Creating user with wallet address:", request.get_json())
    data = request.get_json()
    wallet_address = data.get('wallet_address')
    if not wallet_address:
        return jsonify({"error": "wallet_address is required"}), 400
    
    user = db.create_user(wallet_address)
    return jsonify(user), 201

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = db.get_user(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    wallet_address = data.get('wallet_address')
    if not wallet_address:
        return jsonify({"error": "wallet_address is required"}), 400
    
    user = db.update_user(user_id, wallet_address)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)

# Submission endpoints
@app.route('/submissions', methods=['POST'])
def create_submission():
    try:
        data = request.get_json()
        tweet_text = data.get('tweet_text')
        bid_amount = data.get('bid_amount')
        wallet_address = data.get('wallet_address')
        
        if not all([tweet_text, bid_amount, wallet_address]):
            return jsonify({"error": "tweet_text, bid_amount, and wallet_address are required"}), 400
        
        submission = db.create_submission(tweet_text, float(bid_amount), wallet_address)
        print(f"\n=== New Submission Created ===")
        print(f"Tweet: {tweet_text}")
        print(f"Bid Amount: {bid_amount} SOL")
        print(f"Wallet: {wallet_address}")
        print("============================\n")
        
        return jsonify({
            **submission,
            "message": "Submission successfully created and stored in database!"
        }), 201
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

@app.route('/submissions/<int:submission_id>', methods=['GET'])
def get_submission(submission_id):
    submission = db.get_submission(submission_id)
    if not submission:
        return jsonify({"error": "Submission not found"}), 404
    return jsonify(submission)

@app.route('/submissions/<int:submission_id>/status', methods=['PUT'])
def update_submission_status(submission_id):
    data = request.get_json()
    status = data.get('status')
    if not status:
        return jsonify({"error": "status is required"}), 400
    
    submission = db.update_submission_status(submission_id, status)
    if not submission:
        return jsonify({"error": "Submission not found"}), 404
    return jsonify(submission)

@app.route('/users/<int:user_id>/submissions', methods=['GET'])
def get_user_submissions(user_id):
    submissions = db.get_user_submissions(user_id)
    return jsonify(submissions)

# Tweet endpoints
@app.route('/tweets', methods=['POST'])
def create_tweet():
    data = request.get_json()
    tweet_text = data.get('tweet_text')
    if not tweet_text:
        return jsonify({"error": "tweet_text is required"}), 400
    
    tweet = db.create_tweet(tweet_text)
    return jsonify(tweet), 201

@app.route('/tweets/<int:tweet_id>', methods=['GET'])
def get_tweet(tweet_id):
    tweet = db.get_tweet(tweet_id)
    if not tweet:
        return jsonify({"error": "Tweet not found"}), 404
    return jsonify(tweet)

@app.route('/tweets/<int:tweet_id>/comments', methods=['GET'])
def get_tweet_comments(tweet_id):
    comments = db.get_tweet_comments(tweet_id)
    return jsonify(comments)

@app.route('/tweets', methods=['GET'])
def get_tweets():
    try:
        # Get all tweets ordered by creation time, most recent first
        db.cur.execute("""
            SELECT tweet_text, wallet_address, payout_amount, created_at 
            FROM tweets 
            ORDER BY created_at DESC
            LIMIT 50
        """)
        tweets = db.cur.fetchall()
        
        formatted_tweets = []
        for tweet in tweets:
            formatted_tweets.append({
                'tweet_text': tweet['tweet_text'],
                'wallet_address': tweet['wallet_address'],
                'payout_amount': float(tweet['payout_amount']),
                'created_at': tweet['created_at'].isoformat() if tweet['created_at'] else None
            })
        
        return jsonify(formatted_tweets)
    except Exception as e:
        print(f"Error fetching tweets: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Comment endpoints
@app.route('/comments', methods=['POST'])
def create_comment():
    data = request.get_json()
    tweet_id = data.get('tweet_id')
    user_id = data.get('user_id')
    comment_text = data.get('comment_text')
    
    if not all([tweet_id, user_id, comment_text]):
        return jsonify({"error": "tweet_id, user_id, and comment_text are required"}), 400
    
    comment = db.create_comment(tweet_id, user_id, comment_text)
    return jsonify(comment), 201

@app.route('/comments/<int:comment_id>', methods=['GET'])
def get_comment(comment_id):
    comment = db.get_comment(comment_id)
    if not comment:
        return jsonify({"error": "Comment not found"}), 404
    return jsonify(comment)

@app.route('/total_potential_payout', methods=['POST'])
def total_potential_payout():
    try:
        data = request.get_json()
        user_bid = float(data.get('bid_amount', 0))
        
        if user_bid <= 0:
            return jsonify({"error": "bid_amount must be greater than 0"}), 400

        # Get all bids from the last hour
        one_hour_ago = datetime.now() - timedelta(hours=1)
        db.cur.execute(
            """
            SELECT bid_amount FROM submissions 
            WHERE created_at > %s
            """,
            (one_hour_ago,)
        )
        existing_bids = [float(row['bid_amount']) for row in db.cur.fetchall()]
        
        # Add the user's hypothetical bid
        all_bids = existing_bids + [user_bid]
        
        # Calculate percentile of user's bid
        percentile = np.percentile(all_bids, all_bids.index(user_bid) * 100.0 / len(all_bids))
        
        # Calculate reward percentage (scales from 30% to 70%)
        reward_percentage = 0.3 + (percentile / 100.0 * 0.4)
        
        # Calculate total pool and adjusted pool
        total_pool = sum(all_bids)
        adjusted_pool = total_pool - user_bid
        
        # Calculate reward from pool
        reward_from_pool = adjusted_pool * reward_percentage
        
        # Total potential payout is their bid back plus their share of the pool
        total_payout = user_bid + reward_from_pool
        
        return jsonify({
            "potential_payout": total_payout,
            "original_bid": user_bid,
            "additional_reward": reward_from_pool
        })

    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

# Add this function for the scheduled task
def print_hi():
    print(f"hi (Current time: {datetime.now().strftime('%H:%M:%S')})")

def run_hourly_selection_wrapper():
    """Wrapper to run selection in scheduler"""
    selector = TweetSelector()
    selected_tweet = selector.select_best_tweet()
    if selected_tweet:
        print(f"Hourly tweet selected and posted: {selected_tweet}")
    else:
        print("No tweet selected this hour")

# Add scheduler setup before the app.run
if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=run_hourly_selection_wrapper, trigger='cron', hour='*', minute='0')
    scheduler.start()
    
    app.run(debug=True, port=6000, host='0.0.0.0')