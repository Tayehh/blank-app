import streamlit as st

# إعداد الصفحة
st.set_page_config(page_title="تحليل اتجاه BTcat", layout="centered", initial_sidebar_state="auto")

st.markdown(
    """
    <style>
        body {background-color: #0e1117; color: white;}
        .stButton > button {background-color: #262730; color: white;}
    </style>
    """, unsafe_allow_html=True
)

st.title("📈 تحليل اتجاه BTcat")
st.write("ادخل السعر الحالي، وسيتم تحليل الاتجاه بناءً على آخر 3 أسعار.")

# إنشاء قائمة ديناميكية للأسعار
if "prices" not in st.session_state:
    st.session_state.prices = []

# إدخال السعر
new_price = st.number_input("أدخل السعر الحالي", format="%.2f")

# زر إضافة السعر وتحليل الاتجاه
if st.button("📊 تحليل الاتجاه"):
    st.session_state.prices.append(new_price)

    # نخزن فقط آخر 3 أسعار
    if len(st.session_state.prices) > 3:
        st.session_state.prices.pop(0)

    prices = st.session_state.prices
    st.write("🧾 الأسعار الأخيرة:", prices)

    if len(prices) == 3:
        p1, p2, p3 = prices

        # تحليل الاتجاه الذكي
        if p3 > p2 > p1:
            st.success("🔺 الاتجاه: صعود قوي")
        elif p3 < p2 < p1:
            st.error("🔻 الاتجاه: هبوط قوي")
        elif (p3 > p2 < p1) or (p3 < p2 > p1):
            st.warning("🔃 الاتجاه: متذبذب (غير مستقر)")
        else:
            st.info("⏸️ الاتجاه: ثابت (ضعيف الحركة)")

# زر إعادة تعيين
if st.button("🔄 Reset"):
    st.session_state.prices = []
    st.success("✅ تم مسح الأسعار.")
