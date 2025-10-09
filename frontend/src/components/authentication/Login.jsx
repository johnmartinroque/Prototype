import {
  sendPasswordResetEmail,
  signInWithEmailAndPassword,
} from "firebase/auth";
import React, { useState } from "react";
import { auth } from "../../firebase";
import { useNavigate } from "react-router-dom";
import Spinner from "../Spinner";

function Login({ handleShowLoginForm }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");
  const [showSuccess, setShowSuccess] = useState(false);
  const [resetMessage, setResetMessage] = useState("");

  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setShowSuccess(false);
    try {
      const userCredential = await signInWithEmailAndPassword(
        auth,
        email,
        password
      );
      localStorage.setItem("userInfo", JSON.stringify(userCredential.user));
      setEmail("");
      setPassword("");
      setShowSuccess(true);
      setTimeout(() => {
        navigate("/");
      }, 1500);
    } catch (err) {
      console.error(err);
      setError("Invalid email or password. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleForgotPassword = async () => {
    if (!email) {
      setError("Please enter your email address to reset password.");
      return;
    }
    setLoading(true);
    setError("");
    setResetMessage("");
    try {
      await sendPasswordResetEmail(auth, email);
      setResetMessage("Password reset email sent! Please check your inbox.");
    } catch (err) {
      console.error(err);
      setError("Failed to send reset email. Please check your email address.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-b from-blue-50 to-white dark:from-gray-900 dark:to-gray-800 px-6">
      <form
        onSubmit={handleLogin}
        className="w-full max-w-md bg-white rounded-2xl shadow-lg p-8 border border-gray-200"
      >
        <h1 className="text-3xl font-bold text-gray-900 text-center">Login</h1>
        <p className="text-gray-500 text-sm text-center mt-2">
          Please sign in to continue
        </p>

        {/* Email */}
        <div className="flex items-center w-full mt-8 bg-white border border-gray-300 h-12 rounded-full overflow-hidden pl-6 gap-2">
          <svg
            width="16"
            height="11"
            viewBox="0 0 16 11"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              fillRule="evenodd"
              clipRule="evenodd"
              d="M0 .55.571 0H15.43l.57.55v9.9l-.571.55H.57L0 10.45zm1.143 1.138V9.9h13.714V1.69l-6.503 4.8h-.697zM13.749 1.1H2.25L8 5.356z"
              fill="#6B7280"
            />
          </svg>
          <input
            type="email"
            placeholder="Email"
            className="bg-transparent text-gray-700 placeholder-gray-400 outline-none text-sm w-full h-full"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>

        {/* Password */}
        <div className="flex items-center mt-4 w-full bg-white border border-gray-300 h-12 rounded-full overflow-hidden pl-6 gap-2">
          <svg
            width="13"
            height="17"
            viewBox="0 0 13 17"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M13 8.5c0-.938-.729-1.7-1.625-1.7h-.812V4.25C10.563 1.907 8.74 0 6.5 0S2.438 1.907 2.438 4.25V6.8h-.813C.729 6.8 0 7.562 0 8.5v6.8c0 .938.729 1.7 1.625 1.7h9.75c.896 0 1.625-.762 1.625-1.7zM4.063 4.25c0-1.406 1.093-2.55 2.437-2.55s2.438 1.144 2.438 2.55V6.8H4.061z"
              fill="#6B7280"
            />
          </svg>
          <input
            type="password"
            placeholder="Password"
            className="bg-transparent text-gray-700 placeholder-gray-400 outline-none text-sm w-full h-full"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>

        {/* Forgot password */}
        <div className="mt-3 text-right">
          <button
            type="button"
            onClick={handleForgotPassword}
            className="text-sm text-indigo-500 hover:underline"
          >
            Forgot password?
          </button>
        </div>

        {/* Spinner */}
        {loading && <Spinner />}

        {/* Alerts */}
        {error && (
          <div
            className="flex items-center p-3 mt-4 text-sm text-red-700 border border-red-300 rounded-lg bg-red-50"
            role="alert"
          >
            <span className="font-medium">Error:</span>&nbsp;{error}
          </div>
        )}

        {showSuccess && !error && (
          <div
            className="flex items-center p-3 mt-4 text-sm text-green-700 border border-green-300 rounded-lg bg-green-50"
            role="alert"
          >
            <span className="font-medium">Success:</span>&nbsp;Login Successful
          </div>
        )}

        {resetMessage && (
          <div
            className="flex items-center p-3 mt-4 text-sm text-blue-700 border border-blue-300 rounded-lg bg-blue-50"
            role="alert"
          >
            <span className="font-medium">Info:</span>&nbsp;{resetMessage}
          </div>
        )}

        {/* Submit Button */}
        <button
          type="submit"
          className="mt-6 w-full h-12 rounded-full text-white font-medium bg-indigo-500 hover:bg-indigo-600 transition"
          disabled={loading}
        >
          Login
        </button>

        {/* Switch to Register */}
        <p className="text-gray-500 text-sm text-center mt-4">
          Don’t have an account?{" "}
          <span
            onClick={handleShowLoginForm}
            className="text-indigo-500 font-medium cursor-pointer hover:underline"
          >
            Sign up
          </span>
        </p>
      </form>
    </div>
  );
}

export default Login;
