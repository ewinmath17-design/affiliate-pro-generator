import streamlit as st
import google.generativeai as genai

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Affiliate Pro Generator", page_icon="🔥", layout="wide")

# --- UI HEADER LANDING PAGE ---
st.markdown("<h1 style='text-align: center; color: #ff4b4b; font-weight: 800;'>🔥 Affiliate Pro Generator V.4.7</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; margin-bottom: 30px;'>Ubah Produk Apa Saja Jadi Puluhan Video Konten FYP dalam 5 Menit.</h4>", unsafe_allow_html=True)
st.divider()

# --- SIDEBAR: KONFIGURASI API (PATH 2) ---
with st.sidebar:
    st.header("⚙️ System Config")
    st.markdown("Masukkan akses API Anda untuk mengaktifkan *Auto-UGC Storyboard Engine*.")
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

# --- TOMBOL EKSEKUSI ---
st.divider()
submit_button = st.button("🚀 Generate UGC Storyboard Sekarang!", use_container_width=True, type="primary")

# --- BACKEND LOGIC & AI PROMPT INJECTION ---
if submit_button:
    if not api_key:
        st.error("⚠️ Akses ditolak: Silakan masukkan Gemini API Key di menu sebelah kiri terlebih dahulu.")
    elif product_name and target_audience and pain_point and hope:
        with st.spinner("🧠 Mesin AI sedang meracik hook psikologis dan alur cerita brutal..."):
            try:
                # Inisiasi Path 2
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                # System Prompt Rahasia (Formula Konversi)
                prompt = f"""
                Anda adalah seorang Copywriter Direct Response dan Video Marketer kelas dunia. 
                Tugas Anda adalah membuat 2 opsi Storyboard Video UGC (User Generated Content) berdurasi 15-30 detik untuk produk: '{product_name}'.
                
                Gunakan framework "Identity and Hope" dengan bumbu pemicu emosi "Fear" (Ketakutan tertinggal/rugi) dan "Greed" (Keinginan untung cepat/mudah) untuk mendominasi Blue Ocean market.
                
                Data Psikologi Target:
                - Identitas Audiens: {target_audience}
                - Agitasi Masalah (Fear): {pain_point}
                - Harapan Utama (Hope): {hope}
                
                Format output harus sangat rapi dan siap dieksekusi oleh kreator/affiliator:
                
                ### 🎬 Opsi 1: Angle 'Ketakutan & Solusi Cepat' (UGC Look)
                (Fokus menekan pain point audiens lalu memberikan produk sebagai satu-satunya jalan keluar)
                
                ### 🎬 Opsi 2: Angle 'Pamer Hasil & Testimoni' (Cinematic Mode)
                (Fokus pada Greed/Hope, tunjukkan hasil akhir yang sangat diidamkan audiens)
                
                Untuk setiap opsi, gunakan format breakdown per detik seperti ini:
                - **Detik 0-3 (Visual Hook):** [Aksi kamera/visual yang menghentikan scroll]
                - **Voice Over (Hook):** "[Kata-kata persuasif, gaul, natural yang langsung menusuk identitas]"
                - **Detik 3-10 (Agitasi/Review):** [Aksi visual mendukung]
                - **Voice Over:** "[Penjelasan produk dengan bahasa jualan terselubung]"
                - **Detik 10-15 (Call to Action):** [Aksi menunjuk link/keranjang]
                - **Voice Over (CTA):** "[Perintah mendesak dengan alasan urgensi tinggi]"
                """
                
                response = model.generate_content(prompt)
                
                # Menampilkan Hasil
                st.success("✅ Berhasil! Pabrik konten Anda telah memproduksi script dengan konversi tinggi.")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Terjadi kesalahan teknis pada sistem AI: {e}")
    else:
        st.warning("⚠️ Mohon lengkapi semua amunisi data produk dan psikologi audiens sebelum menekan tombol.")
