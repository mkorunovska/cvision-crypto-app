import React, { useEffect, useState } from "react";

import { Routes, Route } from "react-router-dom";
import Hero from "./components/Hero.jsx";
import Header from "./components/Header.jsx";
import NavMobile from "./components/NavMobile.jsx";
import Newsletter from "./components/Newsletter.jsx";
import Footer from "./components/Footer.jsx";
import DetailsPage from "./components/DetailsPage.jsx";
import About from "./components/About.jsx";

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

  return (
    <div className="overflow-hidden bg-darkblue text-white min-h-screen">
      <Header setNavMobile={setNavMobile} />
      <div
        className={`${
          navMobile ? "right-0" : "-right-full"
        } fixed top-0 h-full transition-all duration-200 z-50`}
      >
        <NavMobile setNavMobile={setNavMobile} />
      </div>

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
        <Route
          path="/details"
          element={
            <>
              <DetailsPage />
            </>
          }
        />
        <Route path="/about" element={<About />} />
      </Routes>
       <Footer />
    </div>
  );
};

export default App;
