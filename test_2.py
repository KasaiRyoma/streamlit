import streamlit as st

# カスタムCSSを適用してボタンをカメラ映像の中央に配置
st.markdown(
    """
    <style>
    /* ボタンの親要素のスタイル調整 */
    [data-testid="stCameraInputWebcamStyledBox"] {
        position: relative; /* 子要素の絶対配置を可能に */
    }

    /* SVGボタンを中央に配置 */
    .st-emotion-cache-clky9d {
        position: absolute;
        top: 50%; /* 親要素の垂直方向の中央 */
        left: 50%; /* 親要素の水平方向の中央 */
        transform: translate(-50%, -50%); /* 完全に中央揃え */
        width: 50px; /* ボタンの幅を調整 */
        height: 50px; /* ボタンの高さを調整 */
        cursor: pointer; /* ポインタを表示 */
        background-color: rgba(0, 0, 0, 0.6); /* 半透明の背景を追加 */
        border-radius: 50%; /* 丸いボタン */
        display: flex; /* アイコンの中央揃え */
        align-items: center;
        justify-content: center;
    }

    /* SVGのアイコンサイズを調整 */
    .st-emotion-cache-clky9d svg {
        width: 24px; /* SVGアイコンの幅 */
        height: 24px; /* SVGアイコンの高さ */
        fill: #ffffff; /* アイコンの色 */
    }

    /* ホバー時のエフェクト */
    .st-emotion-cache-clky9d:hover {
        background-color: rgba(0, 0, 0, 0.8); /* ホバー時に濃い背景色 */
        transform: translate(-50%, -50%) scale(1.1); /* 拡大アニメーション */
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
