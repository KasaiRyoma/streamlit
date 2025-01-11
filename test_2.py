import streamlit as st
import base64

# 状態管理
if "captured_image" not in st.session_state:
    st.session_state.captured_image = None

# フルスクリーン表示のHTML
def show_fullscreen_image(image_data):
    # バイナリデータを Base64 に変換
    image_base64 = base64.b64encode(image_data).decode("utf-8")
    st.markdown(
        f"""
        <div style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; 
                    background-color: black; display: flex; 
                    justify-content: center; align-items: center; z-index: 1000; overflow: hidden;">
            <img src="data:image/jpeg;base64,{image_base64}" alt="Captured Image" 
                 style="width: 100vw; height: 100vh; object-fit: cover;">
        </div>
        """,
        unsafe_allow_html=True,
    )

# カメラ入力
st.write("画面全体をクリックして写真を撮影します。")
camera_image = st.camera_input("")

if camera_image:
    # 撮影した画像をセッションに保存
    st.session_state.captured_image = camera_image.getvalue()

# 撮影された画像がある場合にフルスクリーン表示
if st.session_state.captured_image:
    show_fullscreen_image(st.session_state.captured_image)

# CSSの追加（カメラ切り替えボタンを表示）
custom_css = """
<style>
    /* カメラ映像をフルスクリーン表示に調整 */
    div[data-testid="stCameraInputWebcamComponent"] video {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        object-fit: cover;
        z-index: 1;
        opacity: 0;
    }

    /* 撮影ボタンをフルスクリーンに拡張 */
    div[data-testid="stCameraInputWebcamComponent"] button {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        opacity: 0;
        z-index: 2;
        cursor: pointer;
    }

    /* カメラ切り替えボタンのみ表示 */
    div[data-testid="stCameraInputWebcamComponent"] button[data-testid="toggleCameraButton"] {
        position: relative;
        opacity: 1 !important;
        z-index: 3 !important;
        background-color: white !important;
        color: black !important;
        border: 1px solid black !important;
        width: auto;
        height: auto;
    }

    /* コンテナの背景色を調整 */
    div[data-testid="stCameraInputWebcamComponent"] {
        background-color: black;
        opacity: 0;
        z-index: 1;
    }

    /* ヘッダーを非表示にする */
    header[data-testid="stHeader"] {
        display: none !important;
    }

    /* 指定された <div> を非表示 */
    div[data-testid="stCameraInput"] {
        opacity: 0;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)
