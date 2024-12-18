import streamlit as st
import base64
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="自動カメラ撮影", page_icon="📸")

st.title("📸 自動カメラ撮影アプリ")
st.write("ページを開いてから3秒後に自動撮影します。")

# JavaScriptコードの埋め込み
html_code = """
<script>
    let video = document.createElement('video');
    let canvas = document.createElement('canvas');
    let context = canvas.getContext('2d');
    let stream = null;

    async function startCamera() {
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
        video.play();

        // 自動撮影タイマー
        setTimeout(() => {
            context.drawImage(video, 0, 0, canvas.width, canvas.height);
            let imgData = canvas.toDataURL('image/png');
            document.getElementById('captured_image').value = imgData;
            document.getElementById('image_form').submit();
        }, 3000);
    }

    window.onload = () => {
        document.body.appendChild(video);
        startCamera();
    };
</script>
<form id="image_form" method="post">
    <input type="hidden" name="captured_image" id="captured_image">
</form>
"""
st.components.v1.html(html_code, height=300)

# サーバーサイドでキャプチャした画像を受け取る
if "captured_image" in st.experimental_get_query_params():
    captured_image_data = st.experimental_get_query_params()["captured_image"][0]
    decoded_image = base64.b64decode(captured_image_data.split(",")[1])
    image = Image.open(BytesIO(decoded_image))
    st.image(image, caption="自動撮影された画像", use_column_width=True)
