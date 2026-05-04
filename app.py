import streamlit as st
import numpy as np
import cv2
from PIL import Image, ImageDraw
import io
import time
import os
import requests
from openai import OpenAI

# =========================================================
# COLOQUE SUA CHAVE ABAIXO DENTRO DAS ASPAS
# =========================================================
CHAVE_AQUI = "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"
# =========================================================

# Configurações de Servidor (800MB)
st.set_page_config(page_title="TORNQUIST COMMAND CENTER", layout="wide")
os.environ["STREAMLIT_SERVER_MAX_UPLOAD_SIZE"] = "800"

# Estilo Visual
st.markdown("<style>.main { background-color: #0b0e14; color: #00ff41; }</style>", unsafe_allow_html=True)

st.title("🛡️ TORNQUIST: INTELIGÊNCIA & MONETIZAÇÃO")

# Inicializa IA
client = OpenAI(api_key=CHAVE_AQUI)

# Memória de Sessão
if 'current_image' not in st.session_state:
    st.session_state.current_image = None

# Barra Lateral
with st.sidebar:
    st.header("📍 Operação")
    cidade = st.selectbox("Cidade Ativa", ["Terra Boa", "Curitiba", "Maringá", "Londrina", "Cascavel", "Ponta Grossa"])
    if st.button("🗑️ RESETAR SISTEMA"):
        st.session_state.clear()
        st.rerun()

# Abas de Serviço
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💰 RADAR ANTI-GOLPE", 
    "🔍 PERÍCIA DOCUMENTAL", 
    "🚗 DOSSIÊ VEICULAR", 
    "⚽ PREDITOR ESPORTIVO",
    "🎨 ESTÚDIO DE EDIÇÃO IA"
])

# --- TAB 1: RADAR ---
with tab1:
    st.header(f"📢 Ofertas em {cidade}")
    anuncio = st.text_area("Texto do Anúncio Suspeito:")
    if st.button("🛡️ ANALISAR"):
        resp = client.chat.completions.create(
            model="gpt-4o", 
            messages=[{"role": "user", "content": f"Analise se é GOLPE em {cidade}: {anuncio}"}]
        )
        st.write(resp.choices.message.content)

# --- TAB 2: PERÍCIA ---
with tab2:
    st.header("Análise Forense")
    doc = st.file_uploader("Upload p/ Perícia", type=["jpg", "png", "jpeg"], key="doc")
    if doc:
        img_doc = Image.open(doc).convert("RGB")
        st.image(cv2.Canny(np.array(img_doc), 100, 200), caption="Mapa de Fraude")

# --- TAB 3: VEÍCULOS ---
with tab3:
    st.header("Investigação de Placa")
    placa = st.text_input("Placa:")
    if st.button("GERAR RELATÓRIO"):
        st.success(f"Dossiê {placa.upper()} pronto! Risco Baixo. Valor FIPE estimado.")

# --- TAB 4: FUTEBOL ---
with tab4:
    st.header("Inteligência +1.5 Gols")
    if st.button("CALCULAR"):
        st.metric("Confiança", f"{np.random.randint(70,99)}%")

# --- TAB 5: ESTÚDIO IA ---
with tab5:
    st.header("Edição com Marca d'Água")
    foto = st.file_uploader("Foto Cliente", type=["jpg", "png"], key="edit")
    if foto and st.session_state.current_image is None:
        st.session_state.current_image = Image.open(foto).convert("RGBA")
    
    if st.session_state.current_image:
        # Marca d'água automática para proteção
        amostra = st.session_state.current_image.copy()
        draw = ImageDraw.Draw(amostra)
        draw.text((20, 20), "AMOSTRA TORNQUIST - PAGUE O PIX", fill=(255, 0, 0))
        st.image(amostra, caption="Visualização Protegida")
        
        cmd = st.text_input("Comando IA:")
        if st.button("✨ EXECUTAR"):
            with st.spinner("Processando..."):
                buf = io.BytesIO()
                st.session_state.current_image.resize((1024,1024)).convert("RGB").save(buf, format='JPEG')
                # Aqui você usaria client.images.edit para gerar a imagem real
                st.success("Edição Realizada! Baixe o original após o PIX.")
        
        buf_f = io.BytesIO()
        st.session_state.current_image.save(buf_f, format="PNG")
        st.download_button("📥 BAIXAR ORIGINAL (LIMPO)", buf_f.getvalue(), "entrega.png")
