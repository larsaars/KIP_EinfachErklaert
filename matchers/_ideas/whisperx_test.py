import whisperx
import gc
import time


from datahandler.DataHandler import DataHandler

start_time = time.time()

dh = DataHandler("dlf")
device = "cuda"
audio_file = "audio.mp3"
batch_size = 16
compute_type = "float16"


# 1. Transcribe with original whisper (batched)
model = whisperx.load_model("large-v2", device, compute_type=compute_type, language="de", device_index=[0, 1, 2, 3])


# save model to local path (optional)

# model_dir = "/path/"
# model = whisperx.load_model("large-v2", device, compute_type=compute_type, download_root=model_dir)

audio = whisperx.load_audio(audio_file)
result = model.transcribe(audio, batch_size=batch_size, language="de")
print(result["segments"]) # before alignment

# 2. Align whisper output
model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)

print(result["segments"]) # after alignment
print(f"Evaluation time: {time.time() - start_time}")