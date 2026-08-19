from enum import Enum
from pydantic import BaseModel

class BusinessType(str, Enum):
    FABRICANTE = "MANUFACTURER"
    DISTRIBUIDOR = "DISTRIBUTOR"
    PRESTADOR_SERVICOS = "SERVICE PROVIDER"

class Product(BaseModel):
    name: str
    description: str | None = None
    image_url: str | None = None
    category: str | None = None
    medical_segment: str | None = None


class CompanyExtraction(BaseModel):
    name: str
    description: str
    website: str
    email: str | None = None
    phone: str | None = None
    address: str | None = None
    business_type: BusinessType
    medical_segments: list[str]
    products: list[Product]
    certifications: list[str]
