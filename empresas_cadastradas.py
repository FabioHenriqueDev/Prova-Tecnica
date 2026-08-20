import streamlit as st
from src.repositories.company_repository import CompanyRepository
from src.repositories.medical_segments import MedicalSegmentRepository
from src.repositories.certifications_repository import CertificationsRepository
from src.repositories.products_repository import ProductRepository

company_repository = CompanyRepository()
segment_medical_repository = MedicalSegmentRepository()
certification_repository = CertificationsRepository()
product_repository = ProductRepository()

def empresas_cadastradas():
    st.markdown("### 📊 Resultado da Busca")
    st.divider()
    
    for empresa in company_repository.get_all():
        id_empresa = empresa.id
        nome = empresa.name
        website = empresa.website
        email = empresa.email
        phone = empresa.phone
        endereco = empresa.address
        business_type = empresa.business

        with st.container(border=True):
            # BLOCO 1: EMPRESA
            st.markdown("**🏢 EMPRESA**")
            st.subheader(nome)
            st.caption(f"Tipo: {business_type}")

            st.write(f"🌐 {website}")
            st.write(f"✉️ {email}")
            st.write(f"📞 {phone}")
            st.write(f"📍 {endereco}")

            st.divider()


            # BLOCO 2: SEGMENTOS MÉDICOS
            segmentos = [
                            seg.name for seg in segment_medical_repository.get_all()
                            if seg.company_id == id_empresa
                         ]

            if segmentos:
                st.markdown("**🏥 SEGMENTOS MÉDICOS**")
                for seg in segmentos:
                    st.write(seg)
            else:
                st.markdown("**🏥 SEGMENTOS MÉDICOS**")
                st.write('Nenhum segmento médico encontrado')

                        

            st.divider()
           
            certificacoes = [
                    certificado.certification
                    for certificado in certification_repository.get_all()
                    if certificado.company_id == id_empresa
                ]

            if certificacoes:
                st.markdown("**📜 CERTIFICAÇÕES**")
                for cert in certificacoes:
                    st.write(cert)
            else:
                st.markdown("**📜 CERTIFICAÇÕES**")
                st.write('Nenhuma certificação encontrada')


            st.divider()


             # BLOCO 3: PRODUTOS
            produtos = [
                p for p in product_repository.get_all()
                if p.company_id == id_empresa
            ]

            st.markdown(f"**📦 PRODUTOS: ({len(produtos)})**")

            if produtos:
                with st.expander("Ver produtos"):
                    for p in produtos:
                        col1, col2 = st.columns([1, 5])
                        with col1:
                            if p.image_url:
                                st.image(p.image_url, width=60)
                            else:
                                st.markdown("🏥")
                        with col2:
                            st.write(f"**{p.name}**")
                            if p.category:
                                st.caption(p.category)
            else:
                st.write("Nenhum produto encontrado")

    

