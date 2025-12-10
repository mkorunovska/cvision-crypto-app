import React from "react";
import { navData } from "../data.js";
import { CgClose } from "react-icons/cg";
import { Link } from "react-router-dom";

const NavMobile = ({ setNavMobile} ) => {
  return (
  <nav className="lg:hidden bg-zinc-100 h-full fixed top-0 bottom-0 w-80 flex justify-center items-center">
    <div className="absolute top-2 left-2 cursor-pointer"
    onClick={()=>setNavMobile(false)}>
      <CgClose className="text-3xl" color="black"/>
    </div>
    <ul className="text-xl text-black flex flex-col gap-y-8">
      {navData.map((item,index)=>{
        return <li key={index}>
          <Link to={item.href}>{item.name}</Link>
        </li>
      })}
    </ul>
    </nav>
  );
};

export default NavMobile;


