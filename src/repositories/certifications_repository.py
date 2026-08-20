from abc import ABC, abstractmethod
from src.model.models import CompanyCertifications
from sqlalchemy import select
from src.database.database import get_db

class ICertificationsRepository(ABC):
    @abstractmethod
    def create_certifications(self, certification: str, company_id: int) -> CompanyCertifications:
        ...

    @abstractmethod
    def get_all(self):
            ...

class CertificationsRepository(ICertificationsRepository):
    def create_certifications(self, certification, company_id, db):
        certification_company = CompanyCertifications(certification=certification, company_id=company_id) 
        db.add(certification_company)
        return certification_company


    def get_all(self):
        with get_db() as db:
            query = select(CompanyCertifications)
            certificacoes = db.scalars(query).all()
            return certificacoes
