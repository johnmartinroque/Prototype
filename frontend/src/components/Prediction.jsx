import React, { useEffect, useState } from "react";
import { doc, getDoc, updateDoc } from "firebase/firestore";
import { db } from "../firebase";

const Prediction = () => {
  const [data, setData] = useState(null);
  const [edaAverage, setEdaAverage] = useState(null);
  const [error, setError] = useState(null);

  const ELDERLY_DOC_ID = "pbMm29stjBct5TxxK0bQ";

  const updateEdaAverage = async (gsrValue) => {
    try {
      const docRef = doc(db, "elderly", ELDERLY_DOC_ID);
      const docSnap = await getDoc(docRef);

      let newAverage = gsrValue;

      if (docSnap.exists() && docSnap.data().edaAverage !== undefined) {
        const oldAverage = docSnap.data().edaAverage;
        newAverage = (oldAverage + gsrValue) / 2;
      }

      await updateDoc(docRef, { edaAverage: newAverage });
      setEdaAverage(newAverage.toFixed(2));
    } catch (err) {
      console.error("Error updating edaAverage:", err);
    }
  };

  const fetchLatestData = async () => {
    try {
      const response = await fetch("http://localhost:5000/latest");
      if (!response.ok) throw new Error("No data available yet.");
      const jsonData = await response.json();
      setData(jsonData);

      await updateEdaAverage(jsonData.gsr_value);
    } catch (err) {
      setError(err.message);
    }
  };

  useEffect(() => {
    fetchLatestData();
    const interval = setInterval(fetchLatestData, 5000);
    return () => clearInterval(interval);
  }, []);

  if (error)
    return <p className="text-red-500 text-center mt-10">Error: {error}</p>;
  if (!data)
    return (
      <p className="text-gray-500 text-center mt-10">
        Loading latest GSR data...
      </p>
    );

  return (
    <div className="max-w-3xl mx-auto p-6 space-y-6">
      <h1 className="text-3xl font-bold text-center text-blue-600">
        GSR Prediction (Realtime)
      </h1>

      <div className="bg-white shadow-md rounded-lg p-5 border-l-4 border-blue-500">
        <h2 className="text-xl font-semibold mb-2">GSR Value</h2>
        <p className="text-gray-700">{data.gsr_value}</p>
      </div>

      <div className="bg-white shadow-md rounded-lg p-5 border-l-4 border-purple-500">
        <h2 className="text-xl font-semibold mb-2">📊 EDA Average Today</h2>
        <p className="text-gray-700">
          {edaAverage !== null ? edaAverage : "N/A"}
        </p>
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
        {data.emotion.all_percentages && (
          <div className="text-gray-700 mt-2">
            <strong>All Probabilities:</strong>
            <ul className="list-disc list-inside">
              {Object.entries(data.emotion.all_percentages).map(
                ([key, val]) => (
                  <li key={key}>
                    {key}: {val}%
                  </li>
                ),
              )}
            </ul>
          </div>
        )}
        <p className="text-gray-500 text-sm mt-1">
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
        {data.mwl.all_percentages && (
          <div className="text-gray-700 mt-2">
            <strong>All Probabilities:</strong>
            <ul className="list-disc list-inside">
              {Object.entries(data.mwl.all_percentages).map(([key, val]) => (
                <li key={key}>
                  {key}: {val}%
                </li>
              ))}
            </ul>
          </div>
        )}
        <p className="text-gray-500 text-sm mt-1">
          <strong>Timestamp:</strong> {data.mwl.timestamp}
        </p>
      </div>
    </div>
  );
};

export default Prediction;
