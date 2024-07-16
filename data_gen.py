import json
from collections import Counter
from datetime import datetime

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dotenv import load_dotenv
import os

import re

load_dotenv()
TODAY = os.getenv("TODAY")
GITHUB_RUN_ID = os.getenv("GITHUB_RUN_ID")


repo_data = {"repo_stats": []}

with open("repo_data.json", "r") as json_file:
    repo_data = json.load(json_file)

library_counts = Counter()
excluded_libraries = ["time", "random"]

total_lines_of_code = sum(repo["total_python_lines"]
                          for repo in repo_data["repo_stats"])
libraries_used = set()

for repo in repo_data["repo_stats"]:
    for library in repo["libraries"]:
        if library not in excluded_libraries:
            library_counts[library] += 1
            libraries_used.update(repo["libraries"])

total_libraries_used = len(libraries_used)

top_libraries = library_counts.most_common(15)
libraries, counts = zip(*top_libraries)

# Define colors for the bar chart
colors = [
    "#ff6f61",
    "#a4e4b1",
    "#ffb347",
    "#4ecdc4",
    "#d1ccc0",
    "#ff6b6b",
    "#6ab04c",
    "#d6a2e8",
    "#ff9ff3",
    "#7bed9f",
    "#feca57",
    "#1abc9c",
    "#ff6348",
    "#686de0",
    "#ff4757",
]

# Bar chart of the top 15 libraries used
fig = go.Figure(
    data=[
        go.Bar(
            x=libraries,
            y=counts,
            text=counts,
            textposition="auto",
            marker_color=colors,
            textfont=dict(size=18, weight="bold"),
        )
    ]
)

fig.update_layout(
    title="Top 15 Libraries Used Across Repositories",
    yaxis_title="Count",
    xaxis_tickangle=-45,
    font=dict(family="Arial, sans-serif", size=14, color="rgb(255, 255, 255)"),
    plot_bgcolor="#22272E",
    paper_bgcolor="#22272E",
    margin=dict(l=40, r=40, t=60, b=100),
    hovermode="x unified",
    yaxis=dict(showticklabels=False, ticks="", showgrid=False, zeroline=False),
)

fig.write_image("top_libraries.png", width=1200, height=800)

# Sort repositories by total lines of code in descending order
sorted_repos = sorted(
    repo_data["repo_stats"], key=lambda x: x["total_python_lines"], reverse=True)


# Extract repository names, total lines of code, and total PRs for the top 7 repositories
top_repos = sorted_repos[:7]
repo_names = [repo["repo_name"] for repo in top_repos]
lines_of_code = [repo["total_python_lines"] for repo in top_repos]
total_commits = [repo["total_commits"]
    for repo in top_repos]

df = pd.DataFrame({
    "Repository Name": repo_names,
    "Lines of Python Code": lines_of_code,
    "Total Commits": total_commits
})

# Line chart of the top 7 repositories by lines of code and total PRs
fig = px.scatter(df, x="Repository Name", y="Lines of Python Code", size="Total Commits", color="Total Commits", text="Lines of Python Code", color_continuous_scale=px.colors.sequential.Viridis,)

fig.update_traces(
    line=dict(width=7),
    marker=dict(size=df["Total Commits"] * 10),
    texttemplate="%{x} <br> Lines of Code: %{y}<br>Total Commits: %{text}",
    text=[f"{size//10}" for size in df["Total Commits"] * 10],
    textposition="bottom center",
)

fig.update_layout(
    title="Repos by Lines of Python Code and Total Commits",
    font=dict(family="Arial, sans-serif", size=14, color="rgb(255, 255, 255)"),
    xaxis=dict(
        showgrid=False, 
        showticklabels=False,
        
    ),
    yaxis=dict(
        showgrid=False, 
        showticklabels=False, 
        zeroline=False,
        visible=False,
        showline = False,     
        range=[0, df["Lines of Python Code"].max() + 100]
    ),
    yaxis_title=None,
    xaxis_title=None, 
    plot_bgcolor="#22272E",
    paper_bgcolor="#22272E",
    margin=dict(l=40, r=40, t=60, b=0),
)
fig.write_image("top_lines.png", width=1200, height=800) 


construct_count = repo_data["construct_count"]

df = pd.DataFrame(list(construct_count.items()), columns=['Construct', 'Count'])

df = df.sort_values(by='Count', ascending=False).head(15)

colors = [
    "#ff6f61", "#a4e4b1", "#ffb347", "#4ecdc4", "#d1ccc0",
    "#ff6b6b", "#6ab04c", "#d6a2e8", "#ff9ff3", "#7bed9f",
    "#feca57", "#1abc9c", "#ff6348", "#686de0", "#ff4757"
]


fig = go.Figure(
    data=[
        go.Bar(
            x=df['Construct'],
            y=df['Count'],
            text=df['Count'],
            textposition="auto",
            marker_color=colors[:len(df)],
            textfont=dict(size=14, weight="bold"),
        )
    ]
)

fig.update_layout(
    title="Python Construct Counts",
    yaxis_title="Count",
    xaxis_tickangle=-45,
    font=dict(family="Arial, sans-serif", size=14, color="rgb(255, 255, 255)"),
    plot_bgcolor="#22272E",
    paper_bgcolor="#22272E",
    margin=dict(l=40, r=40, t=60, b=100),
    yaxis=dict(showticklabels=False, ticks="", showgrid=False, zeroline=False),

)

fig.write_image("construct_counts.png", width=1200, height=800)

def format_pr_info(prs):
    formatted_info = []
    for pr in prs:
        pr_info = (
            f'- **[{pr["title"]}]({pr["url"]})**\n'
            f'  - Repository: [{pr["repository"]}]({pr["repo_url"]})\n'
            f'  - Stars: {pr["stars"]}\n'
        )
        formatted_info.append(pr_info)
    return "\n".join(formatted_info)


# Update README.md with new metrics section
readme_file = "README.md"
timestamp = datetime.now().strftime("%Y-%m-%d")
recent_prs_section = f"# 🔀 Recently Merged Pull Requests\n\n{format_pr_info(repo_data['merged_prs'][:3])}\n"

new_metrics_section = [
    f"\n\n",
    f"### Data last generated on: {timestamp} via [GitHub Action {GITHUB_RUN_ID}](https://github.com/sockheadrps/sockheadrps/actions/runs/{GITHUB_RUN_ID})\n\n"
    f"  {recent_prs_section}\n",
    f"# 📊 Python Stats:\n\n",
    f"### Total Lines of Python Code: {total_lines_of_code}\n",
    f"### Total Libraries/Modules Imported: {total_libraries_used}\n\n",
    f"![](data.gif)\n\n",
]

with open(readme_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find the position of '---' in the existing content
split_index = -1
for i, line in enumerate(lines):
    if line.strip() == "---":
        split_index = i
        break

updated_lines = lines[: split_index + 1]  # Include the '---' line
updated_lines += new_metrics_section

# Write updated content back to README.md
with open(readme_file, "w", encoding="utf-8") as f:
    f.writelines(updated_lines)
