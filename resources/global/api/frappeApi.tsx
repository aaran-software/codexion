// Login to Frappe (session-based)
import apiClient from "./apiClients";

export const loginFrappe = async (usr: string, pwd: string) => {
  const user=await apiClient.post("/api/method/login", { usr, pwd });
  console.log(user)
};

// Logout user
export const logoutFrappe = async () => {
  try {
    await apiClient.post("/api/method/logout");
    console.log("Frappe logout successful from frappeApi");
  } catch (error) {
    console.error("Error during Frappe logout:", error);
    throw error;
  }
};

// Get currently logged-in user
export const getLoggedInUser = async (): Promise<string | null> => {
  const response = await apiClient.get(
    "/api/method/frappe.auth.get_logged_user"
  );
  const user = response.data.message;
  return user === "Guest" ? null : user;
};
