from src.errors.product_exeptions import InvalidPrdocutNameError, InvalidImageUrlError
from urllib.parse import urlparse

class CompanyProducts:
    def __init__(self, name, description, image_url, category, medical_segment):
        self.name = self.validate_name_product(name)
        self.description = description
        self.image_url = image_url
        self.category = category
        self.medical_segment = medical_segment

    
    def validate_name_product(self, name):
        if not name or len(name) < 2:
           raise InvalidPrdocutNameError("O nome da empresa deve possuir pelo menos 2 caracteres.")
        return name


def biuld_product(name, description, image_url, category, medical_segment):
    produto = CompanyProducts(name, description, image_url, category, medical_segment)

    return produto
