import { showToast } from "../utils/toastHelper";
import { emailRegex } from "./validators";

// Sanitize it!
export const sanitizeEmailInput = (value, setToast) => {
  if (/[<>"'`;\/\\]/g.test(value)) {
    if (setToast) {
      showToast(setToast, "Invalid characters detected in email.", "error");
    }
    return { sanitized: value.replace(/[<>"'`;\/\\]/g, ""), hasError: true };
  }
  return { sanitized: value, hasError: false };
};

export const sanitizePasswordInput = (value, setToast) => {
  if (/[<>"'`;]/g.test(value)) {
    if (setToast) {
      showToast(setToast, "Invalid characters detected in password.", "error");
    }
    return { sanitized: value.replace(/[<>"'`;]/g, ""), hasError: true };
  }
  return { sanitized: value, hasError: false };
};

export const sanitizeNameInput = (value, setToast) => {
  if (/[<>"'`;]/g.test(value)) {
    if (setToast) {
      showToast(setToast, "Invalid characters detected in name.", "error");
    }
    return { sanitized: value.replace(/[<>"'`;]/g, ""), hasError: true };
  }
  return { sanitized: value, hasError: false };
};

// Validate the shit out of it
export const handleValidateInput = ({
  name,
  value,
  formData,
  setToast,
  mode = "soft",
}) => {
  let error = null;

  if (name === "email") {
    if (mode === "hard" && !emailRegex.test(value)) {
      error = "Invalid email format.";
    }
  } else if (name === "password") {
    if (mode === "hard" && value.length < 6) {
      error = "Password must be at least 6 characters.";
    }
  } else if (name === "confirmPassword") {
    if (mode === "hard" && value !== formData.password) {
      error = "Passwords do not match.";
    }
  }

  if (error && setToast) {
    showToast(setToast, error, "error");
  }

  return error;
};

// Handle Input
export const handleInput = ({
  e,
  formData,
  setFormData,
  setInputStatus,
  setToast,
}) => {
  const { name, value } = e.target;

  const sanitizerMap = {
    name: sanitizeNameInput,
    email: sanitizeEmailInput,
    password: sanitizePasswordInput,
    confirmPassword: sanitizePasswordInput,
  };

  const sanitizeFn = sanitizerMap[name];
  const result = sanitizeFn
    ? sanitizeFn(value, setToast)
    : { sanitized: value, hasError: false };

  const { sanitized, hasError } = result;

  setFormData((prev) => ({
    ...prev,
    [name]: sanitized,
  }));

  if (hasError) {
    setInputStatus((prev) => ({
      ...prev,
      [name]: "error",
    }));
    return;
  }

  const error = handleValidateInput({
    name,
    value: sanitized,
    formData,
    setToast,
    mode: "soft",
  });

  if (error) {
    setInputStatus((prev) => ({
      ...prev,
      [name]: "error",
    }));
  } else {
    setInputStatus((prev) => ({
      ...prev,
      [name]: "success",
    }));
  }
};
