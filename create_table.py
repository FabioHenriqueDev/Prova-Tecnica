# create_tables.py
from src.database.database import Base, engine

# IMPORTANTE: precisa importar os models, mesmo sem usar diretamente,
# senão o Base.metadata não "conhece" as tabelas
from src.model.models import Companies # ajusta o caminho conforme seu projeto

Base.metadata.create_all(bind=engine)

print("Tabelas criadas com sucesso!")