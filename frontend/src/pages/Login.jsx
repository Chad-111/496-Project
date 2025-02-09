import { useState } from "react";
import axios from "axios";
const API_URL = import.meta.env.VITE_API_URL;  // ✅ Read from environment

function Login() {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

const handleSubmit = async (e) => {
  e.preventDefault();
  try {
    const response = await axios.post(`${API_URL}/auth/login`, formData);
    alert(response.data.message);
  } catch (error) {
    alert(error.response?.data?.error || "Login failed");
  }
};

  return (
    <div className="flex flex-col items-center mt-20">
      <h2 className="text-2xl font-bold">Login</h2>
      <form onSubmit={handleSubmit} className="flex flex-col gap-3">
        <input type="email" name="email" placeholder="Email" onChange={handleChange} required />
        <input type="password" name="password" placeholder="Password" onChange={handleChange} required />
        <button type="submit" className="bg-blue-500 text-white px-4 py-2">Login</button>
      </form>
    </div>
  );
}

export default Login;
