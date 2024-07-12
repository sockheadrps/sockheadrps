import json
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime

# Load JSON data
with open('repo_data.json', 'r') as f:
    repo_data = json.load(f)

# Extract all libraries used and count occurrences
library_counts = Counter()
excluded_libraries = ['time', 'random']

total_lines_of_code = sum(repo["total_python_lines"] for repo in repo_data)
libraries_used = set()

for repo in repo_data:
    for library in repo['libraries']:
        if library not in excluded_libraries:
            library_counts[library] += 1
            libraries_used.update(repo["libraries"])


total_libraries_used = len(libraries_used)


# Get the top 15 libraries by frequency
top_libraries = library_counts.most_common(15)
libraries, counts = zip(*top_libraries)

# Custom colors for the bar chart
colors = ['#ff6f61', '#a4e4b1', '#ffb347', '#4ecdc4', '#d1ccc0',
          '#ff6b6b', '#6ab04c', '#d6a2e8', '#ff9ff3', '#7bed9f',
          '#feca57', '#1abc9c', '#ff6348', '#686de0', '#ff4757']

# Plotting the bar chart with custom background and text colors
plt.figure(figsize=(12, 6))
plt.rcParams['axes.facecolor'] = '#22272e'  # Background color rgb(34,39,46)
plt.rcParams['text.color'] = 'black'        # Text color black
bars = plt.bar(libraries, counts, color=colors)

# Adding labels and title with bold text
# Library names color and bold
plt.xlabel('Libraries', color='black', fontweight='bold')
# Frequency labels color and bold
plt.ylabel('Frequency', color='black', fontweight='bold')
plt.title('Top 15 Libraries Used', color='black', fontweight='bold')
plt.xticks(rotation=45, ha='right', color='black',
           fontweight='bold')  # X-axis ticks color and bold
plt.yticks(color='black', fontweight='bold')  # Y-axis ticks color and bold
# Ensure tight layout with background color
plt.tight_layout(rect=[0, 0, 1, 1])

# Removing horizontal grid lines
# Set linestyle to empty string to remove grid lines
plt.grid(axis='y', linestyle='')

# Customizing spines
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

# Adding neon effect with glow effect around bars
for bar in bars:
    bar.set_edgecolor('#0f0f0f')
    bar.set_linewidth(1.5)
plt.savefig('top_libs.png', dpi=300, bbox_inches='tight')


# Update README.md with the calculated values
readme_file = 'README.md'

# Calculate current timestamp
timestamp = datetime.now().strftime('%Y-%m-%d')

# Prepare the new metrics section content
new_metrics_section = (
    f'### Data last generated on: {timestamp}\n\n'
    f'## Top Libraries Used\n\n'
    f'![](top_libs.png)\n\n'
    f'## Project Metrics\n\n'
    f'- Total Lines of Python Code: {total_lines_of_code}\n'
    f'- Total Libraries/Modules Imported: {total_libraries_used}\n'
)

# Read existing README.md content
with open(readme_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
# Check if Project Metrics section already exists
found_metrics_section = False
for idx, line in enumerate(lines):
    if line.strip().startswith('## Project Metrics'):
        found_metrics_section = True
        break

# Update or add the metrics section in README.md
if found_metrics_section:
    # Replace existing metrics section
    updated_lines = []
    in_metrics_section = False
    for line in lines:
        if line.strip().startswith('- Total Lines of Python Code:'):
            in_metrics_section = True
        elif line.strip().startswith('- '):
            in_metrics_section = False
        if not in_metrics_section:
            updated_lines.append(line)
    updated_lines.append(new_metrics_section)
else:
    # Append new metrics section at the end
    lines.append('\n')
    lines.append(new_metrics_section)

# Write updated README.md content
with open(readme_file, 'w', encoding='utf-8') as f:
    f.write(''.join(lines))
