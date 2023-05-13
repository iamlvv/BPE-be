from bpsky import bpsky
import os

if __name__ == "__main__":
    bpsky.run(host="0.0.0.0", port=os.environ.get("PORT", 8000), debug=False)
