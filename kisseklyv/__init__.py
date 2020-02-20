import flask
import config

app = flask.Flask(__name__)
app.config.from_object(config.Config())

from kisseklyv import routes

if __name__ == '__main__':
    app.run(port=5001)
