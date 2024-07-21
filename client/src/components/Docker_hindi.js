import React, { useState } from "react";
import axios from "axios";

const DockerfileGenerator = () => {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");
  const [parsedResponse, setParsedResponse] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const API_URL = "http://65.2.48.169:5000/get_dockerfile";
      const headers = { "Content-Type": "application/json" };
      const payload = { query };
      const response = await axios.post(API_URL, payload, { headers });
      setResponse(JSON.stringify(response.data, null, 2));
      parseResponse(response.data); // Parse the response after receiving it
    } catch (error) {
      console.error("Failed to fetch data:", error);
      setResponse("Error occurred. Check console for details.");
    }
  };

  const parseResponse = (data) => {
    if (
      Array.isArray(data) &&
      data.length > 0 &&
      data[0].hasOwnProperty("generated_text")
    ) {
      const generatedText = data[0].generated_text;
      const dockerfileStartIndex = generatedText.indexOf("```");
      if (dockerfileStartIndex !== -1) {
        const dockerfileText = generatedText.substring(dockerfileStartIndex);
        setParsedResponse(dockerfileText);
      } else {
        setParsedResponse("Dockerfile not found in the response");
      }
    } else {
      setParsedResponse("Invalid response format");
    }
  };

  return (
    <div
      className="chat-container"
      style={{ width: "50%", marginLeft: "25%", marginTop: "30px" }}
    >
      <h1>Dockerfile Generator</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Query:
          <input
            style={{ width: "90%" }}
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            required
            placeholder="Enter query:"
          />
        </label>
        <button type="submit" className="button-50">
          Submit
        </button>
      </form>
      <div className="response-container">
        <h2>Response:</h2>
        <pre>{response}</pre>
        <h2>Parsed Dockerfile:</h2>
        <pre>{parsedResponse}</pre>
      </div>
    </div>
  );
};

export default DockerfileGenerator;
