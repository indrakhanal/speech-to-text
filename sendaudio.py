import pyaudio
import wave
import speech_recognition as sr
import requests

def rec_voice():
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 2
    fs = 44100  # Record at 44100 samples per second
    seconds = 3
    filename = "output.wav"

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Recording')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('Finished recording')

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

r = sr.Recognizer()

# with sr.WavFile("output.wav") as source:
#     audio = r.record(source)
#
# try:
#     print("Transcription:"+ r.recognize_google(audio))
# except LookupError:
#     print("Could not understand audio")
import time


def send_audio():
    rec_voice()
    print('attempting to send audio')

    url = 'https://stt-indra.herokuapp.com/api/'
    with open('output.wav', 'rb') as file:
        data = {'uuid': '-jx-1', 'alarmType': 1, 'timeDuration': 10}
        files = {'output_wav': file}

        req = requests.post(url, files=files, json=data)
        text = req.json()
        print(req.status_code)
        print("You said:", text["text"])
        print("Server Response time:", text['response_time'])

        return text["text"]


def recieve_reply():
    # while True:
    t = time.time()
    text = send_audio()
    print(time.time() - t)
    if text == 'exit':
        print("Thankyou. Please visit again.")
    if text == 0:
        print("Didn't catch that")
    else:
        url = 'https://volg-chatbot.herokuapp.com/webhooks/rest/webhook'
        data = {
            'sender': 11202,
            'message': text,
        }
        req = requests.post(url, json=data)
        reply = req.json()
        print(reply)
        reply_len = len(reply)
        if reply_len == 1:
            if 'buttons' in reply[0].keys():
                print('Reply:', reply[0]['text'])

                button_length = len(reply[0]['buttons'])
                for i in range(button_length):
                    print(reply[0]['buttons'][i]['title'])
            else:
                print('Reply:', reply[0]['text'])
                print(reply)

    # elif reply_len > 1:
        #     for i in range(reply_len):
        #         print(reply[i]['text'])


recieve_reply()
# send_audio()
