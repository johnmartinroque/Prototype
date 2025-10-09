import React, { useEffect, useRef, useState } from "react";

function CameraFeed() {
  const videoRef = useRef(null);
  const [showFeed, setShowFeed] = useState(false);

  useEffect(() => {
    if (showFeed) {
      navigator.mediaDevices
        .getUserMedia({ video: true, audio: false })
        .then((stream) => {
          if (videoRef.current) {
            videoRef.current.srcObject = stream;
          }
        })
        .catch((err) => {
          console.error("Error accessing webcam: ", err);
        });
    } else {
      // Stop camera when feed is hidden
      if (videoRef.current && videoRef.current.srcObject) {
        const tracks = videoRef.current.srcObject.getTracks();
        tracks.forEach((track) => track.stop());
        videoRef.current.srcObject = null;
      }
    }
  }, [showFeed]);

  return (
    <div className="flex flex-col items-center gap-4">
      {!showFeed ? (
        <button
          onClick={() => setShowFeed(true)}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg shadow hover:bg-blue-700"
        >
          Show Video Feed
        </button>
      ) : (
        <video
          ref={videoRef}
          autoPlay
          playsInline
          className="rounded-lg border border-gray-300 shadow-md w-[640px] h-[480px]"
        />
      )}
    </div>
  );
}

export default CameraFeed;
