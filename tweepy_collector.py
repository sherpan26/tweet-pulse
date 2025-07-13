import tweepy
import pymongo
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

# === One-time downloads for NLTK ===
nltk.download('punkt')
nltk.download('stopwords')

# === Twitter Bearer Token ===
BEARER_TOKEN = ""

# === MongoDB Setup ===
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["twitter_db"]
collection = db["tweets"]

# === Twitter API Client ===
twitter_client = tweepy.Client(bearer_token=BEARER_TOKEN)

# === Sentiment Analyzer ===
analyzer = SentimentIntensityAnalyzer()

# === Text Cleaning Function ===
def clean_tweet(text):
    text = re.sub(r"http\S+", "", text)        # Remove URLs
    text = re.sub(r"@\w+", "", text)           # Remove mentions
    text = re.sub(r"#", "", text)              # Remove hashtag symbols
    text = re.sub(r"\s+", " ", text).strip()   # Normalize whitespace
    return text

# === Tokenization & Stopword Removal ===
def tokenize_and_filter(text):
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    return [t for t in tokens if t.isalpha() and t not in stop_words]

# === Hashtag-Based Search Query ===
query = "(#AI OR #MachineLearning OR #Tech) -is:retweet lang:en"

# === Fetch Recent Tweets ===
response = twitter_client.search_recent_tweets(
    query=query,
    tweet_fields=["id", "text", "created_at", "author_id"],
    max_results=10
)

# === Process and Store Each Tweet ===
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

        tweet_doc = {
            "id": tweet.id,
            "original_text": tweet.text,
            "cleaned_text": cleaned_text,
            "tokens": tokens,
            "created_at": tweet.created_at.isoformat(),
            "author_id": tweet.author_id,
            "sentiment": sentiment,
            "score": score
        }

        collection.insert_one(tweet_doc)
        print(f"✅ [{sentiment.upper()}] {cleaned_text[:60]}...")
else:
    print("❌ No tweets found.")
