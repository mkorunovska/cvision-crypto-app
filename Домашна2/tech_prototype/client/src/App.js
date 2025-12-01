import React, { useEffect, useState } from "react";

import { BrowserRouter, Routes, Route } from "react-router-dom";
import Hero from "./components/Hero";
import Header from "./components/Header";
import NavMobile from "./components/NavMobile";
import Newsletter from "./components/Newsletter";
import Footer from "./components/Footer";

import Aos from "aos";
import "aos/dist/aos.css";
import DetailsPage from "./components/DetailsPage";
import About from "./components/About";

const App = () => {
  const [navMobile, setNavMobile] = useState(false);

  useEffect(() => {
    Aos.init({
      duration: 2500,
      delay: 400,
    });
  });

  return (
    <div className="overflow-hidden">
      <Routes>
        <Route
          path="/"
          element={
            <>
              <Header setNavMobile={setNavMobile} />
              <Hero />
              <div
                className={`${navMobile ? "right-0" : "-right-full"} 
        fixed x-10 top-0 h-full transition-all duration-200`}
              >
                <NavMobile setNavMobile={setNavMobile} />
              </div>
              <Newsletter />
              <Footer/>
            </>
          }
        ></Route>
        <Route
          path="/details"
          element={
            <>
              <Header setNavMobile={setNavMobile} />
              <DetailsPage />
              <div
                className={`${navMobile ? "right-0" : "-right-full"} 
        fixed x-10 top-0 h-full transition-all duration-200`}
              >
                <NavMobile setNavMobile={setNavMobile} />
              </div>
              <Footer/>
            </>
          }
        ></Route>
        <Route path="/about" element={<About />}></Route>
      </Routes>
    </div>
  );
};

export default App;
