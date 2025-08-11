import json
import re
from collections import Counter
import plotly.express as px
from wordcloud import WordCloud
import numpy as np
from PIL import Image

with open("repo_data.json", "r") as json_file:
    repo_data = json.load(json_file)

# Check if we have any data
if not repo_data.get("repo_stats"):
    print("❌ No repository data found. Please run data_scrape.py first.")
    exit(1)

# Try to get commit messages from recent_commits first, fallback to repo commit_messages
all_commit_messages = ""
if repo_data.get("recent_commits"):
    all_commit_messages = " ".join(
        commit.get("message", "") for commit in repo_data["recent_commits"]
    )
else:
    # Fallback to old structure if it exists
    all_commit_messages = " ".join(
        message for repo in repo_data["repo_stats"] 
        for message in repo.get("commit_messages", [])
    )

if not all_commit_messages.strip():
    print("❌ No commit messages found. Please run data_scrape.py first to collect data.")
    exit(1)

print(f"📝 Found {len(all_commit_messages.split())} words in commit messages")
print(f"📊 Processing {len(repo_data.get('repo_stats', []))} repositories")

processed_text = re.sub(r"[^a-zA-Z\s]", "", all_commit_messages).lower()

ignore_words = {
    "initial", "commit", "for", "the", "and", "to", "in", "of", "on", "with", "from",
    "by", "a", "an", "readme", "readmemd", "is", "python", "that", "this", "some",
    "update", "beauxmain", "be", "into", "end", "was", "made",
}

word_counts = Counter(word for word in processed_text.split() if word not in ignore_words)
print(f"🔤 Found {len(word_counts)} unique words after filtering")

if not word_counts:
    print("❌ No words found after filtering. Check if commit messages contain meaningful text.")
    exit(1)

top_60_words = dict(word_counts.most_common(60))
print(f"📊 Top word: '{max(word_counts, key=word_counts.get)}' with {max(word_counts.values())} occurrences")

pastel_colors = [
    "#f8d7da",  # Pastel red
    "#d4edda",  # Pastel green
    "#d1ecf1",  # Pastel blue
    "#fff3cd",  # Pastel yellow
    "#f8d7da",  # Pastel pink
    "#e2e0eb"   # Pastel purple
]

def color_func(word, **kwargs):
    return np.random.choice(pastel_colors)

wordcloud = WordCloud(
    width=800, 
    height=400, 
    background_color="#22272E",
    color_func=color_func,
).generate_from_frequencies(top_60_words)

wordcloud_image = np.array(wordcloud)

fig = px.imshow(wordcloud_image)

fig.update_layout(
    font=dict(family="Arial, sans-serif", size=14, color="rgb(255, 255, 255)"),
    title="Top 60 Words in Commit Messages Word Cloud",
    xaxis={"visible": False},
    yaxis={"visible": False},
    margin=dict(l=0, r=0, t=30, b=0),
    plot_bgcolor="#22272E",
    paper_bgcolor="#22272E",
)

fig.write_image("DataVisuals/wordcloud.png", width=1200, height=800)

print("Word cloud image created and saved successfully.")
