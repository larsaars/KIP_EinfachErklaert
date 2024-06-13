from flask import Flask, request, jsonify
import whisperx
import time

app = Flask(__name__)

model = whisperx.load_model("large-v2", "cuda", compute_type="float16", language="de", device_index=[0, 1, 2, 3])

@app.route('/')
def landing_page():
    return 'Welcome to the WhisperX Transcriber!'

@app.route('/transcribe', methods=['POST'])
def transcribe():
    start_time = time.time()
    audio = whisperx.load_audio(request.files['audio'])

    result = model.transcribe(audio, batch_size=16, language="de")

    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)