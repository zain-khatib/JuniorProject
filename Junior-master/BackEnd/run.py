from backend import app

if __name__ == "__main__":
    #app.run(debug=True,host='127.0.0.1',port=5000)
    app.run(debug=True,host='127.0.0.1',port=5000,ssl_context='adhoc')