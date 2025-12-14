import React from "react";
import { Link, useNavigate } from "react-router-dom";

const AccountBtns = () => {
  const navigate = useNavigate();
  const isLoggedIn = !!localStorage.getItem("token");

  const logout = () => {
    localStorage.removeItem("token");
    navigate("/", { replace: true });
  };

  return (
    <div className="flex items-center font-medium">
      {isLoggedIn ? (
        <button
          onClick={logout}
          className="btn h-[40px] px-5 text-base hover:bg-blue/60 hover:text-white"
        >
          Logout
        </button>
      ) : (
        <>
          <Link className="hover:text-blue/60 transition" to="/login">
            Login
          </Link>
          <span className="mx-4 text-white/20">|</span>
          <Link to="/register">
            <button className="btn h-[40px] px-5 text-base hover:bg-blue/60 hover:text-white">
              Register
            </button>
          </Link>
        </>
      )}
    </div>
  );
};

export default AccountBtns;
