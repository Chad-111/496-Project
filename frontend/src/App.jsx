// This is the template file from Vite. We can change this at will.
import { useState } from 'react'
import './App.css'
import { useEffect } from 'react';

function App() {
  const [data, setdata] = useState({
    name: ""
  });
  const [count, setCount] = useState(0);


  useEffect(() => {
    // Using fetch to fetch the api from 
    // flask server it will be redirected to proxy
    fetch("/api").then((res) => console.log(res));
    fetch("/api").then((res) =>
        res.json().then((data) => {
            // Setting a data from api
            setdata({
                name: data.Name
            });
        })
    );
  }, []);

  return (
    <>
      <p></p>
      <h1>Hello World!</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
      </div>
      <p>{data.name}</p>
    </>
  )
}

export default App
