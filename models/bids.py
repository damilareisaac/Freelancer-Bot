from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

Base = declarative_base()

engine = create_engine(
    "postgresql://damilareisaac:v2_3yL7J_c6ZasqzDEjWGcQHncF6vCKp@db.bit.io:5432/damilareisaac/freelancer-jobs",
    isolation_level="AUTOCOMMIT",
    pool_pre_ping=True,
    connect_args={
        "keepalives": 1,
        "keepalives_idle": 3000,
        "keepalives_interval": 3000,
        "keepalives_count": 10,
    },
)

Session = sessionmaker(bind=engine)


class Bids(Base):
    __tablename__ = "Bids"
    id = Column(Integer, primary_key=True)
    url = Column(String)
    description = Column(String(1000000))
    price_detail = Column(String(256))
    proposal = Column(String(1000000))
    skill = Column(String)
    country = Column(String)
    city = Column(String)
    member_since = Column(String)
    created_date = Column(DateTime(timezone=True), server_default=func.now())
    updated_date = Column(DateTime(timezone=True), onupdate=func.now())

    def save(self):
        with Session() as session:
            session.add(self)
            session.commit()

    @classmethod
    def filter(cls, links):
        with Session() as session:
            result = session.query(cls).filter(cls.url.in_(links))
            result_url = [r.url for r in result]
            return [q for q in links if q not in result_url]


Base.metadata.create_all(engine)
