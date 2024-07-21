import React, { useState } from "react";
import Filter_camera from "../components/Filter_camera";
import Hand_detection from "../components/Hand_detection";
import TPoseDetection from "../components/Tpose"; // Assuming you have created this component

const Vision = () => {
  const [showFilterCamera, setShowFilterCamera] = useState(true);
  const [showTPoseDetection, setShowTPoseDetection] = useState(false);

  const toggleComponent = (component) => {
    setShowFilterCamera(component === "FilterCamera");
    setShowTPoseDetection(component === "TPoseDetection");
  };

  return (
    <div style={{ width: "60%", margin: "5% 0px 0px 20%" }}>
      <div style={{ marginBottom: "5%" }}>
        <button
          className="button-50"
          onClick={() => toggleComponent("FilterCamera")}
        >
          Filter Camera
        </button>
        <button
          className="button-50"
          onClick={() => toggleComponent("HandDetection")}
        >
          Hand Detection
        </button>
        <button
          className="button-50"
          onClick={() => toggleComponent("TPoseDetection")}
        >
          T-pose Detection
        </button>
      </div>
      {showFilterCamera && <Filter_camera />}
      {showTPoseDetection && <TPoseDetection />}
      {!showFilterCamera && !showTPoseDetection && <Hand_detection />}
    </div>
  );
};

export default Vision;
