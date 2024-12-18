import base64
import streamlit as st
from langchain_openai import ChatOpenAI


def init_page():
    st.set_page_config(
        page_title="画像からセリフ生成",
        page_icon="🤖"
    )
    st.header("セリフ生成")
    


def main():
    init_page()

    llm = ChatOpenAI(
        temperature=0,
        model="gpt-4o",
        max_tokens=512
    )

    uploaded_file = st.file_uploader(
        label='画像をアップロードしてください。',
        type=['png', 'jpg', 'webp', 'gif']
    )

    if uploaded_file:
        # 画像をBase64でエンコード
        image_base64 = base64.b64encode(uploaded_file.read()).decode()
        image = f"data:image/jpeg;base64,{image_base64}"

        # アップロードした画像を表示
        st.image(uploaded_file)

        # 自動的に画像内容を分析
        query = [
            (
                "user",
                [
                    {
                        "type": "text",
                        "text": "この画像に写っている物が何かを推測し、それを擬人化したセリフのみを出力してください。それが難しいときは「セリフ生成不可能」と出力してください。"  # 固定の質問
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image,
                            "detail": "auto"
                        },
                    }
                ]
            )
        ]

        st.markdown("### セリフ")
        st.write_stream(llm.stream(query))

    else:
        st.write('')


if __name__ == '__main__':
    main()
