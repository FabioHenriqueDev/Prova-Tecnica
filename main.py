import streamlit as st
from extrair_dados import extrair_dados_agente
from empresas_cadastradas import empresas_cadastradas

st.sidebar.title("Company Intelligence")
opcao_menu = st.sidebar.radio(
    "Navegação:",
    ["🚀 Nova Extração", "🏢 Empresas Cadastradas"]
)

if opcao_menu == '🚀 Nova Extração':
    extrair_dados_agente()
elif opcao_menu == '🏢 Empresas Cadastradas':
    empresas_cadastradas()