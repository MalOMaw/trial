from flask import Flask

app = Flask(__name__)

app.secret_key = "NOT A PRODUCT YET"

from app import views