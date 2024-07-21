import React, { useState } from "react";
import axios from "axios";
import "../aws.css";
import "../button.css";
const ImageGenerator = () => {
  const [prompt, setPrompt] = useState("");
  const [message, setMessage] = useState("");
  const [imageUrl, setImageUrl] = useState("");

  const handleChange = (e) => {
    setPrompt(e.target.value);
  };

  const handleClick = async () => {
    try {
      const response = await axios.post(
        "http://localhost:5000/generate_image",
        { prompt }
      );
      setMessage(response.data.message);
      const generatedImageUrl = `http://localhost:5000/${response.data.image_url}`;
      console.log("Generated Image URL:", generatedImageUrl); // Log the URL to check correctness
      setImageUrl(generatedImageUrl);
    } catch (error) {
      setMessage("Error: Unable to generate image.");
      console.error(error);
    }
  };

  return (
    <div className="container">
      <h1>Image Generator</h1>
      <div className="form-container">
        <input
          type="text"
          value={prompt}
          onChange={handleChange}
          placeholder="Enter your prompt"
          style={{ width: "100%", padding: "10px", marginBottom: "10px" }}
        />
        <br />
        <button className="button-50" onClick={handleClick}>
          Generate Image
        </button>
      </div>
      <div className="button-container">
        <p>{message}</p>
        {imageUrl && (
          <div style={{ marginTop: "20px" }}>
            <h2>Generated Image:</h2>
            <img src={imageUrl} alt="Generated" style={{ maxWidth: "100%" }} />
          </div>
        )}
      </div>
    </div>
  );
};

export default ImageGenerator;
