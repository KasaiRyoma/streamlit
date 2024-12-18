import base64
import cv2
import streamlit as st
import time

def init_page():
    st.set_page_config(
        page_title="カメラ起動",
        page_icon="🤖"
    )
    st.header("カメラ")

def capture_image():
    cap = cv2.VideoCapture(0) 
    frame_window = st.image([])
    start_time = time.time()
    while True:
        ret, frame = cap.read()
        if not ret:
            st.error("フレームの取得に失敗しました。カメラを確認してください。")
            break
        
        frame_window.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if time.time() - start_time > 3:
            st.write("3秒経過。画像をキャプチャします。")
            captured_frame = frame  
            break

    cap.release()

    return captured_frame

def process_image():
        st.session_state.captured_frame = capture_image()
        if st.session_state.captured_frame is not None:
            st.image(cv2.cvtColor(st.session_state.captured_frame, cv2.COLOR_BGR2RGB), caption="キャプチャされた画像")


def main():
    init_page()
    process_image()

main()
