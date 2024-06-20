import sys
import subprocess
import librosa
import pickle
import numpy as np
import pandas as pd
import soundfile as sf
from tqdm import tqdm
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report
sys.path.append(subprocess.check_output('git rev-parse --show-toplevel'.split()).decode('utf-8').strip())
from datahandler.DataHandler import DataHandler

tqdm.pandas()


def load_text_data():
    dh = DataHandler("mdr")
    df_easy = dh.get_all("e")
    df_hard = dh.get_all("h")
    print("Loaded text data")
    return df_easy, df_hard

def load_audio_data():
    dh_mdr = DataHandler("mdr")
    df_mdreasy = dh_mdr.get_audio_paths("e")
    df_mdrhard = dh_mdr.get_audio_paths("h")
    dh_dlf = DataHandler("dlf")
    df_dlfeasy = dh_dlf.get_audio_paths("e")
    df_dlfhard = dh_dlf.get_audio_paths("h")
    # join dataframes which are not none with check
    df = pd.concat([df_mdreasy, df_mdrhard, df_dlfeasy, df_dlfhard], ignore_index=True)

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
    try:
        y, sr = librosa.load(audio_path)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        features = {
            'spectral_centroid': np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)),
            'zero_crossing_rate': np.mean(librosa.feature.zero_crossing_rate(y)),
        }
        for i, mfcc in enumerate(np.mean(mfccs.T, axis=0)):
            features[f'mfcc_{i}'] = mfcc
        return pd.Series(features)
    except Exception as e:
        print(f"Error loading {audio_path}: {e}")
        return pd.Series()


def evaluate_audio(df):
    df = df.join(df['audio_path'].progress_apply(extract_audio_features))
    df.dropna(inplace=True)
    print("Extracted audio features")
    return df

def train(df):
    print("Start training")
    # training and testsplit
    X_train, X_test, y_train, y_test = train_test_split(df.drop(['label', 'audio_path'], axis=1), df['label'], test_size=0.2, random_state=42)

    svg_pipe = Pipeline([
        ('scaler', MinMaxScaler()),
        ('svc', SVC(probability=True))
    ])

    param_grid = {'svc__C': [0.1, 1, 10, 100, 1000],
                  'svc__gamma': [1, 0.1, 0.01, 0.001, 0.0001],
                  'svc__kernel': ['rbf', 'linear', 'poly', 'sigmoid']}

    grid = GridSearchCV(svg_pipe, param_grid, cv=5, n_jobs=-1)
    grid.fit(X_train, y_train)

    """
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
    """
    """
    # setting up a pipeline for decision tree
    dt_pipe = Pipeline([
        ('scaler', MinMaxScaler()),
        ('dt', DecisionTreeClassifier())
    ])
    # setting up a parameter grid
    param_grid = {
        'dt__max_depth': [3, 5, 7, 9, 11],
        'dt__min_samples_split': [2, 3, 4, 5, 6],
        'dt__min_samples_leaf': [1, 2, 3, 4, 5]
    }
    """

    # evaluation
    y_pred = grid.predict(X_test)
    y_train_pred = grid.predict(X_train)
    print("Train:")
    print(pd.DataFrame(classification_report(y_train, y_train_pred, output_dict=True)))
    print("Test:")
    print(pd.DataFrame(classification_report(y_test, y_pred, output_dict=True)))
    return df, grid

if __name__ == '__main__':
    load_existing = input("Do you want to load data from 'audio_features.pkl'? (y/n): ")
    if load_existing.lower() == 'y':
        with open('/data/projects/einfach/KIP_EinfachErklaert/gui_application/audio_features.pkl', 'rb') as f:
            df = pickle.load(f)
    else:
        df = load_audio_data()
        df = evaluate_audio(df)
        with open('/data/projects/einfach/KIP_EinfachErklaert/gui_application/audio_features.pkl', 'wb') as f:
            pickle.dump(df, f)

    print(f"Number of samples: {len(df)}")
    print(f"Number of features: {len(df.columns) - 2}")
    print(f"Number of samples per class: {df['label'].value_counts()}")
    print(df.head())

    df, grid = train(df)
    with open('/data/projects/einfach/KIP_EinfachErklaert/gui_application/model_all.pkl', 'wb') as f:
        pickle.dump(grid, f)
    print(grid.best_params_)

