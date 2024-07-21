import React, { useState, useEffect } from "react";

const HandDetection = () => {
  const redirectToFlaskPage = () => {
    window.location.href = "http://localhost:5000/"; // Replace with your Flask server address
  };

  return (
    <div className="App">
      <h1>Redirecting to Video Stream...</h1>
      <button className="button-50" onClick={redirectToFlaskPage}>
        Go to Video Stream
      </button>
    </div>
  );
};

export default HandDetection;
