from app import app
from werkzeug.debug import DebuggedApplication

app.debug = True
app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)
app.secret_key = 'f735e47866cceca5cc3113cab5d2b58b'

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
