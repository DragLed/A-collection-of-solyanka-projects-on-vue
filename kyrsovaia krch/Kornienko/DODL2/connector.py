from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import settings


engine = create_engine(settings.db_url_sync, echo=True)

session = sessionmaker(bind=engine)

session_factory = sessionmaker(bind=engine, autoflush=True)