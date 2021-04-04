FROM ubuntu:18.04

RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y python3 python3-pip
RUN apt-get install -y pulseaudio
RUN python3 -m pip install --no-cache --upgrade pip

RUN apt-get install -y portaudio19-dev python-pyaudio
RUN pip3 install PyAudio

#RUN pip install flask

ADD . /app/


#COPY requirements.txt /app/requirements.txt

RUN pip3 install -r /app/requirements.txt

WORKDIR ./app/

#COPY . /app
#ENTRYPOINT["python3"]

CMD ["python3", "api.py"]
