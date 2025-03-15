import { useState, useEffect } from "react";

export default function Home() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    // fetch(localhost:5000/api/message)  // Works under Flask dev server
    fetch("https://draftempire.win/api/message")
      .then((response) => response.json())
      .then((data) => setMessage(data.message))
      .catch((error) => console.error("Error fetching message:", error));
  }, []);



  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h1>🏚️ Welcome to Draft Empire!</h1>      
      <h3>Follow our progress by clicking the button below!</h3>

      <p><strong>Backend says:</strong> {message}</p>  {/* Displays data from Flask */}

      <div className="card">
        <button onClick={() => window.open("https://www.github.com/chad-111/", "_blank")}>
          Hi, I am below
        </button>
      </div>
    </div>
  );
}
