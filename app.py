from flask import Flask, render_template
from flask.views import View
from speech_to_text.main import SRR
import requests

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('index.html')


class Api(View):
    def dispatch_request(self):
        item_return = self.answer_from_bot()
        # item_return = list[item]
        len(item_return)
        print(item_return, 'item returned from bot')
        if item_return != None:
            if item_return != 404:
                print('returned items   ', item_return)
                bot_replay = item_return
                speech_to_text = self.speech_to_text
                print(speech_to_text, 'sttt')
                return render_template('index.html', context1=speech_to_text, context2=bot_replay)
            else:
                message = 'could not connect to the api'
                return render_template('index.html', message=message)
        else:
            message = 'Sound not recorded'
            return render_template('index.html', message=message)

    def get_request(self):
        try:
            sr = SRR()
            self.speech_to_text = sr.return_text()
            print(self.speech_to_text)
            url = 'http://localhost:5005/webhooks/rest/webhook/'
            data = {
                'sender': 'Indra',
                'message': self.speech_to_text,
            }
            replay = requests.post(url, json=data)
            rep = replay.json()

            reply_len = len(rep)
            if reply_len==1:
                if 'buttons' in rep[0].keys():
                    ans_list = []
                    ans1 = ('Reply:', rep[0]['text'])
                    print(ans1)
                    button_length = len(rep[0]['buttons'])
                    for i in range(button_length):
                        button = (rep[0]['buttons'][i]['title'])
                        ans_list.append(button)
                    print('answer list', ans_list)
                    for item in ans_list:
                        return ans1, item
                    # return ans_list
                else:
                    ans = (rep[0]['text'])
                    return ans
            elif reply_len>1:
                for i in range(reply_len):
                    text = (rep[i]['text'])
                    return text
        except:
            message = 404
            return message

    def answer_from_bot(self):
        item_return =self.get_request()
        return item_return


app.add_url_rule('/speak/', view_func=Api.as_view('speak'))

if __name__ == "__main__":
    app.run(debug=True)
