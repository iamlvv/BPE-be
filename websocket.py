import select
from database.db import DatabaseConnector


def listenForChanges():
    connection = DatabaseConnector.get_connection()

    cursor = connection.cursor()

    cursor.execute("LISTEN workspace_changes;")

    while True:
        if select.select([connection], [], [], 5) == ([], [], []):
            print("Timeout")
        else:
            connection.poll()
            while connection.notifies:
                notify = connection.notifies.pop(0)
                print("Got NOTIFY:", notify.pid, notify.channel, notify.payload)
                cursor.execute("SELECT * FROM workspace;")
                print(cursor.fetchall())
            connection.commit()
        break
