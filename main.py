import subprocess
import sys
import os
from pathlib import Path
import time

class compressor:

    EXTENSIONS = [".mkv", ".mp4", ".avi"]
    ALREADY_ENCODED = ["hevc", "h265"]

    has_nvidia = False


    def get_job(self, file):
        cmd = [
            "ffprobe",
            "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=codec_name",
            "-of", "csv=p=0",
            str(file)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout.strip()

    def run_job(self, file):
        temp = file.with_suffix(file.suffix + ".processing.mkv")
        final = file.with_suffix(".hevc.mkv")

        print(f"gpu setting: {self.has_nvidia}")

        if self.has_nvidia:
            command = [
                "ffmpeg",
                "-hide_banner",
                "-y",
                "-threads", "1",
                "-hwaccel", "cuda",
                "-i", str(file),
                "-map", "0",
                "-c:v", "hevc_nvenc",
                "-preset", "p6",
                "-tune", "ull",
                "-cq", "24",
                "-profile:v", "main",
                "-c:a", "copy",
                "-c:s", "copy",
                str(temp)
            ]
        else:
            command = [
                "ffmpeg",
                "-hide_banner",
                "-y",
                "-threads", "1",
                "-vaapi_device", "/dev/dri/renderD128",
                "-i", str(file),
                "-map", "0",
                "-vf", "format=nv12,hwupload",
                "-c:v", "hevc_vaapi",
                "-qp", "24",
                "-c:a", "copy",
                "-c:s", "copy",
                str(temp)
            ]

        print(f"Starting compressing file: {file}")
        result = subprocess.run(command)

        if result.returncode != 0:
            print(f"Compression failed for: {file}")
            if temp.exists():
                temp.unlink()
            return
        
        temp.rename(final)

        print(f"Compression completed for: {file} -> {final}")

        if os.path.exists(final):    
            os.remove(file)
            print(f"Removed old file")
            return
        
        print(f"Could not remove: {file}")


    def __init__(self, gpu_type, path):

        if gpu_type.strip().lower() not in ["amd", "nvidia"]:
            print(f"You must define what gpu to use, invalid: {gpu_type}")
            return
        
        if gpu_type.strip().lower() == "nvidia":
            self.has_nvidia = True


        for file in path.rglob("*"):
            if file.suffix.lower() not in self.EXTENSIONS:
                continue
            if ".transcoding" in file.name or file.name.endswith(".backup"):
                continue
            
            if self.get_job(file).strip().lower() in self.ALREADY_ENCODED:
                print(f"File is already HVEC: {file}")
                continue
            self.run_job(file)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Compressor needs <gpu_type> <path>")
        sys.exit(1)

    gpu = sys.argv[1]
    path = Path(sys.argv[2])

    compressor(gpu, path)