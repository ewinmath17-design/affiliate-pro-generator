import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Affiliate Pro Generator", page_icon="🔥", layout="wide")

# Inisialisasi Memori (Session State) agar hasil teks tidak hilang saat tombol audio ditekan
if "storyboard_result" not in st.session_state:
    st.session_state.storyboard_result = ""

# --- UI HEADER LANDING PAGE ---
st.markdown("<h1 style='text-align: center; color: #ff4b4b; font-weight: 800;'>🔥 Affiliate Pro Generator V.4.7</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; margin-bottom: 30px;'>Ubah Produk Apa Saja Jadi Puluhan Video Konten FYP dalam 5 Menit.</h4>", unsafe_allow_html=True)
st.divider()

# --- SIDEBAR: KONFIGURASI API ---
with st.sidebar:
    st.header("⚙️ System Config")
    st.markdown("Masukkan akses API Anda untuk mengaktifkan mesin.")
    api_key = st.text_input("Gemini API Key", type="password", help="Dapatkan API Key gratis di Google AI Studio")
    st.markdown("---")
    st.markdown("**Status Lisensi:**")
    st.success("✅ Personal License (Rp 99.000)")
    st.caption("Akses Seumur Hidup | 100% Web Based")

# --- INPUT FORM: STRATEGI DIRECT RESPONSE ---
col1, col2 = st.columns(2)
with col1:
    st.subheader("📦 Identitas Produk & Target")
    product_name = st.text_input("Nama Produk / Penawaran", placeholder="Contoh: E-Book Kavling Digital, Hijab Anti-Kusut...")
    target_audience = st.text_input("Target Audiens (Identity)", placeholder="Contoh: Karyawan yang lelah, Ibu muda sibuk...")
    
with col2:
    st.subheader("🎯 Psikologi Emosi Audiens")
    pain_point = st.text_area("Agitasi Masalah (Fear/Pain)", placeholder="Contoh: Takut inflasi, capek kerja gaji numpang lewat...")
    hope = st.text_input("Harapan Utama (Hope/Greed)", placeholder="Contoh: Punya aset digital yang ngalir terus tiap hari...")

# --- TOMBOL EKSEKUSI UTAMA ---
st.divider()
submit_button = st.button("🚀 Generate UGC Storyboard & Prompt Gambar!", use_container_width=True, type="primary")

# --- BACKEND LOGIC & AI PROMPT INJECTION ---
if submit_button:
    if not api_key:
        st.error("⚠️ Akses ditolak: Silakan masukkan Gemini API Key di menu sebelah kiri terlebih dahulu.")
    elif product_name and target_audience and pain_point and hope:
        with st.spinner("🧠 Mesin AI sedang meracik hook, alur cerita, dan prompt visual..."):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                # Prompt yang di-upgrade dengan instruksi Auto-Prompt B-Roll
                prompt = f"""
                Anda adalah seorang Copywriter Direct Response dan Video Marketer kelas dunia. 
                Buat 2 opsi Storyboard Video UGC (User Generated Content) berdurasi 15-30 detik untuk produk: '{product_name}'.
                
                Gunakan framework "Identity and Hope" dipadu dengan emosi "Fear" dan "Greed".
                Data Psikologi Target:
                - Audiens: {target_audience}
                - Masalah (Fear): {pain_point}
                - Harapan (Hope): {hope}
                
                Format output wajib seperti ini untuk setiap detiknya:
                - **Detik [X]-[Y] (Visual):** [Aksi kamera]
                - **🤖 Prompt AI Image (B-Roll):** "[Berikan instruksi prompt dalam bahasa Inggris yang sangat detail untuk di-copy paste ke Bing Image Creator / Midjourney. Contoh: 'Cinematic close up photography of...']"
                - **🎙️ Voice Over:** "[Kata-kata persuasif berbahasa Indonesia]"
                
                Buat Opsi 1 (Angle Ketakutan & Solusi Cepat) dan Opsi 2 (Angle Pamer Hasil/Testimoni).
                """
                
                response = model.generate_content(prompt)
                # Simpan hasil ke dalam memori
                st.session_state.storyboard_result = response.text
                
            except Exception as e:
                st.error(f"Terjadi kesalahan teknis pada sistem AI: {e}")
    else:
        st.warning("⚠️ Mohon lengkapi semua amunisi data produk dan psikologi audiens sebelum menekan tombol.")

# --- MENAMPILKAN HASIL & FITUR VOICE OVER STUDIO ---
if st.session_state.storyboard_result:
    st.success("✅ Berhasil! Pabrik konten Anda telah memproduksi script dengan konversi tinggi beserta Prompt AI Image.")
    st.markdown(st.session_state.storyboard_result)
    
    # Fitur Baru: Voice Over Studio
    st.divider()
    st.subheader("🎧 AI Voice Over Studio (Gratis)")
    st.markdown("1. *Copy* bagian teks **Voice Over** dari hasil di atas.\n2. *Paste* ke dalam kotak di bawah ini.\n3. Klik tombol untuk mengubahnya menjadi suara MP3 yang siap di-download!")
    
    vo_text = st.text_area("Tempel teks Voice Over di sini:", placeholder="Paste teks di sini...")
    
    if st.button("🎙️ Generate Suara (MP3)"):
        if vo_text:
            with st.spinner("Sedang merekam suara..."):
                try:
                    tts = gTTS(text=vo_text, lang='id')
                    audio_bytes = io.BytesIO()
                    tts.write_to_fp(audio_bytes)
                    st.audio(audio_bytes, format='audio/mp3')
                    st.success("✅ Audio berhasil dibuat! Klik titik tiga pada pemutar suara di atas untuk men-download.")
                except Exception as e:
                    st.error("Gagal membuat suara. Coba lagi beberapa saat.")
        else:
            st.warning("Teksnya masih kosong, Master. Silakan paste teksnya terlebih dahulu.")
