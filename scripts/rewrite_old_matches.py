import os
import sys
import subprocess
import json
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

git_root = (
    subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True)
    .strip()
)
sys.path.append(subprocess.check_output('git rev-parse --show-toplevel'.split()).decode('utf-8').strip())

from matchers.SimpleMatcher import SimpleMatcher


"""
my name is giovanni giorgio
but everybody calls me giorgio
"""

# paths
base_folder = os.path.join(git_root, "data", "mdr", "easy")

data_list = []

sm = SimpleMatcher("mdr")

# iterate over each folder
for folder_name in os.listdir(base_folder):
    folder_path = os.path.join(base_folder, folder_name)

    if os.path.isdir(folder_path):
        metadata_file = os.path.join(folder_path, "metadata.json")

        if os.path.exists(metadata_file):
            with open(metadata_file, "r", encoding="utf-8") as file:
                metadata = json.load(file)
                if metadata.get("match") != None:
                    sm.match_by_url(metadata.get("url"), metadata.get("match"))
