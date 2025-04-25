export const loginUser = async (formData) => {
  try {
    const response = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    });

    if (response.ok) {
      return { success: true, message: "Welcome back!" };
    } else {
      return { success: false, message: "Login failed. Please try again." };
    }
  } catch (err) {
    return {
      success: false,
      message: "A network error occurred. Please try again.",
    };
  }
};
