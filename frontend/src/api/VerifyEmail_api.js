export const verifyEmailToken = async (token) => {
  try {
    const response = await fetch(`/api/verify-email?token=${token}`);
    const data = await response.json();

    return {
      ...data,
      redirectImmediately: response.status === 400,
    };
  } catch (err) {
    return {
      success: false,
      message: "Network error while verifying email.",
      redirectImmediately: true,
    };
  }
};
