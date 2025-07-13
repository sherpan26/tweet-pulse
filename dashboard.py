import streamlit as st
import pymongo
import pandas as pd
import matplotlib.pyplot as plt

# === MongoDB Connection ===
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["twitter_db"]
collection = db["tweets_kafka"]

# === Load Tweets from MongoDB ===
tweets = list(collection.find())

# === Convert to DataFrame ===
df = pd.DataFrame(tweets)

# === Handle Missing Sentiment Field ===
df = df[df['sentiment'].notnull()]

# === Sidebar Filters (optional) ===
st.sidebar.title("Filters")
selected_sentiments = st.sidebar.multiselect(
    "Choose Sentiments", ['positive', 'neutral', 'negative'], default=['positive', 'neutral', 'negative']
)

filtered_df = df[df["sentiment"].isin(selected_sentiments)]

# === Title ===
st.title("📊 Real-Time Twitter Sentiment Dashboard")

# === Show Raw Data ===
with st.expander("🔍 Show Raw Data"):
    st.dataframe(filtered_df[["cleaned_text", "sentiment", "created_at"]])

# === Pie Chart ===
st.subheader("Sentiment Distribution")
sentiment_counts = filtered_df["sentiment"].value_counts()
fig, ax = plt.subplots()
ax.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=140)
ax.axis('equal')
st.pyplot(fig)

# === Line Chart Over Time (optional) ===
st.subheader("Sentiment Over Time")
if 'created_at' in filtered_df.columns:
    filtered_df["created_at"] = pd.to_datetime(filtered_df["created_at"])
    time_data = filtered_df.groupby([pd.Grouper(key='created_at', freq='T'), 'sentiment']).size().unstack().fillna(0)
    st.line_chart(time_data)

