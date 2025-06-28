import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(layout="wide", page_title="Gait Analysis")

st.title("🎥 Video-based Gait Analysis")

# تقسيم الصفحة إلى 3 أعمدة
col1, col2, col3 = st.columns([1.2, 1.5, 2.5])

# -- العمود الأول: الإحصائيات --
with col1:
    st.header("Summary")
    st.write("**Shoulder Tilt (Mean):** -5.2")
    st.write("**STD:** 1.93")
    st.write("**Step Width:** 41.8 cm")
    st.write("**Step Count:** 17")

# -- العمود الثاني: الرسوم البيانية --
with col2:
    st.header("Motion Charts")
    fig, axs = plt.subplots(2, 2, figsize=(8, 6))
    for ax in axs.flatten():
        ax.plot([1, 2, 3], [1, 4, 9])
        ax.set_xticks([])
        ax.set_yticks([])
    st.pyplot(fig)

# -- العمود الثالث: تشغيل الفيديو --
with col3:
    st.header("Video")
    uploaded_file = st.file_uploader("Upload Video", type=["mp4", "avi", "mov"])
    if uploaded_file:
        st.video(uploaded_file)

# -- أزرار في الأسفل --
st.markdown("---")
col_btn1, col_btn2 = st.columns([1, 1])
with col_btn1:
    st.button("📋 Show Analysis Table")
with col_btn2:
    st.button("💾 Save Result")
vxgsgdg