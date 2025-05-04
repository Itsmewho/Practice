import { handleValidateInput } from "./sanitizerHelper";
import { showToast } from "../utils/toastHelper";

export const handleLoginSubmit = async ({
  e,
  formData,
  setFormData,
  setInputStatus,
  setToast,
  loginUser, // backend function to login user
  setAttempts,
  attempts,
  navigate,
}) => {
  e.preventDefault();

  const isLocked = attempts >= 3;

  if (isLocked) {
    showToast(setToast, "Too many login attempts. Please wait.", "error");
    return;
  }

  const isValid = validateBeforeSubmit({
    formData,
    setInputStatus,
    setToast,
  });

  if (!isValid) {
    return;
  }

  const result = await loginUser(formData);

  showToast(setToast, result.message, result.success ? "success" : "error");

  resetForm(setFormData, setInputStatus);

  if (result.success) {
    setTimeout(() => navigate("/verify-2fa"), 1500);
  } else {
    setAttempts((prev) => {
      const updated = prev + 1;
      if (updated >= 3) {
        setTimeout(() => {
          setAttempts(0);
          showToast(setToast, "Login unlocked. Please try again.", "success");
        }, 30000);
      }
      return updated;
    });
  }
};

const resetForm = (setFormData, setInputStatus) => {
  setFormData({
    email: "",
    password: "",
  });

  setInputStatus({
    email: "",
    password: "",
  });
};

const validateBeforeSubmit = ({ formData, setInputStatus, setToast }) => {
  let isValid = true;

  for (const fieldName in formData) {
    const error = handleValidateInput({
      name: fieldName,
      value: formData[fieldName],
      formData,
      setToast,
      mode: "hard",
    });

    if (error) {
      isValid = false;
      setInputStatus((prev) => ({
        ...prev,
        [fieldName]: "error",
      }));
    } else {
      setInputStatus((prev) => ({
        ...prev,
        [fieldName]: "success",
      }));
    }
  }

  return isValid;
};
