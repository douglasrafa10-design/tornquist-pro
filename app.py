import streamlit as st
from openai import OpenAI
from PIL import Image, ImageDraw
import requests
from io import BytesIO
from moviepy.editor import ImageClip, AudioFileClip, vfx

# 🔥 CORREÇÃO MOVIEPY + PILLOW
if not hasattr(Image, "ANTIALIAS"):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

# --- CONFIG ---
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Agência IA PRO+", layout="centered")
st.title("🔥 Agência IA - Vídeo Profissional")

ofertas = st.text_area("Digite produtos (ex: Cerveja R$ 3,99)")

# --- BUSCAR IMAGEM ---
def buscar_imagem():
    try:
        url = "https://picsum.photos/800/1200"
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return Image.open(BytesIO(r.content)).convert("RGB")
    except:
        pass

    return Image.new("RGB", (800,1200), (20,20,20))

# --- TEXTO IA ---
def gerar_texto(produto, preco):
    prompt = f"""
    Crie anúncio curto estilo locutor brasileiro.
    Produto: {produto}
    Preço: {preco}
    """
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )
    return r.choices[0].message.content

# --- BANNER ---
def criar_banner(produto, preco):
    img = buscar_imagem().resize((800,1200))

    overlay = Image.new("RGBA", img.size, (0,0,0,140))
    img = Image.alpha_composite(img.convert("RGBA"), overlay)

    draw = ImageDraw.Draw(img)

    draw.text((50,50), "🔥 OFERTA DO DIA", fill="white")
    draw.text((50,350), produto.upper(), fill="white")

    draw.rectangle((50,650,500,800), fill=(255,200,0))
    draw.text((70,700), preco, fill="black")

    nome = f"{produto}.png"
    img.convert("RGB").save(nome)
    return nome

# --- AUDIO ---
def gerar_audio(texto, nome):
    audio = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=texto
    )
    with open(nome, "wb") as f:
        f.write(audio.read())

# --- VIDEO ANIMADO (ESTÁVEL) ---
def gerar_video_animado(img_path, audio_path, output):

    clip = ImageClip(img_path).set_duration(10)

    # zoom leve
    clip = clip.fx(vfx.resize, lambda t: 1 + 0.03*t)

    # fade suave
    clip = clip.fadein(1).fadeout(1)

    audio = AudioFileClip(audio_path)
    video = clip.set_audio(audio)

    video.write_videofile(output, fps=24)

# --- EXEC ---
if st.button("🚀 GERAR PROPAGANDA PRO"):

    for linha in ofertas.split("\n"):
        if "R$" in linha:

            produto = linha.split("R$")[0].strip()
            preco = "R$" + linha.split("R$")[1].strip()

            st.markdown("---")
            st.subheader(f"📦 {produto}")

            texto = gerar_texto(produto, preco)
            banner = criar_banner(produto, preco)

            audio_nome = f"{produto}.mp3"
            gerar_audio(texto, audio_nome)

            video_nome = f"{produto}_animado.mp4"
            gerar_video_animado(banner, audio_nome, video_nome)

            # MOSTRAR
            st.image(banner)
            st.video(video_nome)
            st.text_area("📲 Texto pronto", texto)

            # DOWNLOADS
            with open(banner, "rb") as f:
                st.download_button("📥 Baixar Banner", f, file_name=banner)

            with open(audio_nome, "rb") as f:
                st.download_button("🎧 Baixar Áudio", f, file_name=audio_nome)

            with open(video_nome, "rb") as f:
                st.download_button("🎬 Baixar Vídeo Animado", f, file_name=video_nome)

    st.success("🔥 Propaganda profissional pronta!")
