from models.video_compressor import VideoCompressor

def compress_video(file_path, resolution, bitrate, format, nvenc_preset):
    print(f"Compressing video: {file_path}")
    compressor = VideoCompressor(file_path, resolution, bitrate, format, nvenc_preset)
    output_file = compressor.compress()
    print(f"Compression completed. Output file: {output_file}")
    return output_file