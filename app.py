import streamlit as st
from openai import OpenAI
from PIL import Image, ImageDraw
import requests
from io import BytesIO
from moviepy.editor import ImageClip, AudioFileClip

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Agência IA PRO", layout="centered")
st.title("🔥 Criador de Propaganda Automática")

ofertas = st.text_area("Digite produtos (ex: Cerveja R$ 3,99)")

def buscar_imagem(produto):
    url = f"https://source.unsplash.com/800x1200/?{produto}"
    r = requests.get(url)
    return Image.open(BytesIO(r.content)).convert("RGB")

def gerar_texto(produto, preco):
    prompt = f"""
    Crie anúncio extremamente chamativo estilo mercado brasileiro.

    Produto: {produto}
    Preço: {preco}
    """
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )
    return r.choices[0].message.content

def criar_banner(produto, preco):
    img = buscar_imagem(produto)
    img = img.resize((800,1200))

    overlay = Image.new("RGBA", img.size, (0,0,0,150))
    img = Image.alpha_composite(img.convert("RGBA"), overlay)

    draw = ImageDraw.Draw(img)

    draw.text((40,50), "🔥 OFERTA DO DIA", fill="white")
    draw.text((40,200), produto.upper(), fill="white")

    draw.rectangle((40,500,500,650), fill=(255,200,0))
    draw.text((60,540), preco, fill="black")

    nome = f"{produto}.png"
    img.convert("RGB").save(nome)
    return nome

def gerar_audio(texto, nome):
    audio = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=texto
    )
    with open(nome, "wb") as f:
        f.write(audio.read())

def gerar_video(img, audio, nome):
    clip = ImageClip(img).set_duration(10)
    audio_clip = AudioFileClip(audio)
    video = clip.set_audio(audio_clip)
    video.write_videofile(nome, fps=24)

if st.button("🚀 GERAR PROPAGANDA"):

    for linha in ofertas.split("\n"):
        if "R$" in linha:

            produto = linha.split("R$")[0].strip()
            preco = "R$" + linha.split("R$")[1].strip()

            texto = gerar_texto(produto, preco)
            banner = criar_banner(produto, preco)

            audio_nome = f"{produto}.mp3"
            gerar_audio(texto, audio_nome)

            video_nome = f"{produto}.mp4"
            gerar_video(banner, audio_nome, video_nome)

            st.image(banner)
            st.video(video_nome)
            st.write(texto)

    st.success("🔥 Tudo pronto!")
