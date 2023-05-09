from flask import Flask
from flask_cors import CORS

# Define bpsky.
bpsky = Flask(__name__, static_url_path="/static/")
cors = CORS(bpsky)
