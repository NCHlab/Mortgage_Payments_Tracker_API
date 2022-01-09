import json

from datetime import datetime

from app.core.db import get_db
from app.core.session import get_session


def log_to_db(data, table_name, state):

    username = get_session()

    con = get_db()
    with con:
        con.execute(
            """INSERT INTO logs (log, user_id, table_name, state, date) VALUES (:log, :username, :table_name, :state, :date)""",
            {
                "log": json.dumps(data),
                "username": username,
                "table_name": table_name,
                "state": state,
                "date": datetime.now().isoformat(),
            },
        )
