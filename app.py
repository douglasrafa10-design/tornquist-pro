import streamlit as st
import numpy as np
from PIL import Image, ImageEnhance
import cv2
import tempfile
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import requests
import io

st.set_page_config(page_title="TORNQUIST PRO MAX", layout="wide")

st.title("TORNQUIST PRO MAX AI")

st.markdown("### Sistema Pericial de Análise e Geração com IA")

# ================= DADOS =================
st.header("📊 Dados")
entrada = st.text_input("Valores (ex: 10,20,100)")

score_dados = 0

if st.button("Analisar Dados"):
    try:
        v = np.array([float(x) for x in entrada.split(",")])
        mu = np.mean(v)
        score_dados = np.mean(np.abs(v-mu))/(mu+1e-9)

        st.write("Média:", round(mu,2))
        st.write("Score:", round(score_dados,3))
    except:
        st.error("Erro nos dados")

# ================= IMAGEM =================
st.header("📸 Imagem")

imagem = st.file_uploader("Enviar imagem", type=["jpg","png"])

score_img = 0
img_final = None

if imagem:
    img = Image.open(imagem)
    st.image(img, caption="Original")

    img_np = np.array(img)

    for i in range(3):  # evolução iterativa
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.5)
        img_np = np.array(img)

    edges = cv2.Canny(img_np,100,200)
    score_img = np.mean(edges)/255

    st.image(img, caption="Imagem evoluída")
    st.image(edges, caption="Mapa incoerência")

    img_final = img

# ================= VIDEO =================
st.header("🎥 Vídeo")

video = st.file_uploader("Enviar vídeo", type=["mp4"])

score_vid = 0

if video:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(video.read())

    cap = cv2.VideoCapture(tfile.name)
    prev = None
    diffs = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if prev is not None:
            diffs.append(np.mean(np.abs(gray-prev)))

        prev = gray

    cap.release()

    if diffs:
        score_vid = max(diffs)/255
        st.write("Frame crítico detectado")

# ================= IA GERAR IMAGEM =================
st.header("🤖 Gerar Imagem com IA")

prompt = st.text_input("Descreva imagem (ex: carro futurista vermelho)")

if st.button("Gerar Imagem IA"):
    try:
        # Pega a chave das configurações do Streamlit (Secrets)
        api_key = st.secrets["OPENAI_API_KEY"]
        response = requests.post(
            "https://openai.com",
            headers={"Authorization": f"Bearer {api_key}"},
            json={"prompt": prompt, "size": "512x512"}
        )
        data = response.json()
        url = data['data'][0]['url']
        st.image(url)
    except:
        st.error("Erro na geração. Verifique a API Key nos Secrets do Streamlit.")

# ================= SCORE FINAL =================
score_total = (score_dados + score_img + score_vid)/3

st.header("📊 Resultado Final")

st.write("Score:", round(score_total,3))

resultado = "NORMAL"
if score_total > 0.6:
    resultado = "ALTO RISCO"
    st.error(resultado)
elif score_total > 0.3:
    resultado = "SUSPEITO"
    st.warning(resultado)
else:
    st.success(resultado)

# ================= RELATÓRIO PDF =================
st.header("📄 Gerar Relatório")

if st.button("Gerar PDF"):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    texto = f"""
    RELATÓRIO TÉCNICO TORNQUIST<br/><br/>
    Score Dados: {round(score_dados,3)}<br/>
    Score Imagem: {round(score_img,3)}<br/>
    Score Vídeo: {round(score_vid,3)}<br/><br/>
    <b>Score Final: {round(score_total,3)}</b><br/>
    <b>Classificação: {resultado}</b><br/><br/>
    Este relatório indica padrões fora do normal. Não constitui prova definitiva de fraude.
    """

    story = [Paragraph(texto, styles["Normal"])]
    doc.build(story)

    st.download_button(
        label="📥 Baixar Relatório PDF",
        data=buffer.getvalue(),
        file_name="relatorio_tornquist.pdf",
        mime="application/pdf"
    )
