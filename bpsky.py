from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# Define bpsky.
bpsky = Flask(__name__, static_url_path="/static/")
CORS(bpsky, supports_credentials=True, resources={r"/*": {"origins": "*"}})

load_dotenv()
from controller.export import *
