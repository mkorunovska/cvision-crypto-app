import React from 'react';

import Logo from "../assets/img/logo.png";
import Nav from "./Nav";
import AccountBtns from "./AccountBtns";

import { CgMenuRight } from "react-icons/cg";

const Header = ({setNavMobile}) => {
  return (
    <header className='py-[30px] lg:pt-[50px]' 
    data-aos='fade-down' 
    data-aos-delay='900' 
    data-aos-duration='2000'>
      <div className='container mx-auto flex items-center justify-between'>
        <a href='#'>
          <img src={Logo} alt="" className="w-[140px] h-auto"/>
        </a>
        
        <div className='hidden lg:flex gap-x-[60px]'>
          <Nav />
          <AccountBtns />
        </div>
        <div className='lg:hidden cursor-pointer' onClick={()=>setNavMobile(true)}>
          <CgMenuRight className='text-2xl'/>
        </div>
       
      </div>
    </header>
  );
};

export default Header;
