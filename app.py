import streamlit as st
import requests

st.set_page_config(page_title="Leitor de Receitas", page_icon="🍽️")
st.title("📘 Leitor de Receitas PDF")
st.write("Faça upload de um arquivo PDF de receitas e faça perguntas sobre ele!")

# Upload do PDF
uploaded_file = st.file_uploader("Escolha um arquivo PDF", type="pdf")

if uploaded_file:
    with st.spinner("Enviando arquivo para a API..."):
        files = {
            'file': (uploaded_file.name, uploaded_file, 'application/pdf')
        }
        headers = {
            'x-api-key': st.secrets["CHATPDF_API_KEY"]
        }
        response = requests.post(
            'https://api.chatpdf.com/v1/sources/add-file',
            headers=headers,
            files=files
        )

    if response.status_code == 200:
        source_id = response.json()["sourceId"]
        st.success("✅ Arquivo enviado com sucesso!")

        # Campo de pergunta
        st.subheader("🔍 Faça uma pergunta sobre o conteúdo")
        question = st.text_input("Digite sua pergunta")

        if question:
            with st.spinner("Consultando a API..."):
                payload = {
                    "sourceId": source_id,
                    "messages": [
                        {
                            "role": "user",
                            "content": question
                        }
                    ]
                }
                answer_response = requests.post(
                    "https://api.chatpdf.com/v1/chats/message",
                    headers=headers,
                    json=payload
                )

                if answer_response.status_code == 200:
                    answer = answer_response.json()["content"]
                    st.markdown(f"**Resposta:** {answer}")
                else:
                    st.error("❌ Erro ao obter resposta da API.")
    else:
        st.error(f"❌ Erro ao enviar PDF: {response.text}")

st.markdown("---")
st.caption("Desenvolvido com ❤️ usando Streamlit")
