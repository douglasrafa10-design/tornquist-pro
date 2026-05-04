import streamlit as st

st.title("TORNQUIST PRO AI")

entrada = st.text_input("Digite valores (ex: 10,20,100)")

if st.button("Analisar"):
    valores = [float(x) for x in entrada.split(",")]
    media = sum(valores)/len(valores)

    maior = max(valores)

    st.write("Média:", round(media,2))
    st.write("Maior valor:", maior)

    if maior > media * 1.5:
        st.error("⚠️ Possível incoerência detectada")
    else:
        st.success("Tudo dentro do padrão")
