import pandas as pd
from pymongo import MongoClient
from scipy.stats import ttest_ind

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["twitter_db"]
collection = db["tweets"]

# Load data from api mongodb
df = pd.DataFrame(list(collection.find()))

#cleanup
df = df.drop(columns=["_id"])  # Drop MongoDB's internal ID column

print(df.columns)
print(df.head())

# Hypothesis Test (example): Positive vs Negative sentiment score ===

# converting compound scores
df["compound"] = df["score"].apply(lambda s: s["compound"] if isinstance(s, dict) else None)

# split by sentiment label
positive = df[df["sentiment"] == "positive"]["compound"]
negative = df[df["sentiment"] == "negative"]["compound"]

# run Welch's t-test
stat, p = ttest_ind(positive.dropna(), negative.dropna(), equal_var=False)
print("Positive vs Negative → t = {:.3f}, p = {:.3f}".format(stat, p))
