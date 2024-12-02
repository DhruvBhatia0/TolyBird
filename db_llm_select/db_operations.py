import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        self.cur = self.conn.cursor(cursor_factory=RealDictCursor)

    def __del__(self):
        self.cur.close()
        self.conn.close()

    # Users CRUD operations
    def create_user(self, wallet_address: str) -> Dict:
        self.cur.execute(
            "INSERT INTO users (wallet_address) VALUES (%s) RETURNING *",
            (wallet_address,)
        )
        self.conn.commit()
        return dict(self.cur.fetchone())

    def get_user(self, user_id: int) -> Optional[Dict]:
        self.cur.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        result = self.cur.fetchone()
        return dict(result) if result else None

    def update_user(self, user_id: int, wallet_address: str) -> Optional[Dict]:
        self.cur.execute(
            "UPDATE users SET wallet_address = %s WHERE user_id = %s RETURNING *",
            (wallet_address, user_id)
        )
        self.conn.commit()
        result = self.cur.fetchone()
        return dict(result) if result else None

    def delete_user(self, user_id: int) -> bool:
        self.cur.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        self.conn.commit()
        return self.cur.rowcount > 0

    # Submissions CRUD operations
    def create_submission(self, tweet_text: str, bid_amount: float) -> Dict:
        self.cur.execute(
            "INSERT INTO submissions (tweet_text, bid_amount) VALUES (%s, %s) RETURNING *",
            (tweet_text, bid_amount)
        )
        self.conn.commit()
        return dict(self.cur.fetchone())

    def get_submission(self, submission_id: int) -> Optional[Dict]:
        self.cur.execute("SELECT * FROM submissions WHERE submission_id = %s", (submission_id,))
        result = self.cur.fetchone()
        return dict(result) if result else None

    def update_submission_status(self, submission_id: int, status: str) -> Optional[Dict]:
        self.cur.execute(
            "UPDATE submissions SET status = %s WHERE submission_id = %s RETURNING *",
            (status, submission_id)
        )
        self.conn.commit()
        result = self.cur.fetchone()
        return dict(result) if result else None

    def delete_submission(self, submission_id: int) -> bool:
        self.cur.execute("DELETE FROM submissions WHERE submission_id = %s", (submission_id,))
        self.conn.commit()
        return self.cur.rowcount > 0

    # Tweets CRUD operations
    def create_tweet(self, tweet_text: str) -> Dict:
        self.cur.execute(
            "INSERT INTO tweets (tweet_text) VALUES (%s) RETURNING *",
            (tweet_text,)
        )
        self.conn.commit()
        return dict(self.cur.fetchone())

    def get_tweet(self, tweet_id: int) -> Optional[Dict]:
        self.cur.execute("SELECT * FROM tweets WHERE tweet_id = %s", (tweet_id,))
        result = self.cur.fetchone()
        return dict(result) if result else None

    def update_tweet(self, tweet_id: int, tweet_text: str) -> Optional[Dict]:
        self.cur.execute(
            "UPDATE tweets SET tweet_text = %s WHERE tweet_id = %s RETURNING *",
            (tweet_text, tweet_id)
        )
        self.conn.commit()
        result = self.cur.fetchone()
        return dict(result) if result else None

    def delete_tweet(self, tweet_id: int) -> bool:
        self.cur.execute("DELETE FROM tweets WHERE tweet_id = %s", (tweet_id,))
        self.conn.commit()
        return self.cur.rowcount > 0

    # Comments CRUD operations
    def create_comment(self, tweet_id: int, user_id: int, comment_text: str) -> Dict:
        self.cur.execute(
            "INSERT INTO comments (tweet_id, user_id, comment_text) VALUES (%s, %s, %s) RETURNING *",
            (tweet_id, user_id, comment_text)
        )
        self.conn.commit()
        return dict(self.cur.fetchone())

    def get_comment(self, comment_id: int) -> Optional[Dict]:
        self.cur.execute("SELECT * FROM comments WHERE comment_id = %s", (comment_id,))
        result = self.cur.fetchone()
        return dict(result) if result else None

    def update_comment(self, comment_id: int, comment_text: str) -> Optional[Dict]:
        self.cur.execute(
            "UPDATE comments SET comment_text = %s WHERE comment_id = %s RETURNING *",
            (comment_text, comment_id)
        )
        self.conn.commit()
        result = self.cur.fetchone()
        return dict(result) if result else None

    def delete_comment(self, comment_id: int) -> bool:
        self.cur.execute("DELETE FROM comments WHERE comment_id = %s", (comment_id,))
        self.conn.commit()
        return self.cur.rowcount > 0

    # Additional utility methods
    def get_user_submissions(self, user_id: int) -> List[Dict]:
        self.cur.execute("SELECT * FROM submissions WHERE user_id = %s", (user_id,))
        return [dict(row) for row in self.cur.fetchall()]

    def get_tweet_comments(self, tweet_id: int) -> List[Dict]:
        self.cur.execute("SELECT * FROM comments WHERE tweet_id = %s", (tweet_id,))
        return [dict(row) for row in self.cur.fetchall()] 