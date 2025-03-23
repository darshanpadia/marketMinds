// src/pages/Login.jsx
import { useState } from "react";
import "./Login.css";
import "../styles.css";

function Login() {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const [error, setError] = useState("");

  const handleChange = (e) => {
    setFormData({ 
      ...formData, 
      [e.target.name]: e.target.value 
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
    const response = await fetch(`${API_BASE_URL}/users/api/login/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    });

    const data = await response.json();

    if (response.ok) {
      alert(`Welcome, ${data.user.email}!`);
      localStorage.setItem("access", data.access);
      localStorage.setItem("refresh", data.refresh);
    } else {
      setError(data.non_field_errors || "Invalid credentials");
    }
  };

  return (
    <div className="page-wrapper">
      <div className="login-container">
        <h2>Login</h2>
        {error && <p className="error">{error}</p>}
        <form onSubmit={handleSubmit} className="login-form">
          <input
            type="email"
            name="email"
            placeholder="Enter your email"
            value={formData.email}
            onChange={handleChange}
            required
          />
          <input
            type="password"
            name="password"
            placeholder="Enter your password"
            value={formData.password}
            onChange={handleChange}
            required
          />
          <button type="submit">Login</button>
        </form>
        <p className="forgot-password">Forgot password?</p>
      </div>
    </div>
  );
}

export default Login;
