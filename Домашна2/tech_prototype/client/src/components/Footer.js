import React from "react";

import Logo from "../assets/img/logo.png";
import { IoLogoYoutube, IoLogoInstagram, IoLogoTwitter } from "react-icons";

const Footer = () => {
  return (
    <footer className="lg:pt-24 pt-0">
      <div className="container mx-auto lg:mb-24">
        <div className="flex flex-col gap-12 lg:flex-row">
          <div
            className="flex-1 mx-auto lg:mx-0 
          mb-6 max-w-[285px]"
          >
            <a href="#">
              <img src={Logo} className="w-[140px] h-auto" alt=""></img>
            </a>
          </div>
          <div
            className="flex flex-1 flex-col gap-16
          lg:flex-row"
          >
            <div
              className="text-center w-full
            lg:justify-left"
            >
              <div className="text-xl font-medium mb-6">Quick Links</div>
              <ul className="space-y-4 text-gray">
                <li>
                  <a className="hover:text-blue/50" href="">
                    Home
                  </a>
                </li>
                <li>
                  <a className="hover:text-blue/50" href="/details">
                    Details
                  </a>
                </li>
                <li>
                  <a className="hover:text-blue/50" href="">
                    About
                  </a>
                </li>
                <li>
                  <a className="hover:text-blue/50" href="">
                    Contact
                  </a>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
