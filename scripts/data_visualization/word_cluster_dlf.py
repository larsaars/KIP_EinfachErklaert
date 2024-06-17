

import os
import subprocess
import sys
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import nltk
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
dh = DataHandler("dlf")
easy = dh.get_all("easy")
hard = dh.get_all("hard")
easy_articles = " ".join(easy["text"].tolist())
hard_articles = " ".join(hard["text"].tolist())

# Generate word clouds
def generate_wordcloud(text, title, lvl):
    # German stopwords
    german_stopwords = set(stopwords.words('german'))
    wordcloud = WordCloud(width=1600, height=800, background_color="white", stopwords=german_stopwords, max_words=100, collocations=False).generate(
        text
    )
    plt.figure(figsize=(20, 10))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.title(title, fontsize=20)
    plt.axis("off")
    file_path = os.path.join(git_root, "documentation", "images", "wordcluster", f"wordcluster_dlf_{lvl}.jpg")
    plt.savefig(file_path, dpi=300, bbox_inches='tight')
    # plt.show()

# Word cloud for easy articles
generate_wordcloud(easy_articles, "Wörter nach Häufigkeit bei Nachrichtenleicht", "easy")

# Word cloud for hard articles
generate_wordcloud(hard_articles, "Wörter nach Häufigkeit bei Deutschlandfunk", "hard")

