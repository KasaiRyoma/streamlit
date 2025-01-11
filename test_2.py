import streamlit as st

# CSSでカメラ映像の中央に丸いボタンを配置
st.markdown(
    """
    <style>
    /* カメラ映像の親要素を相対配置に */
    [data-testid="stCameraInputWebcamStyledBox"] {
        position: relative; /* 子要素を正しく配置するため */
    }

    /* ボタンをカメラ映像の中央に配置 */
    .center-button {
        position: absolute;
        top: 50%; /* 親要素の垂直中央 */
        left: 50%; /* 親要素の水平中央 */
        transform: translate(-50%, -50%); /* 完全な中央揃え */
        width: 60px; /* ボタンの幅 */
        height: 60px; /* ボタンの高さ */
        border-radius: 50%; /* 丸い形状 */
        background-color: rgba(0, 0, 0, 0.6); /* 半透明の背景 */
        color: white; /* テキストやアイコンの色 */
        display: flex; /* 中央揃え用 */
        align-items: center;
        justify-content: center;
        cursor: pointer; /* ポインタ表示 */
        z-index: 999; /* カメラ映像の上に表示 */
    }

    /* ホバーエフェクト */
    .center-button:hover {
        background-color: rgba(0, 0, 0, 0.8); /* 濃い背景色 */
        transform: translate(-50%, -50%) scale(1.1); /* 拡大エフェクト */
    }

    /* SVGアイコンのサイズ調整 */
    .center-button svg {
        width: 30px;
        height: 30px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# HTMLでボタンを追加
st.markdown(
    """
    <div data-testid="stCameraInputWebcamStyledBox">
        <button class="center-button">
            <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                <rect width="24" height="24" fill="none"></rect>
                <path d="M20 5h-3.17l-1.24-1.35A1.99 1.99 0 0014.12 3H9.88c-.56 0-1.1.24-1.48.65L7.17 5H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm-1.35 8.35l-2.79 2.79c-.32.32-.86.1-.86-.35v-1.75H9v1.75c0 .45-.54.67-.85.35l-2.79-2.79c-.2-.2-.2-.51 0-.71l2.79-2.79a.5.5 0 01.85.36v1.83h6v-1.83c0-.45.54-.67.85-.35l2.79 2.79c.2.19.2.51.01.7z"></path>
            </svg>
        </button>
    </div>
    """,
    unsafe_allow_html=True,
)

# カメラ入力
image = st.camera_input("Take a picture")

# 撮影された画像を表示
if image:
    st.image(image)
