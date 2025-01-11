import streamlit as st

# カスタムJavaScriptを挿入してボタンを遅延クリック
st.markdown(
    """
    <script>
    function clickButtonAfterDelay() {
        // タイマーを設定
        setTimeout(function() {
            // ボタンを探す
            const button = document.querySelector('[data-testid="stBaseButton-minimal"]');
            if (button) {
                button.click(); // ボタンをクリック
            } else {
                console.log("ボタンが見つかりません。");
            }
        }, 3000); // 3秒後にクリック（必要に応じて調整可能）
    }

    document.addEventListener("DOMContentLoaded", clickButtonAfterDelay);
    </script>
    """,
    unsafe_allow_html=True,
)

# カメラ入力を使用
image = st.camera_input("Take a picture")

# 撮影された画像を表示
if image:
    st.image(image)
