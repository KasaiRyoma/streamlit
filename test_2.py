import base64
import cv2
import streamlit as st
from langchain_openai import ChatOpenAI
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os  # ファイルパス操作のため

def init_page():
    # ページ設定（UI非表示と背景黒設定を含む）
    st.set_page_config(page_title="自動画像セリフ生成", page_icon="🤖", layout="wide")
    st.markdown(
        """
        <style>
            [data-testid="stHeader"], [data-testid="stToolbar"], footer {
                display: none;
            }
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

    # フォント設定（リポジトリ内のフォントを参照）
    try:
        font_path = os.path.join(os.path.dirname(__file__), "OtsutomeFont_Ver3_16.ttf")  # フォントパス
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

def main():
    init_page()

    llm = ChatOpenAI(
        temperature=0,
        model="gpt-4o",
        max_tokens=512
    )

    # セッションステートの初期化
    if 'captured_image' not in st.session_state:
        st.session_state.captured_image = None
        st.session_state.response = None

    # サイドバーで画像撮影
    st.sidebar.header("カメラで画像を撮影")
    camera_input = st.sidebar.camera_input("撮影してください")

    if camera_input:
        # 画像がアップロードされた場合
        st.session_state.captured_image = Image.open(BytesIO(camera_input.getvalue()))

        # 画像をバイナリ形式に変換
        buffered = BytesIO()
        st.session_state.captured_image.save(buffered, format="JPEG")
        image_base64 = base64.b64encode(buffered.getvalue()).decode()

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
                            "url": f"data:image/jpeg;base64,{image_base64}",
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

        # セリフを画像に埋め込む
        image_with_text = create_image_with_text(generated_text)

        # フルスクリーン表示用の画像エンコード
        buffered = BytesIO()
        image_with_text.save(buffered, format="JPEG")
        full_screen_base64 = base64.b64encode(buffered.getvalue()).decode()

        # Streamlitでフルスクリーン表示
        st.markdown(
            f"""
            <style>
                [data-testid="stHeader"], [data-testid="stToolbar"], footer {{
                    display: none;
                }}
            </style>
            <div style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; 
                        background-color: black; display: flex; 
                        justify-content: center; align-items: center; z-index: 1000; overflow: hidden;">
                <img src="data:image/jpeg;base64,{full_screen_base64}" alt="Captured Image" 
                     style="width: 100vw; height: 100vh; object-fit: cover;">
            </div>
            """,
            unsafe_allow_html=True,
        )

if __name__ == '__main__':
    main()
