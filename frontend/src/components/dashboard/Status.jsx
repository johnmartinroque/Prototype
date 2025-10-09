import React, { useEffect, useState } from "react";
import { collection, query, onSnapshot } from "firebase/firestore";
import { db } from "../../firebase";

function Status() {
  const [status, setStatus] = useState({
    emotion: "",
    eda: "",
    ppg: "",
  });

  useEffect(() => {
    const statusCollection = collection(db, "status");
    const q = query(statusCollection);

    // Real-time listener
    const unsubscribe = onSnapshot(q, (snapshot) => {
      const statusData = snapshot.docs.map((doc) => ({
        id: doc.id,
        ...doc.data(),
      }));

      // Assuming you only have one status document
      if (statusData.length > 0) {
        setStatus({
          emotion: statusData[0].emotion || "",
          eda: statusData[0].eda || "",
          ppg: statusData[0].ppg || "",
        });
      }
    });

    // Cleanup on unmount
    return () => unsubscribe();
  }, []);

  return (
    <div className="flex flex-col items-center p-4 bg-white shadow-sm border border-gray-200 rounded-lg">
      <h1 className="text-3xl font-bold text-gray-900 text-center mb-4">
        Current Status
      </h1>
      <p>Emotional State: {status.emotion || "N/A"}</p>
      <p>EDA: {status.eda || "N/A"}</p>
      <p>PPG: {status.ppg || "N/A"}</p>
    </div>
  );
}

export default Status;
