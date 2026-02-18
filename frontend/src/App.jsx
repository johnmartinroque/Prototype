import React, { useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { onAuthStateChanged } from "firebase/auth";
import Home from "./screens/Home";
import Header from "./components/Header";
import Authentication from "./screens/Authentication";
import HeaderGuest from "./components/HeaderGuest";
import { auth } from "./firebase";
import LandingPage from "./screens/LandingPage";
import Contact from "./screens/Contact";
import About from "./screens/About";
import ProtectedRoute from "./components/ProtectedRoute";
import NotFound from "./screens/NotFound";
import Camera from "./screens/CameraFeed.jsx";
import CameraFeed from "./screens/CameraFeed.jsx";
import Profile from "./screens/Profile.jsx";
import Report from "./screens/Report.jsx";
import "./App.css";

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser);
      setLoading(false); // 🔹 stop loading once auth is resolved
    });

    return () => unsubscribe();
  }, []);

  if (loading) {
    // 🔹 simple loading state (you can replace with spinner)
    return (
      <div className="flex justify-center items-center h-screen">
        <p className="text-lg">Loading...</p>
      </div>
    );
  }

  return (
    <div>
      <Router>
        {user ? <Header /> : <HeaderGuest />}
        <Routes>
          <Route path="/authentication" element={<Authentication />} />
          <Route path="/about" element={<About />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="*" element={<NotFound />} />

          {/* Protected Routes */}
          <Route
            path="/"
            element={
              user ? (
                <ProtectedRoute user={user}>
                  <Home />
                </ProtectedRoute>
              ) : (
                <LandingPage />
              )
            }
          />
          <Route
            path="/camera"
            element={
              <ProtectedRoute user={user}>
                <CameraFeed />
              </ProtectedRoute>
            }
          />
          <Route
            path="/report"
            element={
              <ProtectedRoute user={user}>
                <Report />
              </ProtectedRoute>
            }
          />
          <Route
            path="/profile"
            element={
              <ProtectedRoute user={user}>
                <Profile />
              </ProtectedRoute>
            }
          />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
