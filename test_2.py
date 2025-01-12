import base64
import streamlit as st
from langchain_openai import ChatOpenAI
from PIL import Image
from io import BytesIO

def load_font_as_base64(font_path):
    with open(font_path, "rb") as font_file:
        font_data = font_file.read()
    return base64.b64encode(font_data).decode("utf-8")

def init_page():
    # フォントファイルをBase64形式に変換（同じディレクトリに配置）
    font_base64 = load_font_as_base64("OtsutomeFont_Ver3_16.ttf")

    # ページ設定（UI非表示と背景黒設定を含む）
    st.set_page_config(page_title="自動画像セリフ生成", page_icon="🤖", layout="wide")
    st.markdown(
        f"""
        <style>
            @font-face {{
                font-family: 'OtsutomeFont';
                src: url(data:font/ttf;base64,{font_base64}) format('truetype');
            }}

            /* ヘッダー、ツールバー、フッターを非表示 */
            [data-testid="stHeader"], [data-testid="stToolbar"], footer {{
                display: none;
            }}

            /* アプリ全体の背景を黒に設定 */
            [data-testid="stAppViewContainer"] {{
                background-color: black;
                color: white;
            }}

            /* メインコンテナの背景も黒に設定 */
            [data-testid="stMain"] {{
                background-color: black;
                color: white;
            }}

            /* テキスト要素の色を白に設定 */
            .stMarkdown, .stText {{
                color: white;
            }}

            /* テキストの中央揃え */
            .centered-text {{
                display: flex;
                justify-content: center;
                align-items: center;
                height: 70vh;
                font-size: 2em; /* 任意のサイズに変更可能 */
                text-align: center;
                font-family: 'OtsutomeFont', sans-serif; /* OtsutomeFont を使用 */
            }}
        </style>
        """, 
        unsafe_allow_html=True
    )

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

        # セリフを中央揃えで任意のフォントと大きさで表示
        st.markdown(
            f"""
            <div class="centered-text">
                {generated_text}
            </div>
            """,
            unsafe_allow_html=True
        )

if __name__ == '__main__':
    main()
