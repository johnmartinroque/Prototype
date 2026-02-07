import React from "react";

const CameraFeed = () => {
  return (
    <div style={{ textAlign: "center" }}>
      <h2>Live Camera Feed</h2>
      <img
        src="http://localhost:5000/video_feed"
        alt="Live Camera"
        style={{
          width: "100%",
          maxWidth: "640px",
          borderRadius: "10px",
          border: "2px solid #333",
        }}
      />
    </div>
  );
};

export default CameraFeed;
