from abc import ABC, abstractmethod
from src.domain.entities.product_entites import CompanyProducts
from src.database.database import get_db
from src.model.models import Products
from src.database.database import get_db
from sqlalchemy import select

class ICompanyProductRepository(ABC):

    @abstractmethod
    def create_product(self, product: CompanyProducts) -> CompanyProducts:
        ...
    
    @abstractmethod
    def get_all(self):
        ...


class ProductRepository(ICompanyProductRepository):
    def create_product(self, product: CompanyProducts):
        
        product_model = Products(
                name=product.name,
                description=product.description,
                image_url=product.image_url,
                category=product.category,
                medical_sector=product.medical_segment,
                company_id=product.company_id
            )

          
        
        return product_model

    def get_all(self):
         with get_db() as db:
            query = select(Products)
            produtos = db.scalars(query).all()
            return produtos
