import sqlite3
import os
import sys
import logging

from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(formatter)

logger.addHandler(stdout_handler)


try:
    MPT_DATABASE_FILE_PATH = os.environ["MPT_DATABASE_FILE_PATH"]
except KeyError:
    logger.error("Database FILE NOT FOUND. 'MPT_DATABASE_FILE_PATH' not set")
    sys.exit(1)


def main():
    provider = get_provider()

    user_resp = input(f"Mortgage provider: {provider}. Is this Correct? (y/n): ")
    if user_resp.lower() == "n":
        new_provider = input("New Provider Name: ")
        loan = input("Amount of Loan Taken: ")
        interest_rate = input("Interest Rate: ")
        period = input("Fixed Period: ")
        start_period = input("Mortgage Start Year: ")
        remove_active_provider()
        insert_new_provider(new_provider, loan, interest_rate, period, start_period)

        return

    new_total = input("Enter Updated total: ")

    new_total = new_total.replace("£", "").replace(",", "")
    new_total = float(new_total)

    update_total(provider, new_total)


def remove_active_provider():
    con = get_db()
    with con:
        con.execute("UPDATE mortgage SET active = 0 WHERE active = 1")
    con.close()

    logger.info("Old provider set as Inactive.")


def insert_new_provider(new_provider, loan, interest_rate, period, start_period):

    current_date = datetime.now().isoformat()
    con = get_db()

    with con:
        con.execute(
            f"""INSERT INTO mortgage (provider, loan, interest_rate, period, start_period, date_added, active) VALUES (:provider, :loan, :interest_rate, :period, :start_period, :date_added, :active)""",
            {
                "provider": new_provider,
                "loan": float(loan),
                "interest_rate": float(interest_rate),
                "period": int(period),
                "start_period": int(start_period),
                "date_added": current_date,
                "active": True,
            },
        )

        con.execute(
            f"""INSERT INTO mortgage_balance (balance, date_updated, provider) VALUES (:balance, :date_updated, :provider)""",
            {
                "balance": float(loan),
                "date_updated": current_date,
                "provider": new_provider,
            },
        )

    con.close()

    logger.info("New provider Inserted.")

    data = {
        "provider": new_provider,
        "loan": loan,
        "interest_rate": interest_rate,
        "period": period,
        "start_period": start_period,
    }

    logger.info(f"{data}")


def get_provider():
    query = f"""SELECT provider from mortgage WHERE active == 1;"""

    c = get_db().cursor()
    c.execute(query)
    data = c.fetchone()
    c.close()

    data = dict(data)

    logger.info(f"Retrieved provider information: {data}")

    return data["provider"]


def update_total(provider, new_total):

    con = get_db()
    with con:
        con.execute(
            f"""INSERT INTO mortgage_balance (balance, provider, date_updated) VALUES (:balance, :provider, :date_updated)""",
            {
                "balance": new_total,
                "provider": provider,
                "date_updated": datetime.now().isoformat(),
            },
        )

    c = con.cursor()

    query = "SELECT * FROM mortgage_balance ORDER BY date_updated DESC LIMIT 1;"

    c.execute(query)
    data = c.fetchone()

    con.close()

    data = dict(data)

    logger.info("Data Updated")
    logger.info(f"{data}")


def get_db():
    db = sqlite3.connect(MPT_DATABASE_FILE_PATH)
    db.row_factory = sqlite3.Row

    return db


main()
