import os
import requests
from backend import app
from flask import render_template,request,url_for,flash,redirect,send_file
from backend.forms import ImageForm
from werkzeug.utils import secure_filename
from backend.sec.dh import DiffieHellman
from backend.sec.symmetric import Encryptor
from hashlib import sha256
import io
import webbrowser


@app.route('/')
def Home():
    return render_template('index.html')


@app.route('/home')
def home2():
    return render_template('index.html')


@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/upload',methods=['GET','POST'])
def upload():
    form=ImageForm()
    if request.method=='GET':
        return render_template('upload.html',title='Upload File',form=form)
    else:   
        if form.validate_on_submit():
            file=form.image.data
            filename = secure_filename(file.filename)
            path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            encrypt(path)
            sendImage(path+'.enc',form.language.data)
            return redirect(url_for('Home'))
        else:
            return render_template('upload.html',title='Upload File',form=form)    

def encrypt(file_name):
    key=init_key()
    enc=Encryptor(key.encode('utf-8'))
    enc.encrypt_file(file_name)


def init_key():
    d1=DiffieHellman()
    public_key=d1.gen_public_key()
    share = get_sharedkey(public_key)
    shared_key=d1.gen_shared_key(share['key'])
    return shared_key


def get_sharedkey(public_key):
    URL='http://192.168.43.200:5001/getsharedkey'
    PARAMS = {'key':public_key} 
    req = requests.get(url = URL, json = PARAMS) 
    data=req.json()
    return data

    

def sendImage(path,language):
    URL='http://192.168.43.200:5001/recive'
    PARAMS={ 'ImagePath':path , 'Language':language }
    req = requests.get(url = URL, json = PARAMS)
    webbrowser.open_new_tab(req.json()['file'])
    os.remove(path)
    #os.remove(req.json()['file'])