import streamlit as st

# カメラ入力
st.write("画面全体をクリックして写真を撮影します。")

camera_image = st.camera_input("")

if camera_image:
    st.image(camera_image, caption="撮影された画像", use_column_width=True)

# 撮影ボタンを透明にし、カメラ映像および特定の <img> 要素を透明にするCSS
custom_css = """
<style>
    /* カメラ映像を透明にする */
    div[data-testid="stCameraInputWebcamComponent"] video {
        opacity: 0;
    }

    /* 撮影後もカメラ映像のコンテナを透明にする */
    div[data-testid="stCameraInputWebcamComponent"] {
        opacity: 0;
    }

    /* 撮影ボタンを全画面に拡大し透明化 */
    button[data-testid="stCameraInputButton"] {
        position: absolute;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        opacity: 0;
        z-index: 1000;
        cursor: pointer;
    }

    /* 特定の <img> 要素を透明にする */
    img[src^="data:image/jpeg;base64,"][alt="Snapshot"] {
        opacity: 0;
    }
</style>
"""

# CSSを適用
st.markdown(custom_css, unsafe_allow_html=True)
