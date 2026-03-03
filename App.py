import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io
import urllib.parse

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Affiliate Pro Generator", page_icon="🔥", layout="wide")

# Inisialisasi Memori
if "storyboard_result" not in st.session_state:
    st.session_state.storyboard_result = ""

# --- UI HEADER ---
st.markdown("<h1 style='text-align: center; color: #ff4b4b; font-weight: 800;'>🔥 Affiliate Pro Generator V.4.7</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; margin-bottom: 30px;'>Ubah Produk Apa Saja Jadi Puluhan Video Konten FYP dalam 5 Menit.</h4>", unsafe_allow_html=True)
st.divider()

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ System Config")
    api_key = st.text_input("Gemini API Key", type="password", help="Dapatkan API Key gratis di Google AI Studio")
    st.markdown("---")
    st.success("✅ Personal License (Rp 99.000)")
    st.caption("Akses Seumur Hidup | 100% Web Based")

# --- INPUT FORM ---
col1, col2 = st.columns(2)
with col1:
    st.subheader("📦 Identitas Produk & Target")
    product_name = st.text_input("Nama Produk / Penawaran", placeholder="Contoh: Hijab Anti-Kusut...")
    target_audience = st.text_input("Target Audiens (Identity)", placeholder="Contoh: Ibu muda sibuk...")
    
with col2:
    st.subheader("🎯 Psikologi Emosi")
    pain_point = st.text_area("Agitasi Masalah (Fear/Pain)", placeholder="Contoh: Sering telat karena ribet...")
    hope = st.text_input("Harapan Utama (Hope/Greed)", placeholder="Contoh: Tampil rapi dalam 5 detik...")

# --- TOMBOL GENERATE UTAMA ---
st.divider()
submit_button = st.button("🚀 Generate UGC Storyboard!", use_container_width=True, type="primary")

# --- BACKEND LOGIC ---
if submit_button:
    if not api_key:
        st.error("⚠️ Masukkan Gemini API Key di menu sebelah kiri terlebih dahulu.")
    elif product_name and target_audience and pain_point and hope:
        with st.spinner("🧠 Meracik hook, alur cerita, dan prompt visual..."):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-2.5-flash')
                prompt = f"""
                Anda adalah Copywriter Direct Response kelas dunia. 
                Buat 2 opsi Storyboard Video UGC (15-30 detik) untuk produk: '{product_name}'.
                
                Gunakan framework "Identity and Hope" dipadu "Fear" dan "Greed".
                Target: {target_audience} | Masalah: {pain_point} | Harapan: {hope}
                
                Format setiap detik wajib seperti ini:
                - **Detik [X]-[Y] (Visual):** [Aksi visual]
                - **🎨 Prompt AI Image:** "[Instruksi gambar bahasa Inggris detail. Contoh: Cinematic close up of...]"
                - **🎙️ Voice Over:** "[Kata-kata persuasif bahasa Indonesia]"
                """
                response = model.generate_content(prompt)
                st.session_state.storyboard_result = response.text
            except Exception as e:
                st.error(f"Error sistem: {e}")
    else:
        st.warning("⚠️ Lengkapi data produk dan psikologi dulu.")

# --- MENAMPILKAN HASIL & STUDIO EKSEKUSI ---
if st.session_state.storyboard_result:
    st.success("✅ Script dan Prompt berhasil diproduksi!")
    st.markdown(st.session_state.storyboard_result)
    
    st.divider()
    st.markdown("<h2 style='text-align: center;'>🛠️ STUDIO EKSEKUSI KONTEN</h2>", unsafe_allow_html=True)
    
    col_audio, col_image = st.columns(2)
    
    # STUDIO 1: VOICE OVER
    with col_audio:
        st.subheader("🎧 1. AI Voice Studio")
        st.caption("Paste teks Voice Over ke sini untuk jadi suara MP3.")
        vo_text = st.text_area("Teks Voice Over:", placeholder="Paste teks di sini...", height=150)
        
        if st.button("🎙️ Generate Suara"):
            if vo_text:
                with st.spinner("Merekam suara..."):
                    try:
                        tts = gTTS(text=vo_text, lang='id')
                        audio_bytes = io.BytesIO()
                        tts.write_to_fp(audio_bytes)
                        st.audio(audio_bytes, format='audio/mp3')
                        st.success("✅ Berhasil! Klik titik tiga pada pemutar untuk Download.")
                    except Exception:
                        st.error("Gagal membuat suara. Coba lagi.")
            else:
                st.warning("Teksnya kosong.")

    # STUDIO 2: IMAGE GENERATOR
    with col_image:
        st.subheader("🎨 2. AI Image Studio")
        st.caption("Paste teks Prompt AI Image (Bahasa Inggris) ke sini.")
        img_prompt = st.text_area("Prompt Gambar (Inggris):", placeholder="Paste prompt di sini...", height=150)
        
        if st.button("🖼️ Generate Gambar"):
            if img_prompt:
                with st.spinner("Melukis gambar visual..."):
                    # Encode URL agar aman, format 9:16 (Vertikal/Reels)
                    safe_prompt = urllib.parse.quote(img_prompt)
                    image_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1080&height=1920&nologo=true"
                    st.image(image_url, caption="Hasil Generate (Ukuran TikTok/Reels)")
                    st.info("💡 Tekan tahan (long press) pada gambar di atas lalu pilih 'Simpan Gambar' / 'Download Image' ke HP Anda.")
            else:
                st.warning("Prompt gambarnya kosong.")
