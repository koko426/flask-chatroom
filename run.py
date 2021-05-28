# encoding:utf-8
from flask import Flask
import config
from exct import db, socketio, csrf
from apps.chat_app.views import bp as app_chat
from apps.sock_app import views
import  logging

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(app_chat)
    socketio.init_app(app)
    csrf.init_app(app)
    db.init_app(app)
    log=logging.getLogger('werkzeug')
    log.disabled=True
    return app


app = create_app()

if __name__ == '__main__':
    app.run(port=8085)
