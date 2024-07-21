import React from "react";
import "../button.css";
import "../aws.css";
import S3Manager from "../components/S3Manager";
import ImageGenerator from "../components/ImageGenerator";

function AWS() {
  const initiateInstance = async () => {
    try {
      const response = await fetch("http://localhost:5000/initiate_instance", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });
      const data = await response.json();
      
      console.log("Instance initiated:", data);
    } catch (error) {
      console.error("Error initiating instance:", error);
    }
  };

  const terminateInstances = async () => {
    const instanceIds = prompt(
      "Enter instance IDs to terminate (comma separated):"
    );
    if (!instanceIds) {
      alert("Instance IDs are required");
      return;
    }

    const instanceIdsArray = instanceIds.split(",").map((id) => id.trim());

    try {
      const response = await fetch(
        "http://localhost:5000/terminate_instances",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ instance_ids: instanceIdsArray }),
        }
      );
      const data = await response.json();
      console.log("Instances terminated:", data);
    } catch (error) {
      console.error("Error terminating instances:", error);
    }
  };

  return (
    <>
      <div class="container" style={{ marginTop: "50px" }}>
        <h1>AWS based Programs</h1>
        <p>This page is about the AWS based programs.</p>

        <div class="button-container">
          <button class="button-50" role="button" onclick="initiateInstance()">
            Instance Launch
          </button>

          <button
            class="button-50"
            role="button"
            onclick="terminateInstances()"
          >
            Delete Instance
          </button>
        </div>
      </div>
      <div style={{ marginTop: "50px" }}>
        <S3Manager />
      </div>
      <div style={{ marginTop: "50px" }}>
        <ImageGenerator />
      </div>
    </>
  );
}

export default AWS;
