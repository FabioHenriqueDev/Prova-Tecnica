from abc import ABC, abstractmethod
from src.domain.entities.company_entities import Company
from src.model.models import Companies
from src.database.database import get_db
from sqlalchemy import select

class ICompanyRepository(ABC):

    @abstractmethod
    def create_company(self, company: Company) -> Companies:
        ...

    # @abstractmethod
    # def get_by_id(self, company_id: int):
    #     ...

    @abstractmethod
    def get_all(self):
        ...


class CompanyRepository(ICompanyRepository):
    def create_company(self, db, company: Company):
       
        company_model = Companies(
                name=company.name,
                description=company.description,
                website=company.website,
                email=company.email,
                phone=company.phone,
                address=company.address,
                business=company.business_type,
            )

        db.add(company_model)
        db.flush()

        return company_model

    
    def get_all(self):
        with get_db() as db:
            query = select(Companies)
            empresas = db.scalars(query).all()
            return empresas
