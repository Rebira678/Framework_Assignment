import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Seaborn style
sns.set(style="whitegrid", palette="muted")


# Load dataset
df = pd.read_csv("metadata.csv")

# Keep only relevant columns
df = df[['title', 'abstract', 'publish_time', 'authors', 'journal']]

# Fill missing abstracts
df['abstract'] = df['abstract'].fillna("No abstract provided")

# Convert publish_time to datetime
df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
df = df.dropna(subset=['title', 'publish_time'])
df['year'] = df['publish_time'].dt.year

# Reset index
df = df.reset_index(drop=True)


# Page title
st.set_page_config(page_title="COVID-19 Research Dashboard", layout="wide")
st.title("COVID-19 Research Papers Analysis")
st.markdown("Explore trends and insights from the CORD-19 dataset.")

# Sidebar filter: Year range
year_min = int(df['year'].min())
year_max = int(df['year'].max())
year_range = st.sidebar.slider("Select Year Range", year_min, year_max, (2020, 2023))

# Filter dataframe based on selection
filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]


st.subheader("Sample Papers")
st.dataframe(filtered_df[['title', 'authors', 'journal', 'year']].head(10))


# Publications per year
st.subheader("Number of Papers Published Per Year")
pubs_per_year = filtered_df.groupby('year').size()
fig, ax = plt.subplots(figsize=(10,5))
sns.barplot(x=pubs_per_year.index, y=pubs_per_year.values, palette='coolwarm', ax=ax)
ax.set_xlabel("Year")
ax.set_ylabel("Number of Papers")
st.pyplot(fig)

# Top 10 Journals
st.subheader("Top 10 Journals")
top_journals = filtered_df['journal'].value_counts().head(10)
fig2, ax2 = plt.subplots(figsize=(10,5))
sns.barplot(y=top_journals.index, x=top_journals.values, palette='plasma', ax=ax2)
ax2.set_xlabel("Number of Papers")
ax2.set_ylabel("Journal")
st.pyplot(fig2)
