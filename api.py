from flask import Flask, render_template
from speech_to_text.main import SRR
from flask import request
from flask import json
from pydub import AudioSegment
import os


app = Flask(__name__)

import time


@app.route("/mp3_api/", methods=['GET', 'POST'])
def api_get_view():
    global sr
    if request.method == 'POST':
        t = time.time()
        output_mp3 = request.files["output_mp3"]

        wav_file = 'new.wav'
        sound = AudioSegment.from_mp3(output_mp3)
        sound = sound.normalize()
        sound.export(wav_file, format="wav")
        sr = SRR(wav_file)
        sender = "sender_id"
        text = sr.return_text()
        complete = time.time() - t

        data = {
            'sender_id': sender,
            'text': text,
            'response_time': complete
        }
        response = app.response_class(
            response=json.dumps(data),
            status=200,
            mimetype='application/json'
        )
        return response


@app.route("/wav_api/", methods=['GET', 'POST'])
def api_wav_get():
    global sr
    if request.method == 'POST':
        t = time.time()
        output_wav = request.files["output_wav"]
        sr = SRR(output_wav)
        sender = "sender_id"
        text = sr.return_text()
        complete = time.time() - t

        data = {
            'sender_id': sender,
            'text': text,
            'response_time': complete
        }
        response = app.response_class(
            response=json.dumps(data),
            status=200,
            mimetype='application/json'
        )
        return response


@app.route('/')
def voice():
    message = '<h1>API For Voice Recognition</h1>'
    return message


if __name__ == "__main__":
    app.run(debug=True)
    # port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port, debug=True)
