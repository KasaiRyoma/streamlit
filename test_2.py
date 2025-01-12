import streamlit as st
from PIL import Image
import io
import base64

# base64変換用の関数
def image_to_base64(image):
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    byte_data = buf.getvalue()
    return base64.b64encode(byte_data).decode()

# タイトル
st.title("画像アップロードとフルスクリーン表示")

# 画像アップロード
uploaded_file = st.file_uploader("画像をアップロードしてください", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)

    # 表示
    st.image(image, caption="アップロードされた画像", use_container_width=True)

    # フルスクリーン表示用HTMLとJavaScript
    fullscreen_html = f"""
    <style>
        #fullscreen-container {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background-color: black;
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 9999;
            display: none;
        }}
        #fullscreen-container img {{
            max-width: 100%;
            max-height: 100%;
        }}
    </style>
    <div style="text-align: center;">
        <button onclick="toggleFullscreen()" style="padding: 10px 20px; font-size: 16px; cursor: pointer;">
            画像をフルスクリーン表示
        </button>
    </div>
    <div id="fullscreen-container">
        <img src="data:image/png;base64,{image_to_base64(image)}" alt="Fullscreen Image">
    </div>
    <script>
        function toggleFullscreen() {{
            const container = document.getElementById("fullscreen-container");
            if (container.style.display === "none" || container.style.display === "") {{
                container.style.display = "flex";
                container.requestFullscreen().catch(err => {{
                    console.error("フルスクリーンエラー:", err.message);
                }});
            }} else {{
                document.exitFullscreen();
                container.style.display = "none";
            }}
        }}

        document.addEventListener("fullscreenchange", function() {{
            const container = document.getElementById("fullscreen-container");
            if (!document.fullscreenElement) {{
                container.style.display = "none";
            }}
        }});
    </script>
    """

    # HTML埋め込み
    st.components.v1.html(fullscreen_html, height=0)
