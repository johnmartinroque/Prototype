import { onAuthStateChanged, signOut } from "firebase/auth";
import React, { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { auth } from "../firebase";

function Header() {
  const [user, setUser] = useState(null);
  const [isOpen, setIsOpen] = useState(false); // dropdown state
  const [isMenuOpen, setIsMenuOpen] = useState(false); // mobile nav state
  const [currentNav, setCurrentNav] = useState("/");
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await signOut(auth);
      localStorage.removeItem("userInfo");
      navigate("/");
    } catch (err) {
      console.error(err);
    }
  };

  const linkClass = (path) =>
    currentNav === path
      ? "block py-2 pr-4 pl-3 text-white rounded bg-primary-700 lg:bg-transparent lg:text-primary-700 lg:p-0 dark:text-white"
      : "block py-2 pr-4 pl-3 text-gray-700 border-b border-gray-100 lg:border-0 hover:bg-gray-50 lg:hover:bg-transparent lg:hover:text-primary-700 lg:p-0 dark:text-gray-400 dark:hover:text-white dark:hover:bg-gray-700 lg:dark:hover:bg-transparent dark:border-gray-700";

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser);
    });
    return () => unsubscribe();
  }, []);

  return (
    <div>
      <header>
        <nav className="bg-white border-gray-200 px-4 lg:px-6 py-2.5 dark:bg-gray-800">
          <div className="flex flex-wrap justify-between items-center mx-auto max-w-screen-xl">
            {/* Logo */}
            <Link to="/" className="flex items-center">
              <img
                src="https://flowbite.com/docs/images/logo.svg"
                className="mr-3 h-6 sm:h-9"
                alt="Logo"
              />
              <span className="self-center text-xl font-semibold whitespace-nowrap dark:text-white">
                InsideOut
              </span>
            </Link>

            {/* Mobile menu toggle */}
            <div className="flex items-center lg:order-2">
              <button
                onClick={() => setIsMenuOpen(!isMenuOpen)}
                type="button"
                className="inline-flex items-center p-2 ml-1 text-sm text-gray-500 rounded-lg lg:hidden hover:bg-gray-100 
                focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 
                dark:focus:ring-gray-600"
                aria-controls="mobile-menu-2"
                aria-expanded={isMenuOpen}
              >
                <span className="sr-only">Open main menu</span>
                {!isMenuOpen ? (
                  <svg
                    className="w-6 h-6"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      fillRule="evenodd"
                      d="M3 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 10a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 15a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z"
                      clipRule="evenodd"
                    ></path>
                  </svg>
                ) : (
                  <svg
                    className="w-6 h-6"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      fillRule="evenodd"
                      d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                      clipRule="evenodd"
                    ></path>
                  </svg>
                )}
              </button>
            </div>

            {/* Nav links */}
            <div
              className={`${
                isMenuOpen ? "block" : "hidden"
              } justify-between items-center w-full lg:flex lg:w-auto lg:order-1`}
              id="mobile-menu-2"
            >
              <ul className="flex flex-col mt-4 font-medium lg:flex-row lg:space-x-8 lg:mt-0">
                <li>
                  <Link
                    to="/"
                    onClick={() => setCurrentNav("/")}
                    className={linkClass("/")}
                  >
                    Home
                  </Link>
                </li>
                <li>
                  <Link
                    to="/report"
                    onClick={() => setCurrentNav("/report")}
                    className={linkClass("/report")}
                  >
                    Daily Summary Report
                  </Link>
                </li>
                <li>
                  <Link
                    to="/camera"
                    onClick={() => setCurrentNav("/camera")}
                    className={linkClass("/camera")}
                  >
                    Camera
                  </Link>
                </li>
                <li>
                  <Link
                    to="/alerts"
                    onClick={() => setCurrentNav("/alerts")}
                    className={linkClass("/alerts")}
                  >
                    Alerts and SMS History
                  </Link>
                </li>

                {/* Dropdown */}
                <li className="relative">
                  <button
                    onClick={() => setIsOpen((prev) => !prev)}
                    className="flex items-center py-2 pr-4 pl-3 text-gray-700 border-b border-gray-100 
    hover:bg-gray-50 lg:hover:bg-transparent lg:border-0 lg:hover:text-primary-700 lg:p-0 
    dark:text-gray-400 lg:dark:hover:text-white dark:hover:bg-gray-700 
    dark:hover:text-white lg:dark:hover:bg-transparent dark:border-gray-700"
                  >
                    {user ? user.email : "Guest"}
                    <svg
                      className="w-4 h-4 ml-1"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth="2"
                        d="M19 9l-7 7-7-7"
                      />
                    </svg>
                  </button>

                  {isOpen && (
                    <ul
                      className="absolute right-0 mt-2 w-40 bg-white border border-gray-200 rounded-lg shadow-lg 
  dark:bg-gray-800 dark:border-gray-700 z-50"
                    >
                      {user ? (
                        <>
                          <li>
                            <Link
                              to="/profile"
                              onClick={() => setCurrentNav("/profile")}
                              className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 
          dark:text-gray-300 dark:hover:bg-gray-600"
                            >
                              Profile
                            </Link>
                          </li>
                          <li>
                            <button
                              onClick={handleLogout}
                              className="w-full text-left block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 
          dark:text-gray-300 dark:hover:bg-gray-600"
                            >
                              Logout
                            </button>
                          </li>
                        </>
                      ) : (
                        <>
                          <li>
                            <Link
                              to="/login"
                              onClick={() => setCurrentNav("/")}
                              className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 
          dark:text-gray-300 dark:hover:bg-gray-600"
                            >
                              Login
                            </Link>
                          </li>
                          <li>
                            <Link
                              to="/register"
                              onClick={() => setCurrentNav("/register")}
                              className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 
          dark:text-gray-300 dark:hover:bg-gray-600"
                            >
                              Register
                            </Link>
                          </li>
                        </>
                      )}
                    </ul>
                  )}
                </li>
              </ul>
            </div>
          </div>
        </nav>
      </header>
    </div>
  );
}

export default Header;
