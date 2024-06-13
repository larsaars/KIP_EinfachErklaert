from flask import Flask, request, jsonify
import whisperx
import time
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

model = whisperx.load_model("large-v2", "cuda", compute_type="float16", language="de", device_index=[0, 1, 2, 3])

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
    if 'audio' not in request.files:
        return 'No audio file part'
    audio_file = request.files['audio']
    if audio_file.filename == '':
        return 'No selected file'
    if audio_file:
        filename = secure_filename(audio_file.filename)
        filepath = os.path.join('/tmp', filename)
        audio_file.save(filepath)

        audio = whisperx.load_audio(audio_file)
        result = model.transcribe(audio, batch_size=16, language="de")

        os.remove(filepath)
        return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)