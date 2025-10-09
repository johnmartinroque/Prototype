import React from "react";
import ElderlyInfo from "../components/profile/ElderlyInfo";
import CompanionInfo from "../components/profile/CompanionInfo";

function Profile() {
  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-start py-16 px-6">
      {/* Page Title */}
      <h1 className="text-4xl md:text-5xl font-extrabold mb-10 text-gray-800 text-center relative">
        <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-green-600">
          Profile Overview
        </span>
        <div className="mt-2 w-20 h-1 bg-gradient-to-r from-blue-500 to-green-500 mx-auto rounded-full"></div>
      </h1>

      {/* Info Cards */}
      <div className="grid md:grid-cols-2 gap-10 w-full max-w-5xl">
        <CompanionInfo />
        <ElderlyInfo />
      </div>
    </div>
  );
}

export default Profile;
