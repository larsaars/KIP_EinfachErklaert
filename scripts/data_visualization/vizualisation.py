import os
import subprocess
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import sys
from bs4 import BeautifulSoup
import re
from word_cluster_dlf import dlf_word_cluster
from word_cluster_mdr import mdr_word_cluster

# Get git root directory
git_root = (
    subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True)
    .strip()
)

# Append the git root directory to sys.path
sys.path.append(
    subprocess.check_output("git rev-parse --show-toplevel".split())
    .decode("utf-8")
    .strip()
)

from datahandler.DataHandler import DataHandler

# Set the image directory
image_svg = os.path.join(git_root, "documentation", "images", "svg")
image_png = os.path.join(git_root, "documentation", "images", "png")

os.makedirs(image_svg, exist_ok=True)
os.makedirs(image_png, exist_ok=True)

# Function to extract date from path
def extract_date_from_path(path):
    match = re.search(r'\d{4}-\d{2}-\d{2}', path)
    if match:
        return match.group(0)
    return None

# Function to remove invisible characters
def remove_invisible_chars(text):
    return re.sub(r'[\u200b-\u200d\uFEFF]', '', text)

print("STARTING VISUALIZATION")
print("IMAGE OUT DIRECTORY: ", image_svg)
# ---------------------------------------- DATA COLLECTION ---------------------------------------- 
mdr = DataHandler("mdr")
dlf = DataHandler("dlf")

# MDR
mdr_easy_data = mdr.get_all("easy")
mdr_easy_data['source'] = 'mdr'
mdr_easy_data['niveau'] = 'easy'
mdr_hard_data = mdr.get_all("hard")
mdr_hard_data['source'] = 'mdr'
mdr_hard_data['niveau'] = 'hard'
mdr_easy_data['article'] = BeautifulSoup(" ".join(mdr_easy_data["text"].tolist()), 'lxml').get_text()
mdr_hard_data['article'] = BeautifulSoup(" ".join(mdr_hard_data["text"].tolist()), 'lxml').get_text()

# DLF
dlf_easy_data = dlf.get_all("easy")
dlf_easy_data['source'] = 'dlf'
dlf_easy_data['niveau'] = 'easy'
dlf_hard_data = dlf.get_all("hard")
dlf_hard_data['source'] = 'dlf'
dlf_hard_data['niveau'] = 'hard'
dlf_easy_data['article'] = dlf_easy_data['text']
dlf_hard_data['article'] = dlf_hard_data['text']

# JOIN ALL INTO ONE FRAME
all_data = pd.concat([mdr_easy_data, mdr_hard_data, dlf_easy_data, dlf_hard_data])
all_data['has_audio'] = all_data['audio_audio_url'].apply(lambda x : isinstance(x, str))
all_data['has_match'] = all_data['match'].apply(lambda x : isinstance(x, str))

all_data['path_date'] = all_data['path'].apply(extract_date_from_path)
all_data['path_date'] = pd.to_datetime(all_data['path_date'], errors='coerce')

all_data = all_data.replace([np.inf, -np.inf], np.nan)

all_data['article'] = all_data['article'].apply(remove_invisible_chars)

# calculate article length in words
all_data['article_length'] = all_data['article'].apply(lambda x : len(x.split(" ")))

all_data.drop(columns=['audio_audio_url', 'audio_download_url', 'audio_duration', 'text', 'match', 'date'], inplace=True)

# ---------------------------------------- VISUALIZATION ---------------------------------------- 
# Adjusting font sizes
plt.rcParams.update({'font.size': 25})  # Set the global font size

# Add the text to the plot
plt.text(0.5, 0.5, f"Anzahl der Artikel {all_data.shape[0]}", fontsize=24, ha='center', va='center')
plt.axis('off')
plt.savefig(os.path.join(image_png, 'text_plot.png'), bbox_inches='tight')

plt.axis('on')
plt.clf()

# ---------------------------------------- CAKES ---------------------------------------- 
# x3 cakes
fig, axs = plt.subplots(1, 3, figsize=(18, 8))

# Number of articles by difficulty
articles_by_niveau = all_data['niveau'].value_counts()
axs[0].pie(articles_by_niveau, labels=articles_by_niveau.index, autopct='%1.1f%%', colors=['#ff9999','#66b3ff','#99ff99'])
axs[0].set_title('Nach Schwierigkeit', fontsize=30)

# Number of articles by source
articles_by_source = all_data['source'].value_counts()
axs[1].pie(articles_by_source, labels=articles_by_source.index, autopct='%1.1f%%', colors=['#ffcc99','#c2c2f0','#ffb3e6'])
axs[1].set_title('Artikel nach Quelle', fontsize=30)

