import streamlit as st

st.set_page_config(page_title="Cattea Trading Helper", layout="centered")
st.title("📈 مساعد التداول في لعبة Cattea")

st.write("أدخل آخر 3 أسعار لبيتكوين (BTCAT) من اللعبة بالترتيب")

# نرفع الدقة علشان الأسعار الصغيرة جدًا ما تبقاش صفر
p1 = st.number_input("السعر الأول", format="%.15f")
p2 = st.number_input("السعر الثاني", format="%.15f")
p3 = st.number_input("السعر الثالث", format="%.15f")

suggestion = ""
if st.button("احسب الاتجاه"):
    if p3 > p2 > p1:
        suggestion = "✅ الاقتراح: 📈 LONG"
    elif p3 < p2 < p1:
        suggestion = "✅ الاقتراح: 📉 SHORT"
    else:
        suggestion = "✅ الاقتراح: 💤 STAY OUT"

    st.success(suggestion)
