import React from "react";
import { useHistory } from "react-router-dom"; // Assuming you use react-router for routing

import Footer from "../components/Footer";
import LocationComponent from "../components/Location";

function Home() {
  const redirectToBlog = () => {
    const blogUrl = "http://localhost:5173";
    window.open(blogUrl, "_blank"); // Opens the URL in a new tab
  };
  const redirectToec2 = () => {
    const blogUrl = "http://13.200.128.50";
    window.open(blogUrl, "_blank"); // Opens the URL in a new tab
  };

  return (
    <>
      <div>
        <LocationComponent />
      </div>
      <div style={{ marginTop: "30px", textAlign: "center" }}>
        <p style={{ marginBottom: "10px" }}>
          Want some Updates on ML? Come to my blog page
        </p>
        <button className="button-50" onClick={redirectToBlog}>
          Visit The NEURAL NEWS
        </button>
        <button className="button-50" onClick={redirectToec2}>
          want more programs ?
        </button>
      </div>

      <Footer />
    </>
  );
}

export default Home;
