from kafka import KafkaConsumer
import pymongo
import json

# === MongoDB Setup ===
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["twitter_db"]
collection = db["tweets_kafka"]

# === Kafka Consumer Setup ===
consumer = KafkaConsumer(
    'tweets-topic',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',  # or 'latest'
    enable_auto_commit=True,
    group_id='tweet-consumer-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("📡 Listening to Kafka topic...")

# === Listen for messages and store to MongoDB ===
for message in consumer:
    tweet_data = message.value
    collection.insert_one(tweet_data)
    print(f"✅ Stored to MongoDB: [{tweet_data['sentiment'].upper()}] {tweet_data['cleaned_text'][:60]}...")
