-- First drop existing tables (in reverse order of dependencies)
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS tweets;
DROP TABLE IF EXISTS submissions;

-- Submissions table
CREATE TABLE submissions (
    submission_id SERIAL PRIMARY KEY,
    tweet_text TEXT NOT NULL,
    bid_amount DECIMAL(18,8) NOT NULL,
    wallet_address TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tweets table
CREATE TABLE tweets (
    tweet_id SERIAL PRIMARY KEY,
    tweet_text TEXT NOT NULL,
    wallet_address TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Comments table
CREATE TABLE comments (
    comment_id SERIAL PRIMARY KEY,
    tweet_id INTEGER REFERENCES tweets(tweet_id),
    comment_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
); 