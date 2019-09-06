from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
import os


app = Flask(__name__)
app.data = {}
app.config.from_object(Config)
bootstrap = Bootstrap(app)

from app import routes, models