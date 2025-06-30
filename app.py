import streamlit as st
import pandas as pd

# --- Definisi Kelas BodyShape ---
class BodyShape:
    def __init__(self, name, description, look_for, best_dress_shape, hint, avoid):
        self.name = name
        self.description = description
        
        # Logika untuk mengubah string yang dipisahkan ';' menjadi list
        self.look_for = [item.strip() for item in look_for.split(';')] if isinstance(look_for, str) else []
        self.best_dress_shape = [item.strip() for item in best_dress_shape.split(';')] if isinstance(best_dress_shape, str) else []
        self.hint = [item.strip() for item in hint.split(';')] if isinstance(hint, str) else []
        self.avoid = [item.strip() for item in avoid.split(';')] if isinstance(avoid, str) else []
    
    def get_all_recommendations(self):
        recs = f"**Deskripsi:** {self.description}\n\n"
        recs += "**Yang Perlu Dicari:**\n" + "\n".join([f"- {item}" for item in self.look_for]) + "\n\n"
        recs += "**Bentuk Gaun Terbaik:**\n" + "\n".join([f"- {item}" for item in self.best_dress_shape]) + "\n\n"
        recs += "**Petunjuk Gaya:**\n" + "\n".join([f"- {item}" for item in self.hint]) + "\n\n"
        recs += "**Yang Perlu Dihindari:**\n" + "\n".join([f"- {item}" for item in self.avoid]) + "\n"
        return recs

# --- Memuat Data Rekomendasi Gaya dari CSV dengan Pandas ---
@st.cache_data 
def load_recommendations_data(file_path):
    try:
        df = pd.read_csv(file_path)
        
        recommendations = {}
        for index, row in df.iterrows():
            recommendations[row['name']] = BodyShape(
                name=row['name'],
                description=row['description'],
                look_for=row['look_for'], 
                best_dress_shape=row['best_dress_shape'],
                hint=row['hint'],
                avoid=row['avoid']
            )
        return recommendations
    except FileNotFoundError:
        st.error(f"File data tidak ditemukan: {file_path}. Pastikan file 'body_shape_recommendations.csv' ada di folder 'data/' proyek Anda.")
        return {}
    except Exception as e:
        st.error(f"Terjadi kesalahan saat memuat data dari CSV: {e}. Pastikan format CSV sudah benar.")
        st.warning("Periksa apakah ada masalah dengan koma di dalam teks atau pemisah titik koma.")
        return {}

# Panggil fungsi untuk memuat data saat aplikasi dimulai
RECOMMENDATIONS_DATA = load_recommendations_data("data/body_shape_recommendations.csv")

# --- Fungsi Identifikasi Bentuk Tubuh (Tidak Berubah Signifikan) ---
def identify_body_shape(bahu, dada, pinggang, pinggul):
    # ... (kode identifikasi_bentuk_tubuh Anda yang sudah ada) ...

    # Rasio dan perbedaan
    dada_pinggul_rasio = dada / pinggul if pinggul != 0 else 0
    bahu_pinggul_rasio = bahu / pinggul if pinggul != 0 else 0
    pinggang_dada_rasio = pinggang / dada if dada != 0 else 0
    pinggang_pinggul_rasio = pinggang / pinggul if pinggul != 0 else 0

    diff_dada_pinggul = abs(dada - pinggul)
    diff_bahu_pinggul = abs(bahu - pinggul)
    diff_pinggang_dada = abs(pinggang - dada)
    diff_pinggang_pinggul = abs(pinggang - pinggul)
    diff_pinggang_bahu = abs(pinggang - bahu)


    # --- Implementasi Logika dari Gambar Referensi (SESUAIKAN THRESHOLDS INI!) ---

    # HOURGLASS: Bust and hips are basically the same measurement and you have a defined waist.
    if diff_dada_pinggul <= 3 and pinggang < dada * 0.75 and pinggang < pinggul * 0.75:
        return "hourglass"

    # PEAR: Hips are larger than your bust and you have a defined waist.
    elif pinggul > dada * 1.05 and pinggul > bahu * 1.05 and pinggang < pinggul * 0.8:
        return "pear"

    # INVERTED_TRIANGLE: Bahu/dada lebih lebar dari pinggul.
    elif bahu > pinggul * 1.05 or dada > pinggul * 1.05:
        return "inverted_triangle"

    # RECTANGLE: Bust and hips are basically the same measurement. Waist is lightly smaller than the bust and hips.
    elif diff_dada_pinggul <= 5 and diff_pinggang_dada <= 5 and diff_pinggang_pinggul <= 5:
         return "rectangle"

    # APPLE: Bust is larger than the hips and the waist is well defined (berdasarkan gambar referensi)
    elif dada > pinggul * 1.05 and pinggang < dada * 0.8:
        return "apple"
    
    # OVAL: Large bust, narrow hips, and a full midsection. (berdasarkan gambar referensi)
    # Perhatikan ambang batas di sini agar tidak tumpang tindih dengan Apple.
    elif dada > pinggul * 1.1 and pinggang > pinggul * 1.05 and pinggang > dada * 0.9:
        return "oval"

    # DIAMOND: Waist is larger than the bust and hips...
    elif pinggang > dada * 1.05 and pinggang > pinggul * 1.05:
        return "diamond"

    else:
        return "unknown"


