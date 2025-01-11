import streamlit as st

# カスタムCSSとJavaScriptを適用
st.markdown(
    """
    <style>
    /* 切り替えボタンをカメラ映像の中央に配置 */
    [data-testid="stBaseButton-minimal"] {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 200px;
        height: 60px;
        font-size: 1.5rem;
        background-color: #007BFF;
        color: white;
        border: none;
        border-radius: 10px;
        z-index: 10;
        cursor: pointer;
    }

    /* 撮影ボタンを透明化しない */
    [data-testid="stCameraInputWebcamComponent"] button {
        position: fixed;
        z-index: 2;
        cursor: pointer;
    }

    /* カメラ映像をフルスクリーン表示 */
    [data-testid="stCameraInputWebcamComponent"] video {
        z-index: 0;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        object-fit: cover;
    }
    </style>

    <script>
        document.addEventListener("DOMContentLoaded", function () {
            const switchButton = document.querySelector('[data-testid="stBaseButton-minimal"]');

            if (switchButton) {
                switchButton.addEventListener("click", function () {
                    console.log("Switch button clicked.");
                    
                    // ボタンを消す
                    switchButton.style.display = "none";
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
