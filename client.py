
import requests
import pyaudio

from stt import record_chunk, transcribe_audio

API_URL = "http://127.0.0.1:8000"

p = pyaudio.PyAudio()

stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    input=True,
    frames_per_buffer=1024
)

try:
    print("Speak now. Say 'stop' to finish.")

    while True:
        record_chunk(p, stream, "recording.wav", chunk=3)
        text = transcribe_audio("recording.wav")

        if not text:
            continue

        print("You said:", text)

        if text.strip().lower().rstrip(".!") == "`stop" or text.strip().lower().rstrip(".!") == "stop! stop!" or text.strip().lower().rstrip(".!") == "stop." :
            response = requests.post(f"{API_URL}/execute")
            print("Result:", response.json())
            break

finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
