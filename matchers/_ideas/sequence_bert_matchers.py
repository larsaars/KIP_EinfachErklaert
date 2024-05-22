import pandas as pd
from sentence_transformers import SentenceTransformer, util

# Load your datasets
easy_articles = pd.read_csv('easy_articles.csv')
normal_articles = pd.read_csv('normal_articles.csv')

# Initialize Sentence-BERT model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Encode the articles
easy_embeddings = model.encode(easy_articles['text'].tolist(), convert_to_tensor=True)
normal_embeddings = model.encode(normal_articles['text'].tolist(), convert_to_tensor=True)

# Compute cosine similarities
cosine_scores = util.pytorch_cos_sim(easy_embeddings, normal_embeddings)

# Find the best matches
matches = cosine_scores.argmax(dim=1).tolist()

# Create a DataFrame to display matches
matches_df = pd.DataFrame({
    'Easy Article': easy_articles['text'],
    'Normal Article': normal_articles.iloc[matches]['text']
})

# Display the matches
print(matches_df.head())

# Optionally save the matches to a CSV file
matches_df.to_csv('matched_articles.csv', index=False)
