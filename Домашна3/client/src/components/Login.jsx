import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const res = await fetch("http://localhost:8000/api/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
      });

      if (!res.ok) {
        setError("Invalid username or password");
        return;
      }

      const data = await res.json();
      localStorage.setItem("token", data.token);

      navigate("/");
    } catch (err) {
      console.error(err);
      setError("Backend not reachable");
    }
  };

  return (
    <div className="min-h-screen bg-blue-50 flex items-center justify-center">
      <div className="max-w-md mx-auto bg-darkblue p-8 rounded min-h-[60vh]">
        <h1 className="text-2xl font-bold mb-6 text-white">Login</h1>
        <form onSubmit={handleLogin} className="space-y-3">
          <input
            className="w-full p-3 rounded text-black border border-darkblue"
            placeholder="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />

          <input
            className="w-full p-3 rounded text-black border border-darkblue"
            type="password"
            placeholder="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <button
            className="w-full bg-blue-50 text-darkblue py-3 rounded hover:bg-blue-100"
            type="submit"
          >
            Login
          </button>

          {error && <p style={{ color: "red" }}>{error}</p>}

          <p className="text-sm text-white">
            Don't have an account yet?{" "}
            <Link className="underline" to="/register">
              Register here
            </Link>
          </p>
        </form>
      </div>
    </div>
  );
};

export default Login;
