from flask import Flask, request, jsonify, send_file
from pytube import YouTube
import os
import uuid

app = Flask(__name__)
DOWNLOAD_FOLDER = './downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/download', methods=['POST'])
def download_video():
    try:
        data = request.get_json()
        url = data['url']
        format = data['format']
        yt = YouTube(url)

        # Generate a unique filename
        filename = f"{uuid.uuid4()}.{format}"

        if format == 'mp3':
            audio_stream = yt.streams.filter(only_audio=True).first()
            file_path = audio_stream.download(output_path=DOWNLOAD_FOLDER, filename=filename)
            base, ext = os.path.splitext(file_path)
            mp3_file = f"{base}.mp3"
            os.rename(file_path, mp3_file)
            file_path = mp3_file
        elif format == 'mp4':
            video_stream = yt.streams.get_highest_resolution()
            file_path = video_stream.download(output_path=DOWNLOAD_FOLDER, filename=filename)

        return jsonify({'file_url': f'https://your-backend-service.onrender.com/files/{filename}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/files/<filename>', methods=['GET'])
def serve_file(filename):
    file_path = os.path.join(DOWNLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
