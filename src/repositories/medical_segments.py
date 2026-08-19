from abc import ABC, abstractmethod
from src.model.models import CompanyMedicalSegments

class IMedicalSegmentsRepository(ABC):

    @abstractmethod
    def create_segment(self, name_segment: str, company_id):
        ...

class MedicalSegmentRepository(IMedicalSegmentsRepository):
    def create_segment(self, name_segment, company_id) -> CompanyMedicalSegments:
        segmento_medico = CompanyMedicalSegments(name=name_segment, company_id=company_id)

        return segmento_medico