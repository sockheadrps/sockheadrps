from github import Github
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()

ACCESS_TOKEN = os.getenv("TOKEN")

g = Github(ACCESS_TOKEN)

user = g.get_user()


def count_lines(content):
    return len(content.splitlines())


# Function to find Python libraries in a file content
def find_python_libraries(content):
    libraries = set()
    import_patterns = [r"^import\s+(\w+)", r"^from\s+(\w+)\s+import"]
    for line in content.splitlines():
        for pattern in import_patterns:
            match = re.match(pattern, line)
            if match:
                libraries.add(match.group(1))
    return libraries


repo_data = []

for repo in user.get_repos():
    # Only process repositories that are not forks
    if not repo.fork:
        repo_info = {"repo_name": repo.name, "python_files": [], "libraries": set(), "total_python_lines": 0}

        contents = repo.get_contents("")

        while contents:
            file_content = contents.pop(0)

            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                file_extension = os.path.splitext(file_content.path)[1]

                # Only process .py files
                if file_extension == ".py":
                    # Check the encoding and decode if it's base64
                    if file_content.encoding == "base64":
                        try:
                            file_content_data = file_content.decoded_content.decode("utf-8")
                            repo_info["python_files"].append(file_content.path)
                            repo_info["total_python_lines"] += count_lines(file_content_data)
                            repo_info["libraries"].update(find_python_libraries(file_content_data))

                        # Skip files that are not UTF-8 encoded, images, etc
                        except UnicodeDecodeError:
                            print(f"Skipping non-UTF-8 file: {file_content.path}")
                    else:
                        print(f"Skipping file with unsupported encoding: {file_content.path}")

        # Convert libraries set to list for JSON serialization
        repo_info["libraries"] = list(repo_info["libraries"])

        repo_data.append(repo_info)

# Save the data as JSON
with open("repo_data.json", "w") as json_file:
    json.dump(repo_data, json_file, indent=4)
