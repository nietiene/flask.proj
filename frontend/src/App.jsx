import { useState } from "react";
import axios from "axios";

function App() {
  const [videoURL, setVideoURL] = useState("");
  const [downloading, setDownloading] = useState(false);

  const handleDownload = async () => {
    if (!videoURL) return alert("Please enter a YouTube URL");

    try {
      setDownloading(true);
      const response = await axios.post(
        "http://localhost:5000/download",
        { videoURL },
        { responseType: "blob" }
      );

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const a = document.createElement("a");
      a.href = url;
      a.download = "video.mp4"; // you can later change this dynamically
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch (error) {
      console.error("Download failed:", error);
      alert("Failed to download video. Check URL or try again.");
    } finally {
      setDownloading(false);
    }
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>YouTube Video Downloader</h1>
      <input
        type="text"
        placeholder="Paste YouTube URL here"
        value={videoURL}
        onChange={(e) => setVideoURL(e.target.value)}
        style={{ width: "400px", padding: "10px" }}
      />
      <br />
      <button onClick={handleDownload} style={{ marginTop: "1rem" }}>
        {downloading ? "Downloading..." : "Download"}
      </button>
    </div>
  );
}

export default App;
