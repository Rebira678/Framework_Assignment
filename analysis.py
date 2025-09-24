import pandas as pd

# Load the dataset
df = pd.read_csv("metadata.csv")

# Quick peek at the first rows
print(df.head())

# Check shape and missing values
print(df.shape)
print(df.info())


# Step 2: Data Cleaning

# Keep only relevant columns
df = df[['title', 'abstract', 'publish_time', 'authors', 'journal']]

# Drop rows where 'title' or 'publish_time' is missing
df = df.dropna(subset=['title', 'publish_time'])

# Fill missing abstracts with a placeholder
df['abstract'] = df['abstract'].fillna("No abstract provided")

# Convert publish_time to datetime
df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')

# Drop rows with invalid publish_time
df = df.dropna(subset=['publish_time'])

# Reset index
df = df.reset_index(drop=True)

# Check cleaned data
print(df.info())
print(df.head())



import matplotlib.pyplot as plt
import seaborn as sns

# Set Seaborn style for attractive visuals
sns.set(style="whitegrid", palette="muted")

# 1️⃣ Number of papers published per year
df['year'] = df['publish_time'].dt.year
pubs_per_year = df.groupby('year').size()

plt.figure(figsize=(12,6))
sns.barplot(x=pubs_per_year.index, y=pubs_per_year.values, palette='viridis')
plt.title("Number of COVID-19 Papers Published Per Year", fontsize=16)
plt.xlabel("Year", fontsize=12)
plt.ylabel("Number of Papers", fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 2️⃣ Top 10 journals by publication count
top_journals = df['journal'].value_counts().head(10)

plt.figure(figsize=(12,6))
sns.barplot(y=top_journals.index, x=top_journals.values, palette='magma')
plt.title("Top 10 Journals Publishing COVID-19 Research", fontsize=16)
plt.xlabel("Number of Papers", fontsize=12)
plt.ylabel("Journal", fontsize=12)
plt.tight_layout()
plt.show()
