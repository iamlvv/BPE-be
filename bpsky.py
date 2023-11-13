from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from websocket import listenForChanges

# Define bpsky.
bpsky = Flask(__name__, static_url_path="/static/")
CORS(bpsky, supports_credentials=True, resources={r"/*": {"origins": "*"}})

load_dotenv()
# listenForChanges()
from controller.export import *
