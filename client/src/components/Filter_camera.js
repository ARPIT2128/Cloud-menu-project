import React, { useRef, useEffect, useState } from "react";

const Filter_camera = () => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [isStreaming, setIsStreaming] = useState(false);
  const [message, setMessage] = useState("");
  const [processedImage, setProcessedImage] = useState("");
  const [captureIntervalId, setCaptureIntervalId] = useState(null);

  useEffect(() => {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices
        .getUserMedia({ video: true })
        .then((stream) => {
          videoRef.current.srcObject = stream;
          videoRef.current.play();
          setIsStreaming(true);
        })
        .catch((err) => {
          console.error("Error accessing the camera: ", err);
        });
    }
  }, []);

  const captureFrameContinuously = () => {
    const intervalId = setInterval(() => {
      if (videoRef.current && canvasRef.current) {
        const context = canvasRef.current.getContext("2d");
        context.drawImage(
          videoRef.current,
          0,
          0,
          canvasRef.current.width,
          canvasRef.current.height
        );
        canvasRef.current.toBlob((blob) => {
          if (blob) {
            const formData = new FormData();
            formData.append("frame", blob, "frame.png");
            fetch("http://localhost:5000/process_frame", {
              method: "POST",
              body: formData,
            })
              .then((response) => response.json())
              .then((data) => {
                if (data.success) {
                  setProcessedImage(data.processed_image);
                  setMessage("Frame successfully processed!");
                } else {
                  setMessage("Failed to process the frame.");
                }
              })
              .catch((error) => {
                console.error("Error:", error);
                setMessage("Error processing the frame.");
              });
          }
        }, "image/png");
      }
    }, 1000); // Adjust interval as needed (e.g., every second)
    setCaptureIntervalId(intervalId);
  };

  const stopCapture = () => {
    if (captureIntervalId) {
      clearInterval(captureIntervalId);
      setCaptureIntervalId(null);
      setMessage("Capture stopped.");
    }
  };
  return (
    <div style={{ display: "flex", justifyContent: "space-between" }}>
      {/* Camera Feed Section */}
      <div className="container">
        <h1>Camera Feed</h1>
        <video ref={videoRef} style={{ width: "100%", height: "auto" }} />
        <canvas
          ref={canvasRef}
          style={{ display: "none" }}
          width="640"
          height="480"
        ></canvas>
        {isStreaming && (
          <div className="button-container">
            <button className="button-50" onClick={captureFrameContinuously}>
              Start Continuous Capture
            </button>
            <button className="button-50" onClick={stopCapture}>
              Stop Capture
            </button>
            {message && <p>{message}</p>}
          </div>
        )}
      </div>

      {/* Processed Image Section */}
      <div className="container">
        {processedImage && (
          <div>
            <h2>Processed Image</h2>
            <img
              src={processedImage}
              alt="Processed Frame"
              style={{ width: "100%", height: "auto" }}
            />
          </div>
        )}
      </div>
    </div>
  );
};

export default Filter_camera;
