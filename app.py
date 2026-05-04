import streamlit as st
from openai import OpenAI
from PIL import Image
import requests
import io
import os

# 1. Aumentar limite de upload para 800MB (Configuração de Servidor)
st.set_page_config(page_title="TORNQUIST EVOLUTION PRO", layout="wide")

# Tenta configurar o limite de tamanho (apenas para execução local/custom)
os.environ["STREAMLIT_SERVER_MAX_UPLOAD_SIZE"] = "800"

st.title("🚀 TORNQUIST IMAGE EVOLUTION PRO")

# ============================================================
# COLOQUE SUA CHAVE AQUI ENTRE AS ASPAS:
# Exemplo: client = OpenAI(api_key="sk-12345...")
# ============================================================
client = OpenAI(api_key="COLE_AQUI_SUA_CHAVE_REAL_DA_OPENAI")

# Gerenciamento de Memória (Session State)
if 'current_image' not in st.session_state:
    st.session_state.current_image = None

# Barra Lateral
with st.sidebar:
    st.header("📂 Entrada")
    uploaded_file = st.file_uploader("Enviar foto (Máx 800MB)", type=["png", "jpg", "jpeg"])
    
    if uploaded_file and st.session_state.current_image is None:
        img = Image.open(uploaded_file).convert("RGBA")
        st.session_state.current_image = img
        st.success("Imagem carregada!")

    if st.button("🗑️ Resetar Tudo"):
        st.session_state.current_image = None
        st.rerun()

# Área Principal
col1, col2 = st.columns(2)

with col1:
    st.subheader("🖼️ Imagem Atual")
    if st.session_state.current_image:
        st.image(st.session_state.current_image, use_container_width=True)
    else:
        st.info("Aguardando upload...")

with col2:
    st.subheader("🤖 Comando de Evolução")
    instrucao = st.text_area("O que a IA deve fazer na imagem?", 
                            placeholder="Ex: Adicione uma pessoa de terno ao fundo e melhore a nitidez.")

    if st.button("✨ Evoluir Imagem"):
        if st.session_state.current_image and instrucao:
            with st.spinner("A IA está trabalhando..."):
                try:
                    # Prepara a imagem para a API (Deve ser PNG < 4MB)
                    byte_io = io.BytesIO()
                    # Redimensiona para o padrão da API (1024x1024)
                    temp_img = st.session_state.current_image.resize((1024, 1024))
                    temp_img.save(byte_io, format='PNG')
                    image_bytes = byte_io.getvalue()

                    # Chama a Edição da OpenAI
                    response = client.images.edit(
                        image=image_bytes,
                        prompt=instrucao,
                        n=1,
                        size="1024x1024"
                    )

                    # Atualiza a imagem para a próxima rodada
                    new_url = response.data[0].url
                    new_img_data = requests.get(new_url).content
                    st.session_state.current_image = Image.open(io.BytesIO(new_img_data)).convert("RGBA")
                    
                    st.success("Pronto! Você pode pedir mais mudanças agora.")
                    st.rerun()

                except Exception as e:
                    st.error(f"Erro na IA: {e}")
        else:
            st.warning("Envie a foto e escreva o comando.")
