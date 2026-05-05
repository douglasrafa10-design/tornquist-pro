import streamlit as st
from PIL import Image, ImageDraw

st.set_page_config(page_title="Agência IA Premium", layout="centered")

st.title("🎨 Criador de Banner Profissional")

ofertas = st.text_area("Digite produtos (ex: Cerveja R$ 3,99)")

# --- BANNER PREMIUM ---
def criar_banner_premium(lista_produtos):

    largura, altura = 900, 1200
    img = Image.new("RGB", (largura, altura))
    draw = ImageDraw.Draw(img)

    # fundo gradiente
    for y in range(altura):
        r = int(10 + (y/altura)*40)
        g = int(10 + (y/altura)*40)
        b = int(10 + (y/altura)*40)
        draw.line([(0,y),(largura,y)], fill=(r,g,b))

    # título
    draw.text((200, 80), "🔥 OFERTAS IMPERDÍVEIS", fill=(255,255,255))

    # linha destaque
    draw.rectangle((150, 150, 750, 165), fill=(255,200,0))

    y = 220

    for produto, preco in lista_produtos:

        # sombra
        draw.rectangle((95, y+5, 825, y+105), fill=(10,10,10))

        # caixa principal
        draw.rectangle((90, y, 820, y+100), fill=(30,30,30))

        # produto
        draw.text((120, y+30), produto.upper(), fill=(255,255,255))

        # caixa preço
        draw.rectangle((600, y+15, 800, y+85), fill=(255,200,0))

        # preço
        draw.text((620, y+35), preco, fill=(0,0,0))

        y += 120

    # rodapé
    draw.text((200, 1050), "⚡ APROVEITE HOJE MESMO!", fill=(255,255,255))

    nome = "banner_premium.png"
    img.save(nome)

    return nome

# --- EXEC ---
if st.button("🚀 GERAR BANNER PREMIUM"):

    lista = []

    for linha in ofertas.split("\n"):
        if "R$" in linha:
            produto = linha.split("R$")[0].strip()
            preco = "R$" + linha.split("R$")[1].strip()
            lista.append((produto, preco))

    if lista:

        banner = criar_banner_premium(lista)

        st.image(banner)

        with open(banner, "rb") as f:
            st.download_button("📥 Baixar Banner", f, file_name="banner.png")

        st.success("🔥 Banner profissional pronto!")

    else:
        st.warning("Digite produtos no formato correto")
