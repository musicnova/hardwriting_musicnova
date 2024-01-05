import os
import subprocess
import shutil
from fastapi import FastAPI

app = FastAPI()

KEY = "ShAn675sb5"

def download_repository():
    repository_url = "https://github.com/musicnova/hardwriting_musicnova"
    target_directory = os.path.join("./tmp", KEY)
    shutil.rmtree("./tmp", ignore_errors=True)
    subprocess.call(["git", "clone", repository_url, target_directory])

def ffmpeg_transcode(input_file, output_url, mirror=False):
    mirror_filter = "hflip" if mirror else ""
    subprocess.call(
        [
            "ffmpeg",
            "-y",
            "-loop",
            "-i",
            input_file,
            "-vf",
            f"{mirror_filter},transpose=2",
            "-rtsp_transport",
            "tcp",
            "-f",
            "rtsp",
            output_url,
        ]
    )

def main():
    repository_path = os.path.join("./tmp", KEY)
    videos_directory = os.path.join(repository_path, "videos")
    output_rtsp_url = "rtsp://stream:" + KEY + "@127.0.0.1:13554"
    mirror_frames = False

    download_repository()

    while True:
        for file in os.listdir(videos_directory):
            if file.endswith(".mp4"):
                video_file = os.path.join(videos_directory, file)
                ffmpeg_transcode(video_file, output_rtsp_url, mirror_frames)
                mirror_frames = not mirror_frames

@app.get("/")
def root():
    return {"message": "Server is running"}

if __name__ == "__main__":
    main()