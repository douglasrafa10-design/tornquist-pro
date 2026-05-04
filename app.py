import streamlit as st
import numpy as np
from PIL import Image
import cv2
import tempfile

st.set_page_config(page_title="TORNQUIST PRO MAX", layout="wide")

st.title("TORNQUIST PRO MAX AI")

# ABAS
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Dados",
    "📸 Imagem",
    "🎥 Vídeo",
    "📄 Documento",
    "🚗 Veículo",
    "📑 Relatório"
])

# ================= DADOS =================
with tab1:
    entrada = st.text_input("Valores (ex: 10,20,100)")
    resultado_dados = None

    if st.button("Analisar Dados"):
        try:
            v = np.array([float(x) for x in entrada.split(",")])
            mu = np.mean(v)
            D = np.mean(np.abs(v-mu))/(mu+1e-9)

            st.write("Média:", round(mu,2))
            st.write("Desvio:", round(D,3))

            resultado_dados = D

            if D > 0.6:
                st.error("ALTO RISCO")
            elif D > 0.3:
                st.warning("SUSPEITO")
            else:
                st.success("NORMAL")
        except:
            st.error("Erro nos dados")

# ================= IMAGEM =================
with tab2:
    imagem = st.file_uploader("Enviar imagem", type=["jpg","png"])
    resultado_img = None

    if imagem:
        img = Image.open(imagem)
        img_np = np.array(img)

        edges = cv2.Canny(img_np,100,200)
        I = np.mean(edges)/255

        st.image(edges, caption="Mapa de incoerência")
        st.write("Score imagem:", round(I,3))

        resultado_img = I

# ================= VIDEO =================
with tab3:
    video = st.file_uploader("Enviar vídeo", type=["mp4"])
    resultado_vid = None

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
                diff = np.mean(np.abs(gray-prev))
                diffs.append(diff)

            prev = gray

        cap.release()

        if diffs:
            V = max(diffs)/255
            st.write("Variação máxima:", round(V,3))
            resultado_vid = V

# ================= DOCUMENTO =================
with tab4:
    doc = st.file_uploader("Enviar documento", type=["jpg","png","pdf"])
    if doc:
        st.write("Documento recebido")
        st.warning("Análise básica: verificar inconsistência visual/manual")

# ================= VEÍCULO =================
with tab5:
    placa = st.text_input("Placa do veículo")
    valor = st.text_input("Valor anunciado")

    if st.button("Analisar Veículo"):
        st.write("Placa:", placa)
        st.write("Valor:", valor)
        st.warning("Comparar valor com média de mercado")

# ================= RELATÓRIO =================
with tab6:
    st.subheader("Relatório Técnico")

    st.write("""
    Este sistema realiza análise de padrões com base em:

    - Coerência estatística de dados
    - Estrutura visual de imagem
    - Variação de frames em vídeo

    RESULTADO:
    - NORMAL: padrão esperado
    - SUSPEITO: variação incomum
    - ALTO RISCO: forte incoerência detectada

    OBS: Este sistema não afirma fraude, apenas indica anomalias.
    """)
