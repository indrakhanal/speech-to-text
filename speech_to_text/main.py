import speech_recognition as sr


r = sr.Recognizer()
# m = sr.Microphone()


class SRR:
    def __init__(self, wav_file):
        self.wave_file = wav_file
        self.audio = None
    def return_text(self):
        try:
            # print("A moment of silence, please...")
            # with m as source: r.adjust_for_ambient_noise(source)
            # print("Set minimum energy threshold to {}".format(r.energy_threshold))
            # # while True:
            # print("Say something!")
            # with m as source:
            #     self.audio = r.listen(source)
            # print("Got it! Now to recognize it...")
            with sr.WavFile(self.wave_file)as source:
                self.audio = r.record(source)

            try:

                # recognize speech using Google Speech Recognition
                self.value = r.recognize_google(self.audio)

                # we need some special handling here to correctly print unicode characters to standard output
                if str is bytes:  # this version of Python uses bytes for strings (Python 2)
                    print(u"You said {}".format(self.value).encode("utf-8"))
                    return self.value.encode("utf-8")
                else:  # this version of Python uses unicode for strings (Python 3+)
                    print("You said {}".format(self.value))
                    return self.value
            except sr.UnknownValueError:
                message = "Oops! Didn't catch that"
                return message
            except sr.RequestError as e:
                print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
        except KeyboardInterrupt:
            pass


