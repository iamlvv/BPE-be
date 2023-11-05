from bpsky import bpsky
from socket_python import socketio
import os

socketio.init_app(bpsky)

if __name__ == "__main__":
    socketio.run(bpsky, host="0.0.0.0", port=os.environ.get("PORT", 8000), debug=True)
