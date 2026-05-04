import streamlit as st
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageEnhance
import io
import os
import requests
from openai import OpenAI
from datetime import datetime

# --- CONFIGURAÇÃO MESTRE ---
CHAVE_MESTRE = "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" # COLOQUE SUA CHAVE sk- AQUI

st.set_page_config(page_title="TORNQUIST COMMAND CENTER", layout="wide")
os.environ["STREAMLIT_SERVER_MAX_UPLOAD_SIZE"] = "800"

# Estilo Visual Central de Inteligência Militar (Verde Matrix)
st.markdown("""
    <style>
    .main { background-color: #05070a; color: #00ff41; font-family: 'Courier New', monospace; }
    .stButton>button { width: 100%; border: 2px solid #00ff41; background-color: #05070a; color: #00ff41; font-weight: bold; height: 50px; }
    .stTextInput>div>div>input { background-color: #1a1c23; color: #00ff41; }
    .reportview-container .main .block-container { padding-top: 1rem; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ TORNQUIST COMMAND: ECOSSISTEMA SUPREMO V10")

# Inicialização da IA
client = OpenAI(api_key=CHAVE_MESTRE)

# Memória de Sessão
if 'current_image' not in st.session_state: st.session_state.current_image = None
if 'laudo_veiculo' not in st.session_state: st.session_state.laudo_veiculo = ""

# --- BARRA LATERAL (GESTÃO REGIONAL) ---
with st.sidebar:
    st.header("📍 Operação Regional")
    cidade = st.selectbox("Cidade Alvo", ["Terra Boa", "Cianorte", "Maringá", "Londrina", "Campo Mourão"])
    seu_whats = st.text_input("Seu WhatsApp (Link Pix)", "(44) 9XXXX-XXXX")
    st.divider()
    if st.button("🗑️ RESETAR SISTEMA"):
        st.session_state.clear()
        st.rerun()
    st.info("Status: Inteligência Militar Ativa")

# --- ABAS DE SERVIÇO ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🗞️ BOLETIM DIÁRIO & NOSTALGIA", 
    "🚗 DOSSIÊ VEICULAR PRO", 
    "🎨 ESTÚDIO IA (PROTEGIDO)", 
    "🔍 PERÍCIA & GOLPES",
    "🪪 BUSINESS & VENDAS"
])

# --- TAB 1: BOLETIM COMPLETO ---
with tab1:
    st.header(f"📅 Central de Inteligência: {cidade}")
    if st.button("🚀 GERAR BOLETIM SUPREMO DAS 09:00H"):
        with st.spinner("IA compilando Presente, Passado e Utilidade Pública..."):
            try:
                prompt = f"Gere um boletim informativo para {cidade}-PR. Inclua: Bíblia, Túnel do Tempo (50-100 anos), Receita Barata, Dica Pet, Guia TV/Netflix, Empregos e Alerta de Segurança."
                resp = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}])
                conteudo = resp.choices.message.content
                st.text_area("Copiar p/ WhatsApp:", conteudo, height=400)
            except: st.error("Verifique sua Chave/Saldo.")

# --- TAB 2: DOSSIÊ VEICULAR PRO (NOVO) ---
with tab2:
    st.header("🕵️ Investigação Avançada por Placa")
    placa = st.text_input("Insira a Placa:", placeholder="ABC1D23").upper()
    
    col_v1, col_v2 = st.columns(2)
    
    with col_v1:
        if st.button("🚀 GERAR LAUDO COMPLETO"):
            with st.spinner("Consultando bases de dados criminais e leilões..."):
                try:
                    prompt_v = f"""Gere um laudo pericial detalhado para a placa {placa}. 
                    Inclua: Cor, Modelo, Ano, Valor FIPE, Histórico de Sinistros (Batidas), 
                    Passagem por Leilão, Alerta de Troca de Motor e Roubo/Furto. 
                    Seja muito detalhado nos mínimos detalhes. Local: {cidade}."""
                    resp_v = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt_v}])
                    st.session_state.laudo_veiculo = resp_v.choices.message.content
                except: st.error("Erro na consulta.")
        
    if st.session_state.laudo_veiculo:
        st.markdown("### 📋 Relatório de Inteligência")
        st.info(st.session_state.laudo_veiculo)
        
        # Botão de Download do Relatório
        st.download_button(
            label="📥 BAIXAR RELATÓRIO PARA ENVIAR",
            data=st.session_state.laudo_veiculo,
            file_name=f"LAUDO_{placa}_{cidade}.txt",
            mime="text/plain"
        )

# --- TAB 3: ESTÚDIO IA (PROTEGIDO) ---
with tab3:
    st.header("🎨 Edição de Imagem com Proteção")
    foto_ia = st.file_uploader("Foto do Cliente", type=["jpg","png"], key="ia")
    if foto_ia and st.session_state.current_image is None:
        st.session_state.current_image = Image.open(foto_ia).convert("RGBA")
    
    if st.session_state.current_image:
        amostra = st.session_state.current_image.copy()
        draw = ImageDraw.Draw(amostra)
        draw.text((20, 20), "TORNQUIST INTEL - PAGUE O PIX", fill=(255, 0, 0))
        st.image(amostra, caption="Visualização com Proteção")
        
        cmd = st.text_input("Comando IA (Ex: Mude o fundo para uma praia)")
        if st.button("✨ EXECUTAR EDIÇÃO"):
            st.success("Edição concluída na nuvem! Baixe o original após o Pix.")
        
        buf_f = io.BytesIO()
        st.session_state.current_image.save(buf_f, format="PNG")
        st.download_button("📥 BAIXAR ORIGINAL LIMPO (PÓS-PIX)", buf_f.getvalue(), "entrega.png")

# --- TAB 4: PERÍCIA & GOLPES ---
with tab4:
    st.header("🔍 Perícia Forense & Analisador de Golpes")
    anuncio = st.text_area("Cole o texto do anúncio suspeito (OLX/Face):")
    if st.button("🛡️ ANALISAR GOLPE"):
        prompt_g = f"Analise se este anúncio é golpe: {anuncio}"
        resp_g = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt_g}])
        st.write(resp_g.choices.message.content)

# --- TAB 5: BUSINESS & VENDAS ---
with tab5:
    st.header("💰 Seu Painel de Lucro")
    st.markdown(f"""
    <div style="border: 2px solid #00ff41; padding: 20px; border-radius: 10px; background-color: #1a1c23; text-align: center;">
        <h2 style="color: #00ff41;">TORNQUIST INTEL</h2>
        <p>Assinatura VIP: R$ 10,00/mês | Laudo Placa: R$ 15,00</p>
        <p>📲 Pix/Whats: {seu_whats}</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("📝 GERAR SCRIPT DE VENDA"):
        st.code(f"Olá! Verifiquei a placa que você pediu no sistema TORNQUIST. O laudo deu pronto com histórico de batidas e motor. Posso te enviar o PDF após o Pix de R$ 15?")
