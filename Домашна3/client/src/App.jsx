import React, { useEffect, useState } from "react";
import ProtectedRoute from "./ProtectedRoute.jsx";

import { Routes, Route, useLocation } from "react-router-dom";
import Hero from "./components/Hero.jsx";
import Header from "./components/Header.jsx";
import NavMobile from "./components/NavMobile.jsx";
import Newsletter from "./components/Newsletter.jsx";
import Footer from "./components/Footer.jsx";
import DetailsPage from "./components/DetailsPage.jsx";
import LstmAnalysis from "./components/LstmAnalysis.jsx";
import TechnicalAnalysis from "./components/TechnicalAnalysis.jsx";
import SentimentAnalysis from "./components/SentimentAnalysis.jsx";
import Login from "./components/Login.jsx";
import Register from "./components/Register.jsx";

import Aos from "aos";
import "aos/dist/aos.css";

const App = () => {
  const [navMobile, setNavMobile] = useState(false);

  useEffect(() => {
    Aos.init({
      duration: 2500,
      delay: 400,
    });
  });

  const location = useLocation();

  const isAuthPage =
  location.pathname === "/login" ||
  location.pathname === "/register";

  return (
    <div className="overflow-hidden bg-darkblue text-white min-h-screen">

      {!isAuthPage && (
      <>
        <Header setNavMobile={setNavMobile} />
        <div
          className={`${
            navMobile ? "right-0" : "-right-full"
          } fixed top-0 h-full transition-all duration-200 z-50`}
        >
          <NavMobile setNavMobile={setNavMobile} />
        </div>
      </>
    )}

      <Routes>
        <Route
          path="/"
          element={
            <>
              <Hero />
              <Newsletter />
            </>
          }
        />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route
          path="/details"
          element={
            <>
            <ProtectedRoute>
              <DetailsPage />
            </ProtectedRoute>
            </>
          }
        />
        <Route path="/technical" element={
          <>
            <ProtectedRoute>
              <TechnicalAnalysis />
            </ProtectedRoute>
          </>
          } 
        />
        <Route path="/lstm" element={
          <>
            <ProtectedRoute>
              <LstmAnalysis />
            </ProtectedRoute>
          </>
          } 
        />
        <Route path="/sentiment" element={
          <>
            <ProtectedRoute>
              <SentimentAnalysis />
            </ProtectedRoute>
          </>
          } 
        />
      </Routes>
      
      {!isAuthPage && <Footer />}
    </div>
  );
};

export default App;
