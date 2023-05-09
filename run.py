from bpsky import bpsky
from dotenv import load_dotenv
import os

if __name__ == "__main__":
    load_dotenv()
    from controller import *
    bpsky.run("0.0.0.0", port=os.getenv('PORT', 8000))
