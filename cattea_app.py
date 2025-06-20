import streamlit as st

# تخزين الأسعار السابقة
if "prices" not in st.session_state:
    st.session_state.prices = []

new_price = st.number_input("أدخل السعر الحالي", format="%.2f")

if st.button("تحليل السعر"):
    st.session_state.prices.append(new_price)

    # نخزن آخر 3 فقط
    if len(st.session_state.prices) > 3:
        st.session_state.prices.pop(0)

    prices = st.session_state.prices

    st.write("📊 الأسعار الأخيرة:", prices)

    if len(prices) == 3:
        p1, p2, p3 = prices

        if p3 > p2 > p1:
            st.success("🔺 الاتجاه: صعود")
        elif p3 < p2 < p1:
            st.error("🔻 الاتجاه: هبوط")
        else:
            st.info("⏸️ الاتجاه: Stay Out")

if st.button("🔄 Reset"):
    st.session_state.prices = []
    st.success("تم مسح الأسعار وإعادة التهيئة.")
