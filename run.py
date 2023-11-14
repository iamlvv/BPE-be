from bpsky import bpsky
from bpsky import socketio
import os

if __name__ == "__main__":
    # bpsky.run(host="0.0.0.0", port=os.environ.get("PORT", 8000), debug=True)

    socketio.run(bpsky, host="0.0.0.0", port=os.environ.get("PORT", 8000), debug=True)
