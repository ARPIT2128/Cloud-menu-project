import React, { useRef, useState } from "react";
import "../aws.css";
const MicrophoneRecorder = () => {
  const audioRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const [isRecording, setIsRecording] = useState(false);
  const [recordedChunks, setRecordedChunks] = useState([]);

  const handleStartRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      mediaRecorderRef.current.ondataavailable = handleDataAvailable;
      mediaRecorderRef.current.start();
      setIsRecording(true);
    } catch (error) {
      console.error("Error accessing microphone:", error);
    }
  };

  const handleStopRecording = () => {
    if (
      mediaRecorderRef.current &&
      mediaRecorderRef.current.state !== "inactive"
    ) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const handleDataAvailable = (event) => {
    if (event.data.size > 0) {
      setRecordedChunks((prev) => [...prev, event.data]);
    }
  };

  const handlePlayback = () => {
    const blob = new Blob(recordedChunks, { type: "audio/wav" });
    const url = URL.createObjectURL(blob);
    if (audioRef.current) {
      audioRef.current.src = url;
      audioRef.current.play();
    }
  };

  const handleDownload = () => {
    const blob = new Blob(recordedChunks, { type: "audio/wav" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.style.display = "none";
    a.href = url;
    a.download = "recording.wav";
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
  };

  return (
    <div>
      <button
        className="button-50"
        onClick={handleStartRecording}
        disabled={isRecording}
      >
        Start Recording
      </button>
      <button
        className="button-50"
        onClick={handleStopRecording}
        disabled={!isRecording}
      >
        Stop Recording
      </button>
      <button
        className="button-50"
        onClick={handlePlayback}
        disabled={recordedChunks.length === 0}
      >
        Playback
      </button>
      <button
        className="button-50"
        onClick={handleDownload}
        disabled={recordedChunks.length === 0}
      >
        Download Recording
      </button>
      <audio ref={audioRef} controls />
    </div>
  );
};

export default MicrophoneRecorder;
