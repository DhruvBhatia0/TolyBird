from tweet_selector import run_hourly_selection
from db_operations import DatabaseManager

def test_db_connection():
    db = DatabaseManager()
    try:
        db.cur.execute("SELECT 1")
        result = db.cur.fetchone()
        print("Database connection successful:", result)
    except Exception as e:
        print("Database connection failed:", e)

if __name__ == "__main__":
    print("Testing database connection...")
    test_db_connection()
    print("\nRunning hourly selection...")
    run_hourly_selection()