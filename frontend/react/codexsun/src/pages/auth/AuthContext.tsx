// AuthContext.tsx
import { createContext, useContext, useEffect, useState } from "react";
import { useAppContext } from "../GlobalContext/AppContaxt.tsx";

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

  useEffect(() => {
  const savedToken = localStorage.getItem("token");
  const savedUser = localStorage.getItem("user");

  const verifyToken = async () => {
    if (savedToken && savedUser) {
      try {
        const res = await fetch(`${API_URL}/api/protected`, {
          headers: {
            Authorization: `Bearer ${savedToken}`,
          },
        });

        if (res.ok) {
          setToken(savedToken);
          setUser(JSON.parse(savedUser));
        } else if (res.status === 401 || res.status === 403) {
          // Only remove token if it's clearly unauthorized
          console.warn("Token unauthorized, logging out.");
          localStorage.removeItem("token");
          localStorage.removeItem("user");
        } else {
          console.warn("Unexpected response status:", res.status);
          // Don't remove token, assume temporary issue
        }
      } catch (err) {
        console.error("Network error during token verification:", err);
        // Don't remove token. Assume user still logged in.
      }
    }

    setIsInitialized(true);
  };

  verifyToken();
}, []);


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
    <AuthContext.Provider value={{ user, token, login, logout, isInitialized }}>
      {!isInitialized ? (
        <div className="flex items-center justify-center min-h-screen">
          <span className="text-lg font-medium">Loading...</span>
        </div>
      ) : (
        children
      )}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
