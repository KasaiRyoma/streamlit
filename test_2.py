import base64
import streamlit as st
from langchain_openai import ChatOpenAI

def init_page():
    st.set_page_config(
        page_title="画像から生成",
        page_icon="🤖"
    )
    st.header("セリフ生成")

def main():
    init_page()

    # LLM設定
    llm = ChatOpenAI(
        temperature=0,
        model="gpt-4o",
        max_tokens=512
    )

    if 'response' not in st.session_state:
        st.session_state.response = None

    def process_image(image):
        if image is not None:
            # カメラ入力の画像データを読み込み、エンコードしてbase64に変換
            image_bytes = image.getvalue()
            image_base64 = base64.b64encode(image_bytes).decode()
            image_data_url = f"data:image/jpeg;base64,{image_base64}"

            # LLMへのクエリ
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

            # LLMからのレスポンス
            st.markdown("### 出力")
            with st.spinner('生成中...'):
                try:
                    st.session_state.response = llm.stream(query)
                    st.write(st.session_state.response)
                except Exception as e:
                    st.error(f"生成中にエラーが発生しました: {e}")

    # カメラ入力
    image = st.camera_input("カメラを使用して画像を撮影してください")

    # 撮影された画像がある場合のみ処理を実行
    if image:
        process_image(image)

    # リセットボタン
    if st.button("もう一度"):
        st.session_state.response = None  # 出力をクリア
        st.experimental_rerun()  # ページをリロードして入力をリセット

if __name__ == '__main__':
    main()