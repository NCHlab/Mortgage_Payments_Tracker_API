import sqlite3

conn = sqlite3.connect("mortgage.db")
c = conn.cursor()

c.execute(
    """CREATE TABLE users (
        username TEXT PRIMARY KEY,
        password PASSWORD,
        last_login TEXT 
        )"""
)


c.execute(
    """CREATE TABLE payments (
        id INTEGER PRIMARY KEY,
        user_id TEXT,
        paid REAL,
        date TEXT,
        reason TEXT,
        from_tenant INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(username)
        )"""
)


c.execute(
    """CREATE TABLE overpayments (
        id INTEGER PRIMARY KEY,
        user_id TEXT,
        paid REAL,
        date TEXT,
        reason TEXT,
        FOREIGN KEY(user_id) REFERENCES users(username)
        )"""
)


c.execute(
    """CREATE TABLE logs (
        id INTEGER PRIMARY KEY,
        log TEXT,
        user_id TEXT,
        table_name TEXT,
        state TEXT,
        date TEXT,
        FOREIGN KEY(user_id) REFERENCES users(username)
        )"""
)

c.execute(
    """CREATE TABLE home_improvements (
        id INTEGER PRIMARY KEY,
        user_id TEXT,
        paid REAL,
        chargeable INTEGER,
        date TEXT,
        reason TEXT,
        FOREIGN KEY(user_id) REFERENCES users(username)
        )"""
)


c.execute(
    """CREATE TABLE money_repaid (
        id INTEGER PRIMARY KEY,
        debtor_user_id TEXT,
        debtee_user_id TEXT,
        paid_back REAL,
        FOREIGN KEY(debtor_user_id) REFERENCES users(username),
        FOREIGN KEY(debtee_user_id) REFERENCES users(username)
        )"""
)

c.execute(
    """CREATE TABLE mortgage (
        provider TEXT PRIMARY KEY,
        loan REAL,
        interest_rate REAL,
        period INTEGER,
		start_period INTEGER,
        date_added TEXT
        )"""
)

c.execute(
    """CREATE TABLE mortgage_balance (
        balance REAL,
        date_updated REAL,
        provider TEXT,
		FOREIGN KEY(provider) REFERENCES mortgage(provider)
        )"""
)


conn.commit()
conn.close()
