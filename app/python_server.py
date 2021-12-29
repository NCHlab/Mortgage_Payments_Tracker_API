from app import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=4004)


# https://flask.palletsprojects.com/en/2.0.x/patterns/sqlite3/
# https://flask.palletsprojects.com/en/2.0.x/appcontext/
