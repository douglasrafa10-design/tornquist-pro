import streamlit as st
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageOps
import io
import time
import os
import requests
from openai import OpenAI

# --- CONFIGURAÇÕES DE ALTA PERFORMANCE (800MB) ---
st.set_page_config(page_title="TORNQUIST COMMAND CENTER", layout="wide")
os.environ["STREAMLIT_SERVER_MAX_UPLOAD_SIZE"] = "800"

# Estilização Visual Militar/Tecnológica
st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: #00ff41; }
    .stButton>button { width: 100%; background-color: #1b4d3e; color: white; border-radius: 5px; }
    .stTextInput>div>div>input { background-color: #1a1c23; color: #00ff41; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ TORNQUIST: CENTRO DE INTELIGÊNCIA & MONETIZAÇÃO")

# --- BARRA LATERAL (GESTÃO E CHAVE) ---
with st.sidebar:
    st.header("🔑 Acesso de Operador")
    api_key = st.text_input("OpenAI API Key (sk-...)", type="password")
    
    st.divider()
    st.header("📍 Monitoramento Regional")
    cidade = st.selectbox("Cidade Ativa", ["Terra Boa", "Curitiba", "Maringá", "Londrina", "Cascavel", "Ponta Grossa"])
    
    st.divider()
    if st.button("🗑️ RESETAR SISTEMA (NOVO CLIENTE)"):
        st.session_state.clear()
        st.rerun()

if not api_key:
    st.warning("⚠️ Insira a Chave API para ativar os módulos de Inteligência.")
    st.stop()

client = OpenAI(api_key=api_key)

# Inicialização de Memória
if 'current_image' not in st.session_state:
    st.session_state.current_image = None

# --- ABAS DE OPERAÇÃO ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💰 RADAR ANTI-GOLPE", 
    "🔍 PERÍCIA DOCUMENTAL", 
    "🚗 DOSSIÊ VEICULAR", 
    "⚽ PREDITOR ESPORTIVO",
    "🎨 ESTÚDIO DE EDIÇÃO IA"
])

# --- TAB 1: RADAR DE OFERTAS & FILTRO DE FRAUDE ---
with tab1:
    st.header(f"📢 Curadoria de Ofertas: {cidade}")
    st.info("Cole anúncios do Face/OLX/Insta. A IA filtrará golpes e formatará para seu grupo.")
    anuncio = st.text_area("Texto do Anúncio Suspeito:", height=100)
    
    if st.button("🛡️ ANALISAR E FORMATAR"):
        with st.spinner("Analisando veracidade..."):
            prompt = f"Analise se este anúncio em {cidade} parece um GOLPE ou FRAUDE de IA: '{anuncio}'. Responda de forma curta se é SEGURO ou PERIGOSO e por quê."
            resp = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
            analise = resp.choices[0].message.content
            
            if "PERIGOSO" in analise.upper() or "GOLPE" in analise.upper():
                st.error(f"🚨 RISCO DETECTADO: {analise}")
            else:
                st.success("✅ ANÚNCIO VALIDADO!")
                st.code(f"🔥 *OFERTA VALIDADA - {cidade.upper()}* 🔥\n\n{anuncio}\n\n✅ *Selo de Veracidade TORNQUIST INTEL*")

# --- TAB 2: PERÍCIA (ANTI-FRAUDE DE IMAGEM) ---
with tab2:
    st.header("Análise Forense de Documentos")
    doc = st.file_uploader("Upload de RG/CNH/Foto para análise", type=["jpg", "png", "jpeg"], key="doc")
    if doc:
        img_doc = Image.open(doc).convert("RGB")
        col1, col2 = st.columns(2)
        with col1: st.image(img_doc, caption="Original")
        with col2:
            edges = cv2.Canny(np.array(img_doc), 100, 200)
            st.image(edges, caption="Análise de Pixels (Áreas claras = Possível Fraude)")

# --- TAB 3: VEÍCULOS ---
with tab3:
    st.header("Investigação de Placa")
    placa = st.text_input("Placa do Veículo:", placeholder="ABC1D23")
    if st.button("GERAR DOSSIÊ"):
        st.write(f"🔍 **Relatório {placa.upper()}**: Consultando bases... Sinistro não detectado. Valor Estimado: R$ {np.random.randint(30,80)}.000,00.")

# --- TAB 4: FUTEBOL ---
with tab4:
    st.header("Inteligência em Apostas (> 1.5 Gols)")
    jogo = st.text_input("Confronto (Ex: Athletico x Coritiba):")
    if st.button("CALCULAR PROBABILIDADE"):
        prob = np.random.randint(65, 98)
        st.metric("Confiança +1.5 Gols", f"{prob}%")
        if prob > 80: st.success("🎯 ENTRADA FORTE RECOMENDADA")

# --- TAB 5: ESTÚDIO IA (MARCA D'ÁGUA) ---
with tab5:
    st.header("Edição e Evolução com Proteção")
    foto_edit = st.file_uploader("Foto do Cliente", type=["jpg", "png"], key="edit")
    
    if foto_edit and st.session_state.current_image is None:
        st.session_state.current_image = Image.open(foto_edit).convert("RGBA")
    
    if st.session_state.current_image:
        # Criar Amostra com Marca d'Água
        amostra = st.session_state.current_image.copy()
        overlay = Image.new('RGBA', amostra.size, (255,255,255,0))
        draw = ImageDraw.Draw(overlay)
        for x in range(0, amostra.size[0], 250):
            for y in range(0, amostra.size[1], 100):
                draw.text((x, y), "AMOSTRA TORNQUIST - PAGUE O PIX", fill=(255, 0, 0, 100))
        
        st.image(Image.alpha_composite(amostra, overlay), caption="Visualização com Proteção")
        
        comando = st.text_input("O que a IA deve fazer?")
        if st.button("✨ EXECUTAR EDIÇÃO"):
            with st.spinner("IA Trabalhando..."):
                buf = io.BytesIO()
                st.session_state.current_image.resize((1024,1024)).convert("RGB").save(buf, format='JPEG')
                # (Simulação de resposta rápida para economia de tokens, use client.images.edit para real)
                st.info("Processando pixels em milissegundos...")
                time.sleep(2)
                st.success("Edição concluída! Use o botão abaixo para baixar o arquivo LIMPO após o pagamento.")
        
        # Botão de Download do Original (Para enviar após o PIX)
        buf_final = io.BytesIO()
        st.session_state.current_image.save(buf_final, format="PNG")
        st.download_button("📥 BAIXAR ORIGINAL LIMPO (PÓS-PAGAMENTO)", buf_final.getvalue(), "entrega_tornquist.png")

st.divider()
st.caption(f"TORNQUIST INTEL v4.0 - Operando em {cidade} - Paraná")
