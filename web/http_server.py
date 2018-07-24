import os
from flask import Flask, send_from_directory, request, redirect, url_for, flash
from flask_cors import CORS
from flask import render_template
from flask import url_for
from werkzeug.utils import secure_filename
import re
import subprocess
import json


web_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.join(web_dir, 'dist')
app = Flask(__name__, root_path=root_dir)

CORS(app, supports_credentials=True)


UPLOAD_FOLDER = os.path.join(web_dir, 'uploads')
ALLOWED_EXTENSIONS = set(['zip', 'txt', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_result_file_path(logStr):
    '''
    Parse result file path from log message.
    '''
    m = re.search(r'RESULT_FILE:(.*)', logStr)
    if m:
        result = m.group(1)
        if os.path.isfile(result):
            return result
    return 'No Result'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def check_done(logfile):
    '''
    Check all jobs are done or not from log message.
    '''
    if os.path.isfile(logfile):
        with open(logfile) as f:
            for line in f:
                if '--ALL DONE--' in line:
                    return True
        f.close()
        return False
    else:
        return True


@app.route('/')
def index():
    return send_from_directory(os.path.join(web_dir, 'dist'), "index.html")


@app.route('/GetLog')
def GetLog():
    logfile = 'htmlcapture.log'
    if os.path.isfile(logfile):
        ret = {'log':[], 'zipfile':'' }
        with open(logfile) as f:
            for line in f:
                ret['log'].append(line)
        f.close()

        if len(ret['log']) > 2 and ('--ALL DONE--' in ret['log'][-1]):
            resultFilepath = get_result_file_path(ret['log'][-2])
            if resultFilepath == 'No Result':
                ret['zipfile'] = 'No Result'
            else:
                static_path = os.path.join(web_dir, 'dist', 'static')
                rel_path = os.path.relpath(resultFilepath, static_path)
                ret['zipfile'] = url_for('static', filename=rel_path)

        return json.dumps(ret)
    else:
        return ''

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return "No any file"
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return "No any file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            basename = os.path.splitext(filename)[0]
            save_zip = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            # output_dir = os.path.join(web_dir, '../data/result')
            # output_dir = os.path.realpath(output_dir)
            output_zip = os.path.join(web_dir, 'dist', 'static', basename + '_result.zip')
            file.save(save_zip)
            cmd = '../.env/bin/python ../runall.py {} {}'.format(save_zip, output_zip)
            print(cmd)
            subprocess.Popen([cmd], shell=True)
            return 'Job start'
    return 'NG'
