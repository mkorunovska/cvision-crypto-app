import React from "react";
import Image from "../assets/img/coin_image.png";
import { IoIosArrowDroprightCircle } from "react-icons/io";
import { useNavigate } from 'react-router-dom';

const Hero = () => {
  const navigate = useNavigate();

  const goToDetails = () => {
    navigate("/details");
  };

  return (
    <section className="section">
      <div className='container mx-auto'>
        <div className="flex flex-col items-center lg:flex-row">
          <div className="flex-1">
            <h1 className='text-[32px] lg:text-[64px]
            font-bold leading-tight mb-6 mt-6' 
            data-aos='fade-down'
            data-aos-delay='500'>
              Data Driven Predictions & Insights - the platform to invest in crypto. 
            </h1>
            <p className='max-w-[440px] leading-relaxed mb-8' data-aos='fade-down'
            data-aos-delay='600'>
              Powered by real market data and intelligent forecasting models,
              see the latest trends in the crypto world.
            </p>
            <button onClick={goToDetails} className='btn gap-x-4 pl-6 text-sm lg:text-base hover:bg-white' data-aos='fade-down'
            data-aos-delay='700' >
              Try for free
              <IoIosArrowDroprightCircle className="text-2xl"/>
              </button>
          </div>
          <div className='flex-2'>
            <img src={Image}  alt='' className="image" data-aos='fade-up' data-aos-delay='600'/>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;

