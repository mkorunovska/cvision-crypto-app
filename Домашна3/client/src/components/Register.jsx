import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";

const Register = () => {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    username: "",
    password: "",
    repeatPassword: "",
    name: "",
    surname: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const onChange = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setError("");

    if (!form.username || !form.password) {
      setError("Username and password are required.");
      return;
    }
    if (form.password !== form.repeatPassword) {
      setError("Passwords do not match.");
      return;
    }

    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/api/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });

      if (!res.ok) {
        const msg = await res.text();
        throw new Error(msg || `Register failed (${res.status})`);
      }
      navigate("/login", { replace: true });
    } catch (err) {
      setError(err.message || "Register failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-blue-50 flex items-center justify-center">
      <div className="max-w-md mx-auto p-6 min-h-[80vh]">
        <h1 className="text-2xl font-bold mb-6 text-darkblue">Register</h1>

        <form onSubmit={handleRegister} className="space-y-3">
          <input
            className="w-full p-3 rounded text-black border border-darkblue"
            name="username"
            placeholder="Username"
            value={form.username}
            onChange={onChange}
          />

          <input
            className="w-full p-3 rounded text-black border border-darkblue"
            name="name"
            placeholder="Name"
            value={form.name}
            onChange={onChange}
          />

          <input
            className="w-full p-3 rounded text-black border border-darkblue"
            name="surname"
            placeholder="Surname"
            value={form.surname}
            onChange={onChange}
          />

          <input
            className="w-full p-3 rounded text-black border border-darkblue"
            type="password"
            name="password"
            placeholder="Password"
            value={form.password}
            onChange={onChange}
          />

          <input
            className="w-full p-3 rounded text-black border border-darkblue"
            type="password"
            name="repeatPassword"
            placeholder="Repeat password"
            value={form.repeatPassword}
            onChange={onChange}
          />

          <button
            disabled={loading}
            className="w-full bg-darkblue text-white py-3 rounded hover:bg-blue-100"
            type="submit"
          >
            {loading ? "Creating account..." : "Register"}
          </button>

          {error && (
            <div className="p-3 bg-red-100 text-black rounded">{error}</div>
          )}

          <p className="text-sm text-darkblue">
            Already have an account?{" "}
            <Link className="underline" to="/login">
              Login
            </Link>
          </p>
        </form>
      </div>
    </div>
  );
};

export default Register;
