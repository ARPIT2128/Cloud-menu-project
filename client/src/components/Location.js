import React, { useState, useEffect } from "react";
import "../loc.css";
const LocationComponent = () => {
  const [location, setLocation] = useState(null);

  useEffect(() => {
    const fetchLocation = async () => {
      try {
        const response = await fetch("/location");
        if (!response.ok) {
          throw new Error("Unable to fetch location data");
        }
        const data = await response.json();
        setLocation(data);
      } catch (error) {
        console.error("Error fetching location:", error);
      }
    };
    fetchLocation();
  }, []);

  return (
    <div className="location-container">
      <h2 className="location-header">Location Information</h2>
      {location ? (
        <div className="location-details">
          <p>
            <strong>Latitude:</strong> {location.latitude}
          </p>
          <p>
            <strong>Longitude:</strong> {location.longitude}
          </p>
          <p>
            <strong>City:</strong> {location.city}
          </p>
          <p>
            <strong>State:</strong> {location.state}
          </p>
        </div>
      ) : (
        <p>Loading location...</p>
      )}
    </div>
  );
};

export default LocationComponent;
