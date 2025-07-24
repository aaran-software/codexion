// AuthProvider.tsx
import { createContext, useContext, useEffect, useState } from "react";
import {
  getLoggedInUser,
  loginFrappe,
  logoutFrappe,
} from "../../../resources/global/api/frappeApi";

interface AuthContextType {
  user: string | null;
  login: (usr: string, pwd: string) => Promise<void>;
  logout: () => Promise<void>;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  login: async () => {},
  logout: async () => {},
  loading: true,
});

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Initial check for logged-in user
    getLoggedInUser()
      .then((username) => setUser(username))
      .catch(() => setUser(null))
      .finally(() => setLoading(false));
  }, []);

  const login = async (usr: string, pwd: string) => {
    setUser(null);
    await loginFrappe(usr, pwd);
    const currentUser = await getLoggedInUser();
    setUser(currentUser);
  };

  const logout = async () => {
    await logoutFrappe();
    // Set the user state to null after successful logout
    setUser(null); // <--- Add this line
    console.log("logout completed, user state cleared"); // Added for clarity
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
