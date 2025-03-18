import { useState } from "react";

const Contact = () => {
    const [email, setEmail] = useState("");
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [message, setMessage] = useState("");
    const [isLogin, setIsLogin] = useState(true);

    const handleSubmit = async (e) => {
        e.preventDefault();
        const endpoint = isLogin ? "/api/login" : "/api/signup";
        const body = isLogin ? { email, password } : { email, username, password };

        try {
            const response = await fetch(`http://localhost:5000${endpoint}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(body),
            });

            const result = await response.json();
            setMessage(result.message || result.error);
        } catch (error) {
            setMessage("Error: Unable to reach server");
        }
    };

    return (
        <div>
            <h2>{isLogin ? "Login" : "Sign Up"}</h2>
            <form onSubmit={handleSubmit}>
                {!isLogin && (
                    <input
                        type="text"
                        placeholder="Username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                )}
                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
                <button type="submit">{isLogin ? "Login" : "Sign Up"}</button>
            </form>
            <button onClick={() => setIsLogin(!isLogin)}>
                {isLogin ? "Switch to Sign Up" : "Switch to Login"}
            </button>
            <p>{message}</p>
        </div>
    );
};

export default Contact;
