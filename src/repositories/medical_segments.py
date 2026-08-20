from abc import ABC, abstractmethod
from src.model.models import CompanyMedicalSegments
from sqlalchemy import select
from src.database.database import get_db

class IMedicalSegmentsRepository(ABC):

    @abstractmethod
    def create_segment(self, name_segment: str, company_id):
        ...

    @abstractmethod
    def get_all(self):
        ...

class MedicalSegmentRepository(IMedicalSegmentsRepository):
    def create_segment(self, name_segment, company_id, db) -> CompanyMedicalSegments:
        segmento_medico = CompanyMedicalSegments(name=name_segment, company_id=company_id)
        db.add(segmento_medico)
        return segmento_medico

    def get_all(self):
        with get_db() as db:
            query = select(CompanyMedicalSegments)
            segmentos = db.scalars(query).all()
            return segmentos