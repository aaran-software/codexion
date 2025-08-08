import { logoutFrappe } from "../../../resources/global/api/frappeApi";
// import { useFrappeAuth } from "../auth/frappeAuthContext";
// logoutUser.ts
export async function logoutUser(API_URL: string, API_METHOD: string, setUser: (user: any) => void) {
  if (API_METHOD === "FAST_API") {
    console.log("fastapi logout")

    const token = localStorage.getItem("token");
    if (!token) return;

    try {
      const response = await fetch(`${API_URL}/api/logout`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });

      if (response.ok) {
        await response.json();

        localStorage.removeItem("token");
        localStorage.removeItem("user");
        localStorage.removeItem("editor-draft");
        window.location.href = "/";
      } else {
        console.error("Logout failed");
      }
    } catch (err) {
      console.error("Logout error:", err);
    }
  } else if (API_METHOD === "FRAPPE") {
    console.log("frappe logout from logout")
    await logoutFrappe();
    setUser(null);
    console.log("logout completed, user state cleared");
  }
}

