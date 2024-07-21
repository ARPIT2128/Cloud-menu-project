import React from "react";

const TPoseDetection = () => {
  const redirectToFlaskPage = () => {
    window.location.href = "http://localhost:5050/pose"; // Replace with your Flask server address
  };

  return (
    <div className="App">
      <h1>Redirecting to T-pose Detection...</h1>
      <button className="button-50" onClick={redirectToFlaskPage}>
        Go to T-pose Detection
      </button>
    </div>
  );
};

export default TPoseDetection;
