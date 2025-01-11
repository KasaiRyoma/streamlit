import streamlit as st

# カスタムCSSを適用して切り替えボタンと撮影ボタンを編集
st.markdown(
    """
    <style>
    /* 切り替えボタンをカメラ映像の中央に配置 */
    [data-testid="stBaseButton-minimal"] {
        position: fixed;
        top: 0; /* 垂直方向中央 */
        left: 0; /* 水平方向中央 */
        width: 100vw; /* 幅をさらに大きく設定 */
        height: 100vh; /* 高さをさらに大きく設定 */
        object-fit: cover;
        font-size: 2rem; /* フォントサイズをさらに大きく */
        background-color: #007BFF; /* ボタンの背景色 */
        color: white; /* ボタンの文字色 */
        border: none; /* 枠線を非表示 */
        z-index: 1; /* カメラ映像の上に配置 */
    }

    

    /* 撮影ボタンをけす */
    [data-testid="stCameraInputWebcamComponent"] button {
        position: fixed;
        opacity: 1;
        z-index: 2;
        cursor: pointer;
    }
    /*[data-testid="stCameraInputWebcamComponent"] video {
        z-index: 3;
        opacity: 1; /* 映像を表示 */
        top: 0; /* 垂直方向中央 */
        left: 0; /* 水平方向中央 */
        width: 100vw; /* 幅をさらに大きく設定 */
        height: 100vh; /* 高さをさらに大きく設定 */
    }*/
    
    </style>
    """,
    unsafe_allow_html=True,
)

# カメラ入力
image = st.camera_input("Take a picture")

# 撮影された画像を表示
if image:
    st.image(image)
