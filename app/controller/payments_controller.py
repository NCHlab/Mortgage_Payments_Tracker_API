from app.core.utils import get_session, parse_db_data
from app.core.db import get_db


def single_user_payments():

    username = get_session()

    c = get_db().cursor()
    c.execute("""SELECT * FROM payments WHERE user_id == :user""", {"user": username})
    data = c.fetchall()

    list_of_payments = parse_db_data(data)

    return list_of_payments


def all_user_payments():

    # Only using to validate user is authenticated
    get_session()

    c = get_db().cursor()
    c.execute("""SELECT * FROM payments""")
    data = c.fetchall()

    list_of_payments = parse_db_data(data)

    return list_of_payments


def insert_payment(body):

    username = get_session()

    con = get_db()
    with con:
        con.execute(
            """INSERT INTO payments 
        (user_id, paid, date, reason, from_tenant) 
        VALUES 
        (:user_id, :paid, :date, :reason, :from_tenant)""",
            {
                "user_id": username,
                "paid": body["paid"],
                "date": body["date"],
                "reason": body["reason"],
                "from_tenant": body["from_tenant"],
            },
        )
