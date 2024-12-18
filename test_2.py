import streamlit as st
import time
import cv2
import numpy as np
from PIL import Image

st.set_page_config(page_title="自動カメラ撮影", page_icon="📸")

st.title("📸 自動カメラ撮影アプリ")
st.write("ページを開いてから3秒後に自動撮影します。")

# 初期状態の設定
if "captured_frame" not in st.session_state:
    st.session_state.captured_frame = None

# カメラ撮影機能
def capture_image():
    captured_frame = None  # 変数を初期化
    try:
        cap = cv2.VideoCapture(0)  # カメラを起動
        if not cap.isOpened():
            st.error("カメラが起動できませんでした。デバイスを確認してください。")
            return None

        st.write("カメラ起動中...")
        time.sleep(3)  # 3秒待機
        ret, frame = cap.read()
        cap.release()  # カメラリソースを解放

        if ret:
            captured_frame = frame
        else:
            st.error("画像を取得できませんでした。")

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")

    return captured_frame  # 初期化した変数を確実に返す

# 画像のキャプチャと表示
if st.session_state.captured_frame is None:
    st.session_state.captured_frame = capture_image()

if st.session_state.captured_frame is not None:
    # OpenCVの画像をPillow形式に変換
    image = Image.fromarray(cv2.cvtColor(st.session_state.captured_frame, cv2.COLOR_BGR2RGB))
    st.image(image, caption="自動撮影された画像", use_column_width=True)
