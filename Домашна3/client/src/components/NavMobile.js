import React from "react";

import { navData } from "../data";
import { CgClose } from "react-icons/cg";

const NavMobile = ({ setNavMobile} ) => {
  return (
  <nav className="lg:hidden bgw bg-zinc-100 h-full top-0 botton-0 w-80 flex justify-center items-center">
    <div className="absolute top-2 left-2 cursor-poiner"
    onClick={()=>setNavMobile(false)}>
      <CgClose className="text-3xl" color="black"/>
    </div>
    <ul className="text-xl text-black flex flex-col gap-y-8">
      {navData.map((item,index)=>{
        return <li key={index}>
          <a href={item.href}>{item.name}</a>
        </li>
      })}
    </ul>
    </nav>
  );
};

export default NavMobile;
