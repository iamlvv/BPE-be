from flask import Flask
from flask_cors import CORS

# Define bpsky.
bpsky = Flask(__name__, static_url_path="/static/")
CORS(bpsky, supports_credentials=True, resources={r"/*": {"origins": "*"}})

from controller.export import *
