import { useState } from 'react'
import './App.css'
import { useEffect } from 'react';

function Signup() {
    const API_BASE_URL = "https://draftempire.win/api";
    const [data, setData] = useState({
        username: "",
        password: "",
        email: ""
    })

    const handleSubmit = async (event) => {
        event.preventDefault();
        const formData = new FormData(event.target);
        const formValues = Object.fromEntries(formData.entries());
        console.log(formValues)
        try {
            const response = await fetch('${API_BASE_URL}/signup', {
                method: "POST",
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: formValues.username,
                    password: formValues.password,
                    email: formValues.email
                })
            });
    
            const data = await response.json();
    
            if (response.ok) {
                alert("Registration successful!");
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
        <p>Sign up here:</p>
        <form onSubmit={handleSubmit}>
          <label>Enter username:
            <input 
              type="text"
              name="username"
            />
          </label>
          <p></p>
          <label>Enter password:
            <input
              type="password"
              name="password"
            />
          </label>
          <p></p>
          <label>Enter email address:
            <input
              type="email"
              name="email"
            />
          </label>
          <p></p>
          <input type="submit" />
        </form>
        </>
      )
}

export default Signup