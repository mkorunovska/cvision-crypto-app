import React from "react";

import Logo from "../assets/img/logo.png";
import { IoLogoYoutube, IoLogoInstagram, IoLogoTwitter } from "react-icons/io";
import { Link } from "react-router-dom";

const Footer = () => {
  return (
    <footer className="lg:pt-24 pt-0">
      <div className="container mx-auto lg:mb-24">
        <div className="flex flex-col gap-12 lg:flex-row">
          <div className="flex-1 mx-auto lg:mx-0 mb-6 max-w-[285px]">
            <Link to="/">
              <img src={Logo} className="w-[140px] h-auto" alt="CVision Logo" />
            </Link>

          </div>
          <div className="flex flex-1 flex-col gap-16lg:flex-row">
            <div className="text-center w-full lg:justify-left">
              
              <div className="text-xl font-medium mb-6">Quick Links</div>
              <ul className="space-y-4 text-gray">
                <li>
                  <Link className="hover:text-blue/50" to="/">
                    Home
                  </Link>
                </li>
                <li>
                  <Link className="hover:text-blue/50" to="/details">
                    Details
                  </Link>
                </li>
                <li>
                  <Link className="hover:text-blue/50" to="/about">
                    About
                  </Link>
                </li>
                <li>
                  <Link className="hover:text-blue/50" to="/contact">
                    Contact
                  </Link>
                </li>
              </ul>
            </div>
          </div>
          <div className="flex gap-4 text-white text-2xl">
              <IoLogoYoutube className="hover:text-blue transition" />
              <IoLogoInstagram className="hover:text-blue transition" />
              <IoLogoTwitter className="hover:text-blue transition" />
            </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
