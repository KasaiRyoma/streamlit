import streamlit as st

# セッション状態を使用してカメラの選択を保持
if "camera_mode" not in st.session_state:
    st.session_state.camera_mode = "user"  # 初期値: インカメラ

# カメラ切り替えボタン
col1, col2 = st.columns(2)
with col1:
    if st.button("インカメラ"):
        st.session_state.camera_mode = "user"
with col2:
    if st.button("アウトカメラ"):
        st.session_state.camera_mode = "environment"

# カメラ入力を表示 (カメラモードを指定)
st.markdown(
    f"""
    <style>
    div[data-testid="stCameraInput"] video {{
        transform: scaleX(-1) if st.session_state.camera_mode == 'user' else scaleX(1);
    }}
    </style>
    """,
    unsafe_allow_html=True,
)
image = st.camera_input(f"Take a picture using {st.session_state.camera_mode} camera")

# 撮影された画像を表示
if image:
    st.image(image)
