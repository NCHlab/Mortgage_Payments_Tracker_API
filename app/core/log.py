import json

from datetime import datetime

from app.core.db import get_db


def log_to_db(data):
    con = get_db()
    with con:
        con.execute(
            """INSERT INTO logs (log, date) VALUES (:log, :date)""",
            {"log": json.dumps(data), "date": datetime.now().isoformat()},
        )
