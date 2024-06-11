import librosa
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from datahandler.DataHandler import DataHandler


def load_text_data():
    dh = DataHandler("mdr")
    df_easy = dh.get_all("e")
    df_hard = dh.get_all("h")
    print(df_easy.columns, "\n", df_hard.columns)
    return df_easy, df_hard

def load_audio_data():
    dh = DataHandler("dlf")
    df_easy = dh.get_audio_paths("e")
    df_hard = dh.get_audio_paths("h")
    # join dataframes
    df = pd.concat([df_easy, df_hard], ignore_index=True)
    print(df.columns)
    return df


# Merkmalsextraktion
def extract_text_features(texts):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)
    return X


def extract_audio_features(audio_path):
    y, sr = librosa.load(audio_path)
    features = {
        'mfcc': np.mean(librosa.feature.mfcc(y=y, sr=sr), axis=1),
        'spectral_centroid': np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)),
        'zero_crossing_rate': np.mean(librosa.feature.zero_crossing_rate(y)),
        # andere Merkmale?
    }
    return np.concatenate(list(features.values()))


def evaluate_audio(df):
    num_easy = len(df[df['label'] == 0])
    num_hard = len(df[df['label'] == 1])

    df['audio_features'] = df['audio_path'].apply(extract_audio_features)

    # training and testsplit
    X_train, X_test, y_train, y_test = train_test_split(
        np.stack(df['audio_features'].values),
        df['label'].values,
        test_size=0.2,
        random_state=42
    )

    # Modelltraining
    model = SVC(kernel='linear')
    model.fit(X_train, y_train)

    # Modellbewertung
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))


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
    print(df)
    evaluate_audio(df)
