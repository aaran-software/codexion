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
      console.log("Logout successful");
      window.location.href = "/"; // ✅ AFTER everything finishes
    } else {
      console.error("Logout failed");
    }
  } catch (err) {
    console.error("Logout error:", err);
  }
}
