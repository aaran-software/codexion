// src/components/LoginForm.tsx
import {useState} from "react";
import {useNavigate} from "react-router-dom";
import FloatingInput from "../Input/FloatingInput";
import PasswordInput from "../SecondaryInput/PasswordInput";
import Button from "../Input/Button";
// import {useAuth} from "@/pages/auth/AuthContext";
import {Card, CardContent, CardHeader, CardTitle} from "../Chart/card";
import {useAppContext} from "../../pages/GlobalContext/AppContaxt.tsx";
import { useAuth } from "../../pages/app/auth/AuthContext.tsx";

export function LoginForm({className}: { className?: string }) {
    const [usr, setUsr] = useState("");
    const [pwd, setPwd] = useState("");
    const [error, setError] = useState("");
    const [usrError, setUsrError] = useState("");
    const [pwdError, setPwdError] = useState("");
    const navigate = useNavigate();
    const {login} = useAuth();
    const {API_URL} = useAppContext();

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");
        setUsrError("");
        setPwdError("");

        if (!usr && !pwd) {
            setUsrError("Username Required");
            setPwdError("Password Required");
            return;
        } else if (!usr) {
            setUsrError("Username Required");
            return;
        } else if (!pwd) {
            setPwdError("Password Required");
            return;
        }

        try {
            // const form = new URLSearchParams();
            // form.append("username", usr);
            // form.append("password", pwd);
            // form.append("grant_type", "password");
            //
            // const response = await fetch(`${API_URL}/api/login`, {
            //     method: "POST",
            //     headers: {
            //         "Content-Type": "application/x-www-form-urlencoded",
            //     },
            //     body: form.toString(),
            //     credentials: "include",
            // });
            const response = await fetch(`${API_URL}/api/login`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({username: usr, password: pwd}),
                credentials: "include",
            });


            if (!response.ok) {
                throw new Error("Login failed");
            }

            const data = await response.json();

            // If FastAPI returns `access_token` and `token_type`, use this
            const token = data.access_token;
            const user = {username: usr}; // Adjust this if your API returns user info

            login(user, token); // From your AuthContext
            navigate("/dashboard");
        } catch (err) {
            console.error("Login failed:", err);
            setError("Invalid credentials or server error.");
        }
    };

    return (
        <div className={`flex flex-col gap-6 ${className}`}>
            <Card>
                <CardHeader>
                    <CardTitle className="text-center py-2 text-xl font-bold text-update">
                        Welcome
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <form onSubmit={handleLogin}>
                        <div className="flex flex-col gap-6">
                            <FloatingInput
                                id="usr"
                                type="text"
                                placeholder="demo@gmail.com"
                                required
                                value={usr}
                                onChange={(e) => setUsr(e.target.value)}
                                label="User"
                                err={usrError}
                            />

                            <PasswordInput
                                id="pwd"
                                value={pwd}
                                error={pwdError}
                                label="Password"
                                onChange={(e) => setPwd(e.target.value)}
                            />

                            {error && (
                                <p className="text-red-500 text-sm text-center">{error}</p>
                            )}

                            <Button
                                type="submit"
                                className="w-full bg-update text-update-foreground"
                                label={"Login"}
                            />

                            <div className="text-center text-sm">
                                Don&apos;t have an account?{" "}
                                <a
                                    href="/signup"
                                    className="underline text-update underline-offset-4"
                                >
                                    Sign up
                                </a>
                            </div>
                        </div>
                    </form>
                </CardContent>
            </Card>
        </div>
    );
}
