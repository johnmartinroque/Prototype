import React from "react";
import Login from "../components/authentication/Login";
import Register from "../components/authentication/Register";
import { useState } from "react";

function Authentication() {
  const [showLogin, setShowLogin] = useState(true);

  const handleShowLoginForm = () => {
    try {
      if (showLogin === true) {
        setShowLogin(false);
      } else {
        setShowLogin(true);
      }
    } catch (err) {
      console.error(err);
    }
  };
  return (
    <div>
      {showLogin ? (
        <Login handleShowLoginForm={handleShowLoginForm} />
      ) : (
        <Register handleShowLoginForm={handleShowLoginForm} />
      )}
    </div>
  );
}

export default Authentication;
