import { showToast } from "../utils/toastHelper";
import { handleValidateInput } from "./sanitizerHelper";

export const handleRegisterSubmit = async ({
  e,
  formData,
  setFormData,
  setInputStatus,
  setToast,
  registerUser,
  setAttempts,
  attempts,
}) => {
  e.preventDefault();

  const isLocked = attempts >= 3;

  if (isLocked) {
    showToast(setToast, "Too many attempts. Please wait.", "error");
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

  const result = await registerUser(formData);

  resetForm(setFormData, setInputStatus);

  if (result.success) {
    showToast(
      setToast,
      "Registration successful! Please verify your email.",
      "success"
    );
  } else {
    showToast(setToast, result.message || "Registration failed.", "error");
    setAttempts((prev) => {
      const updated = prev + 1;
      if (updated >= 3) {
        setTimeout(() => {
          setAttempts(0);
          showToast(setToast, "You can try registering again.", "success");
        }, 30000);
      }
      return updated;
    });
  }
};

const resetForm = (setFormData, setInputStatus) => {
  setFormData({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  setInputStatus({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
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
