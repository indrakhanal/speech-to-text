from flask import Flask, render_template
from speech_to_text.main import SRR
from flask import jsonify
from flask import request
# import speech_recognition as sr
from flask import json
from twilio.twiml.voice_response import VoiceResponse

# r = sr.Recognizer()
# m = sr.Microphone()

app = Flask(__name__)


@app.route("/api/", methods=['GET', 'POST'])
def api_get_view():
    global sr
    if request.method == 'POST':
        output_wav = request.files["output_wav"]
        sr = SRR(output_wav)
        sender = "sender_id"
        text = sr.return_text()
        data = {
            'sender_id': sender,
            'text': text
        }
        response = app.response_class(
            response=json.dumps(data),
            status=200,
            mimetype='application/json'
        )
        return response


@app.route('/')
def voice():
    return render_template('voice.html')


@app.route('/api/audio', methods=['GET', 'POST'])
def get_score():
    if request.method == 'POST':
        length = request.content_length
        content_type = request.content_type
        data = request.data
        return f"""Content Type is  {content_type} and data is {data} \n length is {length}"""
    elif request.method == 'GET':
        return 'get method received'


if __name__ == "__main__":
    app.run(debug=True)
