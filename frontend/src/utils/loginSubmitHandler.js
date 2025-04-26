export const handleLoginSubmit = async ({
  e,
  formData,
  setInputStatus,
  setToast,
  emailRef,
  passwordRef,
  loginUser,
  setAttempts,
  attempts,
  navigate,
}) => {
  e.preventDefault();

  const isLocked = attempts >= 3;

  const showToast = (message, type) => {
    setToast(null);
    setTimeout(() => {
      setToast({ message, type });
    }, 100);
  };

  if (isLocked) {
    showToast("Too many login attempts. Please wait.", "error");
    return;
  }

  if (!formData.email) {
    showToast("Email is required.", "error");
    setInputStatus({ email: "error", password: "" });
    emailRef.current?.focus();
    return;
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(formData.email)) {
    showToast("Invalid email format.", "error");
    setInputStatus({ email: "error", password: "" });
    emailRef.current?.focus();
    return;
  }

  if (!formData.password) {
    showToast("Password is required.", "error");
    setInputStatus({ email: "success", password: "error" });
    passwordRef.current?.focus();
    return;
  }

  if (formData.password.length < 6) {
    showToast("Password must be at least 6 characters.", "error");
    setInputStatus({ email: "success", password: "error" });
    passwordRef.current?.focus();
    return;
  }

  setInputStatus({ email: "success", password: "success" });

  const result = await loginUser(formData);

  showToast(result.message, result.success ? "success" : "error");

  if (result.success) {
    setTimeout(() => navigate("/2Fa"), 1500);
  } else {
    setAttempts((prev) => {
      const updated = prev + 1;
      if (updated >= 3) {
        setTimeout(() => {
          setAttempts(0);
          showToast("Login unlocked. Please try again.", "success");
        }, 30000);
      }
      return updated;
    });
  }
};
