import streamlit as st
from src.scraping.scrap import scraping_site
from src.services.company_services import company_service
import streamlit as st
from urllib.parse import urlparse


def extrair_dados_agente():
    st.set_page_config(page_title="Company Intelligence | Extrator de Saúde", page_icon="🔗", layout="centered")

    st.title("🔗 Extrator de Dados e Agentes")
    st.caption("Insira a URL abaixo para iniciar o processo de raspagem e análise.")

   
    with st.form(key="form_url"):
        url = st.text_input("URL do site:", placeholder="https://www.exemplo.com.br")
        botao_enviar = st.form_submit_button("🚀 Extrair Dados", use_container_width=True)

    if botao_enviar:
        if url.strip():
            parsed = urlparse(url)
            if parsed.scheme not in ("http", "https") or not parsed.netloc:
                st.warning("⚠️ Por favor, insira uma URL válida.")
                return

            with st.status("Iniciando processamento...", expanded=True) as status:
                status.write("🌐 Baixando o site e convertendo para Markdown...")
                scraping_site(url)

                status.write("🧠 Enviando para o agente de IA analisar...")
                try:
                    company_service(url)
                except Exception as e:
                    st.error(f'Erro: {e}')

                status.write("💾 Dados analisados e salvos no banco de dados!")
                st.success("Tudo pronto! A empresa foi cadastrada.")
            
        else:
            st.warning("⚠️ Por favor, insira uma URL válida.")


if __name__ == '__main__':
    extrair_dados_agente()