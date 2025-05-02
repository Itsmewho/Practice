import { showToast } from "../utils/toastHelper";

export const loginUser = async (formData, setToast) => {
  try {
    const response = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    });

    if (response.ok) {
      showToast(setToast, "Welcome Back!", "success");
    } else {
      showToast(setToast, "Login failed. Please try again.", "error");
    }
  } catch (err) {
    return {
      success: false,
      message: "A network error occurred. Please try again.",
    };
  }
};
