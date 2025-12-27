import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# KONFIGURASI HALAMAN
st.set_page_config(
    page_title="Dashboard E-Commerce Analytics", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
/* BACKGROUND */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #ffffff;
}

/* MAIN PADDING */
.main {
    padding: 0rem 3rem;
}

/* CARD – HANYA container(border=True) */
[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #ffffff;
    border-radius: 12px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.06);
}

/* METRIC */
[data-testid="stMetricValue"] {
    font-size: 1.4rem !important;
    font-weight: 800 !important;
    color: #1e293b !important;
}
</style>
""", unsafe_allow_html=True)




# LOAD DATA
@st.cache_data
def load_data():
    try:
        produk_terbanyak = pd.read_csv("dashboard/produk_terbanyak.csv")
        metode_pembayaran = pd.read_csv("dashboard/metode_pembayaran.csv")
        city_customer_summary = pd.read_csv("dashboard/city_customer_summary.csv")
        order_review = pd.read_csv("dashboard/order_review_summary.csv")
        feature_importance = pd.read_csv("dashboard/feature_importance.csv")
        return produk_terbanyak, metode_pembayaran, city_customer_summary, order_review, feature_importance
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return [None] * 5

df_prod, df_pay, df_city, df_rev, df_feat = load_data()

# Global Style
sns.set_style("white")

# HEADER DASHBOARD
st.write("") 

st.markdown("""
    <div style="text-align: center;">
        <h1 style="margin-bottom: 0;">Dashboard Analisis E-Commerce</h1>
    </div>
    """, unsafe_allow_html=True)

# st.divider()

# BARIS 1: PRODUK TERLARIS
if df_prod is not None:
    m1, col_main, m2 = st.columns([0.05, 0.9, 0.05])
    with col_main:
        with st.container(border=True):
            st.subheader("10 Kategori Produk Terlaris")
            c1, c2, c3, c4 = st.columns(4)
            top_p = df_prod.iloc[0]
            c1.metric("Top Kategori", top_p['Product']) 
            c2.metric("Jumlah Order", f"{top_p['Frequency']:,}")
            c3.metric("Total Top 10", f"{df_prod['Frequency'].sum():,}")
            c4.metric("Rata-rata", f"{df_prod['Frequency'].mean():,.0f}")
            
            fig, ax = plt.subplots(figsize=(12, 3.5))
            sns.barplot(x="Frequency", y="Product", data=df_prod, palette="viridis", ax=ax)
            ax.set_xlabel("Jumlah Pembelian")
            ax.set_ylabel("Kategori Produk")
            ax.grid(False)
            sns.despine()
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close()
            
            with st.expander("Analisis Kategori Produk"):
                st.write("""
                        Analisis kategori produk menunjukkan bahwa kebutuhan rumah tangga, perawatan diri, dan gaya hidup 
                        mendominasi total transaksi, dengan kategori bed_bath_table dan health_beauty sebagai penyumbang 
                        pesanan terbesar. Dominasi ini mengindikasikan bahwa konsumen memiliki kecenderungan kuat untuk 
                        melakukan pembelian rutin dan berulang pada produk-produk dasar, sehingga strategi bisnis sebaiknya 
                        difokuskan pada optimalisasi stok, skema bundling produk, serta promosi musiman untuk memaksimalkan 
                        potensi penjualan pada kategori dengan frekuensi tinggi ini.
                        """)

st.write("") 

# BARIS 2: PEMBAYARAN & KOTA

m_l, card_pay, gap, card_city, m_r = st.columns([0.05, 0.44, 0.02, 0.44, 0.05])

with card_pay:
    with st.container(border=True):
        st.subheader("Metode Pembayaran Terpopuler")
        if df_pay is not None:
            top_pay = df_pay.iloc[0]
            total_pay = df_pay['total_transactions'].sum()
            dom_pay = (top_pay['total_transactions'] / total_pay) * 100
            
            pcol1, pcol2, pcol3 = st.columns(3)
            pcol1.metric("Metode Utama", top_pay['payment_type'])
            pcol2.metric("Jumlah Transaksi", f"{int(top_pay['total_transactions']):,}")
            pcol3.metric("Dominasi", f"{dom_pay:.1f}%")
            
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.barplot(x="payment_type", y="total_transactions", data=df_pay, palette="mako", ax=ax)
            ax.set_xlabel("Metode Pembayaran")
            ax.set_ylabel("Jumlah Transaksi")
            ax.grid(False)
            sns.despine()
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close()

            with st.expander("Analisis Metode Pembayaran"):
                st.write("""
                        Penggunaan kartu kredit mendominasi platform secara mutlak dibandingkan metode lainnya, yang mencerminkan 
                        tingkat kepercayaan tinggi pelanggan terhadap sistem pembayaran non-tunai serta kebutuhan akan fleksibilitas 
                        pembayaran seperti fitur cicilan. Meskipun kartu kredit menjadi instrumen utama, ketersediaan metode 
                        alternatif seperti boleto tetap krusial untuk menjaga inklusivitas pasar dan menjangkau segmen pelanggan 
                        yang lebih luas, guna memastikan proses konversi transaksi berjalan lancar bagi seluruh lapisan pengguna.
                        """)

with card_city:
    with st.container(border=True):
        st.subheader("10 Kota dengan Pelanggan Terbanyak")
        if df_city is not None:
            top_city = df_city.iloc[0]
            total_cust = df_city['total_customers'].sum()
            m_share = (top_city['total_customers'] / total_cust) * 100
            
            ccol1, ccol2, ccol3 = st.columns(3)
            ccol1.metric("Kota Terbesar", top_city['customer_city'])
            ccol2.metric("Jumlah Pelanggan", f"{int(top_city['total_customers']):,}")
            ccol3.metric("Market Share", f"{m_share:.1f}%")
            
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.barplot(x="total_customers", y="customer_city", data=df_city.head(10), palette="viridis", ax=ax)
            ax.set_xlabel("Jumlah Pelanggan")
            ax.set_ylabel("Kota")
            ax.grid(False)
            sns.despine()
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close()

            with st.expander("Analisis Kota"):
                st.write("""
                        São Paulo muncul sebagai pusat pasar utama dengan jumlah pelanggan yang sangat signifikan, bahkan mencapai 
                        lebih dari dua kali lipat populasi pelanggan di kota besar lainnya seperti Rio de Janeiro. Konsentrasi 
                        pelanggan yang sangat terpusat di wilayah urban dan pusat ekonomi ini menegaskan perlunya prioritas strategi 
                        operasional pada wilayah tersebut, seperti penempatan gudang strategis (fulfillment center) dan penguatan 
                        armada logistik untuk menjamin kecepatan pengiriman di area dengan permintaan tertinggi.
                        """)

st.write("") 

# BARIS 3: KETERLAMBATAN & LOGISTIK

m_l2, card_late, gap2, card_feat, m_r2 = st.columns([0.05, 0.44, 0.02, 0.44, 0.05])

with card_late:
    with st.container(border=True):
        st.subheader("Keterlambatan Pengiriman VS Review Score")
        if df_rev is not None:
            scores = df_rev.groupby('is_late')['review_score'].mean()
            diff = scores[0] - scores[1]
            
            c_a, c_b = st.columns(2)
            c_a.metric("Tepat Waktu", f"{scores[0]:.2f} ")
            c_b.metric("Terlambat", f"{scores[1]:.2f} ", delta=f"-{diff:.2f}", delta_color="inverse")
            
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.bar(["Tepat Waktu", "Terlambat"], scores, color=["#4CAF50", "#F44336"], width=0.6)
            ax.set_ylim(0, 5.5)
            ax.set_xlabel("Status Pengiriman")
            ax.set_ylabel("Rata-rata Review Score")
            ax.grid(False)
            sns.despine()
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close()

            with st.expander("Analisis Kepuasan"):
                st.write("""
                        Keterlambatan pengiriman terbukti menjadi faktor kritis yang menurunkan tingkat kepuasan pelanggan secara drastis, 
                        terlihat dari penurunan rata-rata skor ulasan yang signifikan dari 4,26 pada pengiriman tepat waktu menjadi 
                        hanya 2,43 pada pesanan yang terlambat. Adanya korelasi negatif yang nyata ini menunjukkan bahwa ketepatan 
                        waktu bukan sekadar target operasional, melainkan pilar utama dalam menjaga reputasi platform dan loyalitas 
                        pelanggan, sehingga setiap bentuk keterlambatan akan langsung berdampak buruk pada penilaian terhadap layanan.
                        """)

with card_feat:
    with st.container(border=True):
        st.subheader("Faktor yang memengaruhi Lama Waktu Pengiriman")
        if df_feat is not None:
            top_f = df_feat.nlargest(1, 'importance').iloc[0]
            fcol1, fcol2 = st.columns(2)
            fcol1.metric("Faktor Utama", top_f['feature'])
            fcol2.metric("Tingkat Pengaruh", f"{top_f['importance']:.3f}")
            
            fig, ax = plt.subplots(figsize=(6, 4.02))

            df_feat_sorted = df_feat.sort_values("importance", ascending=False)
            sns.barplot(x="importance", y="feature", data=df_feat_sorted, palette="viridis", ax=ax)
            
            ax.set_xlabel("Importance Score")
            ax.set_ylabel("Fitur")
            ax.grid(False)
            sns.despine()
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close()

            with st.expander("Analisis Pengiriman"):
                st.write("""
                        Berdasarkan analisis feature importance, variabel freight_value (biaya pengiriman) 
                        diidentifikasi sebagai faktor yang paling dominan dalam menentukan durasi pengiriman dibandingkan dimensi 
                        fisik produk. Hal ini menunjukkan bahwa kompleksitas biaya, berat paket, dan lokasi geografis pelanggan 
                        memiliki pengaruh lebih besar terhadap efisiensi logistik, sehingga perusahaan perlu memfokuskan strategi 
                        pada pemilihan mitra pengiriman yang tepat serta optimasi rute distribusi untuk menekan waktu tempuh 
                        secara lebih efektif.
                        """)


# FOOTER
st.markdown("""
    <div style="text-align: center; color: #94a3b8; padding-top: 30px; padding-bottom: 20px;">
        Dashboard Analytics © 2025 | Brazilian E-Commerce Dataset
    </div>

    """, unsafe_allow_html=True)





