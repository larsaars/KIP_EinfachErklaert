from flask import Flask, request, redirect, url_for, render_template
import whisperx
import time
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

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

        print(filepath)

        audio_file.save(filepath)

        audio = whisperx.load_audio(filepath)
        result = model.transcribe(audio, batch_size=__BATCH_SIZE__, language="de")

        model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=__DEVICE__)
        result = whisperx.align(result["segments"], model_a, metadata, audio, __DEVICE__, return_char_alignments=False)

        os.remove(filepath)

        processing_time = time.time() - start_time
        print(result)

        return redirect(url_for('results', transcription=results, processing_time=processing_time))

@app.route('/results')
def results():
    transcription, processing_time = request.args['transcription'], request.args['processing_time']
    return render_template('results.html', transcription=transcription, processing_time=processing_time)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)