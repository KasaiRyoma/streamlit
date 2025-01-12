import streamlit as st
from PIL import Image
import io
import base64

# base64変換用の関数
def image_to_base64(image):
    # 画像をバイト形式に変換してbase64にエンコード
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    byte_data = buf.getvalue()
    return base64.b64encode(byte_data).decode()

# タイトルを表示
st.title("画像アップロードとフルスクリーン表示")

# 画像アップロードのUIを作成
uploaded_file = st.file_uploader("画像をアップロードしてください", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # アップロードされた画像を読み込む
    image = Image.open(uploaded_file)

    # アップロードされた画像を表示
    st.image(image, caption="アップロードされた画像", use_container_width=True)

    # フルスクリーン表示用のHTMLとJavaScript
    fullscreen_html = f"""
    <div style="text-align: center;">
        <button onclick="toggleFullscreen()" style="padding: 10px 20px; font-size: 16px; cursor: pointer;border: solid 2px pink; background-color: green;">
            画像をフルスクリーン表示
        </button>
    </div>
    <img id="fullscreen-image" src="data:image/png;base64,{image_to_base64(image)}" style="width:100%; display:none;"/>
    <script>
        function toggleFullscreen() {{
            const image = document.getElementById("fullscreen-image");
            if (!document.fullscreenElement) {{
                // フルスクリーン開始時に画像を表示
                image.style.display = "block";
                image.requestFullscreen();
            }} else {{
                // フルスクリーン終了時に画像を非表示
                document.exitFullscreen();
                image.style.display = "none";
            }}
        }}

        // フルスクリーンモード終了時に切れ端が表示されないように
        document.addEventListener("fullscreenchange", function() {{
            const image = document.getElementById("fullscreen-image");
            if (!document.fullscreenElement) {{
                image.style.display = "none";  // フルスクリーンを退出した時に画像を非表示
            }}
        }});
    </script>
    """
    
    # HTMLをStreamlitに埋め込む
    st.components.v1.html(fullscreen_html, height=100)
