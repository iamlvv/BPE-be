from bpsky import bpsky
from bpsky import socketio
import os
import threading

from services.survey_service.cron.scheduling import Scheduling_send_email

if __name__ == "__main__":
    # bpsky.run(host="0.0.0.0", port=os.environ.get("PORT", 8000), debug=True)
    email_thread = threading.Thread(target=Scheduling_send_email.main)
    email_thread.daemon = True
    email_thread.start()
    socketio.run(bpsky, host="0.0.0.0", port=os.environ.get("PORT", 8000), debug=True)
