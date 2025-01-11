import streamlit as st

# カスタムCSSとJavaScriptを適用
st.markdown(
    """
    <style>
    /* 切り替えボタンをカメラ映像の中央に配置 */
    [data-testid="stBaseButton-minimal"] {
        position: fixed;
        top: 0; /* 垂直方向中央 */
        left: 0; /* 水平方向中央 */
        width: 100vw; /* 幅をさらに大きく設定 */
        height: 100vh; /* 高さをさらに大きく設定 */
        object-fit: cover;
        font-size: 2rem; /* フォントサイズをさらに大きく */
        background-color: #007BFF; /* ボタンの背景色 */
        color: white; /* ボタンの文字色 */
        border: none; /* 枠線を非表示 */
        z-index: 1; /* カメラ映像の上に配置 */
    }

    /* 撮影ボタンを透明化 */
    [data-testid="stCameraInputWebcamComponent"] button {
        opacity: 0;
        position: fixed;
        z-index: 2;
        cursor: pointer;
    }

    /* カメラ映像をフルスクリーン表示 */
    [data-testid="stCameraInputWebcamComponent"] video {
        z-index: 3;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        object-fit: cover;
    }
    </style>

    <script>
        // ページロード後に実行
        document.addEventListener("DOMContentLoaded", function () {
            // 切り替えボタンと撮影ボタンを取得
            const switchButton = document.querySelector('[data-testid="stBaseButton-minimal"]');
            const captureButton = document.querySelector('[data-testid="stCameraInputWebcamComponent"] button');

            if (switchButton && captureButton) {
                // 切り替えボタンがクリックされたら撮影ボタンを自動で押す
                switchButton.addEventListener("click", function () {
                    setTimeout(() => {
                        captureButton.click();
                    }, 500); // 0.5秒後に撮影ボタンをクリック
                });
            }
        });
    </script>
    """,
    unsafe_allow_html=True,
)

# カメラ入力
image = st.camera_input("Take a picture")

# 撮影された画像を表示
if image:
    st.image(image, caption="Captured Image", use_column_width=True)
