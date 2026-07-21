import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

function Login() {
    
    const navigate = useNavigate();

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const login = async () => {

        try {

            const response = await api.post("/login", {
                email,
                password
            });

            alert(response.data.message);

            localStorage.setItem(
                "user",
                JSON.stringify(response.data)
            );
            console.log("LOGIN RESPONSE =", response.data);

console.log("LOCAL STORAGE =", localStorage.getItem("user"));
            navigate("/chat");
        } catch (error) {

            alert(
                error.response?.data?.detail ||
                "Login Failed"
            );

        }

    };

    return (

        <div
            style={{
                width: "350px",
                margin: "100px auto"
            }}
        >

            <h2>EduAssist AI Login</h2>

            <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) =>
                    setEmail(e.target.value)
                }
            />

            <br /><br />

            <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) =>
                    setPassword(e.target.value)
                }
            />

            <br /><br />

            <button onClick={login}>
                Login
            </button>

        </div>

    );

}

export default Login;