# Number of articles with audio
articles_with_audio = all_data['has_audio'].value_counts()
articles_with_audio.index = ['ohne', 'mit']
axs[2].pie(articles_with_audio, labels=articles_with_audio.index, autopct='%1.1f%%', colors=['#c2f0c2','#ff6666'])
axs[2].set_title('Artikel mit Audio', fontsize=30)

plt.tight_layout()
plt.savefig(os.path.join(image_svg, 'cakes_x3.svg'))
plt.savefig(os.path.join(image_svg, 'cakes_x3.png'))
plt.clf() 

# x4 cakes
fig, axs = plt.subplots(2, 2, figsize=(18, 14))

# Number of articles by difficulty
articles_by_niveau = all_data['niveau'].value_counts()
axs[0, 0].pie(articles_by_niveau, labels=articles_by_niveau.index, autopct='%1.1f%%', colors=['#ff9999','#66b3ff','#99ff99'])
axs[0, 0].set_title('Nach Schwierigkeit')

# Number of articles by source
articles_by_source = all_data['source'].value_counts()
axs[0, 1].pie(articles_by_source, labels=articles_by_source.index, autopct='%1.1f%%', colors=['#ffcc99','#c2c2f0','#ffb3e6'])
axs[0, 1].set_title('Artikel nach Quelle')

# Number of articles with audio
articles_with_audio = all_data['has_audio'].value_counts()
articles_with_audio.index = ['ohne', 'mit']
axs[1, 0].pie(articles_with_audio, labels=articles_with_audio.index, autopct='%1.1f%%', colors=['#c2f0c2','#ff6666'])
axs[1, 0].set_title('Artikel mit Audio')

# Number of articles with match
articles_with_audio = all_data['has_match'].value_counts()
articles_with_audio.index = ['ohne', 'mit']
axs[1, 1].pie(articles_with_audio, labels=articles_with_audio.index, autopct='%1.1f%%', colors=['#66b3ff','#ffcc99'])
axs[1, 1].set_title('Artikel mit Match')

plt.tight_layout()
plt.savefig(os.path.join(image_svg, 'cakes_x4.svg'))
plt.savefig(os.path.join(image_png, 'cakes_x4.png'))
plt.clf() 


# ---------------------------------------- LENGTH BOXPLOT ---------------------------------------- 

dlf_part = all_data[all_data['source'] == 'dlf']

plt.figure(figsize=(16, 12))  
sns.boxplot(x='niveau', y='article_length', data=dlf_part, palette='pastel', showfliers=False)
plt.title('Wörter pro Artikel bei DLF/ NL')
plt.xlabel('Sprachniveau')
plt.ylabel('Wörter')
plt.tight_layout()  # Adjust the layout
plt.savefig(os.path.join(image_svg, 'box_plot_length.svg'))
plt.savefig(os.path.join(image_png, 'box_plot_length.png'))
plt.clf()

# ---------------------------------------- ERSCHEINUNGSDATUM ---------------------------------------- 
all_data['path_date'] = pd.to_datetime(all_data['path_date'])
articles_over_time = all_data.groupby(all_data['path_date'].dt.to_period('W')).size().reset_index(name='count')
articles_over_time['path_date'] = articles_over_time['path_date'].dt.to_timestamp()

plt.figure(figsize=(24, 12))
sns.lineplot(x='path_date', y='count', data=articles_over_time, marker='o', linestyle='-')
plt.title('Veröffentlichungsdatum')
plt.xlabel('Datum')
plt.ylabel('Anzahl Artikel')
plt.grid(True)
plt.tight_layout()

plt.savefig(os.path.join(image_svg, 'articles_over_time.svg'))
plt.savefig(os.path.join(image_png, 'articles_over_time.png'))

# log scale
all_data['path_date'] = pd.to_datetime(all_data['path_date'])
articles_over_time = all_data.groupby(all_data['path_date'].dt.to_period('W')).size().reset_index(name='count')
articles_over_time['path_date'] = articles_over_time['path_date'].dt.to_timestamp()

plt.figure(figsize=(24, 12))
sns.lineplot(x='path_date', y='count', data=articles_over_time, marker='o', linestyle='-')
plt.title('Veröffentlichungsdatum')
plt.xlabel('Datum')
plt.ylabel('Anzahl Artikel')
plt.yscale('log')  
plt.grid(True)
plt.tight_layout()

plt.savefig(os.path.join(image_svg, 'articles_over_time_log.svg'))
plt.savefig(os.path.join(image_png, 'articles_over_time_log.png'))
plt.clf()
# ---------------------------------------- WORD CLUSTER ----------------------------------------
dlf_word_cluster()
mdr_word_cluster()

print("VISUALIZATION FINISHED")