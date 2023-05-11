from bpsky import bpsky
from dotenv import load_dotenv
import os

if __name__ == "__main__":
    load_dotenv()
    bpsky.run(host="0.0.0.0", port=os.environ.get("PORT", 8000), debug=False)
