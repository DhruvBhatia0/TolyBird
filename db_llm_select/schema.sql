-- Users table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    wallet_address VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Submissions table
CREATE TABLE submissions (
    submission_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    tweet_text TEXT NOT NULL,
    bid_amount DECIMAL(18,8) NOT NULL,
    status VARCHAR(50) DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tweets table
CREATE TABLE tweets (
    tweet_id SERIAL PRIMARY KEY,
    tweet_text TEXT NOT NULL,
    tweeted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Comments table
CREATE TABLE comments (
    comment_id SERIAL PRIMARY KEY,
    tweet_id INTEGER REFERENCES tweets(tweet_id),
    user_id INTEGER REFERENCES users(user_id),
    comment_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
); 