from db.postgresql import session_psql


def get_db():
    db = session_psql()
    try:
        yield db
    finally:
        db.close()