import { showToast } from "../utils/toastHelper";

export const handleTwoFaSubmit = async ({ e, code, setToast, navigate }) => {
  e.preventDefault();

  if (!/^\d{6}$/.test(code)) {
    showToast(setToast, "Enter a valid 6-digit code.", "error");
    return;
  }

  try {
    const res = await fetch("/api/verify-login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ code }),
    });

    const data = await res.json();
    showToast(setToast, data.message, data.success ? "success" : "error");

    if (data.success) {
      setTimeout(() => navigate("/Dashboard"), 1500);
    }
  } catch {
    showToast(setToast, "Network error. Try again.", "error");
  }
};
