from flask import Flask
import os

app=Flask(__name__)
app.config['SECRET_KEY']='Random String'
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path,'uploads')
from backend import routes