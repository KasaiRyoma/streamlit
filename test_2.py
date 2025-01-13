import base64
import time
import streamlit as st
import random
from langchain_openai import ChatOpenAI
from PIL import Image
from io import BytesIO

# フォントをBase64形式で読み込む関数
def load_font_as_base64(font_path):
    with open(font_path, "rb") as font_file:
        font_data = font_file.read()
    return base64.b64encode(font_data).decode("utf-8")

#音声を再生する関数
@st.cache_data
def load_audio_as_base64(audio_path):
    with open(audio_path, "rb") as audio_file:
        audio_base64 = base64.b64encode(audio_file.read()).decode()
        audio_html = f"""
        <audio autoplay=True>
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            Your browser does not support the audio element.
        </audio>
        """
        return audio_html


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

            /* サイドバーの背景色と文字色を初期状態に戻す */
            [data-testid="stSidebar"] {
                color: initial;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

def main():
    init_page()
    if "sound_a" not in st.session_state:
        st.session_state.sound_a = load_audio_as_base64("./audio/akarui.mp3")
        st.session_state.sound_b = load_audio_as_base64("./audio/kurai.mp3")
        st.session_state.sound_c = load_audio_as_base64("./audio/omosiro.mp3")
        st.session_state.sound_d = load_audio_as_base64("./audio/horror.mp3")
        time.sleep(1.0)

    llm = ChatOpenAI(
        temperature=0,
        model="gpt-4o",
        max_tokens=512
    )

    # サイドバー
    st.sidebar.header("オプション")

    # 文字数選択
    text_length = st.sidebar.selectbox(
        "文字数", [50, 100, 150, 200, "ランダム"], index=1
    )
    if text_length == "ランダム":
        text_length = random.choice([50, 100, 150, 200])

    # 雰囲気選択
    mood = st.sidebar.selectbox(
        "雰囲気", ["明るい", "暗い", "コメディ", "ホラー", "ランダム", ], index=0
    )
    if mood == "ランダム":
        mood = random.choice(["明るい", "暗い", "コメディ", "ホラー"])

    # フォントサイズ
    font_size = st.sidebar.selectbox(
        "フォントサイズ", ["小", "中", "大"], index=1
    )

    # 音声選択
    sound_f = st.sidebar.radio(
        "効果音", ["オン", "オフ"], index=1
    )

    kana = st.sidebar.radio(
    "ひらがなモード", ["オン", "オフ"], index=1
    )
    
    # カメラで画像撮影
    camera_input = st.sidebar.camera_input("撮影してください")

    if camera_input:
        # 画像がアップロードされた場合
        captured_image = Image.open(BytesIO(camera_input.getvalue()))

        # 画像をバイナリ形式に変換
        buffered = BytesIO()
        captured_image.save(buffered, format="JPEG")
        image_base64 = base64.b64encode(buffered.getvalue()).decode()

        # 1つ目のクエリ：画像の内容を分析
        
        query1_text =f"この画像には何が写っていますか？単語で答えてください。またこの画像の明るさや場所、時間帯についても単語で答えてください。単語以外の文章は絶対に出力しないでください。"
        query1 = [
            (
                "user",
                [
                    {
                        "type": "text",
                        "text": query1_text
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


        response1 = llm.invoke(query1)
        result1 = response1.content.strip()  # 1つ目のクエリの結果


        # 2つ目のクエリ：1つ目のクエリ結果を使用した質問
        if kana == "オン":
            query2_text = f"'{result1}'を用いた物語を{text_length}字程度で考えなさい。出力は物語のみとすること。可能であればその状況にあった絵文字などを用いること。'{result1}'以外のものはできるだけ話に登場させないこと。物語の雰囲気は{mood}にしてください。漢字は使わずにすべてひらがなで出力してください。"
        else:
            query2_text = f"'{result1}'を用いた物語を{text_length}字程度で考えなさい。出力は物語のみとすること。可能であればその状況にあった絵文字などを用いること。'{result1}'以外のものはできるだけ話に登場させないこと。物語の雰囲気は{mood}にしてください。"
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

        response2 = llm.invoke(query2)
        result2 = response2.content.strip()  # 2つ目のクエリの結果

        # フォントサイズと行間を文字数に応じて調整
        if font_size == "小":
            if text_length == 50:
                font_size = "2.9em"
                line_height = "1.5"
            elif text_length == 100:
                font_size = "2.3em"
                line_height = "1.3"
            elif text_length == 150:
                font_size = "2.0em"
                line_height = "1.0"
            else:  # 200文字
                font_size = "1.8em"
                line_height = "1.0"
        elif font_size == "中":
            if text_length == 50:
                font_size = "6.0em"
                line_height = "1.5"
            elif text_length == 100:
                font_size = "4.3em"
                line_height = "1.3"
            elif text_length == 150:
                font_size = "3.7em"
                line_height = "1.0"
            else:  # 200文字
                font_size = "3.5em"
                line_height = "1.0"
        else:
            if text_length == 50:
                font_size = "7.0em"
                line_height = "1.5"
            elif text_length == 100:
                font_size = "5.3em"
                line_height = "1.3"
            elif text_length == 150:
                font_size = "4.4em"
                line_height = "1.0"
            else:  # 200文字
                font_size = "4.2em"
                line_height = "1.0"

        # フォントを雰囲気に応じて選択
        if mood == "明るい":
            font_base64 = load_font_as_base64("./font/001Shirokuma-Regular.otf")
        elif mood == "暗い":
            font_base64 = load_font_as_base64("./font/OtsutomeFont_Ver3_16.ttf")
        elif mood == "コメディ":
            font_base64 = load_font_as_base64("./font/pugnomincho-mini.otf")
        else:  # ホラー
            font_base64 = load_font_as_base64("./font/ibaraji04.ttf")

        # CSSを動的に生成
        st.markdown(
            f"""
            <style>
                @font-face {{
                    font-family: 'DynamicFont';
                    src: url(data:font/ttf;base64,{font_base64}) format('truetype');
                }}
                .dynamic-text {{
                    font-family: 'DynamicFont', sans-serif;
                    display: flex; 

                    height: 70vh; /* 高さを画面全体に設定 */
                    align-items: center;                                                
                    font-size: {font_size};
                    line-height: {line_height};
                }}
            </style>
            """,
            unsafe_allow_html=True
        )

        # 結果を表示
        st.markdown(
            f"""
            <div class="dynamic-text">
                {result2}
            </div>
            """,
            unsafe_allow_html=True
        )

        
        if sound_f == "オン":
            audio_placeholder = st.empty()
            audio_placeholder.empty()
            time.sleep(0.5) #これがないと上手く再生されません
            if mood == "明るい":
                audio_placeholder.markdown(st.session_state.sound_a, unsafe_allow_html=True)
            elif mood == "暗い":
                audio_placeholder.markdown(st.session_state.sound_b, unsafe_allow_html=True)     
            elif mood == "コメディ":
                audio_placeholder.markdown(st.session_state.sound_c, unsafe_allow_html=True)
            elif mood == "ホラー":
                audio_placeholder.markdown(st.session_state.sound_d, unsafe_allow_html=True)       

if __name__ == '__main__':
    main()
