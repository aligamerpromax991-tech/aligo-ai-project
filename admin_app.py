import streamlit as st
import requests

# ==========================================
# SƏHİFƏ TƏNZİMLƏMƏLƏRİ VƏ DİZAYN (Dark Theme)
# ==========================================
st.set_page_config(
    page_title="AliGo - Məxfi Admin Mərkəzi",
    page_icon="⚡",
    layout="wide"
)

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
# SUPABASE MƏLUMATLARI (Secrets-dən)
# ==========================================
try:
    SUPABASE_URL = st.secrets["supabase"]["url"]
    SUPABASE_KEY = st.secrets["supabase"]["key"]
except Exception as e:
    st.error("❌ Supabase məlumatları Streamlit Secrets-də tapılmadı!")
    st.stop()

ADMIN_SECRET_PASSWORD = "AliGo_Secure_Admin_2026#X9!z"

# Yardımçı funksiya: Supabase-dən birbaşa məlumat çəkmək üçün
def fetch_from_supabase(table_name):
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }
    url = f"{SUPABASE_URL}/rest/v1/{table_name}?select=*"
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Supabase xətası ({response.status_code}): {response.text}")
            return []
    except Exception as ex:
        st.error(f"Sorğu xətası: {ex}")
        return []

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
# ADMIN PANELİNİN ƏSAS HİSSƏSİ
# ==========================================
st.markdown("⚡ **ALIGO İDARƏETMƏ PANELİ**")

if st.button("🔄 Məlumatları Yenilə"):
    st.rerun()

st.markdown("---")

tab1, tab2 = st.tabs(["  👥 İstifadəçilər  ", "  👍 Bəyənmələr & Rəylər  "])

# 1-ci Tab: İstifadəçilər
with tab1:
    st.subheader("Qeydiyyatdan Keçən İstifadəçilər")
    users = fetch_from_supabase("users_log")
    
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
        st.info("ℹ️ Hələ ki bazada heç bir istifadəçi qeydi yoxdur və ya bağlantı gözlənilir.")

# 2-ci Tab: Bəyənmələr və Rəylər
with tab2:
    st.subheader("İstifadəçi Reaksiyaları və Mesajlar")
    likes = fetch_from_supabase("likes_log")
    
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
