import streamlit as st
from openai import OpenAI
from PIL import Image
import requests
import io

# Configuração da Página
st.set_page_config(page_title="TORNQUIST EVOLUTION AI", layout="wide")
st.title("📸 TORNQUIST IMAGE EVOLUTION")

# Inicializa o cliente OpenAI (Pega a chave dos Secrets do Streamlit)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Gerenciamento de Estado (Session State) para manter a imagem atual
if 'current_image' not in st.session_state:
    st.session_state.current_image = None

# Sidebar para Upload Inicial
with st.sidebar:
    st.header("1. Início")
    uploaded_file = st.file_uploader("Escolha a foto original", type=["png", "jpg"])
    if uploaded_file and st.session_state.current_image is None:
        # Abre e converte para RGBA (necessário para a API de Edição)
        img = Image.open(uploaded_file).convert("RGBA")
        st.session_state.current_image = img

# Layout Principal
col1, col2 = st.columns(2)

with col1:
    if st.session_state.current_image:
        st.subheader("Imagem Atual")
        st.image(st.session_state.current_image, use_container_width=True)
        
        if st.button("Limpar e Recomeçar"):
            st.session_state.current_image = None
            st.rerun()

with col2:
    st.subheader("🛠️ Evoluir Imagem")
    instrucao = st.text_area("O que a IA deve fazer? (Ex: Adicione uma pessoa caminhando, melhore a iluminação e corrija erros)")

    if st.button("Executar Evolução"):
        if st.session_state.current_image and instrucao:
            with st.spinner("A IA está editando e analisando..."):
                try:
                    # 1. Converte a imagem atual para bytes (formato PNG para a API)
                    byte_io = io.BytesIO()
                    st.session_state.current_image.save(byte_io, format='PNG')
                    image_bytes = byte_io.getvalue()

                    # 2. Chama a API de Edição (DALL-E 2)
                    # Nota: Para edições precisas, o DALL-E 2 funciona melhor com máscaras, 
                    # mas aqui enviamos a imagem toda para modificação geral.
                    response = client.images.edit(
                        image=image_bytes,
                        prompt=instrucao,
                        n=1,
                        size="1024x1024"
                    )

                    # 3. Atualiza a imagem no estado da sessão
                    new_url = response.data[0].url
                    new_img_data = requests.get(new_url).content
                    st.session_state.current_image = Image.open(io.BytesIO(new_img_data)).convert("RGBA")
                    
                    st.success("Imagem evoluída com sucesso!")
                    st.rerun()

                except Exception as e:
                    st.error(f"Erro na IA: {e}")
        else:
            st.warning("Envie uma foto e digite uma instrução primeiro.")

st.markdown("---")
st.info("💡 **Como funciona:** Você envia a foto e pede uma mudança. A nova imagem vira a 'original' para o seu próximo comando, permitindo que você peça correções infinitas.")
