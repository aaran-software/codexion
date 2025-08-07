import { createContext, useContext, useEffect, useState } from "react";
import {
  getLoggedInUser,
  loginFrappe,
  logoutFrappe,
} from "../../../resources/global/api/frappeApi";
import { useAppContext } from "../AppContaxt";

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
  const [loading, setLoading] = useState(true); // loading is true initially
  const { API_URL } = useAppContext();

  useEffect(() => {
    if (!API_URL) return; // wait for AppContext to be ready

    const checkUser = async () => {
      try {
        const username = await getLoggedInUser();
        setUser(username);
      } catch (error) {
        console.warn("No user logged in or session expired");
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    checkUser();
  }, [user]);

  const login = async (usr: string, pwd: string) => {
    await loginFrappe(usr, pwd);
    const currentUser = await getLoggedInUser();
    setUser(currentUser);
  };

  const logout = async () => {
    await logoutFrappe();
    setUser(null);
    console.log("logout completed, user state cleared");
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useFrappeAuth() {
  return useContext(AuthContext);
}
