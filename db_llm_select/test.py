from tweet_selector import TweetSelector
from db_operations import DatabaseManager

def test_db_connection():
    db = DatabaseManager()
    try:
        db.cur.execute("SELECT 1")
        result = db.cur.fetchone()
        print("Database connection successful:", result)
    except Exception as e:
        print("Database connection failed:", e)

def main():
    print("Testing database connection...")
    test_db_connection()
    print("\nRunning hourly selection...")
    selector = TweetSelector()
    selected_tweet = selector.select_best_tweet()
    if selected_tweet:
        print(f"Tweet selected: {selected_tweet}")
    else:
        print("No tweet selected")

if __name__ == "__main__":
    main()