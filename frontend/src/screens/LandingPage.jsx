import React from "react";
import { Link } from "react-router-dom";
import Footer from "../components/Footer";

function LandingPage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 text-center px-6">
      {/* Hero Section */}
      <h1 className="text-5xl md:text-6xl font-bold text-gray-800 dark:text-white mb-6">
        InsideOut
      </h1>
      <p className="text-lg md:text-2xl text-gray-600 dark:text-gray-300 max-w-3xl mb-8">
        An AI-powered system designed to monitor emotions of elderly individuals
        and provide calming responses, such as music, to improve their
        well-being.
      </p>

      {/* Login screen */}
      <Link
        to="/authentication"
        className="px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg shadow hover:bg-blue-700 transition"
      >
        Get Started
      </Link>

      {/* Features / Overview Section */}
      <div className="mt-16 grid gap-8 md:grid-cols-3 max-w-5xl w-full">
        <div className="p-6 bg-white dark:bg-gray-800 rounded-2xl shadow">
          <h3 className="text-xl font-semibold mb-2 text-gray-800 dark:text-white">
            Emotion Monitoring
          </h3>
          <p className="text-gray-600 dark:text-gray-300">
            Wearable devices and monitoring tools detect basic emotional states
            in real-time.
          </p>
        </div>
        <div className="p-6 bg-white dark:bg-gray-800 rounded-2xl shadow">
          <h3 className="text-xl font-semibold mb-2 text-gray-800 dark:text-white">
            Relaxing Music
          </h3>
          <p className="text-gray-600 dark:text-gray-300">
            AI selects calming music based on the detected emotions to enhance
            mood and reduce stress.
          </p>
        </div>
        <div className="p-6 bg-white dark:bg-gray-800 rounded-2xl shadow">
          <h3 className="text-xl font-semibold mb-2 text-gray-800 dark:text-white">
            Companion Feedback
          </h3>
          <p className="text-gray-600 dark:text-gray-300">
            Companions can provide feedback through surveys, helping to validate
            the system’s effectiveness.
          </p>
        </div>
      </div>
      <Footer/>
    </div>
  );
}

export default LandingPage;
