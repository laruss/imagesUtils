import os

import flask
from flask import send_from_directory
from flask_cors import CORS

from web_interface.backend.routes.api import api_bp

from web_interface.backend import settings
from web_interface.backend.settings import static_folder

app = flask.Flask(__name__)
CORS(app)

app.register_blueprint(api_bp)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if not os.path.exists(static_folder):
        return flask.jsonify({'error': 'Static folder not found'}), 500
    if path != "" and os.path.exists(static_folder + '/' + path):
        return send_from_directory(static_folder, path)
    else:
        return send_from_directory(static_folder, 'index.html')


@app.route('/static/css/<path:path>')
def send_css(path):
    return send_from_directory(f'{static_folder}/static/css', path)


@app.route('/static/js/<path:path>')
def send_js(path):
    return send_from_directory(f'{static_folder}/static/js', path)


if __name__ == '__main__':
    app.run(debug=True, host=settings.server.host, port=settings.server.port)
