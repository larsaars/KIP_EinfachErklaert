import os
import sys
import subprocess
import json
import pandas as pd

'''
run once to cache the matches from existing files
'''

# add git root dir to the python path to enable importing services module (and by that BaseScraper and DataHandler)
sys.path.append(subprocess.check_output('git rev-parse --show-toplevel'.split()).decode('utf-8').strip())

# paths
base_folder = 'data/mdr/easy'
output_file = 'data/mdr/match_cashe_mdr.csv'

data_list = []

# iterate over eacch folder
for folder_name in os.listdir(base_folder):
    folder_path = os.path.join(base_folder, folder_name)
    
    if os.path.isdir(folder_path):
        metadata_file = os.path.join(folder_path, 'metadata.json')
        
        if os.path.exists(metadata_file):
            with open(metadata_file, 'r', encoding='utf-8') as file:
                metadata = json.load(file)
                if metadata.get('match') != None:
                    data_list.append({
                        'url': metadata.get('url'),
                        'match': metadata.get('match')
                    })

df = pd.DataFrame(data_list)
df.to_csv(output_file, index=False)

