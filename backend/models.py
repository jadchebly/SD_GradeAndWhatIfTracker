from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float, Date

Base = declarative_base()

class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    weight_pct = Column(Float, nullable=False)       # e.g., 20.0
    due_date = Column(Date, nullable=False)
    score_pct = Column(Float, nullable=True)         # None until graded




#10452
