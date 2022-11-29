#=================================================================================================================
#=================================================================================================================

# SYSTEM MODULE
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# CUSTOM MODULE
from ..config import DATABASE_URL

#=================================================================================================================
#=================================================================================================================

# print("DATABASE_URL", DATABASE_URL)

# engine = create_engine(DATABASE_URL, pool_size=20, max_overflow=0, pool_timeout=30, pool_recycle=3600)
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

#=================================================================================================================
#=================================================================================================================
