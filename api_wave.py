import os
from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client


app = Flask(__name__)

# pulls credentials from environment variables
client = Client()

BASE_URL = os.getenv("BASE_URL")
twiml_instructions_url = "{}/record".format(BASE_URL)
recording_callback_url = "{}/callback".format(BASE_URL)
twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")


@app.route("/record", methods=["GET", "POST"])
def record():
    """Returns TwiML which prompts the caller to record a message"""
    # Start our TwiML response
    response = VoiceResponse()

    # Use <Say> to give the caller some instructions
    response.say('Ahoy! Call recording starts now.')

    # Use <Record> to record the caller's message
    response.record()

    # End the call with <Hangup>
    response.hangup()

    return str(response)