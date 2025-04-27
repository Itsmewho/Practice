export const registerUser = async (formData) => {
  try {
    const response = await fetch("/api/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    });
    if (response.ok) {
      return;
    }
  } catch (err) {
    return {
      success: false,
      message: "A network error occurred. Please try again.",
    };
  }
};
