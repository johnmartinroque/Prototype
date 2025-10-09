import React from "react";
import { collection, getDoc, getDocs } from "firebase/firestore";

function ElderlyInfo() {
  const fetchElderly = async () => {
    const elderlyCollectionRef = collection(db, "elderly");
    const elderly = await getDoc(elderlyCollectionRef);
  };

  return (
    <div className="bg-white shadow-md rounded-xl p-6 border border-gray-200 hover:shadow-lg transition-all duration-200 flex flex-col items-center">
      {/* Title */}
      <h2 className="text-2xl font-semibold text-green-700 text-center mb-4">
        Elderly Information
      </h2>

      {/* Avatar Circle */}
      <div className="w-24 h-24 rounded-full bg-green-100 flex items-center justify-center text-green-600 text-3xl font-bold shadow-md mb-4">
        JC
      </div>

      {/* Details */}
      <div className="space-y-2 text-center text-gray-700">
        <p className="text-lg font-medium">Jon Cain Rivera</p>
        <p>joncain@email.com</p>
        <p>0969 452 3456</p>
        <hr className="my-3 border-gray-300" />
        <p className="font-semibold text-gray-800">Companions:</p>
        <ul className="space-y-1">
          <li>John Martin Roque</li>
          <li>Irah Lourene Tanhueco</li>
        </ul>
      </div>
    </div>
  );
}

export default ElderlyInfo;
