import React from "react";

import { navData } from "../data.js";
import { Link } from "react-router-dom";

const Nav = () => {
  return (
    <nav className="flex items-center">
      <ul className="flex gap-x-8">
        {navData.map((item, index) => {
          return (
            <li className='border-b-2 border-transparent hover:border-white transition-all' key={index}>
              <Link to={item.href}>{item.name}</Link>
            </li>
          );
        })}
      </ul>
    </nav>
  );
};

export default Nav;


