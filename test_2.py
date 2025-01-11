import streamlit as st

# カスタムCSSを適用してボタンをカメラ映像の中央に配置
st.markdown(
    """
    <style>
    /* 切り替えボタンをカメラ映像の中央に配置 */
    [data-testid="stBaseButton-minimal"] {
        position: absolute;
        top: 50%; /* 垂直方向中央 */
        left: 50%; /* 水平方向中央 */
        transform: translate(-50%, -50%); /* 中央揃え調整 */
        width: 2000px; /* 幅をさらに大きく設定 */
        height: 2000px; /* 高さをさらに大きく設定 */
        font-size: 2rem; /* フォントサイズをさらに大きく */
        border-radius: 50%; /* 丸いボタン */
        background-color: #007BFF; /* ボタンの背景色 */
        color: white; /* ボタンの文字色 */
        border: none; /* 枠線を非表示 */
        cursor: pointer; /* ポインタ表示 */
        display: flex; /* 中央揃え用 */
        align-items: center;
        justify-content: center;
        z-index: 999; /* カメラ映像の上に配置 */
        opacity: 0; /* 初期状態で透明 */
    }

    /* ホバー時のエフェクト */
    [data-testid="stBaseButton-minimal"]:hover {
        background-color: #0056b3; /* ホバー時の背景色 */
        transform: translate(-50%, -50%) scale(1.1); /* 拡大エフェクト */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

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
