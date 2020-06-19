import base64
import io
import os
import random
import string

from flask import Flask, render_template, url_for, request, current_app, send_file, g
from werkzeug.utils import redirect, secure_filename
import os
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/docs', methods=["GET"])
def docs():
    return redirect('/static/swagger-ui/dist/index.html')

@app.route('/', methods=["GET"])
def index():
    return redirect(url_for('makeLouder'))

def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

@app.route("/info", methods=["GET"])
def mp3gaininfo():
    stream = os.popen('mp3gain 2>&1')
    output = stream.read()
    return output

def mp3gainFile(db, file):
    stream = os.popen('mp3gain -c -d ' + str(db) + ' -r ' + file + ' 2>&1 ; echo "|7"')
    output = stream.read()
    pos = output.rfind("|")
    if pos >= 0:
        rc = int(output[pos + 1:])
    else:
        rc = -1
    indicateSuccess = ('No changes to', 'Applying mp3 gain change of')
    success = len(list(filter(lambda to_search: (to_search in output), indicateSuccess )))
    if success >=1:
        rc = 0
    res = "Thanks for your file upload, stored at " + file
    res += "\ndb=" + str(db)
    res += "\nMP3Gain Run:\n" + output + "\nRC=" + str(rc)+"\nsuccesses="+str(success)

    return (rc, res)

def convertToMP3(file):
    mp3file = file+'.mp3'
    stream = os.popen('ffmpeg -i ' + file + ' -c:a libmp3lame -ac 2 -b:a 190k '+mp3file+' 2>&1 && echo "|"$?')
    output = stream.read()
    pos = output.rfind("|")
    if pos >= 0:
        rc = int(output[pos + 1:])
    else:
        rc = -1
    if rc == 0:
        os.rename(mp3file, file)
    return (rc, output)

@app.route('/makelouder', methods=["GET", "POST"])
def makeLouder():
    if request.method == 'POST':
        db = request.form.get('db', 5, type=int)
        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            filename = randomString(24)
            fullfile = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            while os.path.exists(fullfile):
                fullfile = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(fullfile)

            (rc, res) = mp3gainFile(db, fullfile)
            print(res)

            if "MPEG Layer " in res:
                print("Need to convert to mp3")
                (crc, cres) = convertToMP3(fullfile)
                print("Converted: "+str(crc)+" "+cres)
                (rc, res) = mp3gainFile(db, fullfile)
                print(res)

            if rc == 0:
                return_data = io.BytesIO()
                with open(fullfile, 'rb') as fo:
                    return_data.write(fo.read())
                return_data.seek(0)
                os.remove(fullfile)
                return send_file(return_data, attachment_filename='download.mp3', as_attachment=True)
            else:
                return res, 400
        else:
            return "No file found", 400
    return render_template("upload.html", appname=current_app.config['APP_NAME'])