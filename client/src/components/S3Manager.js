import React, { useState, useEffect } from "react";
import "../s3.css";

const S3Manager = () => {
  const [buckets, setBuckets] = useState(null); // Initialize as null
  const [bucketName, setBucketName] = useState("");
  const [file, setFile] = useState(null);
  const [files, setFiles] = useState([]);
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetchBuckets();
  }, []);

  const fetchBuckets = () => {
    fetch("/list_files", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ bucket_name: bucketName }), // Ensure bucketName is defined
    })
      .then((response) => response.json())
      .then((data) => {
        setBuckets(data.buckets || []); // Set to empty array if data.buckets is undefined
      })
      .catch((error) => console.error("Error fetching buckets:", error));
  };

  const handleCreateBucket = async (event) => {
    event.preventDefault();
    try {
      const response = await fetch("/create_bucket", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ bucket_name: bucketName }),
      });
      const data = await response.json();
      setMessage(data.message || data.error);
      fetchBuckets(); // Refresh buckets list
    } catch (error) {
      console.error("Error creating bucket:", error);
      setMessage("Error creating bucket");
    }
  };

  return (
    <div className="container">
      <h2>Create S3 Bucket</h2>
      <form onSubmit={handleCreateBucket}>
        <label htmlFor="bucket_name">Bucket Name:</label>
        <input
          type="text"
          id="bucket_name"
          value={bucketName}
          onChange={(e) => setBucketName(e.target.value)}
          required
        />
        <br />
        <br />
        <button className="button-50" type="submit">
          Create Bucket
        </button>
      </form>

      {message && <div className="message">{message}</div>}
    </div>
  );
};

export default S3Manager;
