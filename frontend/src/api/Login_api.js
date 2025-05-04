export const loginUser = async (formData) => {
  try {
    const response = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
      credentials: "include",
    });

    const data = await response.json();

    if (response.ok) {
      return { success: true, message: data.message };
    } else {
      return { success: false, message: data.message || "Login failed." };
    }
  } catch (err) {
    return {
      success: false,
      message: "A network error occurred. Please try again.",
    };
  }
};
