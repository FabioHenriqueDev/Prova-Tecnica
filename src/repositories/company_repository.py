from abc import ABC, abstractmethod
from src.domain.entities.company_entities import Company

class ICompanyRepository(ABC):

    @abstractmethod
    def create_company(self, company: Company) -> Company:
        ...

    @abstractmethod
    def get_by_id(self, company_id: int):
        ...

    @abstractmethod
    def get_all(self):
        ...


class CompanyRepository(ICompanyRepository):
    def create_company(self, company):
        ...

    def get_by_id(self, company_id: int):
            ...

    def get_all(self):
            ...