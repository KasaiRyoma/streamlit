if sound_f == "オン":
    # 雰囲気に対応する音声ファイルのマッピング
    audio_files = {
        "明るい": "./audio/akarui.mp3",
        "暗い": "./audio/kurai.mp3",
        "コメディ": "./audio/omosiro.mp3",
        "ホラー": "./audio/horror.mp3",
    }

    # 対応する音声ファイルを再生
    if mood in audio_files:
        audio_placeholder.markdown(load_audio_as_base64(audio_files[mood]), unsafe_allow_html=True)
