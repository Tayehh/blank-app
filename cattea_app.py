import streamlit as st
from PIL import Image
import pytesseract
import numpy as np
import cv2
import re

st.set_page_config(page_title="تحليل BTcat", layout="centered")
st.title("📷 تحليل الاتجاه من لقطة الشاشة (مع قص السعر من الطيارة)")

if "prices" not in st.session_state:
    st.session_state.prices = []

uploaded_file = st.file_uploader("📸 ارفع صورة من اللعبة", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="📷 الصورة الأصلية", use_column_width=True)

    # تحويل الصورة إلى numpy array ومعالجتها
    img = np.array(image)
    height, width, _ = img.shape

    # 👇 قص منطقة السعر داخل الطيارة (تقديريًا منتصف الصورة)
    crop_top = int(height * 0.42)
    crop_bottom = int(height * 0.52)
    crop_left = int(width * 0.25)
    crop_right = int(width * 0.75)

    cropped = img[crop_top:crop_bottom, crop_left:crop_right]
    st.image(cropped, caption="✂️ المنطقة المقصوصة (السعر فقط)")

    # تحويل لصورة رمادية ومعالجة
    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # OCR
    extracted_text = pytesseract.image_to_string(thresh)
    st.text_area("📄 النص المستخرج:", extracted_text, height=100)

    match = re.search(r"\d{4,6}\.\d{2}", extracted_text)
    if match:
        price = float(match.group())
        st.success(f"✅ السعر المستخرج: {price}")
        st.session_state.prices.append(price)

        if len(st.session_state.prices) > 3:
            st.session_state.prices.pop(0)

        st.write("🧾 آخر 3 أسعار:", st.session_state.prices)

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
    else:
        st.warning("❌ السعر غير واضح، جرّب صورة أوضح أو تكبير الطيارة")

# زر Reset
if st.button("🔄 Reset"):
    st.session_state.prices = []
    st.success("✅ تم إعادة التهيئة.")
