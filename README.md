# TweetPulse: Real-Time Twitter Sentiment Analysis

## Overview
A Kafka → MongoDB → Streamlit pipeline that collects tweets on #AI/#Tech, runs VADER sentiment, stores results, and visualizes trends.

## Getting Started

1. **Clone**  
   ```bash
   git clone https://github.com/your-username/project210.git
   cd project210

2. **Setup**

bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

3. **Run**

Start Mongo: brew services start mongodb-community

Start Kafka+Zoo (or Docker)

python tweepy_collector.py

python tweet_producer.py

python tweet_consumer.py

streamlit run dashboard.py

4.**Hypothesis Tests**

bash
Copy
Edit
python hypothesis_tests.py
File Structure
Copy
Edit
├─ tweepy_collector.py
├─ tweet_producer.py
├─ tweet_consumer.py
├─ dashboard.py
├─ hypothesis_tests.py
├─ requirements.txt
└─ README.md