export const sanitizeInput = (value) => {
  return value.replace(/[<>]/g, "");
};
