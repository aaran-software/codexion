// AuthContext.tsx
import { createContext, useContext, useEffect, useState } from "react";
import { useAppContext } from "../../GlobalContext/AppContaxt.tsx";

type User = {
  username: string;
};

type AuthContextType = {
  user: User | null;
  token: string | null;
  isInitialized: boolean;
  login: (user: User, token: string) => void;
  logout: () => void;
};

const AuthContext = createContext<AuthContextType>({
  user: null,
  token: null,
  isInitialized: false,
  login: () => {},
  logout: () => {},
});

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isInitialized, setIsInitialized] = useState(false);
  const { API_URL } = useAppContext();

  console.log("hi")
  console.log("API_URL:", API_URL);

 useEffect(() => {
  const savedToken = localStorage.getItem("token");
  const savedUser = localStorage.getItem("user");

  const verifyToken = async () => {
    console.log("Verifying token...");

    if (savedToken && savedUser) {
      try {
        const res = await fetch(`${API_URL}/api/protected`, {
          headers: {
            Authorization: `Bearer ${savedToken}`,
          },
        });

        console.log("Token verification response:", res.status);

        if (res.ok) {
          setToken(savedToken);
          setUser(JSON.parse(savedUser));
        } else if (res.status === 401 || res.status === 403) {
          console.warn("Token unauthorized, clearing...");
          localStorage.removeItem("token");
          localStorage.removeItem("user");
        } else {
          console.warn("Unexpected response during token check:", res.status);
        }
      } catch (err) {
        console.error("Network error during token check:", err);
      }
    } else {
      console.log("No saved token or user found.");
    }

    setIsInitialized(true); // Ensure this runs in all cases
  };

  verifyToken();
}, [API_URL]);
 // rerun when API_URL is ready

  const login = (user: User, token: string) => {
    setUser(user);
    setToken(token);
    localStorage.setItem("user", JSON.stringify(user));
    localStorage.setItem("token", token);
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem("user");
    localStorage.removeItem("token");
  };

  return (
    <AuthContext.Provider value={{ user, token, isInitialized, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
