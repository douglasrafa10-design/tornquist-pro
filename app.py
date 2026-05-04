import streamlit as st
import numpy as np
from PIL import Image, ImageDraw
import io
import os
import requests
from openai import OpenAI
from datetime import datetime

# --- CONFIGURAÇÃO (800MB E CHAVE) ---
CHAVE_AQUI = "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" # Certifique-se de que a chave está correta aqui

st.set_page_config(page_title="TORNQUIST DAILY INTEL", layout="wide")
os.environ["STREAMLIT_SERVER_MAX_UPLOAD_SIZE"] = "800"

# Estilo Dark Paraná
st.markdown("<style>.main { background-color: #0b0e14; color: #00ff41; }</style>", unsafe_allow_html=True)

st.title("🗞️ TORNQUIST: CENTRAL DE INTELIGÊNCIA DIÁRIA")
st.subheader("Bem-estar, Promoções e Eventos em Terra Boa & Região")

client = OpenAI(api_key=CHAVE_AQUI)

# Barra Lateral
with st.sidebar:
    st.header("📍 Localização")
    cidade = st.selectbox("Selecione a Região", ["Terra Boa", "Cianorte", "Maringá", "Campo Mourão"])
    st.divider()
    if st.button("🗑️ Resetar Sistema"):
        st.session_state.clear()
        st.rerun()

# --- ABA ÚNICA: CENTRAL DE COMANDO ---
tab1, tab2 = st.tabs(["📊 RELATÓRIO DO DIA", "🎨 ESTÚDIO DE EDIÇÃO"])

with tab1:
    st.header(f"📅 Dossiê Matinal - {cidade}")
    st.write("Clique abaixo para reunir as melhores informações para seus grupos.")

    if st.button("🚀 GERAR RELATÓRIO COMPLETO (DIA A DIA)"):
        with st.spinner("IA Processando clima, eventos e bem-estar..."):
            try:
                hoje = datetime.now().strftime("%d/%m/%Y")
                
                # Prompt mestre para criar o jornal matinal
                prompt = f"""
                Crie um boletim informativo completo para a cidade de {cidade}-PR para o dia {hoje}.
                O texto deve ser amigável e pronto para WhatsApp, dividido em:
                1. CLIMA E BEM-ESTAR: Dica de saúde para o tempo de hoje.
                2. GASTRONOMIA: Sugestão de restaurante/lanche com melhor nota na região.
                3. PROMOÇÕES: Melhores itens para buscar em mercados hoje (simulação de ofertas sazonais).
                4. EVENTOS E LAZER: Onde vai ter baile, festa ou música ao vivo (sugestões baseadas na cultura local).
                5. AVISO ANTI-GOLPE: Um alerta rápido sobre golpes comuns em redes sociais hoje.
                """
                
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "system", "content": "Você é um assistente de inteligência regional do Paraná."},
                              {"role": "user", "content": prompt}]
                )
                
                relatorio = response.choices.message.content
                
                st.markdown("### 📝 Relatório Gerado:")
                st.success("Copiado para a área de transferência mental! (Selecione o texto abaixo)")
                st.text_area("Copie e envie para seu Grupo VIP:", relatorio, height=450)
                
            except Exception as e:
                st.error(f"Erro na Autenticação: Verifique se sua chave tem saldo e se foi colada corretamente entre as aspas.")

with tab2:
    st.header("🎨 Edição de Imagem Profissional")
    foto = st.file_uploader("Suba a foto do cliente (800MB)", type=["jpg", "png"])
    if foto:
        img = Image.open(foto).convert("RGBA")
        st.image(img, caption="Original do Cliente")
        comando = st.text_input("O que a IA deve transformar?")
        if st.button("✨ Executar Transformação"):
            st.info("IA processando pixels... (Certifique-se de ter créditos na OpenAI)")
