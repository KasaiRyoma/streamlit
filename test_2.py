import streamlit as st

# カスタムCSSを適用してカメラボタンを全画面に配置し、透明化
st.markdown(
    """
    <style>
    /* ボタンを全画面に配置して透明化 */
    [data-testid="stBaseButton-minimal"] {
        position: absolute;
        top: 0;
        left: 0;
        width: 100vw; /* 画面全体の幅 */
        height: 100vh; /* 画面全体の高さ */
        opacity: 0; /* ボタンを透明にする */
        z-index: 999; /* 最前面に配置 */
        cursor: pointer; /* ポインタの見た目を維持 */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# カメラ入力を使用
image = st.camera_input("Take a picture")

# 撮影された画像を表示
if image:
    st.image(image)
