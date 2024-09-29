import streamlit as st
from pytube import YouTube

st.title("YouTube Downloader")

youtube_url = st.text_input("Enter the YouTube URL")

resolution = st.selectbox("Select the resolution", ["Highest Resolution", "720p", "480p", "360p", "240p", "144p"])
file_format = st.selectbox("Select the format", ["MP4", "MP3"])

if st.button("Download Video"):
    try:
        youtube_object = YouTube(youtube_url)
        
        if resolution == "Highest Resolution":
            if file_format == "MP4":
                youtube_object.streams.get_highest_resolution().download()
            elif file_format == "MP3":
                youtube_object.streams.filter(only_audio=True).first().download(filename_prefix="audio_")
        elif resolution in ["720p", "480p", "360p", "240p", "144p"]:
            if file_format == "MP4":
                youtube_object.streams.filter(res=resolution, file_extension='mp4').first().download()
            elif file_format == "MP3":
                youtube_object.streams.filter(only_audio=True, abr='128kbps').first().download(filename_prefix="audio_")
        
        st.success("Download completed successfully.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
        
