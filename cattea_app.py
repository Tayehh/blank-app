import streamlit as st

st.set_page_config(page_title="تحليل اتجاه BTcat", layout="centered")
st.title("📈 تحليل الاتجاه (يدوي) لعملة BTcat")

# تهيئة القائمة
if "prices" not in st.session_state:
    st.session_state.prices = []

# إدخال السعر يدويًا
price = st.number_input("💰 أدخل السعر الحالي", format="%.2f", step=0.01)

# زر لإضافة السعر للقائمة
if st.button("➕ أضف السعر"):
    st.session_state.prices.append(price)
    if len(st.session_state.prices) > 3:
        st.session_state.prices.pop(0)  # نحتفظ بآخر 3 فقط

    st.success(f"✅ تم إضافة السعر: {price}")

# عرض الأسعار الحالية
st.write("📊 آخر 3 أسعار:", st.session_state.prices)

# تحليل الاتجاه
if len(st.session_state.prices) == 3:
    p1, p2, p3 = st.session_state.prices
    if p3 > p2 > p1:
        st.success("🔺 الاتجاه: صعود")
    elif p3 < p2 < p1:
        st.error("🔻 الاتجاه: هبوط")
    elif (p3 > p2 < p1) or (p3 < p2 > p1):
        st.warning("🔃 الاتجاه: متذبذب")
    else:
        st.info("⏸️ الاتجاه: ثابت")
elif len(st.session_state.prices) < 3:
    st.info("🕒 أضف 3 أسعار لتحليل الاتجاه")

# زر إعادة تعيين
if st.button("🔄 Reset"):
    st.session_state.prices = []
    st.success("✅ تم مسح جميع الأسعار")
