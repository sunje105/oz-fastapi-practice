from models import Base, User
from db_connection import engine

Base.metadata.create_all(bind=engine)

from db_connection import SessionFactory
from sqlalchemy import insert, select


session = SessionFactory()
stmt = select(User)

result = session.execute(stmt)
mappings = result.mappings().all()