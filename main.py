# from src.agent.agent import extract_agent  
# import json

# with open("site.md", encoding="utf-8") as a:
#     texto = a.read()

# resultado = extract_agent(texto)
# print(resultado.model_dump_json(indent=2))

from src.services.company_services import company_service

company_service()