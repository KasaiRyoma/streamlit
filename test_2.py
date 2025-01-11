import streamlit as st

# カスタムCSSを適用して映像とボタンを適切に配置
st.markdown(
    """
    <style>
    /* カメラ映像をフルスクリーン表示 */
    div[data-testid="stCameraInputWebcamComponent"] video {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        object-fit: cover;
        z-index: 1; /* 映像を最下層に配置 */
    }

    /* カメラ切り替えボタンを表示 */
    div[data-testid="stCameraInputWebcamComponent"] select {
        position: fixed;
        bottom: 10%; /* 画面下部に配置 */
        left: 50%; /* 水平方向中央 */
        transform: translateX(-50%); /* 中央揃え調整 */
        z-index: 2; /* 映像の上に配置 */
        background-color: rgba(255, 255, 255, 0.8); /* 背景色と透明度 */
        border: 1px solid #ccc; /* ボーダー */
        padding: 5px 10px; /* 余白 */
        border-radius: 5px; /* 角丸 */
        font-size: 1rem; /* フォントサイズ */
        cursor: pointer; /* ポインタ */
    }

    /* コンテナ全体の背景を非表示に調整 */
    div[data-testid="stCameraInputWebcamComponent"] {
        background-color: black;
        opacity: 1;
        z-index: 1;
    }

    /* カメラ入力全体コンテナを表示 */
    div[data-testid="stCameraInput"] {
        opacity: 1;
    }

    /* ヘッダーを非表示にする */
    header[data-testid="stHeader"] {
        display: none !important;
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
