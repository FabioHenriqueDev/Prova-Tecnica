from src.domain.entities.company_entities import biuld_company
from src.domain.entities.product_entites import biuld_product
from src.domain.entities.company_entities import Company
from src.repositories.company_repository import CompanyRepository
from src.agent.agent import extract_agent

# pego os dados da IA e jogo na func
company_repositorie = CompanyRepository()


def company_service() -> Company:

    with open("site.md", encoding="utf-8") as a:
        texto = a.read()

    resultado = extract_agent(texto)
    print(resultado.model_dump_json(indent=2))


    name = resultado.name
    description = resultado.description
    website = resultado.website
    email = resultado.email
    phone = resultado.phone
    address = resultado.address
    business_type = resultado.business_type

    company = biuld_company(name=name, description=description, website=website, email=email, phone=phone, address=address, business_type=business_type)


    # PRODUTOS:

    produtos = resultado.products

    if produtos:
        for p in produtos:
            produto = biuld_product( name=p.name, description=p.description, image_url=p.image_url, category=p.category, medical_segment=p.medical_segment,)
            # aq joga no banco de dados
    
    print(produtos)


    # SEGMENTOS MEDICOS

    segmentos_medicos = resultado.medical_segments

    if segmentos_medicos:
        for s in segmentos_medicos:
            # Adiciona no banco
            ...

    print(segmentos_medicos)

    #CERTIFICACAO

    certificacoes = resultado.certifications

    if certificacoes:
        for c in certificacoes:
            #Adicionar no banco de dados
            ...
    print(certificacoes)
    # company_repositorie.create_company(company)
    return company