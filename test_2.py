import streamlit as st

# カスタムCSSを適用して切り替えボタンと撮影ボタンを編集
st.markdown(
    """
    <style>
    /* 切り替えボタンをカメラ映像の中央に配置 */
    [data-testid="stBaseButton-minimal"] {
        position: fixed;
        top: 50%; /* 垂直方向中央 */
        left: 50%; /* 水平方向中央 */
        transform: translate(-50%, -50%); /* 中央揃え調整 */
        width: 100vw; /* 幅をさらに大きく設定 */
        height: 100vh; /* 高さをさらに大きく設定 */
        font-size: 2rem; /* フォントサイズをさらに大きく */
        background-color: #007BFF; /* ボタンの背景色 */
        color: white; /* ボタンの文字色 */
        border: none; /* 枠線を非表示 */
        cursor: pointer; /* ポインタ表示 */
        display: flex; /* 中央揃え用 */
        align-items: center;
        justify-content: center;
        z-index: 999; /* カメラ映像の上に配置 */
    }

    /* ホバー時のエフェクト */
    [data-testid="stBaseButton-minimal"]:hover {
        background-color: #0056b3; /* ホバー時の背景色 */
        transform: translate(-50%, -50%) scale(1.1); /* 拡大エフェクト */
    }

    /* 撮影ボタンをけす */
    [data-testid="stCameraInputWebcamComponent"] button {
        position: fixed;
        opacity: 0;
        z-index: 2;
        cursor: pointer;
    }
    [data-testid="stCameraInputWebcamComponent"] video {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 1;
        opacity: 1; /* 映像を表示 */
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
