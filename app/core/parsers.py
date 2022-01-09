from typing import List, Type
from datetime import datetime
import sqlite3


def parse_multi_db_data(data: Type[sqlite3.Row]) -> List[dict]:
    """
    Converts sql.Row to Dict for processing
    Casts Boolean stored as Integers (SQLite3 limitation) as Boolean
    """

    # Generator comprehension to save memory, even though memory usage negligible here
    data = (dict(row) for row in data)

    list_of_data = []

    for row in data:
        if "chargeable" in row:
            row["chargeable"] = bool(row["chargeable"])
        elif "from_tenant" in row:
            row["from_tenant"] = bool(row["from_tenant"])

        list_of_data.append(dict(row))

    return list_of_data


def parse_single_db_data(data) -> dict:
    return dict(data)


def parse_filename(prefix, tablename, filetype):
    time = datetime.now().strftime("%d-%m-%Y")
    filename = f"{prefix}-{tablename}-{str(time)}.{filetype}"

    return filename
