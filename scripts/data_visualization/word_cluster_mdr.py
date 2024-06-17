import os
import subprocess
import sys
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import nltk
from bs4 import BeautifulSoup

nltk.download('stopwords')
from nltk.corpus import stopwords

sys.path.append(
    subprocess.check_output("git rev-parse --show-toplevel".split())
    .decode("utf-8")
    .strip()
)

from datahandler.DataHandler import DataHandler

# Get the git root directory
git_root = subprocess.check_output(
    ["git", "rev-parse", "--show-toplevel"], text=True
).strip()
base_dir = os.path.join(git_root, "data")

# Load the data
dh = DataHandler("mdr")
easy = dh.get_all("easy")
hard = dh.get_all("hard")
easy_articles = BeautifulSoup(" ".join(easy["text"].tolist()), 'lxml').get_text()
hard_articles = BeautifulSoup(" ".join(hard["text"].tolist()), 'lxml').get_text()

# Generate word clouds
def generate_wordcloud(text, title, lvl):
    # German stopwords
    german_stopwords = set(stopwords.words('german'))
    wordcloud = WordCloud(width=1600, height=800, background_color="white", stopwords=german_stopwords, max_words=20, collocations=False).generate(
        text
    )
    plt.figure(figsize=(20, 10))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.title(title, fontsize=20)
    plt.axis("off")
    file_path = os.path.join(git_root, "documentation", "images", "wordcluster", f"wordcluster_mdr_{lvl}.jpg")
    plt.savefig(file_path, dpi=300, bbox_inches='tight')
    # plt.show()

# Word cloud for easy articles
generate_wordcloud(easy_articles, "Wörter nach Häufigkeit bei Nachrichtenleicht", "easy")

# Word cloud for hard articles
generate_wordcloud(hard_articles, "Wörter nach Häufigkeit bei Deutschlandfunk", "hard")
