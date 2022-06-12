from app import app
from API import login_register
from API import user_kantong
from flask import make_response
from flask import jsonify
from app import db
from flask import request
from flask import Flask
import logging
from typing import Union

app = Flask(__name__)

def response():
    def success(values,message='success'):
        res = {
            'data': values,
            'message': message
        }
        return make_response(jsonify(res), 200)

    def badRequest(values,message='success'):
        res = {
            'data': values,
            'message': message
        }
        return make_response(jsonify(res), 400)

    def server_error(e: Union[Exception, int]) -> str:
        logging.exception('An error occurred during a request.')
        return """
            An internal error occurred: <pre>{}</pre>
            See logs for full stacktrace.
            """.format(e), 500


@app.errorhandler(500)
def serverError():
    return response.server_error()

@app.route('/')
def index():
    return 'Hello Flask!! its Work!!'

@app.route('/showUser', methods=['GET'])
def showUser():
    return login_register.showUser()

@app.route('/login', methods=['POST'])
def login():
    return login_register.login()

@app.route('/register', methods=['POST'])
def register():
    return login_register.register()

@app.route('/upload', methods=['POST'])
def upload():
    return user_kantong.upload()

@app.route('/addKantong', methods=['POST'])
def addKantong():
    return user_kantong.addKantong()

@app.route('/lihatKantong', methods=['GET'])
def lihatKantong():
    return user_kantong.lihatKantong()

if __name__== '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
