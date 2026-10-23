import wave
import pyaudio

from faster_whisper import WhisperModel


def record_chunk(p ,stream ,file_path , chunk=1):
    frames =[]
    for _ in range(0 ,int(16000/ 1024 * chunk)):
        data = stream.read(1024)
        frames.append(data)

    wf = wave.open(file_path , 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(16000)
    wf.writeframes(b''.join(frames))
    wf.close()



model = WhisperModel("base", device="cpu", compute_type="int8")

def transcribe_audio(file_path):
    segments, _ = model.transcribe(file_path, beam_size=5)
    text = " ".join(segment.text.strip() for segment in segments)
    return text.strip()

# p  = pyaudio.PyAudio()
# stream = p.open(format=pyaudio.paInt16,
#                 channels=1,
#                 rate=16000,
#                 input=True,
#                 frames_per_buffer=1024)

# try:
#     print("speak now ... ")
#     while True:
#         record_chunk(p, stream, "recording.wav", chunk=3)
#         transcribe_audio("recording.wav")
#     print("Recording saved successfully!")
# finally:
#     stream.stop_stream()
#     stream.close()
#     p.terminate()

