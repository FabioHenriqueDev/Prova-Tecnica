from src.agent.agent import extract_agent  
import json

with open("site.md", encoding="utf-8") as a:
    texto = a.read()

resultado = extract_agent(texto, "https://spmmedicare.com")
print(resultado.model_dump_json(indent=2))

with open("dados.json", 'w', encoding="utf-8") as a:
    json.dump(resultado.model_dump(), a, ensure_ascii=False, indent=4)