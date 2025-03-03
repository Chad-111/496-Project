import { useState } from 'react'
import './App.css'
import { useEffect } from 'react';

function Login() {
    const handleSubmit = async (event) => {
        event.preventDefault();
        const formData = new FormData(event.target);
        const formValues = Object.fromEntries(formData.entries());
        console.log(formValues)
        try {
            const response = await fetch("http://127.0.0.1:5000/api/login", {
                method: "POST",
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    password: formValues.password,
                    email: formValues.email
                })
            });
    
            const data = await response.json();
    
            if (response.ok) {
                alert("Login successful!");
            } else {
                alert(`Error: ${data.error}`);
            }
        } catch (error) {
            console.error("Network error:", error);
            alert("A network error occurred. Please try again.");
        }
    }

    return (
        <>
        <p>Login here:</p>
        <form onSubmit={handleSubmit}>
        <label>Enter email address:
            <input
              type="email"
              name="email"
            />
          </label>
          <p></p>
          <label>Enter password:
            <input
              type="password"
              name="password"
            />
          </label>
          <input type="submit" />
        </form>
        </>
      )
}

export default Login;