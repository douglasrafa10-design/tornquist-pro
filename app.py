import streamlit as st
from PIL import Image, ImageDraw, ImageFont

st.set_page_config(page_title="Banner Profissional", layout="centered")

st.title("🔥 Criador de Banner Nível Mercado")

ofertas = st.text_area("Digite produtos (ex: Cerveja R$ 3,99)")

# --- FUNÇÃO PRINCIPAL ---
def criar_banner(lista):

    largura, altura = 900, 1200
    img = Image.new("RGB", (largura, altura), (8,8,8))
    draw = ImageDraw.Draw(img)

    # ===== CARREGAR FONTE =====
    try:
        titulo_font = ImageFont.truetype("anton.ttf", 80)
        produto_font = ImageFont.truetype("anton.ttf", 45)
        preco_font = ImageFont.truetype("anton.ttf", 65)
        rodape_font = ImageFont.truetype("anton.ttf", 40)
    except:
        titulo_font = produto_font = preco_font = rodape_font = ImageFont.load_default()

    # ===== TÍTULO =====
    draw.text((100, 60), "OFERTAS DO DIA", font=titulo_font, fill=(255,255,255))

    draw.rectangle((100, 150, 800, 170), fill=(255,180,0))

    y = 220

    for produto, preco in lista:

        # fundo com sombra
        draw.rectangle((70, y+10, 850, y+150), fill=(15,15,15))
        draw.rectangle((60, y, 840, y+140), fill=(30,30,30))

        # produto
        draw.text((90, y+40), produto.upper(), font=produto_font, fill=(255,255,255))

        # caixa preço
        draw.rectangle((520, y+20, 820, y+120), fill=(255,180,0))

        # preço grande
        draw.text((540, y+35), preco, font=preco_font, fill=(0,0,0))

        y += 170

    # rodapé
    draw.text((200, 1050), "CORRE QUE ACABA HOJE!", font=rodape_font, fill=(255,255,255))

    nome = "banner_profissional.png"
    img.save(nome)

    return nome

# --- EXEC ---
if st.button("🚀 GERAR BANNER TOP"):

    lista = []

    for linha in ofertas.split("\n"):
        if "R$" in linha:
            produto = linha.split("R$")[0].strip()
            preco = "R$" + linha.split("R$")[1].strip()
            lista.append((produto, preco))

    if lista:

        banner = criar_banner(lista)

        st.image(banner)

        with open(banner, "rb") as f:
            st.download_button("📥 Baixar Banner", f, file_name="banner.png")

        st.success("🔥 Banner nível profissional pronto!")

    else:
        st.warning("Digite corretamente (Produto R$ preço)")
