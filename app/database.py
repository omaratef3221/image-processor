from sqlalchemy import create_engine, Column, Integer, LargeBinary, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./image_data.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class ImageFrame(Base):
    __tablename__ = "image_frames"
    
    id = Column(Integer, primary_key=True, index=True)
    depth = Column(Float, unique=True, index=True)
    image_data = Column(LargeBinary)  # Storing as PNG bytes
    
Base.metadata.create_all(bind=engine)