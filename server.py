from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from pytube import YouTube
from pytube.exceptions import VideoUnavailable, RegexMatchError, PytubeError
import os
import logging

app = Flask(__name__)
CORS(app)  # Allow all CORS requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def sanitize_filename(title):
    """Sanitize the filename to remove invalid characters"""
    keepchars = (' ', '.', '_', '-')
    return "".join(c for c in title if c.isalnum() or c in keepchars).rstrip()

@app.route("/download", methods=["POST"])
def download_video():
    try:
        data = request.get_json()
        logger.info(f"📥 Incoming request data: {data}")
        
        if not data or "videoURL" not in data:
            return jsonify({"error": "No URL provided"}), 400

        video_url = data["videoURL"]
        logger.info(f"🔗 Processing URL: {video_url}")

        # Initialize YouTube object
        yt = YouTube(video_url)
        logger.info(f"🎬 Video title: {yt.title}")
        
        # Get highest resolution progressive mp4 stream (includes audio)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        
        if not stream:
            return jsonify({"error": "No downloadable video stream found"}), 400

        # Sanitize filename and create full path
        filename = sanitize_filename(yt.title) + ".mp4"
        filepath = os.path.join(DOWNLOAD_FOLDER, filename)
        logger.info(f"💾 Downloading to: {filepath}")

        # Download video if not already downloaded
        if not os.path.exists(filepath):
            stream.download(output_path=DOWNLOAD_FOLDER, filename=filename)
            logger.info("✅ Download successful")
        else:
            logger.info("⚠️ File already exists, skipping download")

        # Send the file back to the client
        return send_file(
            filepath,
            as_attachment=True,
            download_name=filename,
            mimetype='video/mp4'
        )

    except VideoUnavailable:
        logger.error("Video is unavailable or private")
        return jsonify({"error": "Video is unavailable or private"}), 400
    except RegexMatchError:
        logger.error("Invalid YouTube URL format")
        return jsonify({"error": "Invalid YouTube URL format"}), 400
    except PytubeError as e:
        logger.error(f"Pytube error: {str(e)}")
        return jsonify({"error": f"YouTube processing error: {str(e)}"}), 400
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return jsonify({
            "error": "Failed to download video",
            "details": str(e),
            "type": type(e).__name__
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
