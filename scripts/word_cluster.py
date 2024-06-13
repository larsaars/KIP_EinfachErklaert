import os
import subprocess
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

# Get the git root directory
git_root = (
    subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True)
    .strip()
)

base_dir = os.path.join(git_root, "data")

data = []

# Walk through the directory structure
for source in os.listdir(base_dir):
    source_dir = os.path.join(base_dir, source)
    if os.path.isdir(source_dir):
        for niveau in os.listdir(source_dir):
            niveau_dir = os.path.join(source_dir, niveau)
            if os.path.isdir(niveau_dir):
                for article_dir in os.listdir(niveau_dir):
                    article_path = os.path.join(niveau_dir, article_dir)
                    if os.path.isdir(article_path):
                        content_file = os.path.join(article_path, "Content.txt")
                        
                        with open(content_file, 'r') as file:
                            content = file.read()
                        
                        # Use BeautifulSoup to remove HTML tags
                        soup = BeautifulSoup(content, "html.parser")
                        text_content = soup.get_text()

                        article_length = len(text_content.split())

                        data.append({
                            "source": source,
                            "niveau": niveau,
                            "article": article_dir,
                            "content": text_content,
                            "length": article_length
                        })

# Convert to DataFrame
df = pd.DataFrame(data)

# Filter articles from "dlf"
dlf_df = df[df['source'] == 'mdr']

# Separate easy and hard articles
easy_articles = dlf_df[dlf_df['niveau'] == 'easy']['content'].str.cat(sep=' ')
hard_articles = dlf_df[dlf_df['niveau'] == 'hard']['content'].str.cat(sep=' ')

# Generate word clouds
def generate_wordcloud(text, title, lvl):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.savefig(os.path.join(git_root, "documentation", "images", f'wordcloud{lvl}.png'))
    plt.title(title, fontsize=20)
    plt.axis('off')
    plt.show()

# Word cloud for easy articles
generate_wordcloud(easy_articles, 'Wörter nach Häufigkeit bei MDR (leicht)', "easy")

# Word cloud for hard articles
generate_wordcloud(hard_articles, 'Wörter nach Häufigkeit bei MDR (normal)', "hard")

