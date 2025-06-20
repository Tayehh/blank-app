import streamlit as st
from PIL import Image
import pytesseract

# إعداد صفحة Streamlit
st.set_page_config(page_title="Cattea Price Analyzer", layout="centered")
st.markdown(
    """
    <style>
        body {background-color: #0e1117; color: white;}
        .stButton > button {background-color: #262730; color: white;}
    </style>
    """, unsafe_allow_html=True
)

st.title("📷 تحليل اتجاه BTcat من الصورة")

# إعداد قائمة الأسعار
if "prices" not in st.session_state:
    st.session_state.prices = []

# رفع صورة
uploaded_file = st.file_uploader("📸 ارفع لقطة الشاشة من اللعبة", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="📷 الصورة المرفوعة", use_column_width=True)

    # قراءة السعر من الصورة
    extracted_text = pytesseract.image_to_string(image)

    # استخراج أول رقم عشري موجود
    import re
    match = re.search(r"\d{2,6}\.\d{1,2}", extracted_text)
    if match:
        price = float(match.group())
        st.success(f"✅ السعر المُستخرج: {price}")
        st.session_state.prices.append(price)

        # نخزن فقط آخر 3 أسعار
        if len(st.session_state.prices) > 3:
            st.session_state.prices.pop(0)

        prices = st.session_state.prices
        st.write("🧾 الأسعار الأخيرة:", prices)

        if len(prices) == 3:
            p1, p2, p3 = prices

            if p3 > p2 > p1:
                st.success("🔺 الاتجاه: صعود قوي")
            elif p3 < p2 < p1:
                st.error("🔻 الاتجاه: هبوط قوي")
            elif (p3 > p2 < p1) or (p3 < p2 > p1):
                st.warning("🔃 الاتجاه: متذبذب")
            else:
                st.info("⏸️ الاتجاه: ثابت")

    else:
        st.warning("❌ لم يتم العثور على رقم في الصورة")

# زر Reset
if st.button("🔄 Reset"):
    st.session_state.prices = []
    st.success("✅ تم مسح الأسعار.")
