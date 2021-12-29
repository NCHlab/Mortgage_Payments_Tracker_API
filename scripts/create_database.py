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
        date TEXT
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
    """CREATE TABLE tenants (
        id TEXT PRIMARY KEY,
        tenant_name TEXT,
        current_tenant TEXT,
        estate_agent TEXT,
        rent_amount FLOAT,
        date TEXT
        )"""
)


c.execute(
    """CREATE TABLE money_owed (
        id INTEGER PRIMARY KEY,
        debtor TEXT,
        debtee TEXT,
        FOREIGN KEY(debtor) REFERENCES users(username),
        FOREIGN KEY(debtee) REFERENCES users(username)
        )"""
)


c.execute(
    """CREATE TABLE money_repaid (
        id INTEGER PRIMARY KEY,
        debtor_user_id TEXT,
        debtee_user_id TEXT,
        paid_back FLOAT,
        FOREIGN KEY(debtor_user_id) REFERENCES users(username),
        FOREIGN KEY(debtee_user_id) REFERENCES users(username)
        )"""
)

conn.commit()
conn.close()
