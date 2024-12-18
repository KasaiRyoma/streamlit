import base64
import cv2
import streamlit as st
import time
from langchain_openai import ChatOpenAI

def init_page():
    st.set_page_config(
        page_title="画像から生成",
        page_icon="🤖"
    )
    st.header("生成")

def capture_image():
    cap = cv2.VideoCapture(0)  # カメラの初期化（デフォルトカメラ）

    if not cap.isOpened():
        st.error("カメラの起動に失敗しました。")
        return None

    st.write("カメラが正常に起動しました。3秒後に画像をキャプチャします。")

    # ウェブカメラの映像を表示（カメラが起動中であることを確認）
    frame_window = st.image([])

    # フレームをキャプチャするまでのループ処理
    start_time = time.time()
    while True:
        ret, frame = cap.read()
        if not ret:
            st.error("フレームの取得に失敗しました。カメラを確認してください。")
            break

        # フレームを表示
        frame_window.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # 3秒後に自動的にキャプチャ
        if time.time() - start_time > 3:
            st.write("3秒経過。画像をキャプチャします。")
            captured_frame = frame  # 現在のフレームをキャプチャ
            break

    # カメラを解放
    cap.release()

    return captured_frame

def main():
    init_page()

    llm = ChatOpenAI(
        temperature=0,
        model="gpt-4o",
        max_tokens=512
    )

    # セッションステートの初期化
    if 'captured_frame' not in st.session_state:
        st.session_state.captured_frame = None
        st.session_state.response = None

    # 画像をキャプチャしてセリフを生成する処理
    def process_image():
        st.session_state.captured_frame = capture_image()
        if st.session_state.captured_frame is not None:
            # キャプチャした画像を表示
            st.image(cv2.cvtColor(st.session_state.captured_frame, cv2.COLOR_BGR2RGB), caption="キャプチャされた画像")

            # キャプチャした画像を処理
            _, img_encoded = cv2.imencode('.jpg', st.session_state.captured_frame)
            image_base64 = base64.b64encode(img_encoded).decode()
            image_data_url = f"data:image/jpeg;base64,{image_base64}"

            # 自動的に画像内容を分析
            query = [
                (
                    "user",
                    [
                        {
                            "type": "text",
                            "text": "この画像に写っている物が何かを推測し、それを擬人化したセリフのみを出力してください。それが難しいときは「セリフ生成不可能」と出力してください。人が写っている場合は「人物検出」と出力してください。"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_data_url,
                                "detail": "auto"
                            },
                        }
                    ]
                )
            ]

            st.markdown("### 出力")
            try:
                st.session_state.response = llm.stream(query)
                st.write(st.session_state.response)
            except Exception as e:
                st.error(f"生成中にエラーが発生しました: {e}")

    # 最初の画像キャプチャまたは再キャプチャ
    if st.session_state.captured_frame is None:
        process_image()

    # もう一度キャプチャするボタン
    if st.button("もう一度キャプチャ"):
        st.session_state.captured_frame = None  # 画像をクリア
        st.session_state.response = None  # 出力をクリア
        st.write("新しい画像をキャプチャします...")
        process_image()

if __name__ == '__main__':
    main()
