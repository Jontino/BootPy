from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
basedir = path.abspath(path.dirname(__file__))

# Platform ("PC" or "RPi")
# app.config['APP_PLATFORM'] = 'PC'

# Configure database
app.config['SECRET_KEY'] = '2aec8317ea23944c6328c3db31ca42ab'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


from bootpy.api.routes import api as api_blueprint
from bootpy.site.routes import site as site_blueprint
from .udp.udp import UdpServer

udp_server = UdpServer('localhost', 5001)

app.register_blueprint(api_blueprint, url_prefix='/api')
app.register_blueprint(site_blueprint)
