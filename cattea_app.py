# تثبيت المكتبات
!pip install opencv-python pillow matplotlib pandas

import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd
from google.colab import files

# رفع الصورة
uploaded = files.upload()
image_path = list(uploaded.keys())[0]

# قراءة الصورة
img = cv2.imread(image_path)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# تحويلها للرمادي
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# ----------------------------
# إعداد قوالب (Templates)
# ----------------------------
# هنا ترفع صور صغيرة للرموز (بطة، قطة، بيتكوين..) بنفس الأيقونات
# تحفظها باسم: cat.png, duck.png, btc.png, paw.png, ton.png
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
        continue
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.7  # نسبة التشابه
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        detected.append((pt[0], pt[1], w, h, name))
        cv2.rectangle(img_rgb, pt, (pt[0]+w, pt[1]+h), (255,0,0), 2)
        cv2.putText(img_rgb, name, (pt[0], pt[1]-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1)

# عرض الصورة مع العلامات
plt.figure(figsize=(8,8))
plt.imshow(img_rgb)
plt.axis("off")
plt.show()

# تحويل النتائج لـ DataFrame
data = [{"x":x, "y":y, "w":w, "h":h, "symbol":name} for (x,y,w,h,name) in detected]
df = pd.DataFrame(data).sort_values(by=["y","x"]).reset_index(drop=True)
import pandas as pd
from IPython.display import display
display(df)
