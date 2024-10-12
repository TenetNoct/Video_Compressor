import os
import subprocess

class VideoCompressor:
    def __init__(self, file_path, resolution, bitrate, format, nvenc_preset):
        self.file_path = file_path
        self.resolution = resolution
        self.bitrate = bitrate
        self.format = format
        self.nvenc_preset = nvenc_preset
        self.output_file = self.generate_output_filename()

    def generate_output_filename(self):
        base, ext = os.path.splitext(os.path.basename(self.file_path))
        return os.path.join('./compressed', f"{base}_compressed.{self.format}")

    def compress(self):
        try:
            command = [
                "ffmpeg", "-i", self.file_path, 
                "-b:v", self.bitrate, 
                "-s", self.resolution, 
                "-c:v", "hevc_nvenc", 
                "-preset", self.nvenc_preset, 
                self.output_file
            ]
            print(f"Executing command: {' '.join(command)}")
            subprocess.run(command, check=True)
            return self.output_file
        except subprocess.CalledProcessError as e:
            raise Exception(f"Error during compression: {e}")