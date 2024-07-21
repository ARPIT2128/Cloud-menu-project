import React, { useState } from "react";
import axios from "axios";

function Gemini() {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");

  const handleMessageSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post("/chat_gemini", { message });
      setResponse(response.data.response);
    } catch (error) {
      console.error("Error fetching response:", error);
    }
  };

  return (
    <div
      className="chat-container"
      style={{ width: "50%", marginLeft: "25%", marginTop: "30px" }}
    >
      <h1>✨Chat with Gemini</h1>
      <form onSubmit={handleMessageSubmit}>
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Enter your message"
        />
        <button className="button-50" type="submit">
          Send
        </button>
      </form>
      {response && (
        <div className="response-container">
          <h2>Response:</h2>
          <p>{response}</p>
        </div>
      )}
    </div>
  );
}

export default Gemini;
