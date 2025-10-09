import React, { useState, useEffect } from "react";
import axios from "axios";

const GSRMonitor = () => {
  const [gsrValue, setGsrValue] = useState(null);
  const [prediction, setPrediction] = useState("");
  const [confidence, setConfidence] = useState(null);
  const [error, setError] = useState(null);

  // Function to fetch data from Flask server
  const fetchGSRData = async () => {
    try {
      const response = await axios.get("http://localhost:5000/latest"); // We'll discuss endpoint later
      const data = response.data;
      setGsrValue(data.gsr_value);
      setPrediction(data.prediction);
      setConfidence(data.confidence);
      setError(null);
    } catch (err) {
      console.error("Error fetching GSR data:", err);
      setError("Failed to fetch data");
    }
  };

  // Poll every 2 seconds
  useEffect(() => {
    const interval = setInterval(fetchGSRData, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h2>GSR Monitor</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}
      {gsrValue !== null ? (
        <div>
          <p>
            <strong>GSR Value:</strong> {gsrValue.toFixed(3)} V
          </p>
          <p>
            <strong>MWL Prediction:</strong>{" "}
            <span
              style={{
                color: prediction === "High MWL" ? "red" : "green",
                fontWeight: "bold",
              }}
            >
              {prediction}
            </span>
          </p>
          {confidence && (
            <p>
              <strong>Confidence:</strong> {confidence.toFixed(1)}%
            </p>
          )}
        </div>
      ) : (
        <p>Waiting for data...</p>
      )}
    </div>
  );
};

export default GSRMonitor;
