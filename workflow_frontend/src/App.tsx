import { useEffect, useState } from 'react';

export default function App() {
  const [videoUrl, setVideoUrl] = useState('');
  const BACKEND_URL = 'http://localhost:5000'; // Adjust this if necessary
  const VIDEO_PATH = '/videos/7906b351-a.mp4'; // Constant video path

  // Function to construct the full video URL
  const getFullVideoUrl = (videoPath) => {
    return videoPath.startsWith('http') ? videoPath : BACKEND_URL + videoPath;
  };

  useEffect(() => {
    const fullUrl = getFullVideoUrl(VIDEO_PATH);
    setVideoUrl(fullUrl);
  }, []); // Runs once when component mounts

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
      <h1>Constant Video Render</h1>
      {videoUrl && (
        <video
          key={videoUrl} // Prevent caching issues
          controls
          autoPlay
          loop
          style={{ maxWidth: '100%', height: 'auto', border: '1px solid #ccc' }}
        >
          <source src={videoUrl} type="video/mp4" />
          Your browser does not support the video tag.
        </video>
      )}
    </div>
  );
}
