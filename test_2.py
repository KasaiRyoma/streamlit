import streamlit as st

# カスタムCSSを適用してボタンをカメラ映像の中央に配置


# カメラ入力
image = st.camera_input("Take a picture")

# 撮影された画像を表示
if image:
    st.image(image)

custom_css = """
<style>
    /* カメラ映像をフルスクリーン表示に調整 */
    div[data-testid="stCameraInputWebcamComponent"] video {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        object-fit: cover;
        z-index: 1;
        opacity: 1; /* 映像を表示 */
    }
    /* 撮影ボタンをフルスクリーンに拡張 */
    div[data-testid="stBaseButton-minimal"] {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        opacity: 0;
        z-index: 2;
        cursor: pointer;
    }
    /* コンテナの背景色を調整 */
    div[data-testid="stCameraInputWebcamComponent"] {
        background-color: black;
        z-index: 1;
        opacity: 1; /* コンテナを表示 */
    }

    /* ヘッダーを非表示にする */
    header[data-testid="stHeader"] {
        display: none !important;
    }

    /* カメラ入力の全体コンテナを表示 */
    div[data-testid="stCameraInput"] {
        opacity: 1; /* カメラ入力を表示 */
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)
