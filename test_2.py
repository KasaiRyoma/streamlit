import streamlit as st
import time
from PIL import Image

# ページ設定
def init_page():
    st.set_page_config(
        page_title="カメラ撮影アプリ",
        page_icon="📸"
    )
    st.title("📸 カメラ撮影アプリ")
    st.write("カメラを起動し、3秒後に自動撮影を行います。")


# カメラ撮影ロジック
def camera_capture():
    # カメラ入力UIを表示
    st.write("以下のボタンをクリックしてカメラを起動してください。")
    camera_input = st.camera_input("カメラを起動")
    
    if camera_input:
        st.write("撮影中です...しばらくお待ちください。")
        with st.spinner("3秒後に自動撮影します..."):
            time.sleep(3)  # 3秒待機

        # アップロードされた画像を表示
        st.success("撮影が完了しました！")
        captured_image = Image.open(camera_input)
        st.image(captured_image, caption="キャプチャされた画像", use_column_width=True)


# メイン関数
def main():
    init_page()
    camera_capture()


if __name__ == "__main__":
    main()
