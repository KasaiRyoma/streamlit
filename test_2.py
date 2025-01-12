import base64
import os
import streamlit as st
from langchain_openai import ChatOpenAI
from PIL import Image
from io import BytesIO

# フォントをBase64形式で読み込む関数
def load_font_as_base64(font_path):
    with open(font_path, "rb") as font_file:
        font_data = font_file.read()
    return base64.b64encode(font_data).decode("utf-8")

# ページの初期化
def init_page():
    # ページ設定（UI非表示と背景黒設定を含む）
    st.set_page_config(page_title="自動画像セリフ生成", page_icon="🤖", layout="wide")
    st.markdown(
        """
        <style>
            /* ヘッダー、ツールバー、フッター非表示 */
            [data-testid="stHeader"], [data-testid="stToolbar"], footer {
                display: none;
            }

            /* アプリ全体の背景黒*/
            [data-testid="stAppViewContainer"] {
                background-color: black;
                color: white;
            }

            /* メインコンテナの背景黒*/
            [data-testid="stMain"] {
                background-color: black;
                color: white;
            }

            /* テキスト色を白*/
            .stMarkdown, .stText {
                color: white;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

def main():
    init_page()

    # フォントファイルをBase64形式で読み込み
    font_a = os.path.abspath("font/OtsutomeFont_Ver3_16.ttf")
    font_b = os.path.abspath("font/NotoSansCJKjp-Regular.otf")  # 暗いとき

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

                # 1つ目のクエリ：画像の内容を分析
        query1 = [
            (
                "user",
                [
                    {
                        "type": "text",
                        "text": "この画像には何が写っていますか？単語で答えてください。"
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
            response1 = llm.invoke(query1)
            result1 = response1.content.strip()  # 1つ目のクエリの結果
        except Exception as e:
            st.error(f"1つ目の生成中にエラーが発生しました: {e}")
            result1 = "不明"

        # 2つ目のクエリ：1つ目のクエリ結果を使用した質問
        query2_text = f"'{result1}'を用いた物語を200字程度で考えなさい。出力は物語のみとすること。可能であればその状況にあった絵文字などを用いること。物語の雰囲気は明るい、悲しい、怖い、面白いからランダムで選んでください。"
        query2 = [
            (
                "user",
                [
                    {
                        "type": "text",
                        "text": query2_text
                    }
                ]
            )
        ]

        try:
            response2 = llm.invoke(query2)
            result2 = response2.content.strip()  # 2つ目のクエリの結果
        except Exception as e:
            st.error(f"2つ目の生成中にエラーが発生しました: {e}")
            result2 = "result2 error"

        # 3つ目のクエリ：2つ目のクエリ結果を使用した質問
        query3_text = f"物語'{result2}'は暗いですが明るいですか。暗い か 明るい か 不明 で答えなさい。それ以外の文字や記号を出力してはいけません。"
        query3 = [
            (
                "user",
                [
                    {
                        "type": "text",
                        "text": query3_text
                    }
                ]
            )
        ]

        try:
            response3 = llm.invoke(query3)
            result3 = response3.content.strip()  # 2つ目のクエリの結果
        except Exception as e:
            st.error(f"2つ目の生成中にエラーが発生しました: {e}")
            result3 = "result3 error"

        # CSSを動的に生成
        if result3 == "明るい":
            font = font_a
        elif result3 == "暗い":
            font = font_b
        else:
            font = None  # デフォルトフォント使用

        if font:
            st.markdown(
                f"""
                <style>
                    @font-face {{
                        font-family: 'DynamicFont';
                        src: url('font/OtsutomeFont_Ver3_16.ttf') format('truetype');
                    }}
                    .dynamic-text {{
                        font-family: 'DynamicFont', sans-serif;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 70vh; /* 高さを画面全体に設定 */
                        font-size: 2em; /* 任意のサイズに変更可能 */
                        text-align: center;
                        line-height: 4.0;
                    }}
                </style>
                """,
                unsafe_allow_html=True
            )

            font_class = "dynamic-text"
        else:
            font_class = ""  # デフォルトフォント使用

        # 結果を表示
        st.markdown(
            f"""
            <div class="{font_class}">
                {result2}
            </div>
            """,
            unsafe_allow_html=True
        )

if __name__ == '__main__':
    main()
