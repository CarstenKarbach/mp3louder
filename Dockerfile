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

COPY ["Readme.txt", "app.py", "boot.sh", "config.py", "requirements.txt", \
            "./"]
COPY "static" "./static"
COPY "templates" "./templates"
COPY "uploads" "./uploads"

RUN chmod +x boot.sh

ENV FLASK_APP app.py
ENV APP_NAME "supermp3"

RUN chown -R appuser:appuser ./

USER appuser

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]