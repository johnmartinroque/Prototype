import React from "react";

function CompanionInfo() {
  return (
    <div className="bg-white shadow-md rounded-xl p-6 border border-gray-200 hover:shadow-lg transition-all duration-200 flex flex-col items-center">
      {/* Title */}
      <h2 className="text-2xl font-semibold text-blue-700 text-center mb-4">
        Companion Information
      </h2>

      {/* 1st Avatar */}
      <div className="w-24 h-24 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 text-3xl font-bold shadow-md mb-4">
        JM
      </div>

      {/* 1st Companion Details */}
      <div className="space-y-2 text-center text-gray-700">
        <p className="text-lg font-medium">John Martin Roque</p>
        <p>jmroque@email.com</p>
        <p>0912 231 4142</p>
      </div>

      {/* 2nd Avatar may space sa taas */}
      <div className="w-24 h-24 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 text-3xl font-bold shadow-md mt-8 mb-4">
        IL
      </div>

      {/* 2nd Companion Details */}
      <div className="space-y-2 text-center text-gray-700">
        <p className="text-lg font-medium">Irah Lourene Tanhueco</p>
        <p>il.tanhueco@email.com</p>
        <p>0954 645 3478</p>
      </div>
    </div>
  );
}

export default CompanionInfo;
