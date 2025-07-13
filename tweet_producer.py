# tweet_producer.py

import tweepy
import json
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from kafka import KafkaProducer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

# NLTK downloads
nltk.download('punkt')
nltk.download('stopwords')

# Twitter credentials
BEARER_TOKEN = ""

# Kafka setup
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Cleaning functions
def clean_tweet(text):
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"#", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def tokenize_and_filter(text):
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    return [t for t in tokens if t.isalpha() and t not in stop_words]

# Twitter client
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Search query
query = "(#AI OR #MachineLearning OR #Tech) -is:retweet lang:en"
response = client.search_recent_tweets(
    query=query,
    tweet_fields=["id", "text", "created_at", "author_id"],
    max_results=10
)

# Send tweets to Kafka
if response.data:
    for tweet in response.data:
        cleaned_text = clean_tweet(tweet.text)
        tokens = tokenize_and_filter(cleaned_text)
        score = analyzer.polarity_scores(cleaned_text)
        sentiment = (
            "positive" if score["compound"] > 0.05 else
            "negative" if score["compound"] < -0.05 else
            "neutral"
        )

        tweet_data = {
            "id": tweet.id,
            "original_text": tweet.text,
            "cleaned_text": cleaned_text,
            "tokens": tokens,
            "created_at": tweet.created_at.isoformat(),
            "author_id": tweet.author_id,
            "sentiment": sentiment,
            "score": score
        }

        # Send to Kafka
        producer.send("tweets-topic", tweet_data)
        print(f"🌀 Sent to Kafka: [{sentiment.upper()}] {cleaned_text[:60]}...")

    producer.flush()
else:
    print("❌ No tweets found.")
