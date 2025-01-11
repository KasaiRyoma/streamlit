import streamlit as st

# ページ設定
st.set_page_config(layout="wide", page_title="フルスクリーンカメラ", page_icon="📸")

# カスタムCSSとJavaScript
st.markdown(
    """
    <style>
    /* フルスクリーンボタンをカメラ映像の中央に配置 */
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
    }

    /* ホバー時のエフェクト */
    [data-testid="stBaseButton-minimal"]:hover {
        background-color: #0056b3; /* ホバー時の背景色 */
        transform: translate(-50%, -50%) scale(1.1); /* 拡大エフェクト */
    }

    /* カメラフィードの透明化 */
    [data-testid="stCameraInput"] {
        background-color: transparent;
    }

    /* ストリームリットヘッダーを非表示 */
    header[data-testid="stHeader"] {
        display: none;
    }

    /* ページ全体をフルスクリーン化 */
    body {
        margin: 0;
        padding: 0;
        overflow: hidden;
    }
    </style>

    <script>
    // フルスクリーンモードを切り替える関数
    function toggleFullscreen() {
        const elem = document.documentElement;
        if (!document.fullscreenElement) {
            elem.requestFullscreen();
        } else {
            if (document.exitFullscreen) {
                document.exitFullscreen();
            }
        }
    }
    </script>
    """,
    unsafe_allow_html=True,
)

# カメラ入力
image = st.camera_input("Take a picture")

# フルスクリーンボタン
st.button(
    "Toggle Fullscreen",
    on_click=None,
    args=None,
    kwargs=None,
    type="primary",
    key="fullscreen_button",
)

# 撮影された画像を表示
if image:
    st.image(image, use_column_width=True)
