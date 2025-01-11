import streamlit as st

# カスタムCSSを適用してデフォルトのボタンをカメラ映像の中央に配置
st.markdown(
    """
    <style>
    /* デフォルトボタンをスタイリング */
    [data-testid="stBaseButton-minimal"] {
        position: absolute; /* ボタンを絶対位置に */
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
        z-index: 999; /* カメラ映像の上に表示 */
        border: none; /* 枠線を非表示 */
        cursor: pointer; /* ポインタ表示 */
    }

    /* ボタンのホバー時の効果 */
    [data-testid="stBaseButton-minimal"]:hover {
        background-color: rgba(0, 0, 0, 0.8); /* 背景色を濃くする */
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
