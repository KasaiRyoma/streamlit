import streamlit as st

# カメラ入力を使用
image = st.camera_input("Take a picture")

# 撮影された画像を表示
if image:
    st.image(image)
