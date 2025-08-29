import cv2
import numpy as np
import pandas as pd
import streamlit as st
import os
from PIL import Image

st.title("🎮 Cattea Symbol Detector")

# --- رفع صورة اللعبة ---
uploaded = st.file_uploader("📸 ارفع صورة من اللعبة", type=["png", "jpg", "jpeg"])

if uploaded is not None:
    # حفظ الصورة المرفوعة مؤقتًا
    image_path = "game.png"
    with open(image_path, "wb") as f:
        f.write(uploaded.getbuffer())

    # قراءة الصورة
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # --- قراءة الـ templates من مجلد templates/ ---
    template_dir = "templates"
    templates = {}
    if not os.path.exists(template_dir) or not os.listdir(template_dir):
        st.warning("⚠️ مجلد 'templates/' فاضي. لازم تضيف صور الرموز فيه الأول.")
    else:
        for filename in os.listdir(template_dir):
            if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                path = os.path.join(template_dir, filename)
                template = cv2.imread(path, 0)
                if template is not None:
                    name = os.path.splitext(filename)[0]
                    templates[name] = template

        detected = []

        # البحث عن كل رمز
        for name, template in templates.items():
            w, h = template.shape[::-1]
            res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.7
            loc = np.where(res >= threshold)
            for pt in zip(*loc[::-1]):
                detected.append((pt[0], pt[1], w, h, name))
                cv2.rectangle(img_rgb, pt, (pt[0]+w, pt[1]+h), (255,0,0), 2)
                cv2.putText(img_rgb, name, (pt[0], pt[1]-5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1)

        # --- عرض النتيجة ---
        st.image(img_rgb, caption="📍 النتيجة بعد التعرف على الرموز", use_container_width=True)

        # --- جدول النتائج ---
        data = [{"x":x, "y":y, "w":w, "h":h, "symbol":name} for (x,y,w,h,name) in detected]
        df = pd.DataFrame(data).sort_values(by=["y","x"]).reset_index(drop=True)

        if not df.empty:
            st.subheader("📊 الرموز المكتشفة")
            st.dataframe(df)
            # تحميل CSV
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ تحميل النتائج كـ CSV", data=csv,
                               file_name="results.csv", mime="text/csv")
        else:
            st.info("🚫 لم يتم العثور على رموز متطابقة")
