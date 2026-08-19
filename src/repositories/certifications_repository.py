from abc import ABC, abstractmethod
from src.model.models import CompanyCertifications

class ICertificationsRepository(ABC):
    @abstractmethod
    def create_certifications(self, certification: str, company_id: int) -> CompanyCertifications:
        ...

class CertificationsRepository(ICertificationsRepository):
    def create_certifications(self, certification, company_id):
        certification_company = CompanyCertifications(certification=certification, company_id=company_id) 

        return certification_company