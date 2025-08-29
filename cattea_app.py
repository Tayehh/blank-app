import cv2
import numpy as np
import pandas as pd
import streamlit as st

st.title("🐱🎮 Cattea Symbol Detector")

# رفع صورة اللعبة
uploaded_game = st.file_uploader("📸 ارفع صورة من اللعبة", type=["png", "jpg", "jpeg"])

# رفع صور القطع
uploaded_templates = st.file_uploader("🧩 ارفع صور القطع (templates)", 
                                      type=["png", "jpg"], accept_multiple_files=True)

if uploaded_game is not None and uploaded_templates:
    # قراءة صورة اللعبة
    file_bytes = np.asarray(bytearray(uploaded_game.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # قراءة القوالب
    templates = {}
    for file in uploaded_templates:
        name = file.name.split(".")[0]  # اسم الملف بدون الامتداد
        file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
        template = cv2.imdecode(file_bytes, 0)
        templates[name] = template

    detected = []

    # البحث عن كل رمز
    for name, template in templates.items():
        if template is None:
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

    # عرض الصورة
    st.image(img_rgb, caption="📍 النتائج بعد التعرف على الرموز", use_container_width=True)

    # عرض النتائج
    data = [{"x":x, "y":y, "w":w, "h":h, "symbol":name} for (x,y,w,h,name) in detected]
    df = pd.DataFrame(data).sort_values(by=["y","x"]).reset_index(drop=True)

    if not df.empty:
        st.subheader("📊 الرموز المكتشفة")
        st.dataframe(df)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ تحميل النتائج كـ CSV", data=csv, file_name="results.csv", mime="text/csv")
    else:
        st.info("🚫 لم يتم العثور على رموز متطابقة")
