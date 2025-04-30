import streamlit as st
import pandas as pd
from fpdf import FPDF
from io import BytesIO

# Configuração da página
st.set_page_config(page_title="Receitas Sustentáveis", layout="wide")

# Função para limpar caracteres incompatíveis com fpdf
def limpar_texto(texto):
    if not isinstance(texto, str):
        texto = str(texto)
    return (
        texto.replace("•", "-")
        .replace("–", "-")
        .replace("“", '"')
        .replace("”", '"')
        .replace("’", "'")
        .replace("‘", "'")
        .replace("…", "...")
        .encode("latin1", "ignore")
        .decode("latin1")
    )

# Carregar dados com cache
@st.cache_data
def load_data():
    return pd.read_csv("receitas.csv")

df = load_data()

# Título
st.title("🍽️ Banco de Receitas Sustentáveis")

# Filtros
with st.sidebar:
    st.header("🔍 Filtrar receitas")
    ingredientes = st.multiselect("🥦 Ingrediente Principal", sorted(df['ingrediente_principal'].dropna().unique()))
    autores = st.multiselect("👩‍🍳 Autor", sorted(df['autor'].dropna().unique()))
    nome_receita = st.text_input("📌 Nome da Receita")

# Aplicar filtros
filtered_df = df.copy()
if ingredientes:
    filtered_df = filtered_df[filtered_df['ingrediente_principal'].isin(ingredientes)]
if autores:
    filtered_df = filtered_df[filtered_df['autor'].isin(autores)]
if nome_receita:
    filtered_df = filtered_df[filtered_df['nome_receita'].str.contains(nome_receita, case=False, na=False)]

st.markdown(f"### 📋 {len(filtered_df)} Receita(s) Encontrada(s)")

# Função para gerar PDF
def gerar_pdf(row):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    nome = limpar_texto(row.get("nome_receita", "Receita Sem Nome"))
    pdf.cell(0, 10, nome, ln=True)

    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 10, limpar_texto(f"Ingrediente Principal: {row.get('ingrediente_principal', '')}"))
    autor = limpar_texto(row.get('autor', ''))
    if autor:
        pdf.multi_cell(0, 10, f"Autor: {autor} ({limpar_texto(row.get('curso', ''))} - {limpar_texto(row.get('semestre', ''))})")

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Ingredientes:", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 10, limpar_texto(row.get('ingredientes', '')))

    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Modo de Preparo:", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 10, limpar_texto(row.get('modo_de_preparo', '')))

    pdf_bytes = pdf.output(dest='S').encode('latin1')
    buffer = BytesIO(pdf_bytes)
    buffer.seek(0)
    return buffer

# Exibição das receitas
for _, row in filtered_df.iterrows():
    nome = row.get("nome_receita", "Receita sem nome")
    with st.expander(f"🍲 {nome}"):
        st.markdown(f"**Ingrediente Principal:** {row.get('ingrediente_principal', '')}")
        if row.get('autor', ''):
            st.markdown(f"**Autor:** {row['autor']} ({row.get('curso', '')} - {row.get('semestre', '')})")
        st.markdown("### Ingredientes")
        st.write(row.get('ingredientes', ''))
        st.markdown("### Modo de Preparo")
        st.write(row.get('modo_de_preparo', ''))

        pdf_file = gerar_pdf(row)
        st.download_button(
            label="📥 Baixar em PDF",
            data=pdf_file,
            file_name=f"{nome.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )
