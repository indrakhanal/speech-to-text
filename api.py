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


# def return_text():
#     try:
#         # print("A moment of silence, please...")
#         with m as source: r.adjust_for_ambient_noise(source)
#         print("Set minimum energy threshold to {}".format(r.energy_threshold))
#         print("Say something!")
#         with m as source:
#             audio = r.listen(source)
#         print("Got it! Now to recognize it...")
#         try:
#             value = r.recognize_google(audio)
#             if str is bytes:
#                 print(u"You said {}".format(value).encode("utf-8"))
#                 return value.encode("utf-8")
#             else:
#                 print("You said {}".format(value))
#                 return value, audio
#         except sr.UnknownValueError:
#             message = "Oops! Didn't catch that"
#             return message
#         except sr.RequestError as e:
#             print(f" Error Occur{0}".format(e))
#     except KeyboardInterrupt:
#         pass


@app.route("/api/")
def api_get_view():
    global sr
    sr = SRR()
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


@app.route("/record", methods=["POST"])
def record():
    item_return = sr.return_text()
    print(item_return)
    audio = item_return[1]
    response = VoiceResponse()

    # Make sure this is the first call to our URL and record and transcribe
    if 'RecordingUrl' not in request.form:
        # Use <Say> verb to provide an outgoing message
        response.say("Hello, please leave your message after the tone.")

        # Use <Record> verb to record incoming message and set the transcribe arguement to true
        response.record(transcribe=True)
        print(str(response))
    else:
        # Hang up the call
        print("Hanging up...")
        response.hangup()
    res=str(response)
    print(res, 'response')
    return res


if __name__ == "__main__":
    app.run(debug=True)
