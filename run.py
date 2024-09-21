from app import app

app.secret_key = 'f735e47866cceca5cc3113cab5d2b58b'

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)

