import sys
import os

sys.path.insert(0, "/var/www/newavkeadmin")

from app import app as application

# Enable automatic reloading
#if os.environ.get('MOD_WSGI_RELOAD_ON_CHANGES') == '1':
#    from werkzeug._reloader import run_with_reloader
#    def run_server():
#        run_with_reloader(lambda: application.run())
#    run_server()
#else:
#    application.run()
