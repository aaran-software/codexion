export async function logoutUser(API_URL: string) {
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
      // ✅ Wait for server to complete before redirecting
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
}
