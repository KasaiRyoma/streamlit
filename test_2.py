import streamlit as st

# カスタムJavaScriptを挿入してボタンを自動クリック
st.markdown(
    """
    <script>
    document.addEventListener("DOMContentLoaded", function() {
        // ボタンを特定して自動クリック
        const button = document.querySelector('[data-testid="stBaseButton-minimal"]');
        if (button) {
            button.click();
        }
    });
    </script>
    """,
    unsafe_allow_html=True,
)

# カメラ入力を使用
image = st.camera_input("Take a picture")

# 撮影された画像を表示
if image:
    st.image(image)
