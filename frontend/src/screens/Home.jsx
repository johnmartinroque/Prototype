import React, { useEffect, useState } from "react";
import HeartRateChart from "../components/dashboard/HeartRateChart";
import EdaChart from "../components/dashboard/EdaChart";
import Prediction from "../components/Prediction";
function Home() {
  return (
    <div>
      <HeartRateChart />

      <EdaChart />
      <Prediction />
    </div>
  );
}

export default Home;
