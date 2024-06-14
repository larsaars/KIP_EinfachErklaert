import librosa
import numpy as np
import pandas as pd
import soundfile as sf
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from datahandler.DataHandler import DataHandler


def load_text_data():
    dh = DataHandler("mdr")
    df_easy = dh.get_all("e")
    df_hard = dh.get_all("h")
    print("Loaded text data")
    return df_easy, df_hard

def load_audio_data():
    dh = DataHandler("mdr")
    df_easy = dh.get_audio_paths("e")
    df_hard = dh.get_audio_paths("h")
    # join dataframes
    df = pd.concat([df_easy, df_hard], ignore_index=True)
    print("Loaded audio data")
    return df


# merkmalsextraktionen
def extract_text_features(texts):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)
    return X

def load_and_split_audio(audio_path):
    y, sr = librosa.load(audio_path)
    segment_length = 5 * sr
    num_segments = len(y) // segment_length
    split = []
    for i in range(num_segments):
        split.append(y[i * segment_length:(i + 1) * segment_length])
    for i in range(num_segments):
        sf.write(audio_path[:-4] + f"_split_{i}.wav", split[i], sr)


def extract_audio_features(audio_path):
    y, sr = librosa.load(audio_path)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    features = {
        'spectral_centroid': np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)),
        'zero_crossing_rate': np.mean(librosa.feature.zero_crossing_rate(y)),
        # andere Merkmale?
    }
    for i, mfcc in enumerate(np.mean(mfccs.T, axis=0)):
        features[f'mfcc_{i}'] = mfcc
    return pd.Series(features)

def evaluate_audio(df):
    # num_easy = len(df[df['label'] == 0])
    # num_hard = len(df[df['label'] == 1])

    df = df.join(df['audio_path'].apply(extract_audio_features))
    print("Extracted audio features")
    return df

def train(df):
    print("Start training")
    # training and testsplit
    X_train, X_test, y_train, y_test = train_test_split(df.drop(['label', 'audio_path'], axis=1), df['label'], test_size=0.2, random_state=42)

    # setting up a pipeline
    knn_pipe = Pipeline([
        ('scaler', MinMaxScaler()),
        ('knn', KNeighborsClassifier())
    ])
    # setting up a parameter grid
    param_grid = {
        'knn__n_neighbors': [2, 3, 5, 7, 9, 11],
        'knn__weights': ['uniform', 'distance'],
        'knn__metric': ['euclidean', 'manhattan']
    }
    grid = GridSearchCV(knn_pipe, param_grid, cv=5, n_jobs=-1)
    grid.fit(X_train, y_train)

    # modeltraining
    # model = SVC(kernel='linear')
    # model.fit(X_train, y_train)

    # evaluation
    y_pred = grid.predict(X_test)
    print(pd.DataFrame(classification_report(y_test, y_pred, output_dict=True)))
    return df, grid

    def plot_results():
        pass


if __name__ == '__main__':
    '''
    df_easy, df_hard = load_data()

    df_easy = df_easy[["text"]]
    df_hard = df_hard[["text"]]

    # df_easy['text'] = df_easy['text'].str.replac

    df_easy["label"] = 0
    df_hard["label"] = 1

    print(df_easy.head())
    '''
    df = load_audio_data()
    df = evaluate_audio(df)

    print(df['label'])
    df, grid = train(df)
    print(grid.best_params_)
