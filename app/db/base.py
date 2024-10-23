from sqlalchemy import create_engine


from sqlalchemy.orm import sessionmaker, declarative_base


SQLALCHEMY_DATABASE_URL = "postgresql://justparkdb_owner:xgvL79EwbByR@ep-tiny-hall-a1c6p0so.ap-southeast-1.aws.neon.tech/justparkdb?sslmode=require"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
