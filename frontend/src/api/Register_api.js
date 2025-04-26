export const registerUser = async (formData) => {
  try {
    const response = await fetch("/api/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    });

    if (response.ok) {
      showToast(setToast, "User Registerd!", "success");
    } else {
      showToast(setToast, "Register failed. Please try again.", "error");
    }
  } catch (err) {
    return {
      // Still need to work on this but this will be a thing later one
      success: false,
      message: "A network error occurred. Please try again.",
    };
  }
};
