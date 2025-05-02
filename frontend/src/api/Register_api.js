export const registerUser = async (formData) => {
  try {
    const response = await fetch("/api/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    });

    const result = await response.json();

    return {
      success: response.ok,
      message: result.message,
    };
  } catch (err) {
    return {
      success: false,
      message: "A network error occurred. Please try again.",
    };
  }
};
