import React, { useEffect, useState } from "react";
import HeartRateChart from "../components/dashboard/HeartRateChart";
import EdaChart from "../components/dashboard/EdaChart";
import Status from "../components/dashboard/Status";
import GSRValue from "../components/GSRValue";
function Home() {
  const [backendStatus, setBackendStatus] = useState("Checking...");

  useEffect(() => {
    // If you set up Vite proxy: fetch("/api")
    fetch("http://localhost:5000/")
      .then((res) => {
        if (res.ok) {
          setBackendStatus("✅ Backend detected");
        } else {
          setBackendStatus("❌ Backend not detected");
        }
      })
      .catch(() => setBackendStatus("❌ Backend not detected"));
  }, []);

  return (
    <div>
      <p className="text-xl">{backendStatus}</p>
      <HeartRateChart />

      <EdaChart />
      <Status />
      <GSRValue />
    </div>
  );
}

export default Home;
