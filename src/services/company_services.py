from src.domain.entities.company_entities import biuld_company
from src.domain.entities.product_entites import biuld_product
from src.domain.entities.company_entities import Company
from src.repositories.company_repository import CompanyRepository
from src.repositories.products_repository import ProductRepository
from src.repositories.medical_segments import MedicalSegmentRepository
from src.repositories.certifications_repository import CertificationsRepository
from src.agent.agent import extract_agent
from src.database.database import get_db

# pego os dados da IA e jogo na func
company_repositorie = CompanyRepository()
product_repository = ProductRepository()
segment_medical_repository = MedicalSegmentRepository()
certification_repository = CertificationsRepository()

def company_service() -> Company:

    with open("site.md", encoding="utf-8") as a:
        texto = a.read()

    resultado = extract_agent(texto)
    print(resultado.model_dump_json(indent=2))

    with get_db() as db:
        name = resultado.name
        description = resultado.description
        website = resultado.website
        email = resultado.email
        phone = resultado.phone
        address = resultado.address
        business_type = resultado.business_type

        company = biuld_company(name=name, description=description, website=website, email=email, phone=phone, address=address, business_type=business_type)
        company_model = company_repositorie.create_company(db=db, company=company)
        company_id = company_model.id

        # PRODUTOS:

        produtos = resultado.products

        if produtos:
            for p in produtos:
                produto = biuld_product( name=p.name, description=p.description, image_url=p.image_url, category=p.category, medical_segment=p.medical_segment, company_id=company_id)
                produto_model = product_repository.create_product(produto)
                db.add(produto_model)
        


        # # SEGMENTOS MEDICOS

        segmentos_medicos = resultado.medical_segments

        if segmentos_medicos:
            for s in segmentos_medicos:
                segmento_model = segment_medical_repository.create_segment(s, company_id)
                db.add(segmento_model)


        

        # #CERTIFICACAO

        certificacoes = resultado.certifications

        if certificacoes:
            for c in certificacoes:
                certificacao = certification_repository.create_certifications(certification=c, company_id=company_id)
                db.add(certificacao)
        
        db.commit()

    return True