# --- Bagian Streamlit UI (Tidak Berubah dari sebelumnya) ---
st.set_page_config(
    page_title="Personal Stylist: Temukan Bentuk Tubuhmu!",
    layout="centered",
    initial_sidebar_state="auto"
)

st.title("👗 Personal Stylist: Temukan Bentuk Tubuhmu! 👗")
st.markdown("Dapatkan rekomendasi gaya pakaian yang paling cocok untuk menonjolkan keindahan alami bentuk tubuh Anda. Masukkan pengukuran Anda di bawah ini:")

# Input Pengukuran Tubuh
st.header("1. Masukkan Pengukuran Tubuh Anda (dalam cm)")

col1, col2 = st.columns(2)
with col1:
    bahu = st.number_input("Lingkar Bahu (cm)", min_value=30, max_value=150, value=90, help="Ukur di sekitar bagian terlebar bahu Anda.")
    pinggang = st.number_input("Lingkar Pinggang (cm)", min_value=40, max_value=120, value=70, help="Ukur di sekitar bagian tersempit pinggang Anda.")
with col2:
    dada = st.number_input("Lingkar Dada (cm)", min_value=60, max_value=150, value=95, help="Ukur di sekitar bagian terlebar dada Anda (di bawah ketiak).")
    pinggul = st.number_input("Lingkar Pinggul (cm)", min_value=70, max_value=160, value=100, help="Ukur di sekitar bagian terlebar pinggul Anda.")

if st.button("Identifikasi Bentuk Tubuh & Dapatkan Rekomendasi"):
    st.markdown("---")

    if bahu <= 0 or dada <= 0 or pinggang <= 0 or pinggul <= 0:
        st.error("Mohon masukkan semua pengukuran dengan nilai yang valid (lebih dari 0).")
    else:
        body_shape = identify_body_shape(bahu, dada, pinggang, pinggul)

        if body_shape != "unknown":
            display_name = body_shape.replace('_', ' ').title()
            st.success(f"🎉 Bentuk Tubuh Anda adalah: **{display_name}** 🎉")

            data_bentuk = RECOMMENDATIONS_DATA.get(body_shape)

            if data_bentuk:
                st.markdown("---")
                st.header(f"Rekomendasi Gaya untuk Bentuk Tubuh {display_name}:")

                st.subheader("💡 Deskripsi Bentuk Tubuh Anda:")
                st.write(data_bentuk.description)

                st.subheader("✅ Yang Perlu Anda Cari (Look for):")
                for item in data_bentuk.look_for:
                    st.write(f"- {item}")

                st.subheader("👗 Bentuk Gaun Terbaik (Best Dress Shape):")
                for item in data_bentuk.best_dress_shape:
                    st.write(f"- {item}")

                st.subheader("🎯 Petunjuk Gaya (Hint):")
                for item in data_bentuk.hint:
                    st.write(f"- {item}")

                st.subheader("🚫 Yang Perlu Dihindari (Avoid):")
                for item in data_bentuk.avoid:
                    st.write(f"- {item}")
            else:
                st.warning("Maaf, detail rekomendasi untuk bentuk tubuh ini belum tersedia.")

            st.markdown("---")
            st.info("Penting: Rekomendasi ini adalah panduan umum. Kenakan apa yang membuat Anda merasa percaya diri dan nyaman!")

        else:
            st.warning("🤔 Maaf, kami tidak dapat mengidentifikasi bentuk tubuh Anda dengan pengukuran yang diberikan. Mohon periksa kembali input Anda.")

st.markdown("---")
st.header("2. Pelajari Bentuk Tubuh Umum")
st.write("Berikut adalah gambaran singkat beberapa bentuk tubuh yang umum:")

for shape_key, body_shape_obj in RECOMMENDATIONS_DATA.items():
    with st.expander(f"**Bentuk Tubuh: {body_shape_obj.name.replace('_', ' ').title()}**"):
        st.write(body_shape_obj.description)
        
        st.markdown("**Yang Perlu Dicari:**")
        for item in body_shape_obj.look_for:
            st.write(f"- {item}")
        
        st.markdown("**Bentuk Gaun Terbaik:**")
        for item in body_shape_obj.best_dress_shape:
            st.write(f"- {item}")
        
        st.markdown("**Petunjuk Gaya:**")
        for item in body_shape_obj.hint:
            st.write(f"- {item}")
        
        st.markdown("**Yang Perlu Dihindari:**")
        for item in body_shape_obj.avoid:
            st.write(f"- {item}")
            
st.markdown("---")
st.caption("Dibuat dengan ❤️ oleh Dyah Ayu Putri Zhafira.")