import streamlit as st
from openai import OpenAI
from PIL import Image
import requests
import io
import os

# CONFIGURAÇÃO DE LIMITE DE UPLOAD (800MB) E LAYOUT
st.set_page_config(
    page_title="TORNQUIST EVOLUTION PRO", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Comando interno para aumentar o limite de bytes (800MB)
# Nota: O Streamlit Cloud às vezes limita isso pelo servidor, 
# mas este comando é o padrão para aplicações locais/servidores próprios.
os.environ["STREAMLIT_SERVER_MAX_UPLOAD_SIZE"] = "800"

st.title("🚀 TORNQUIST IMAGE EVOLUTION PRO")

# --- CONEXÃO COM A IA ---
# Tenta pegar dos Secrets, se não achar, avisa o usuário
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except:
    st.error("⚠️ Erro: Chave API não configurada nos Secrets do Streamlit!")
    st.stop()

# --- GERENCIAMENTO DE MEMÓRIA (SESSION STATE) ---
if 'current_image' not in st.session_state:
    st.session_state.current_image = None
if 'history' not in st.session_state:
    st.session_state.history = []

# --- BARRA LATERAL (UPLOADS) ---
with st.sidebar:
    st.header("📂 Entrada de Arquivo")
    uploaded_file = st.file_uploader("Enviar foto (Máx 800MB)", type=["png", "jpg", "jpeg"])
    
    if uploaded_file and st.session_state.current_image is None:
        img = Image.open(uploaded_file).convert("RGBA")
        # Redimensiona se for muito grande para a API da OpenAI (máximo 4MB após processada)
        if uploaded_file.size > 4 * 1024 * 1024:
             img = img.resize((1024, 1024))
        st.session_state.current_image = img
        st.success("Imagem carregada!")

    if st.button("🗑️ Resetar Tudo"):
        st.session_state.current_image = None
        st.session_state.history = []
        st.rerun()

# --- ÁREA PRINCIPAL ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🖼️ Imagem Atual")
    if st.session_state.current_image:
        st.image(st.session_state.current_image, use_container_width=True)
    else:
        st.info("Aguardando upload de imagem...")

with col2:
    st.subheader("🤖 Comando de Evolução")
    instrucao = st.text_area("Descreva as melhorias ou adições:", 
                            placeholder="Ex: Adicione uma iluminação cinematográfica, uma pessoa ao fundo e corrija falhas na textura.")

    if st.button("✨ Evoluir Imagem"):
        if st.session_state.current_image and instrucao:
            with st.spinner("A IA está analisando e recriando sua imagem..."):
                try:
                    # Converter imagem atual para Bytes (PNG)
                    byte_io = io.BytesIO()
                    # A API de Edição exige PNG e geralmente imagens quadradas
                    temp_img = st.session_state.current_image.resize((1024, 1024))
                    temp_img.save(byte_io, format='PNG')
                    image_bytes = byte_io.getvalue()

                    # Chamada para Edição (DALL-E 2 Edit)
                    response = client.images.edit(
                        image=image_bytes,
                        prompt=instrucao,
                        n=1,
                        size="1024x1024"
                    )

                    # Atualizar Imagem na Sessão
                    new_url = response.data[0].url
                    new_img_data = requests.get(new_url).content
                    st.session_state.current_image = Image.open(io.BytesIO(new_img_data)).convert("RGBA")
                    
                    st.success("Evolução concluída!")
                    st.rerun()

                except Exception as e:
                    st.error(f"Erro na IA: {e}")
        else:
            st.warning("Envie uma foto e escreva o que deseja mudar.")

# --- RODAPÉ ---
st.markdown("---")
st.caption("TORNQUIST PRO MAX - Sistema de Evolução Iterativa via IA")
