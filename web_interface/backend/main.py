import flask

from web_interface.backend.routes.api import api_bp

from web_interface.backend import settings

app = flask.Flask(__name__)

app.register_blueprint(api_bp)


@app.route('/')
def index():
    return flask.jsonify({'message': 'Hello, World!'})


if __name__ == '__main__':
    app.run(debug=True, host=settings.server.host, port=settings.server.port)
