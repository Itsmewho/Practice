export const checkTokenValid = async (token) => {
  try {
    const res = await fetch(`/api/check-token-valid?token=${token}`);
    const data = await res.json();
    return data.valid;
  } catch {
    return false;
  }
};
