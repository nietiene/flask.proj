import { useState } from "react";
import axios from "axios";

function App() {
  const [videoURL, setVideoURL] = useState("");
  const [downloading, setDownloading] = useState(false);
  const [message, setMessage] = useState("");
  const [errorDetails, setErrorDetails] = useState("");

  const handleDownload = async () => {
    if (!videoURL) {
      setMessage("❌ Please enter a YouTube URL");
      return;
    }

    try {
      setDownloading(true);
      setMessage("⏳ Processing your request...");
      setErrorDetails("");

      const response = await axios.post(
        "http://localhost:5000/download",
        { videoURL },
        { 
          responseType: "blob",
          headers: {
            'Content-Type': 'application/json'
          }
        }
      );

      // Extract filename from content-disposition or use default
      let filename = "video.mp4";
      const contentDisposition = response.headers['content-disposition'];
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="?(.+)"?/);
        if (filenameMatch) filename = filenameMatch[1];
      }

      const blob = new Blob([response.data], { type: "video/mp4" });
      const url = window.URL.createObjectURL(blob);

      const a = document.createElement("a");
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();

      // Clean up the object URL
      setTimeout(() => window.URL.revokeObjectURL(url), 100);

      setMessage("✅ Download started!");
    } catch (error) {
      console.error("Download failed:", error);
      
      let errorMessage = "❌ Failed to download video";
      let details = "";
      
      if (error.response) {
        // Server responded with error status
        errorMessage = error.response.data.error || errorMessage;
        details = error.response.data.details || "";
      } else if (error.request) {
        // Request was made but no response
        details = "Server didn't respond. Is the backend running?";
      } else {
        // Other errors
        details = error.message;
      }
      
      setMessage(errorMessage);
      setErrorDetails(details);
    } finally {
      setDownloading(false);
    }
  };

  return (
    <div style={{ 
      padding: "2rem", 
      fontFamily: "Arial, sans-serif",
      maxWidth: "800px",
      margin: "0 auto"
    }}>
      <h1 style={{ color: "#ff0000" }}>YouTube Video Downloader</h1>
      <p>Paste a valid YouTube video URL below:</p>
      
      <input
        type="text"
        placeholder="https://www.youtube.com/watch?v=..."
        value={videoURL}
        onChange={(e) => setVideoURL(e.target.value)}
        style={{
          width: "100%",
          padding: "12px",
          margin: "8px 0",
          fontSize: "1rem",
          border: "1px solid #ccc",
          borderRadius: "4px"
        }}
      />
      
      <button
        onClick={handleDownload}
        style={{
          padding: "12px 24px",
          fontSize: "1rem",
          cursor: "pointer",
          backgroundColor: "#ff0000",
          color: "white",
          border: "none",
          borderRadius: "4px",
          margin: "8px 0",
          fontWeight: "bold",
          opacity: downloading ? 0.7 : 1
        }}
        disabled={downloading}
      >
        {downloading ? "⏳ Downloading..." : "⬇️ Download Video"}
      </button>
      
      {message && (
        <p style={{ 
          margin: "1rem 0",
          color: message.startsWith("❌") ? "#d32f2f" : "#388e3c",
          fontWeight: "bold"
        }}>
          {message}
        </p>
      )}
      
      {errorDetails && (
        <div style={{
          margin: "1rem 0",
          padding: "12px",
          backgroundColor: "#ffebee",
          borderLeft: "4px solid #d32f2f",
          color: "#5f2120"
        }}>
          <p style={{ margin: "0" }}>{errorDetails}</p>
        </div>
      )}
      
      <div style={{ marginTop: "2rem", color: "#666" }}>
        <p>Note: Some videos may not be available due to copyright restrictions.</p>
      </div>
    </div>
  );
}

export default App;