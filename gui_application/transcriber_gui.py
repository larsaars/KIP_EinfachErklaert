from flask import Flask, request, redirect, url_for, render_template, session
import whisperx
import time
import os
import sys
import subprocess
from werkzeug.utils import secure_filename

sys.path.append(subprocess.check_output('git rev-parse --show-toplevel'.split()).decode('utf-8').strip())
from datahandler.DataHandler import DataHandler


app = Flask(__name__)
app.secret_key = 'secret_key'
dh_dlf = DataHandler("dlf")
dh_mdr = DataHandler("mdr")

__DEVICE__ = "cuda"
__TYPE__ = "float16"
__BATCH_SIZE__ = 16

model = whisperx.load_model("large-v2", __DEVICE__, compute_type=__TYPE__, language="de", device_index=[0, 1, 2, 3])


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

        # print(filepath)

        audio_file.save(filepath)

        audio = whisperx.load_audio(filepath)
        results = model.transcribe(audio, batch_size=__BATCH_SIZE__, language="de")
        # print(results["segments"])

        model_a, metadata = whisperx.load_align_model(language_code=results["language"], device=__DEVICE__)
        results = whisperx.align(results["segments"], model_a, metadata, audio, __DEVICE__, return_char_alignments=False)
        # print(results["segments"])
        os.remove(filepath)

        database = {}
        # clip string if . is at the end and/or whitespace at the beginning
        article_title = results["segments"][0]["text"]
        if article_title[-1] == ".":
            article_title = article_title[:-1]
        if article_title[0] == " ":
            article_title = article_title[1:]

        print(article_title)

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

        # print(results["segments"][:5])

        processing_time = round(time.time() - start_time, 3)
        session['transcription'] = results["segments"]
        session['processing_time'] = processing_time
        session['database'] = database
        print("check session")
        print(session.get('transcription')[:2])

        return redirect(url_for('results'))


@app.route('/results')
def results():
    transcription = session.get('transcription')
    processing_time = session.get('processing_time')
    database = session.get('database')
    print("check session before clear")
    print(transcription)
    # session.clear()
    print("check session after clear")
    print(transcription)
    return render_template('results.html',
                           transcription=transcription,
                           processing_time=processing_time,
                           database=database)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)