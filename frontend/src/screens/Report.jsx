import React from "react";
import HeartRateChart from "../components/dashboard/HeartRateChart";
import EdaChart from "../components/dashboard/EdaChart";
function Report() {
  return (
    <div>
      <HeartRateChart />
      <EdaChart />
    </div>
  );
}

export default Report;
