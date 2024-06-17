import os
import subprocess
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import sys
from bs4 import BeautifulSoup

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
image_dir = os.path.join(git_root, "documentation", "final_report", "images")

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
all_data.drop(columns=['audio_audio_url', 'audio_download_url', 'audio_duration', 'text'], inplace=True)

# ---------------------------------------- VISUALIZATION ---------------------------------------- 

# ---------------------------------------- CAKES ---------------------------------------- 

total_articles = all_data['article'].nunique()
fig, axs = plt.subplots(1, 3, figsize=(18, 8))

# Number of articles by difficulty
articles_by_niveau = all_data['niveau'].value_counts()
axs[0].pie(articles_by_niveau, labels=articles_by_niveau.index, autopct='%1.1f%%', colors=['#ff9999','#66b3ff','#99ff99'])
axs[0].set_title('Nach Schwierigkeit')

# Number of articles by source
articles_by_source = all_data['source'].value_counts()
axs[1].pie(articles_by_source, labels=articles_by_source.index, autopct='%1.1f%%', colors=['#ffcc99','#c2c2f0','#ffb3e6'])
axs[1].set_title('Artikel nach Quelle')

# Number of articles with audio
articles_with_audio = all_data['has_audio'].value_counts()
articles_with_audio.index = ['ohne', 'mit']
axs[2].pie(articles_with_audio, labels=articles_with_audio.index, autopct='%1.1f%%', colors=['#c2f0c2','#ff6666'])
axs[2].set_title('Artikel mit Audio')

plt.tight_layout()
plt.savefig(os.path.join(image_dir, 'cakes.png'))
plt.clf() 

# ---------------------------------------- LENGTH BOXPLOT ---------------------------------------- 
# Length difference between easy and hard articles using seaborn box plot
all_data['length'] = all_data['article'].apply(lambda x : len(x.split()))

# Adjusting font sizes
plt.rcParams.update({'font.size': 18})  # Set the global font size

plt.figure(figsize=(16, 12))  
sns.boxplot(x='niveau', y='length', data=all_data, palette='pastel')
plt.title('Wörter pro Artikel')
plt.xlabel('Sprachniveau')
plt.ylabel('Wörter')
plt.tight_layout()  # Adjust the layout
plt.savefig(os.path.join(image_dir, 'box_plot_length.png'))
plt.clf()

# ---------------------------------------- ERSCHEINUNGSDATUM ---------------------------------------- 
all_data['date'] = pd.to_datetime(all_data['date'])
articles_over_time = all_data.groupby(all_data['date'].dt.to_period('M')).size()

# Adjusting font sizes
plt.rcParams.update({'font.size': 18})  # Set the global font size

plt.figure(figsize=(24, 12))
articles_over_time.plot(kind='line', marker='o', linestyle='-')
plt.title('Veröffentlichungsdatum')
plt.xlabel('Datum')
plt.ylabel('Anzahl Artikel')
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(image_dir, 'articles_over_time.png'))
