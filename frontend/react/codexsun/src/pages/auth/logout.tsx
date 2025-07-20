// logout.ts
export async function logoutUser() {
  const token = localStorage.getItem("token");

  if (!token) return;

  try {
    const response = await fetch("http://127.0.0.1:8000/api/logout", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json"
      },
    });

    if (response.ok) {
      localStorage.removeItem("token");
      window.location.href = "/"; // or use navigate() if using react-router
    } else {
      console.error("Logout failed");
    }
  } catch (err) {
    console.error("Logout error:", err);
  }
}
