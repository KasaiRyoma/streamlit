import streamlit as st
import time
from PIL import Image

# ページ設定
def init_page():
    st.set_page_config(
        page_title="自動カメラ撮影",
        page_icon="📸"
    )
    st.title("📸 自動カメラ撮影アプリ")
    st.write("ページを開いた瞬間からカメラが起動し、3秒後に自動撮影を行います。")

# 撮影ロジック
def capture_image():
    # 初回アクセス時のタイマー開始
    if "start_time" not in st.session_state:
        st.session_state.start_time = time.time()
    
    # カメラ入力UI
    st.write("カメラが起動中です。撮影を待っています...")
    camera_input = st.camera_input("カメラを起動")
    
    # 撮影タイマーの経過確認
    elapsed_time = time.time() - st.session_state.start_time
    if elapsed_time >= 3:
        if camera_input:
            st.success("撮影が完了しました！")
            captured_image = Image.open(camera_input)
            st.image(captured_image, caption="キャプチャされた画像", use_column_width=True)
        else:
            st.warning("カメラ入力がありません。カメラが有効になっているか確認してください。")

# メイン関数
def main():
    init_page()
    capture_image()

if __name__ == "__main__":
    main()
