import streamlit as st

st.set_page_config(page_title="Cattea Trading Helper", layout="centered")
st.title("📈 مساعد التداول في لعبة Cattea")

st.write("أدخل آخر 3 أسعار لبيتكوين (BTC) من اللعبة بالترتيب")

p1 = st.number_input("السعر الأول", format="%.8f")
p2 = st.number_input("السعر الثاني", format="
