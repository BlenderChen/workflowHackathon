import { useState } from 'react';

export default function App() {
  const [text, setText] = useState('');
  const [videoUrl, setVideoUrl] = useState('');
  const [loading, setLoading] = useState(false);

  // Define the backend base URL so that the full video URL can be constructed.
  const BACKEND_URL = 'http://localhost:5000';

  const handleInputChange = (event) => {
    setText(event.target.value);
  };

  // This function prepends the backend URL if the videoPath is relative.
  const getFullVideoUrl = (videoPath) => {
    return videoPath.startsWith('http') ? videoPath : BACKEND_URL + videoPath;
  };

  const checkFileExists = async (videoPath) => {
    const fullUrl = getFullVideoUrl(videoPath);
    try {
      const response = await fetch(fullUrl, { method: 'HEAD' });
      return response.ok;
    } catch (error) {
      return false;
    }
  };

  const waitForVideoFile = async (videoPath) => {
    const fullUrl = getFullVideoUrl(videoPath);
    let fileExists = false;
    let attempts = 0;
    while (!fileExists && attempts < 30) { // Poll for up to ~30 seconds
      fileExists = await checkFileExists(videoPath);
      if (fileExists) {
        console.log("Video file is ready:", fullUrl);
        setVideoUrl(fullUrl);
        return;
      }
      console.log("Waiting for video file...");
      await new Promise(resolve => setTimeout(resolve, 2000)); // Wait 2 seconds
      attempts++;
    }
    console.error("Video file did not appear in time.");
  };

  const handleGenerateVideo = async () => {
    if (!text.trim()) return;

    setLoading(true);
    setVideoUrl(''); // Clear previous video

    try {
      // The backend returns a relative path (e.g., "/videos/XXXXXXXXXX.mp4")
      const response = await fetch(`${BACKEND_URL}/?query=${encodeURIComponent(text)}`);
      const data = await response.json();

      if (data.videoUrl) {
        console.log("Video URL received:", data.videoUrl);
        waitForVideoFile(data.videoUrl); // Wait until the video file is available
      } else {
        console.error("No video URL received from backend");
      }
    } catch (error) {
      console.error("Error generating video:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className="app-container"
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '100vh',
        padding: '20px'
      }}
    >
      <h1>New Story Teller</h1>
      <input 
        type="text" 
        value={text} 
        onChange={handleInputChange} 
        placeholder="Enter text here..."
        style={{ padding: '10px', width: '80%', marginBottom: '10px' }}
      />
      <br />
      <button 
        onClick={handleGenerateVideo} 
        style={{ padding: '10px 20px', cursor: 'pointer' }} 
        disabled={loading}
      >
        {loading ? "Generating..." : "Generate Video"}
      </button>
      <br /><br />

      {loading && <p>Loading...</p>}

      {videoUrl && (
        <video 
          key={videoUrl} // Prevent caching issues
          controls 
          autoPlay
          style={{ maxWidth: '100%', height: 'auto', border: '1px solid #ccc' }}
        >
          <source src={videoUrl} type="video/mp4" />
          Your browser does not support the video tag.
        </video>
      )}
    </div>
  );
}
