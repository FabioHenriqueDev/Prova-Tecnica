from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from src.database.database import Base
from sqlalchemy_utils.types import ChoiceType
from datetime import datetime
from sqlalchemy import Column, DateTime, func

class Companies(Base):
    __tablename__ = "companies"

    BUSINESS_TYPE = (
        ('MANUFACTURER', 'MANUFACTURER'),
        ('DISTRIBUTOR', 'DISTRIBUTOR'),
        ('SERVICE PROVIDER', 'SERVICE PROVIDER')
    )

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String(100), unique=True, nullable=False)
    description = Column('description', Text, nullable=False)
    website = Column('website', String(300), nullable=False)
    email = Column('email', String(100))
    phone = Column('phone', String(25))
    address = Column('address', String(100))
    business = Column('business_type', ChoiceType(choices=BUSINESS_TYPE)) # Manufacturer, Distributor, Service Provider
    created_at = Column('created_at', DateTime, server_default=func.now())

    certifications = relationship("CompanyCertifications", back_populates="company", cascade="all, delete-orphan")
    medical_segments = relationship("CompanyMedicalSegments", back_populates="company", cascade="all, delete-orphan")
    products = relationship("Products", back_populates="company", cascade="all, delete-orphan")


class CompanyMedicalSegments(Base):
    __tablename__ = 'company_medical_segments'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String(100), nullable=False)
    company_id = Column('company_id', ForeignKey('companies.id'), nullable=False)
    created_at = Column('created_at', DateTime, server_default=func.now())

    company = relationship("Companies", back_populates="medical_segments")
    


class Products(Base):
    __tablename__ = 'company_products'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    company_id = Column('company_id', ForeignKey('companies.id'), nullable=False)
    name = Column('name', String(100), nullable=False)
    description = Column('description', Text)
    image_url = Column('image_url', String(300))
    category = Column('category', String(100))
    medical_sector = Column('medical_sector', String(100))
    created_at = Column('created_at', DateTime, server_default=func.now())

    company = relationship("Companies", back_populates="products")


class CompanyCertifications(Base):
    __tablename__ = 'company_certifications'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    certification = Column('certification', String(100))
    company_id = Column('company_id', ForeignKey('companies.id'), nullable=False)
    created_at = Column('created_at', DateTime, server_default=func.now())

    company = relationship("Companies", back_populates="certifications")
