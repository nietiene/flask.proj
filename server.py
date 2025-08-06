from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from pytube import YouTube
import os

app = Flask(__name__)
CORS(app)  # Allow all CORS requests

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/download", methods=["POST"])
def download_video():
    try:
        data = request.get_json()
        video_url = data.get("videoURL")

        if not video_url:
            return jsonify({"error": "No URL provided"}), 400

        yt = YouTube(video_url)
        stream = yt.streams.get_highest_resolution()

        filename = yt.title.replace(" ", "_").replace("/", "_") + ".mp4"
        filepath = os.path.join(DOWNLOAD_FOLDER, filename)
        stream.download(output_path=DOWNLOAD_FOLDER, filename=filename)

        return send_file(filepath, as_attachment=True)

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000)
