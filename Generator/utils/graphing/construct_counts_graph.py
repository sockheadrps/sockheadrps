import json
import pandas as pd
import plotly.express as px
import configparser
import os

# Load the data from JSON
with open("repo_data.json", "r") as file:
    data = json.load(file)

# Print the data to check its structure
print("Data loaded from JSON:")
print(data)

config = configparser.ConfigParser()
config.read("config.ini")

GENERATE = config.getboolean("Settings", "generate_commit_heatmap")

def hour_to_am_pm(hour):
    return f"{hour % 12 or 12} {'AM' if hour < 12 else 'PM'}"

# Convert JSON data to DataFrame
# If the data is a list of dictionaries, use pd.json_normalize for nested structures
commit_counts = pd.json_normalize(data)

# Print the DataFrame structure to verify
print("DataFrame structure:")
print(commit_counts.head())

commit_counts["HourOfDay"] = commit_counts["HourOfDay"].apply(hour_to_am_pm)

heatmap_data = commit_counts.pivot(index="DayOfWeek", columns="HourOfDay", values="Count").fillna(0)

ordered_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
heatmap_data = heatmap_data.reindex(ordered_days)
hours_order = [f"{hour % 12 or 12} {'AM' if hour < 12 else 'PM'}" for hour in range(24)]
heatmap_data = heatmap_data.reindex(columns=hours_order)

fig = px.imshow(
    heatmap_data,
    labels=dict(x="Hour of Day", y="Day of Week", color="Commit Count"),
    x=heatmap_data.columns,
    y=heatmap_data.index,
    aspect="auto"
)

fig.update_layout(
    title="Heatmap of Commit Frequency by Hour of Day and Day of Week",
    xaxis_nticks=24,
    yaxis_nticks=7,
    margin=dict(l=0, r=0, t=30, b=0),
    plot_bgcolor="#22272E",
    paper_bgcolor="#22272E",
    xaxis=dict(
        tickfont=dict(color='white')
    ),
    yaxis=dict(
        tickfont=dict(color='white')
    ),
    coloraxis_colorbar=dict(
        tickfont=dict(color='white')
    )
)

if GENERATE:
    os.makedirs("DataVisuals", exist_ok=True)
    fig.write_image("DataVisuals/commit_heatmap.png", width=1200, height=800)
    print("Commit heatmap generated successfully.")
else:
    print("Commit heatmap not generated.")
