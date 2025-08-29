import streamlit as st
import cv2
import numpy as np
import os
from PIL import Image
import matplotlib.pyplot as plt

# ==============================
# مجلد الرموز
# ==============================
TEMPLATES_DIR = "templates"
os.makedirs(TEMPLATES_DIR, exist_ok=True)

st.title("🎮 Cattea Symbol Detector")

# رفع صورة من اللعبة
uploaded_file = st.file_uploader("ارفع صورة من اللعبة", type=["png", "jpg", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file).convert("RGB")
    img_np = np.array(img)
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)

    # تحقق لو في قوالب محفوظة
    template_files = [f for f in os.listdir(TEMPLATES_DIR) if f.endswith((".png",".jpg",".jpeg"))]

    if not template_files:
        st.warning("مجلد templates/ فاضي ‼️ قص الرموز الأولى عشان نستخدمها بعدين.")

        # أداة بسيطة لقص الرموز بالماوس
        st.info("📌 استخدم الماوس لقص الرموز: اختار جزء من الصورة واحفظه كـ Template.")

        from streamlit_cropper import st_cropper

        cropped = st_cropper(img, realtime_update=True, box_color='#FF0000', aspect_ratio=None)

        if st.button("💾 حفظ الرمز كـ Template"):
            if cropped:
                name = st.text_input("ادخل اسم الرمز (مثلاً cat, duck...)", "")
                if name.strip() != "":
                    save_path = os.path.join(TEMPLATES_DIR, f"{name}.png")
                    cropped.save(save_path)
                    st.success(f"✅ تم حفظ {save_path}")
                else:
                    st.error("❌ لازم تكتب اسم للرمز قبل الحفظ.")

    else:
        st.success("✅ تم تحميل القوالب من مجلد templates/")
        detected = []

        # جلب القوالب
        templates = {}
        for f in template_files:
            path = os.path.join(TEMPLATES_DIR, f)
            templates[os.path.splitext(f)[0]] = cv2.imread(path, 0)

        # البحث عن الرموز
        for name, template in templates.items():
            if template is None:
                continue
            w, h = template.shape[::-1]
            res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.7
            loc = np.where(res >= threshold)
            for pt in zip(*loc[::-1]):
                detected.append((pt[0], pt[1], w, h, name))
                cv2.rectangle(img_np, pt, (pt[0]+w, pt[1]+h), (255,0,0), 2)
                cv2.putText(img_np, name, (pt[0], pt[1]-5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1)

        # عرض النتيجة
        st.image(img_np, caption="📍 النتيجة", use_container_width=True)

        # عرض جدول النتائج
        if detected:
            import pandas as pd
            data = [{"x":x, "y":y, "w":w, "h":h, "symbol":name}
                    for (x,y,w,h,name) in detected]
            df = pd.DataFrame(data).sort_values(by=["y","x"]).reset_index(drop=True)
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("⚠️ لم يتم العثور على أي رموز.")
