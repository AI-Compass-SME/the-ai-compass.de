from sqlalchemy import Column, Integer, String, Text
from database import Base

class Company(Base):
    __tablename__ = "companies"

    company_id = Column(Integer, primary_key=True, index=True)
    industry = Column(String)
    website = Column(String)
    number_of_employees = Column(String)
    city = Column(String)
    company_name = Column(String)
    email = Column(Text)
