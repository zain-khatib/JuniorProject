from EndPoint import app
from flask import request , jsonify
from EndPoint.sec.DH import DiffieHellman
from EndPoint.sec.symmetric import Encryptor
import os 

Gkey=None

@app.route('/')
def hello():
    return 'hi'

@app.route('/getsharedkey')
def getsharedkey():
    input_json = request.get_json(force=True) 
    d2publicKey=int(input_json['key'])
    return init_key(d2publicKey)



def init_key(d2publicKey):
    d1=DiffieHellman()
    public_key=d1.gen_public_key()
    global Gkey
    Gkey=d1.gen_shared_key(d2publicKey)
    return jsonify({'key':public_key})


@app.route('/recive')
def recive():
    input_json = request.get_json(force=True) 
    language= input_json["Language"]
    Path = input_json["ImagePath"]
    global Gkey
    dec=Encryptor(Gkey.encode('utf-8'))
    dec.decrypt_file(Path)
    from EndPoint.Extractor import Extractor
    temp = Extractor()
    countPic,countTxt = temp.ProcessFile(Path,language)
    from EndPoint.NLPModule import NLPModule
    TEMP = NLPModule(language)
    TEMP.ForDel(countPic,countTxt)
    del TEMP
    from EndPoint.Remover import remove
    TEMP = remove()
    TEMP.RemoveFromData(countPic,countTxt,language)
    temp.delete(os.getcwd()+'/EndPoint/data')
    del TEMP
    del temp
    #os.remove(Path)
    res = dict()
    res['file'] = os.getcwd()+"/EndPoint/result.pdf"
    return jsonify(res)

@app.route('/recive/mobile',methods=['POST'])
def mobile():
    input_json = request.form 
    
    language= input_json["Language"]
    base64File = input_json["base64File"]
    flag = input_json["flag"]
    
    from EndPoint.Extractor import Extractor
    temp = Extractor()
    countPic,countTxt = temp.ProcessFileMobile(base64File,language, flag)
    from EndPoint.NLPModule import NLPModule
    TEMP = NLPModule(language)
    TEMP.ForDel(countPic,countTxt)
    del TEMP
    from EndPoint.Remover import remove
    TEMP = remove()
    TEMP.RemoveFromData(countPic,countTxt,language)
    temp.delete(os.getcwd()+'/EndPoint/data')
    del TEMP
    del temp
    
    import base64
    with open(os.getcwd()+"/EndPoint/result.pdf",'rb') as f: 
        return jsonify({'file':base64.b64encode(f.read())})