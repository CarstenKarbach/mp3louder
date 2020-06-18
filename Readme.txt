vagrant up
vagrant ssh
~/.local/bin/flask run --host=0.0.0.0 --port=5000
http://192.168.33.12:5000/

docker pull registry.hub.docker.com/carstenkarbach/mp3louder:latest
docker build -t mp3louder:latest .
docker run --rm -d -p 5000:5000 mp3louder
