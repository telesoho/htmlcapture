import os
from flask import Flask
from flask import render_template
import subprocess

import json

app = Flask(__name__)

def CheckDone(logfile):
    if os.path.isfile(logfile):
        with open(logfile) as f:
            for line in f:
                if '--ALL DONE--' in line:
                    return True
        f.close()
        return False
    else:
        return True


@app.route('/caphtml')
def caphtml():
    if CheckDone('htmlcapture.log'):
        cmd = 'python ../runall.py'
        subprocess.Popen([cmd], shell=True)
        return 'Job start'
    else:
        return 'prev Job are still running, please wait a moment.'

@app.route('/GetLog')
def GetLog():
    logfile = 'htmlcapture.log'
    if os.path.isfile(logfile):
        ret = []
        with open(logfile) as f:
            for line in f:
                ret.append(line)
        f.close()
        return json.dumps(ret)
    else:
        return ''
