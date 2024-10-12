import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from video_controller import compress_video
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

# Define the directory where files will be saved temporarily
UPLOAD_FOLDER = './uploads'
COMPRESSED_FOLDER = './compressed'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['COMPRESSED_FOLDER'] = COMPRESSED_FOLDER

# Define allowed extensions for upload
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the file was sent
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        files = request.files.getlist('file')
        if not files:
            return jsonify({'error': 'No selected file'}), 400

        results = []
        with ThreadPoolExecutor() as executor:
            futures = []
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)  # Save the file to the specified directory

                    # Compress the video
                    resolution = request.form.get('resolution', '1280x720')
                    bitrate = request.form.get('bitrate', '1000k')
                    format = request.form.get('format', 'mp4')
                    nvenc_preset = request.form.get('nvenc_preset', 'p7')

                    future = executor.submit(compress_video, file_path, resolution, bitrate, format, nvenc_preset)
                    futures.append(future)

            for future in futures:
                try:
                    compressed_file_path = future.result()
                    results.append(compressed_file_path)
                except Exception as e:
                    results.append(str(e))

        return jsonify({'message': f'Files successfully uploaded and compressed to {results}'}), 200
    return render_template('upload.html')

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    if not os.path.exists(COMPRESSED_FOLDER):
        os.makedirs(COMPRESSED_FOLDER)
    app.run(debug=True)