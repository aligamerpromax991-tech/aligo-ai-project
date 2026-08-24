import streamlit as st
from supabase import create_client

# ==========================================
# SƏHİFƏ TƏNZİMLƏMƏLƏRİ VƏ DİZAYN (Dark Theme)
# ==========================================
st.set_page_config(
    page_title="AliGo - Məxfi Admin Mərkəzi",
    page_icon="⚡",
    layout="wide"
)

# Xüsusi CSS dizaynı
st.markdown("""
    <style>
    .main {
        background-color: #0f172a;
    }
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    h1, h2, h3 {
        color: #00f2fe !important;
    }
    .stTextInput>div>div>input {
        background-color: #1e293b;
        color: white;
        border: 1px solid #334155;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# SUPABASE QOŞULMA MƏLUMATLARI (Secrets-dən oxunur)
# ==========================================
try:
    SUPABASE_URL = st.secrets["supabase"]["url"]
    SUPABASE_KEY = st.secrets["supabase"]["key"]
except Exception as e:
    st.error("❌ Supabase məlumatları Streamlit Secrets-də tapılmadı! Zəhmət olmasa Secrets bölməsini tənzimləyin.")
    st.stop()

# Sənin təyin etdiyin güclü şifrə
ADMIN_SECRET_PASSWORD = "AliGo_Secure_Admin_2026#X9!z"

# ==========================================
# GİRİŞ (ŞİFRƏ) YOXLAMASI
# ==========================================
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if not st.session_state.admin_logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<h2 style='text-align: center;'>🔒 ADMİN GİRİŞİ</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #94a3b8;'>Zəhmət olmasa təhlükəsizlik kodunu daxil edin:</p>", unsafe_allow_html=True)
        
        entered_pass = st.text_input("Şifrə:", type="password", key="admin_pass_input")
        if st.button("Daxil ol", use_container_width=True):
            if entered_pass == ADMIN_SECRET_PASSWORD:
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("❌ Yanlış şifrə! Giriş rədd edildi.")
    st.stop()

# ==========================================
# SUPABASE BAĞLANTISI
# ==========================================
@st.cache_resource
def init_supabase():
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        return None

supabase = init_supabase()

# ==========================================
# ADMIN PANELİNİN ƏSAS HİSSƏSİ
# ==========================================
st.markdown("⚡ **ALIGO İDARƏETMƏ PANELİ**")

if st.button("🔄 Məlumatları Yenilə"):
    st.rerun()

st.markdown("---")

# Tablar (Səhifələr)
tab1, tab2 = st.tabs(["  👥 İstifadəçilər  ", "  👍 Bəyənmələr & Rəylər  "])

# 1-ci Tab: İstifadəçilər
with tab1:
    st.subheader("Qeydiyyatdan Keçən İstifadəçilər")
    if supabase:
        try:
            res = supabase.table("users_log").select("*").order("created_at", desc=True).execute()
            users = res.data if res.data else []
            
            if users:
                table_data = []
                for idx, u in enumerate(users, 1):
                    created_at = str(u.get("created_at", ""))[:19].replace("T", " ")
                    table_data.append({
                        "#": idx,
                        "İstifadəçi Adı": u.get("name", "Adsız"),
                        "Email Ünvanı": u.get("email", "-"),
                        "User Code (ID)": u.get("user_code", "-"),
                        "Giriş Tarixi": created_at
                    })
                st.dataframe(table_data, use_container_width=True)
            else:
                st.info("ℹ️ Hələ ki bazada heç bir istifadəçi qeydi yoxdur.")
        except Exception as e:
            st.error(f"❌ Xəta baş verdi: {e}")
    else:
        st.error("❌ Supabase bağlantısı qurulmadı!")

# 2-ci Tab: Bəyənmələr və Rəylər
with tab2:
    st.subheader("İstifadəçi Reaksiyaları və Mesajlar")
    if supabase:
        try:
            res = supabase.table("likes_log").select("*").order("id", desc=True).execute()
            likes = res.data if res.data else []
            
            if likes:
                table_data_likes = []
                for idx, l in enumerate(likes, 1):
                    created_at = str(l.get("created_at", ""))[:19].replace("T", " ")
                    table_data_likes.append({
                        "#": idx,
                        "İstifadəçi": l.get("user_name", "Naməlum"),
                        "Reaksiya": l.get("feedback_type", "-"),
                        "AI Cavabı / Mesaj": l.get("message", "-"),
                        "Tarix": created_at
                    })
                st.dataframe(table_data_likes, use_container_width=True)
            else:
                st.info("ℹ️ Hələ ki bazada heç bir bəyənmə və ya rəy yoxdur.")
        except Exception as e:
            st.error(f"❌ Xəta baş verdi: {e}")
    else:
        st.error("❌ Supabase bağlantısı qurulmadı!")
