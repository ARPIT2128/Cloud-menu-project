import React, { useState } from "react";
import axios from "axios";
import "../audio.css";
import "../button.css";
const Audio_text = () => {
  const [recordedText, setRecordedText] = useState("");
  const [text, setText] = useState("");
  const [processedText, setProcessedText] = useState("");

  const handleSpeechToText = async () => {
    try {
      const response = await fetch("/speech-to-text", {
        method: "POST",
      });
      const data = await response.json();
      if (response.ok) {
        setRecordedText(data.text);
      } else {
        console.error(data.error);
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(
        "http://localhost:5000/text_to_speech",
        {
          text,
        }
      );
      const processedText = response.data.processed_text;
      setProcessedText(processedText);
      speakText(processedText);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const speakText = (text) => {
    if ("speechSynthesis" in window) {
      const utterance = new SpeechSynthesisUtterance(text);
      window.speechSynthesis.speak(utterance);
    } else {
      alert("Speech synthesis is not supported in this browser.");
    }
  };

  const handleInputChange = (event) => {
    setText(event.target.value);
  };

  return (
    <div className="container">
      <h1>Speech-to-Text and Text-to-Speech Example</h1>
      <button className="button-50" onClick={handleSpeechToText}>
        Start Recording
      </button>
      <p>Recorded Text: {recordedText}</p>
      <div>
        <form onSubmit={handleSubmit}>
          <input
            className="input"
            type="text"
            value={text}
            onChange={handleInputChange}
            placeholder="Enter text to speak"
          />
          <button className="button-50" type="submit">
            Speak
          </button>
        </form>
        <div>
          <h3>Processed Text:</h3>
          <pre className="processed-text">{processedText}</pre>
        </div>
      </div>
    </div>
  );
};

export default Audio_text;
