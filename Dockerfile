FROM ubuntu:bionic

RUN apt update
RUN apt install -y software-properties-common
RUN add-apt-repository -y ppa:flexiondotorg/audio
RUN apt-get install -y mp3gain
RUN apt install -y ffmpeg
RUN apt install -y python3-pip

RUN adduser appuser

WORKDIR /home/appuser

COPY requirements.txt requirements.txt

RUN apt install -y python3-venv

RUN python3 -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY ["Readme.txt", "app.py", "config.py", "requirements.txt", \
            "./"]
COPY "static" "./static"
COPY "templates" "./templates"
COPY "uploads" "./uploads"

ENV FLASK_APP app.py
ENV APP_NAME "supermp3"

RUN chown -R appuser:appuser ./

RUN apt-get install -y openssh-server
RUN mkdir ~/.ssh
COPY "boot.sh" "./"
RUN chmod +x boot.sh

EXPOSE 5000
EXPOSE 22
ENTRYPOINT ["./boot.sh"]