from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.util import ngrams
import re

nltk.download('stopwords')

class ArticleVectorizer(BaseEstimator, TransformerMixin):
    def __init__(self, ngram_range=(1,1), convert_segmented_words=False, stop_words=True,
                 non_alnum=True, capitalized_only=False, lowercase=True):
        self.ngram_range = ngram_range
        self.convert_segmented_words = convert_segmented_words
        self.stop_words = stop_words
        self.non_alnum = non_alnum
        self.capitalized_only = capitalized_only
        self.lowercase = lowercase
        self.stop_words_set = set(stopwords.words('german')) if stop_words else set()
        self.vectorizer = CountVectorizer(analyzer=self.analyzer)

        if lowercase and capitalized_only:
            self.capitalized_only = False

    def generate_tokens(self, text: str) -> list[str]:
        tokens = word_tokenize(text, language='german')
        
        if self.stop_words: # Allow stop words
            stop_words = set(stopwords.words('german'))
            tokens = [token for token in tokens if token.lower() not in self.stop_words_set]

        if self.non_alnum: # Allow non alpha-numerics
            tokens = filter_tokens(tokens)
        
        if self.convert_segmented_words: # Convert segmented words to regular words
            tokens = [convert_segmented_word(token) if is_segmented_word(token) else token 
                      for token in tokens]
        return tokens

    def generate_ngrams(self, tokens: list[str]) -> list[str]:
        n_grams = []
        for i in range(self.ngram_range[0], self.ngram_range[1]+1):
            grams = list(ngrams(tokens, i))
            n_grams.extend([' '.join(gram) for gram in grams])

        if self.capitalized_only:
            n_grams = get_ngrams_with_capitalized(n_grams)
        return n_grams

    def analyzer(self, text: str) -> list[str]:
        tokens  = self.generate_tokens(text)
        ngrams = self.generate_ngrams(tokens)
        return ngrams

    def fit(self, X, y=None):
        self.vectorizer.fit(X)
        return self

    def transform(self, X):
        return [self.analyzer(text) for text in X]



def get_ngrams_with_capitalized(ngrams: list[str]) -> list[str]:
    return [ngram for ngram in ngrams if any(word.istitle() for word in ngram.split())]
    
def is_segmented_word(word: str) -> bool:
    return '-' in word and word.count('-') > 0

def convert_segmented_word(segmented_word: str) -> str:
    segments = segmented_word.split('-')
    segments = [segments[0].capitalize()] + [segment.lower() for segment in segments[1:]]
    return ''.join(segments)

def filter_tokens(tokens: list[str]) -> list[str]:
    filtered_tokens = [
        token for token in tokens if token.isalnum() or 
        re.match(r'^\d{1,3}(\.\d{3})*(,\d+)?$', token)  # Matches German number format
    ]
    return filtered_tokens 