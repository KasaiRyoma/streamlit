import streamlit as st
import streamlit.components.v1 as components

st.title("カメラ切り替えデモ（Streamlit Cloud対応）")

# JavaScriptとHTMLでカメラ切り替えを実現
html_code = """
<div>
  <video id="video" autoplay style="width: 100%; max-width: 400px;"></video>
  <br>
  <button id="switchCamera">Switch Camera</button>
  <button id="capture">Capture</button>
  <canvas id="canvas" style="display:none;"></canvas>
  <img id="output" style="margin-top: 10px; width: 100%; max-width: 400px;">
</div>

<script>
  let videoElement = document.getElementById('video');
  let canvas = document.getElementById('canvas');
  let outputImage = document.getElementById('output');
  let switchCameraButton = document.getElementById('switchCamera');
  let captureButton = document.getElementById('capture');

  let currentStream = null;
  let usingFrontCamera = true;

  async function startCamera() {
    if (currentStream) {
      currentStream.getTracks().forEach(track => track.stop());
    }

    let constraints = {
      video: {
        facingMode: usingFrontCamera ? 'user' : 'environment'
      }
    };

    currentStream = await navigator.mediaDevices.getUserMedia(constraints);
    videoElement.srcObject = currentStream;
  }

  switchCameraButton.addEventListener('click', () => {
    usingFrontCamera = !usingFrontCamera;
    startCamera();
  });

  captureButton.addEventListener('click', () => {
    canvas.width = videoElement.videoWidth;
    canvas.height = videoElement.videoHeight;
    canvas.getContext('2d').drawImage(videoElement, 0, 0);
    outputImage.src = canvas.toDataURL('image/png');
  });

  startCamera();
</script>
"""

# StreamlitでHTMLを埋め込む
components.html(html_code, height=600)
