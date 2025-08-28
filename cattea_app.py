import cv2
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image

st.title("🐱🎮 Cattea Symbol Detector")

# رفع الصورة
uploaded_file = st.file_uploader("ارفع صورة من اللعبة", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # قراءة الصورة
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # ----------------------------
    # تحميل قوالب الرموز (Templates)
    # ----------------------------
    templates = {
        "cat": cv2.imread("cat.png", 0),
        "duck": cv2.imread("duck.png", 0),
        "btc": cv2.imread("btc.png", 0),
        "paw": cv2.imread("paw.png", 0),
        "ton": cv2.imread("ton.png", 0),
    }

    detected = []

    # البحث عن كل رمز
    for name, template in templates.items():
        if template is None:
            st.warning(f"⚠️ لم أجد ملف: {name}.png - تخطيت الرمز.")
            continue
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.7
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            detected.append((pt[0], pt[1], w, h, name))
            cv2.rectangle(img_rgb, pt, (pt[0]+w, pt[1]+h), (255,0,0), 2)
            cv2.putText(img_rgb, name, (pt[0], pt[1]-5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1)

    # عرض الصورة المعالجة
    st.image(img_rgb, caption="النتيجة بعد التعرف على الرموز", use_column_width=True)

    # عرض النتائج كجدول
    data = [{"x":x, "y":y, "w":w, "h":h, "symbol":name} for (x,y,w,h,name) in detected]
    df = pd.DataFrame(data).sort_values(by=["y","x"]).reset_index(drop=True)

    if not df.empty:
        st.subheader("📊 الرموز المكتشفة")
        st.dataframe(df)
        # تحميل CSV
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ تحميل النتائج كـ CSV", data=csv, file_name="results.csv", mime="text/csv")
    else:
        st.info("لم يتم العثور على رموز متطابقة في الصورة 🚫")
