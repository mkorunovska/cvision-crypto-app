import React from "react";
import { Link } from "react-router-dom";

const AccountBtns = () => {
  return (
    <div className="flex items-center font-medium">
      <Link className="hover:text-blue/60 transition" to="/login">
        Login
      </Link>
      <span className="mx-4 text-white/20">|</span>

      <Link to="/register">
        <button className="btn h-[40px] px-5 text-base hover:bg-blue/60 hover:text-white">
          Register
        </button>
      </Link>
    </div>
  );
};

export default AccountBtns;
