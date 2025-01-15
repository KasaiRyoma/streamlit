import base64
import time
import streamlit as st
import random
from langchain_openai import ChatOpenAI
from PIL import Image
from io import BytesIO

def load_font_base64(font_path):
    with open(font_path, "rb") as font_file:
        font_base64 = base64.b64encode(font_file.read()).decode()
    return font_base64

def apply_font(font_base64, font_size, line_height):
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
                justify-content: center; 
                font-size: {font_size};
                line-height: {line_height};
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

def load_audio_base64(audio_path):
    with open(audio_path, "rb") as audio_file:
        audio_base64 = base64.b64encode(audio_file.read()).decode()
        audio_html = f"""
        <audio autoplay=True>
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        </audio>
        """
    return audio_html

def image_base64(camera_input):
    captured_image = Image.open(BytesIO(camera_input.getvalue()))
    buffered = BytesIO()
    captured_image.save(buffered, format="JPEG")
    image_base64 = base64.b64encode(buffered.getvalue()).decode()
    return image_base64

def init_page():
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

def chatgpt(llm, text, image_base64=None):
    query = [
        (
            "user",
            [
                {"type": "text", "text": text},
            ]
        )
    ]
    if image_base64:
        query[0][1].append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{image_base64}",
                "detail": "auto"
            }
        })
    response = llm.invoke(query).content.strip()
    return response

def main():
    init_page()
    audio_placeholder = st.empty()
    audio_placeholder.empty()
    time.sleep(0.5)
    llm = ChatOpenAI(
        temperature=0,
        model="gpt-4o",
        max_tokens=512
    )

    text_length = st.sidebar.selectbox("文字数", [50, 100, 150, 200, "ランダム"], index=1)
    if text_length == "ランダム":
        text_length = random.choice([50, 100, 150, 200])

    mood = st.sidebar.selectbox("雰囲気", ["明るい", "暗い", "コメディ", "ホラー", "雑学", "ランダム", ], index=0)
    if mood == "ランダム":
        mood = random.choice(["明るい", "暗い", "コメディ", "ホラー", "雑学"])

    font_size = st.sidebar.selectbox("フォントサイズ", ["小", "中", "大"], index=1)

    sound_f = st.sidebar.radio("効果音", ["オン", "オフ"], index=1)

    kana = st.sidebar.radio("ひらがなモード", ["オン", "オフ"], index=1)
    
    camera_input = st.sidebar.camera_input("撮影してください")

    if camera_input:
        if mood == "雑学":
            query1_text = (
                "この画像には何が写っていますか？単語で答えてください。"
                "単語以外の文章は絶対に出力しないでください。"
            )
        else:
            query1_text = (
                "この画像には何が写っていますか？できるだけたくさん単語で答えてください。"
                "単語以外の文章は絶対に出力しないでください。"
            )
        response1 = chatgpt(llm, query1_text, image_base64(camera_input))        

        if mood == "雑学":
            query2_text = {
                "オン": (
                    f"'{response1}'に関する雑学や豆知識を{text_length}字程度で考えなさい。"
                    f"出力は文章のみとすること。"
                    f"可能であればその状況にあった絵文字などを用いること。"
                    f"漢字は使わずにすべてひらがなで出力してください。"
                    f"口調を子供向けにしてください。"
                ),
                "オフ": (
                    f"'{response1}'に関する雑学や豆知識を{text_length}字程度で考えなさい。"
                    f"出力は文章のみとすること。"
                    f"可能であればその状況にあった絵文字などを用いること。"
                ),
            }
        else:
            query2_text = {
                "オン": (
                    f"'{response1}'を用いた文章を{text_length}字程度で考えなさい。"
                    f"出力は文章のみとすること。"
                    f"可能であればその状況にあった絵文字などを用いること。"
                    f"'{response1}'以外のものはできるだけ話に登場させないこと。"
                    f"文章の雰囲気は{mood}にしてください。"
                    f"漢字は使わずにすべてひらがなで出力してください。"
                    f"口調を子供向けにしてください。"
                ),
                "オフ": (
                    f"'{response1}'を用いた文章を{text_length}字程度で考えなさい。"
                    f"出力は文章のみとすること。"
                    f"可能であればその状況にあった絵文字などを用いること。"
                    f"'{response1}'以外のものはできるだけ話に登場させないこと。"
                    f"文章の雰囲気は{mood}にしてください。"
                ),
            }
        response2 = chatgpt(llm, query2_text[kana])   

        font_path = {
            "明るい": "./font/001Shirokuma-Regular.otf",
            "暗い": "./font/OtsutomeFont_Ver3_16.ttf",
            "コメディ": "./font/PopRumCute.otf",
            "ホラー": "./font/onryou.TTF",
            "雑学": "./font/komorebi-gothic.ttf"
        }
        font_settings = {
            "小": {50: ("2.9em", "1.5"), 100: ("2.3em", "1.3"), 150: ("2.0em", "1.0"), 200: ("1.8em", "1.0")},
            "中": {50: ("6.0em", "1.5"), 100: ("4.3em", "1.3"), 150: ("3.7em", "1.0"), 200: ("3.5em", "1.0")},
            "大": {50: ("7.0em", "1.5"), 100: ("5.3em", "1.3"), 150: ("4.4em", "1.0"), 200: ("4.2em", "1.0")},
        }
        apply_font(load_font_base64(font_path[mood]), *font_settings[font_size][text_length])

        st.markdown(
            f"""
            <div class="dynamic-text">
                {response1}
            </div>
            """,
            unsafe_allow_html=True
        )

        if sound_f == "オン":
            audio_path = {
                "明るい": "./audio/akarui.mp3",
                "暗い": "./audio/kurai.mp3",
                "コメディ": "./audio/omosiro.mp3",
                "ホラー": "./audio/horror.mp3",
                "雑学": "./audio/zatugaku.mp3"
            }
            audio_placeholder.markdown(load_audio_base64(audio_path[mood]), unsafe_allow_html=True)
     
if __name__ == '__main__':
    main()
