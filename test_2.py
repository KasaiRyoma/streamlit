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

    # フォントファイルをBase64形式で読み込み
    font_a_base64 = load_font_as_base64("./font/001Shirokuma-Regular.otf")  # 明るいとき
    font_b_base64 = load_font_as_base64("./font/OtsutomeFont_Ver3_16.ttf")  # 暗いとき
    font_c_base64 = load_font_as_base64("./font/pugnomincho-mini.otf")  # オプション3
    font_d_base64 = load_font_as_base64("./font/ibaraji04.ttf")  # オプション4

    sound_a = load_audio_as_base64("./audio/akarui.mp3")
    sound_b = load_audio_as_base64("./audio/kurai.mp3")
    sound_c = load_audio_as_base64("./audio/omosiro.mp3")
    sound_d = load_audio_as_base64("./audio/horror.mp3")

   

    llm = ChatOpenAI(
        temperature=0,
        model="gpt-4o",
        max_tokens=512
    )

    # セッションステートの初期化
    if 'captured_image' not in st.session_state:
        st.session_state.captured_image = None
        st.session_state.response = None

    # サイドバー
    st.sidebar.header("オプション")

    # 文字数選択
    text_length = st.sidebar.selectbox(
        "文字数を選択してください", [50, 100, 150, 200, "ランダム"], index=1
    )

    if text_length == "ランダム":
        text_length = random.choice([50, 100, 150, 200])

    # 雰囲気選択
    mood = st.sidebar.selectbox(
        "雰囲気を選択してください", ["明るい", "暗い", "コメディ", "ホラー", "ランダム", ], index=0
    )

    if mood == "ランダム":
        mood = random.choice(["明るい", "暗い", "コメディ", "ホラー"])

    # 音声選択
    sound_f = st.sidebar.radio(
        "効果音", ["オン", "オフ"], index=1
    )

    kana = st.sidebar.radio(
    "ひらがなモード", ["オン", "オフ"], index=1
    )
    
    # カメラで画像撮影
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
        
        query1_txt =f"この画像には何が写っていますか？単語で答えてください。またこの画像の明るさや場所、時間帯についても単語で答えてください。"
        query1 = [
            (
                "user",
                [
                    {
                        "type": "text",
                        "text": query1_txt
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

        try:
            response2 = llm.invoke(query2)
            result2 = response2.content.strip()  # 2つ目のクエリの結果
        except Exception as e:
            st.error(f"2つ目の生成中にエラーが発生しました: {e}")
            result2 = "result2 error"

        # フォントサイズと行間を文字数に応じて調整
        if text_length == 50:
            font_size = "3em"
            line_height = "1.5"
        elif text_length == 100:
            font_size = "2.5em"
            line_height = "1.3"
        elif text_length == 150:
            font_size = "1.8em"
            line_height = "1.2"
        else:  # 200文字
            font_size = "1.7em"
            line_height = "1.0"

        # フォントを雰囲気に応じて選択
        if mood == "明るい":
            font_base64 = font_a_base64
        elif mood == "暗い":
            font_base64 = font_b_base64
        elif mood == "コメディ":
            font_base64 = font_c_base64
        else:  # ホラー
            font_base64 = font_d_base64

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
                    justify-content: center;
                    align-items: center;
                    height: 70vh; /* 高さを画面全体に設定 */
                    font-size: {font_size};
                    text-align: center;
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

        audio_placeholder = st.empty()

        if sound_f == "オン" and mood == "明るい":
            audio_placeholder.empty()
            time.sleep(0.5) #これがないと上手く再生されません
            audio_placeholder.markdown(sound_a, unsafe_allow_html=True)
        elif sound_f == "オン" and mood == "暗い":
            audio_placeholder.empty()
            time.sleep(0.5) 
            audio_placeholder.markdown(sound_b, unsafe_allow_html=True)     
        elif sound_f == "オン" and mood == "コメディ":
            audio_placeholder.empty()
            time.sleep(0.5) 
            audio_placeholder.markdown(sound_c, unsafe_allow_html=True)
        elif sound_f == "オン" and mood == "ホラー":
            audio_placeholder.empty()
            time.sleep(0.5) 
            audio_placeholder.markdown(sound_d, unsafe_allow_html=True)       

if __name__ == '__main__':
    main()
