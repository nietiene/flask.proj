from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from pytube import YouTube
import os

app = Flask(__name__)
CORS(app)  # Allow all CORS requests

@app.route("/download", methods=["POST"])
def download_video():
    try:
        data = request.get_json()
        if not data or "videoURL" not in data:
            return jsonify({"error": "No URL provided"}), 400

        video_url = data["videoURL"]
        yt = YouTube(video_url)
        
        # Get the highest resolution stream
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        if not stream:
            return jsonify({"error": "No suitable stream found"}), 400

        # Sanitize filename
        filename = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in yt.title) + ".mp4"
        filepath = os.path.join(DOWNLOAD_FOLDER, filename)
        
        # Download the video
        stream.download(output_path=DOWNLOAD_FOLDER, filename=filename)
        
        return send_file(filepath, as_attachment=True, download_name=filename)

    except Exception as e:
        print("Detailed Error:", str(e))
        return jsonify({
            "error": "Failed to download video",
            "details": str(e),
            "type": type(e).__name__
        }), 500
if __name__ == "__main__":
    app.run(port=5000)
