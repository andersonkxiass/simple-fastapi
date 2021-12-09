import logging
import time

import databases
import psycopg2
import sqlalchemy
from fastapi import FastAPI
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from . import config

log = logging.getLogger("my-logger")

app = FastAPI()

secrets: config.Settings = config.Settings()

DATABASE_URL = f"postgresql://{secrets.DB_USER}:{secrets.DB_PASSWORD}@127.0.0.1:5432/sample_database"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("email", sqlalchemy.String),
    sqlalchemy.Column("cell_phone", sqlalchemy.String),
)

engine = create_engine(DATABASE_URL, pool_size=15, max_overflow=5)

metadata.create_all(engine)

Session = sessionmaker(bind=engine)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@event.listens_for(engine, "do_connect")
def receive_do_connect(dialect, conn_rec, cargs, cparams):
    print("opening new connections...")

    cparams["user"] = secrets.DB_USER
    cparams["password"] = secrets.DB_PASSWORD

    return psycopg2.connect(*cargs, **cparams)


@app.post("/")
async def create_user():
    query = users.insert().values(name="name", email="email", cell_phone="cell_phone")
    last_record_id = await database.execute(query)
    return {**users.dict(), "id": last_record_id}


@app.get("/")
async def test_db():
    query = users.select()
    return await database.fetch_all(query)


@app.get("/test_pool")
async def test():
    for i in range(0, 10):
        print(i)
        session_test = Session()  # A new connection will be created
        session_test.query(users).filter_by(id=1).first()  # some random query
        # session_test.close() # Just for test, keep open to request pool new one
        print(engine.pool.status())  # show pool info
        time.sleep(1)

    return {"response": "ok"}
