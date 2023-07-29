# database/connection.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Update the database URL to use the MySQL container's name as the host
DATABASE_URL = "mysql+mysqlconnector://grpc_user:grpc_password@grpc_db/grpc_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
