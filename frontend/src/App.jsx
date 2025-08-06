import { useState } from "react";
import axios from "axios";

function App() {
  const [videoURL, setVideoURL] = useState("");
  const [downloading, setDownloading] = useState(false);
  const [message, setMessage] = useState("");

  const handleDownload = async () => {
    if (!videoURL) {
      alert("Please enter a YouTube URL");
      return;
    }

    try {
      setDownloading(true);
      setMessage("");

      const response = await axios.post(
        "http://localhost:5000/download",
        { videoURL },
        { responseType: "blob" }
      );

      const blob = new Blob([response.data], { type: "video/mp4" });
      const url = window.URL.createObjectURL(blob);

      const a = document.createElement("a");
      a.href = url;
      a.download = "video.mp4"; // Optional: Use title from server
      document.body.appendChild(a);
      a.click();
      a.remove();

      setMessage("✅ Download started!");
    } catch (error) {
      console.error("Download failed:", error);
      setMessage(error?.response?.data?.error || "❌ Failed to download video.");
    } finally {
      setDownloading(false);
    }
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial, sans-serif" }}>
      <h1>YouTube Video Downloader</h1>
      <p>Paste a valid YouTube video URL below:</p>
      <input
        type="text"
        placeholder="https://www.youtube.com/watch?v=example"
        value={videoURL}
        onChange={(e) => setVideoURL(e.target.value)}
        style={{
          width: "400px",
          padding: "10px",
          marginBottom: "10px",
          fontSize: "1rem",
        }}
      />
      <br />
      <button
        onClick={handleDownload}
        style={{
          padding: "10px 20px",
          fontSize: "1rem",
          cursor: "pointer",
          backgroundColor: "#ff0000",
          color: "white",
          border: "none",
          borderRadius: "4px",
        }}
        disabled={downloading}
      >
        {downloading ? "Downloading..." : "Download"}
      </button>
      {message && <p style={{ marginTop: "1rem" }}>{message}</p>}
    </div>
  );
}

export default App;
