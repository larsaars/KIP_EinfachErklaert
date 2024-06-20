from flask import Flask, request, redirect, url_for, render_template, session
from flask_session import Session
import matplotlib.pyplot as plt
import numpy as np
import whisperx
import time
import os
import sys
import subprocess
import pickle
import warnings
from werkzeug.utils import secure_filename
from audio_classification import extract_audio_features


sys.path.append(subprocess.check_output('git rev-parse --show-toplevel'.split()).decode('utf-8').strip())
from datahandler.DataHandler import DataHandler

warnings.filterwarnings("ignore")

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'secret_key'
Session(app)
dh_dlf = DataHandler("dlf")
dh_mdr = DataHandler("mdr")

__DEVICE__ = "cuda"
__TYPE__ = "float16"
__BATCH_SIZE__ = 16

model = whisperx.load_model("large-v2", __DEVICE__, compute_type=__TYPE__, language="de", device_index=[0, 1, 2, 3])

def plot_model:
    pass


@app.route('/')
def landing_page():
    return 'Welcome to the WhisperX Transcriber!'


@app.route('/upload')
def upload():
    return '''
    <!doctype html>
    <title>Upload an audio file</title>
    <h1>Upload an audio file</h1>
    <form method="POST" action="/transcribe" enctype="multipart/form-data">
      <input type="file" name="audio">
      <input type="submit" value="Transcribe">
    </form>
    '''


@app.route('/transcribe', methods=['POST'])
def transcribe():
    start_time = time.time()
    if 'audio' not in request.files:
        return 'No audio file part'
    audio_file = request.files['audio']
    if audio_file.filename == '':
        return 'No selected file'
    if audio_file:
        # save file temporarily in script directory
        filename = secure_filename(audio_file.filename)
        filepath = os.path.join(os.getcwd(), filename)
        audio_file.save(filepath)

        audio = whisperx.load_audio(filepath)
        results = model.transcribe(audio, batch_size=__BATCH_SIZE__, language="de")

        model_a, metadata = whisperx.load_align_model(language_code=results["language"], device=__DEVICE__)
        results = whisperx.align(results["segments"], model_a, metadata, audio, __DEVICE__, return_char_alignments=False)

        test_audio = extract_audio_features(filepath)
        os.remove(filepath)
        with open('model_all.pkl', 'rb') as f:
            classification_model = pickle.load(f)

        # handling a single sample needs to be reshaped to 2D array
        test_audio = test_audio.to_numpy().reshape(1, -1)

        print(classification_model.predict(test_audio))
        print(classification_model.predict_proba(test_audio)[0])

        classification = {"prediction": classification_model.predict(test_audio)[0]}
        classification["probability"] = classification_model.predict_proba(test_audio)[0][classification["prediction"]]

        database = {}
        # clip string if . is at the end and/or whitespace at the beginning
        # problems occur when transcriber does not recognize end of title

        article_title = results["segments"][0]["text"]
        if article_title[-1] == ".":
            article_title = article_title[:-1]
        if article_title[0] == " ":
            article_title = article_title[1:]

        if dh_dlf.search_by("e", "title", article_title):
            database["source"] = "dlf"
            database["level"] = "easy"
        elif dh_dlf.search_by("h", "title", article_title):
            database["source"] = "dlf"
            database["level"] = "hard"
        elif dh_mdr.search_by("e", "title", article_title):
            database["source"] = "mdr"
            database["level"] = "easy"
        elif dh_mdr.search_by("h", "title", article_title):
            database["source"] = "mdr"
            database["level"] = "hard"
        else:
            database["source"] = "unknown"
            database["level"] = "unknown"

        processing_time = round(time.time() - start_time, 3)
        session['transcription'] = results["segments"]
        session['processing_time'] = processing_time
        session['database'] = database
        session['classification'] = classification

        return redirect(url_for('results'))


@app.route('/results')
def results():
    transcription = session.get('transcription')
    processing_time = session.get('processing_time')
    database = session.get('database')
    classification = session.get('classification')
    return render_template('results.html',
                           transcription=transcription,
                           processing_time=processing_time,
                           database=database,
                           classification=classification)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)