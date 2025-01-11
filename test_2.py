import streamlit as st

# カスタムCSSを適用してボタンを大きく変更
st.markdown(
    """
    <style>
    /* 切り替えボタンを大きくする */
    [data-testid="stBaseButton-minimal"] {
        width: 100px; /* 幅を変更 */
        height: 100px; /* 高さを変更 */
        font-size: 1.5rem; /* テキストサイズを大きく */
        border-radius: 10px; /* 角を丸める */
        background-color: #007BFF; /* 背景色を変更 */
        color: white; /* テキスト色を変更 */
        border: none; /* 枠線を非表示 */
        position: relative; /* 必要に応じて位置調整 */
        cursor: pointer; /* ポインタ表示 */
        display: flex; /* 中央揃えのためにflexを使用 */
        align-items: center;
        justify-content: center;
    }

    /* ボタンにホバー時のエフェクトを追加 */
    [data-testid="stBaseButton-minimal"]:hover {
        background-color: #0056b3; /* ホバー時の背景色 */
        transform: scale(1.1); /* ホバー時に拡大 */
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
