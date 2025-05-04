export const sanitizeTwoFaCode = (value, setToast = null) => {
  const sanitized = value.replace(/\D/g, "");
  if (sanitized.length > 6) {
    if (setToast) {
      setToast({
        message: "2FA code must be 6 digits.",
        type: "error",
      });
    }
    return sanitized.slice(0, 6);
  }
  return sanitized;
};
