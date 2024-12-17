import base64
import cv2
import streamlit as st
import time
from langchain_openai import ChatOpenAI
from PIL import Image, ImageDraw, ImageFont

def init_page():
    # ページ設定（UI非表示）
    st.set_page_config(page_title="自動画像セリフ生成", page_icon="🤖", layout="wide")
    st.markdown(
        """
        <style>
            [data-testid="stHeader"], [data-testid="stToolbar"], footer {display: none;}
            .block-container {padding: 0; margin: 0; max-width: 100%; overflow: hidden;}
            img {object-fit: cover;}
        </style>
        """, 
        unsafe_allow_html=True
    )
    

def create_image_with_text(text, width=1920, height=1080, font_size=80):
    # 背景色と文字色
    bg_color = (0, 0, 0)  # 黒
    text_color = (255, 255, 255)  # 白

    # 画像作成
    image = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(image)

    # フォント設定（ローカルパス）
    try:
        font_path = "C:/Users/flogt/OneDrive/ドキュメント/NotoSansCJKjp-Regular.otf"  # フォントパスを指定
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()  # フォントがない場合はデフォルトフォント

    # テキストサイズを計算し中央に配置
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2
    draw.text((text_x, text_y), text, fill=text_color, font=font)

    return image

def capture_image():
    cap = cv2.VideoCapture(0)  # カメラの初期化（デフォルトカメラ）

    if not cap.isOpened():
        st.error("カメラの起動に失敗しました。")
        return None

    # フレームをキャプチャするまでのループ処理
    start_time = time.time()
    while True:
        ret, frame = cap.read()
        if not ret:
            st.error("フレームの取得に失敗しました。カメラを確認してください。")
            break

        # 3秒後に自動的にキャプチャ
        if time.time() - start_time > 3:
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
                            "text": "この画像に写っている物が何かを推測し、それを擬人化したセリフのみを出力してください。それが難しいときは「セリフ生成不可能」と出力してください。人が写っている場合は「人間」が言いそうなセリフを出力してください。"
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

            
            try:
                response = llm.invoke(query)
                generated_text = response.content.strip()
            except Exception as e:
                st.error(f"生成中にエラーが発生しました: {e}")
                generated_text = "セリフ生成不可能"

            # セリフを画像に埋め込んで表示

            # テキスト入り画像生成
            image_with_text = create_image_with_text(generated_text)

            # Streamlitで表示
            st.image(image_with_text, use_container_width=True)

    # 最初の画像キャプチャまたは再キャプチャ
    if st.session_state.captured_frame is None:
        process_image()


if __name__ == '__main__':
    main()
