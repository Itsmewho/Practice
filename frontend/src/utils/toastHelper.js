export const showToast = (setToast, message, type) => {
  setToast(null);
  setTimeout(() => {
    setToast({ message, type });
  }, 100);
};
