import React, { useEffect, useState } from "react";

const Prediction = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch latest data
  const fetchLatestData = async () => {
    try {
      const response = await fetch("http://localhost:5000/latest");
      if (!response.ok) throw new Error("No data available yet.");
      const jsonData = await response.json();
      setData(jsonData);
      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLatestData();
    const interval = setInterval(fetchLatestData, 5000);
    return () => clearInterval(interval);
  }, []);

  if (loading)
    return (
      <p className="text-gray-500 text-center mt-10">
        Loading latest GSR data...
      </p>
    );
  if (error)
    return <p className="text-red-500 text-center mt-10">Error: {error}</p>;

  return (
    <div className="max-w-3xl mx-auto p-6 space-y-6">
      <h1 className="text-3xl font-bold text-center text-blue-600">
        GSR Prediction
      </h1>

      <div className="bg-white shadow-md rounded-lg p-5 border-l-4 border-blue-500">
        <h2 className="text-xl font-semibold mb-2">GSR Value</h2>
        <p className="text-gray-700 text-lg">{data.gsr_value}</p>
      </div>

      <div className="bg-white shadow-md rounded-lg p-5 border-l-4 border-green-500">
        <h2 className="text-xl font-semibold mb-2">🧠 Emotion</h2>
        <p className="text-gray-700">
          <strong>Prediction:</strong> {data.emotion.prediction}
        </p>
        <p className="text-gray-700">
          <strong>Confidence:</strong>{" "}
          {data.emotion.confidence !== null
            ? `${data.emotion.confidence}%`
            : "N/A"}
        </p>
        <p className="text-gray-500 text-sm">
          <strong>Timestamp:</strong> {data.emotion.timestamp}
        </p>
      </div>

      <div className="bg-white shadow-md rounded-lg p-5 border-l-4 border-yellow-500">
        <h2 className="text-xl font-semibold mb-2">⚡ MWL (Mental Workload)</h2>
        <p className="text-gray-700">
          <strong>Prediction:</strong> {data.mwl.prediction}
        </p>
        <p className="text-gray-700">
          <strong>Confidence:</strong>{" "}
          {data.mwl.confidence !== null ? `${data.mwl.confidence}%` : "N/A"}
        </p>
        <p className="text-gray-500 text-sm">
          <strong>Timestamp:</strong> {data.mwl.timestamp}
        </p>
      </div>
    </div>
  );
};

export default Prediction;
