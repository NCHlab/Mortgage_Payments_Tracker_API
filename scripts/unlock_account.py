import sqlite3
import os
import sys
import logging

import argparse


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
    logger.info("Unlock Account Script Started.....")
    parser = argparse.ArgumentParser(description="Optional")
    parser.add_argument("--name", type=str, help="Requires name as string")

    args = parser.parse_args()
    username = args.name

    find_user(username)
    unlock_acc(username)


def find_user(username):

    con = get_db()
    cur = con.cursor()

    cur.execute(
        "SELECT username from users where username == :username", {"username": username}
    )

    data = cur.fetchone()
    con.close()

    if not data:
        logger.error("Username does not exist in Database")
        sys.exit()


def unlock_acc(username):

    con = get_db()
    with con:
        con.execute(
            "UPDATE users set login_attempt = 0, locked = 0 WHERE username == :username;",
            {"username": username},
        )
    con.close()

    logger.info(f"Unlocked Account for: {username}")


def get_db():
    db = sqlite3.connect(MPT_DATABASE_FILE_PATH)
    db.row_factory = sqlite3.Row

    return db


main()
