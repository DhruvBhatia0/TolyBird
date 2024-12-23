from db_operations import DatabaseManager

def test_crud_operations():
    db = DatabaseManager()
    
    try:
        # 1. Test Users CRUD
        print("\n=== Testing User Operations ===")
        # Create
        user = db.create_user(wallet_address="0xabc123def456")
        print(f"Created user: {user}")
        
        # Read
        user_id = user['user_id']
        fetched_user = db.get_user(user_id)
        print(f"Fetched user: {fetched_user}")
        
        # Update
        updated_user = db.update_user(user_id, wallet_address="0xnew789address")
        print(f"Updated user: {updated_user}")

        # 2. Test Tweets CRUD
        print("\n=== Testing Tweet Operations ===")
        # Create tweet
        tweet = db.create_tweet(tweet_text="Hello Web3 World!")
        print(f"Created tweet: {tweet}")
        
        # 3. Test Comments
        print("\n=== Testing Comment Operations ===")
        comment = db.create_comment(
            tweet_id=tweet['tweet_id'],
            user_id=user_id,
            comment_text="This is a test comment!"
        )
        print(f"Created comment: {comment}")
        
        # 4. Test Submissions
        print("\n=== Testing Submission Operations ===")
        submission = db.create_submission(
            user_id=user_id,
            tweet_text="My submission tweet",
            bid_amount=0.5
        )
        print(f"Created submission: {submission}")
        
        # Test utility methods
        print("\n=== Testing Utility Methods ===")
        user_submissions = db.get_user_submissions(user_id)
        print(f"User's submissions: {user_submissions}")
        
        tweet_comments = db.get_tweet_comments(tweet['tweet_id'])
        print(f"Tweet's comments: {tweet_comments}")

        # Optional: Test deletion
        print("\n=== Testing Deletion ===")
        # Uncomment these if you want to test deletion
        # print(f"Delete comment: {db.delete_comment(comment['comment_id'])}")
        # print(f"Delete tweet: {db.delete_tweet(tweet['tweet_id'])}")
        # print(f"Delete user: {db.delete_user(user_id)}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_crud_operations()