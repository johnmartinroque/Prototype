import React, { useEffect, useState } from "react";
import Prediction from "../components/Prediction";
import CameraFeed from "../components/CameraFeed";

function Home() {
  return (
    <div>
      <Prediction />
      <CameraFeed />
    </div>
  );
}

export default Home;
