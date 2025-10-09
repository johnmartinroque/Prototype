import React from "react";

function About() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 text-center px-6">
      {/* Main Section */}
      <div className="max-w-3xl">
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
          About Us
        </h1>
        <p className="text-lg text-gray-600 dark:text-gray-300 mb-8">
          Welcome to{" "}
          <span className="font-semibold text-indigo-500">InsideOut</span>, 
          an AI-powered emotion monitoring system created to support{" "}
          <span className="font-medium">elderly individuals</span>. 
          Our goal is to provide a compassionate tool that helps companions 
          and caregivers better understand and respond to the emotional needs 
          of the elderly.
        </p>

        {/* Mission */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-md p-6 mb-8">
          <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-2">
            Our Mission
          </h2>
          <p className="text-gray-600 dark:text-gray-300">
            We aim to improve the emotional well-being of elderly individuals 
            through AI-assisted monitoring. By combining vital sign tracking, and supportive feedback, we strive 
            to foster healthier, happier, and more connected lives.
          </p>
        </div>

        {/* Features / Benefits */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-md p-6">
            <h3 className="text-lg font-semibold text-indigo-500">Compassionate Support</h3>
            <p className="text-gray-600 dark:text-gray-300">
              Helps caregivers identify and respond to negative emotions promptly.
            </p>
          </div>
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-md p-6">
            <h3 className="text-lg font-semibold text-indigo-500">Health Monitoring</h3>
            <p className="text-gray-600 dark:text-gray-300">
              Wearable devices track vital signs such as heart rate and 
              skin conductance to detect stress or discomfort.
            </p>
          </div>
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-md p-6">
            <h3 className="text-lg font-semibold text-indigo-500">Elderly-Friendly</h3>
            <p className="text-gray-600 dark:text-gray-300">
              Designed with simplicity, accessibility, and comfort in mind 
              for older users and their companions.
            </p>
          </div>
        </div>

        {/* Team Section */}
        <div className="mt-12">
          <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
            Meet the Team
          </h2>
          <p className="text-gray-600 dark:text-gray-300 mb-6">
            A passionate group of students and innovators working together 
            to make emotional well-being more accessible through technology.
          </p>

          {/* Team Members */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-8 mt-6">
            {/* Member 1 */}
            <div className="flex flex-col items-center">
              <div className="w-24 h-24 rounded-full bg-indigo-200 flex items-center justify-center text-indigo-600 text-3xl font-bold shadow-md">
                J
              </div>
              <p className="mt-3 text-gray-900 dark:text-white font-medium">
                Jon Cain C. Rivera
              </p>
            </div>

            {/* Member 2 */}
            <div className="flex flex-col items-center">
              <div className="w-24 h-24 rounded-full bg-indigo-200 flex items-center justify-center text-indigo-600 text-3xl font-bold shadow-md">
                M
              </div>
              <p className="mt-3 text-gray-900 dark:text-white font-medium">
                John Martin L. Roque
              </p>
            </div>

            {/* Member 3 */}
            <div className="flex flex-col items-center">
              <div className="w-24 h-24 rounded-full bg-indigo-200 flex items-center justify-center text-indigo-600 text-3xl font-bold shadow-md">
                I
              </div>
              <p className="mt-3 text-gray-900 dark:text-white font-medium">
                Irah Lourene T. Tanhueco
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default About;
