import streamlit as st
import requests
from collections import deque

# إعداد الصفحة
st.set_page_config(page_title="Cattea Trading Helper", layout="centered")
st.title("📈 مساعد التداول في لعبة Cattea (BTCAT)")

st.write("يتم جلب السعر مباشرة من CoinGecko كل ما تضغط على الزر")

# صف أسعار لحفظ آخر 3 أسعار فقط
if "prices" not in st.session_state:
    st.session_state.prices = deque(maxlen=3)

# دالة لجلب سعر بيتكوين من CoinGecko
@st.cache_data(ttl=30)
def get_btc_price():
    try:
        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
        data = response.json()
        return data["bitcoin"]["usd"]
    except:
        return None

# تقسيم الأزرار في صف واحد
col1, col2 = st.columns(2)

with col1:
    if st.button("📥 جلب السعر الحالي"):
        price = get_btc_price()
        if price:
            st.session_state.prices.append(price)
            st.success(f"تم جلب السعر: {price} $")
        else:
            st.error("فشل في الاتصال بـ CoinGecko")

with col2:
    if st.button("🔄 إعادة تعيين"):
        st.session_state.prices.clear()
        st.info("تمت إعادة التعيين، ابدأ من جديد ✨")

# عرض الأسعار
st.subheader("📊 آخر 3 أسعار:")
if len(st.session_state.prices) > 0:
    for i, p in enumerate(reversed(st.session_state.prices), 1):
        st.write(f"السعر {i}: {p} $")
else:
    st.info("لم يتم تحميل أي أسعار بعد.")

# التحليل الفوري
if len(st.session_state.prices) == 3:
    p1, p2, p3 = st.session_state.prices
    suggestion = ""
    if p3 > p2 > p1:
        suggestion = "✅ الاتجاه الحالي: 📈 LONG"
    elif p3 < p2 < p1:
        suggestion = "✅ الاتجاه الحالي: 📉 SHORT"
    else:
        suggestion = "✅ الاتجاه الحالي: 💤 STAY OUT"
    st.subheader(suggestion)
