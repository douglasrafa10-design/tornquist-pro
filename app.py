import streamlit as st
import feedparser
from openai import OpenAI
from supabase import create_client
import datetime

# --- CONFIGURAÇÃO DE ACESSO ---
# As chaves ficam escondidas nos 'Secrets' do Streamlit
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
except:
    st.error("Configure as chaves OPENAI_API_KEY, SUPABASE_URL e SUPABASE_KEY nos Secrets!")

# --- FONTES DE ALIMENTAÇÃO AUTOMÁTICA (Rádios e Portais) ---
RSS_FEEDS = [
    "https://globo.com", # Notícias Gerais
    "https://bbc.com", # Global
    "https://jovempan.com.br" # Rádio/Notícias Rápidas
]

def coletar_noticias_mundo():
    """Lê as notícias mais recentes das fontes automáticas"""
    dados_coletados = ""
    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries[:3]: # Pega as 3 principais de cada fonte
            dados_coletados += f"- {entry.title}: {entry.description}\n"
    return dados_coletados

def gerar_caderno_imperio(noticias_web):
    prompt = f"""
    Você é a Inteligência Central do Império Regional. 
    DADOS CAPTADOS DA WEB/RÁDIOS AGORA:
    {noticias_web}

    SUA MISSÃO: Criar o 'Caderno Matinal' de hoje.
    REGRAS:
    1. Una as notícias globais com o bem-estar regional.
    2. Crie uma 'História Programada' baseada na evolução (DNA).
    3. Defina a Frequência Vibracional do dia (400Hz a 1000Hz).
    4. Estilo: Profissional, Imperial e Motivador.
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "Você é o Editor do Império."},
                  {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# --- INTERFACE ---
st.set_page_config(page_title="IMPÉRIO IA - SISTEMA ATIVO", layout="wide")
st.title("🏙️ IMPÉRIO IA: CADERNO MATINAL AUTOMÁTICO")

if st.sidebar.button("🛰️ Sincronizar com Rádios e Web"):
    with st.spinner("IA Escaneando o Planeta..."):
        noticias_atuais = coletar_noticias_mundo()
        caderno_final = gerar_caderno_imperio(noticias_atuais)
        
        st.markdown("---")
        st.markdown(caderno_final)
        
        # Salva no Banco de Dados (Memória do Império)
        supabase.table("historico_caderno").insert({
            "conteudo": caderno_final,
            "data": str(datetime.date.today())
        }).execute()
        st.success("Caderno gerado e arquivado com sucesso!")

# Exibir Histórico (O que o sistema já aprendeu)
if st.sidebar.checkbox("📚 Ver Memória do Império"):
    historico = supabase.table("historico_caderno").select("*").order("created_at", desc=True).execute()
    for item in historico.data:
        st.write(f"📅 **{item['data']}**: {item['conteudo'][:200]}...")
