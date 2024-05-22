import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import cosine_similarity

# Load your datasets
easy_articles = pd.read_csv('easy_articles.csv')
normal_articles = pd.read_csv('normal_articles.csv')

# Combine the datasets for joint processing
all_articles = pd.concat([easy_articles['text'], normal_articles['text']])

# Vectorize the text using TF-IDF
tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
tfidf_matrix = tfidf_vectorizer.fit_transform(all_articles)

# Apply NMF for topic modeling
nmf = NMF(n_components=10, random_state=1)
nmf_features = nmf.fit_transform(tfidf_matrix)
nmf_features = normalize(nmf_features)

# Separate the transformed features back into easy and normal sets
easy_features = nmf_features[:len(easy_articles)]
normal_features = nmf_features[len(easy_articles):]

# Compute cosine similarity between easy and normal articles
similarity_matrix = cosine_similarity(easy_features, normal_features)

# Find the best matches
matches = similarity_matrix.argmax(axis=1)

# Create a DataFrame to display matches
matches_df = pd.DataFrame({
    'Easy Article': easy_articles['text'],
    'Normal Article': normal_articles.iloc[matches]['text']
})

# Display the matches
print(matches_df.head())

# Optionally save the matches to a CSV file
matches_df.to_csv('matched_articles.csv', index=False)
