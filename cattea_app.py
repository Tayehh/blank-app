import streamlit as st
import requests
from collections import deque

st.set_page_config(page_title="Cattea Trading Helper", layout="centered")
st.title("📈 مساعد التداول الذكي في Cattea (BTcat أو BTC)")

st.markdown("أدخل أو اجلب السعر، وسيقوم البرنامج بتحليل الاتجاه العام 👇")

# إعداد التخزين المؤقت لآخر 3 أسعار
if "prices" not in st.session_state:
    st.session_state.prices = deque(maxlen=3)

# زر جلب سعر بيتكوين (اختياري)
@st.cache_data(ttl=30)
def get_btc_price():
    try:
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
        return r.json()["bitcoin"]["usd"]
    except:
        return None

col1, col2 = st.columns(2)

with col1:
    if st.button("📥 جلب السعر (BTC فقط)"):
        price = get_btc_price()
        if price:
            st.session_state.prices.append(price)
            st.success(f"السعر المضاف: {price} $")
        else:
            st.error("فشل في جلب السعر من CoinGecko")

with col2:
    if st.button("🔄 إعادة تعيين"):
        st.session_state.prices.clear()
        st.info("تم حذف كل الأسعار")

# إدخال يدوي
manual_price = st.number_input("أو أدخل السعر يدويًا (BTcat)", format="%.20f")
if st.button("➕ أضف السعر اليدوي"):
    if manual_price > 0:
        st.session_state.prices.append(manual_price)
        st.success(f"تمت إضافة السعر: {manual_price}")
    else:
        st.warning("يجب إدخال سعر أكبر من صفر")

# عرض الأسعار
st.subheader("📊 آخر 3 أسعار:")
for i, price in enumerate(reversed(st.session_state.prices), 1):
    st.write(f"السعر {i}: {price}")

# التحليل الذكي
if len(st.session_state.prices) == 3:
    p1, p2, p3 = st.session_state.prices
    delta1 = p2 - p1
    delta2 = p3 - p2
    avg_change = (delta1 + delta2) / 2

    # عتبات شديدة الحساسية
    threshold_weak = 0.0
    threshold_strong = 0.000000000000001

    # تحديد الاتجاه
    direction = "💤 STAY OUT"
    strength = "❔ غير واضح"

    if avg_change > threshold_weak:
        direction = "📈 LONG"
        strength = "🔥 قوي" if avg_change > threshold_strong else "⚠️ ضعيف"
    elif avg_change < -threshold_weak:
        direction = "📉 SHORT"
        strength = "🔥 قوي" if avg_change < -threshold_strong else "⚠️ ضعيف"
    else:
        direction = "💤 STAY OUT"
        strength = "🔍 الاتجاه الجانبي"

    # عرض النتيجة
    st.subheader(f"✅ الاتجاه الحالي: {direction}")
    st.write(f"📐 قوة الاتجاه: {strength}")
    st.write(f"📈 متوسط التغير: {avg_change:.20f}")
