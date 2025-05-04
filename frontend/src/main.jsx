import React from "react";
import { StrictMode } from "react";
import ReactDOM from "react-dom/client";
import {
  createBrowserRouter,
  createRoutesFromElements,
  Route,
  RouterProvider,
} from "react-router";
import "./global.css";

// Main app
import App from "./App.jsx";

// Main screens
import LoginScreen from "./screens/LoginScreen.jsx";
import RegisterScreen from "./screens/RegisterScreen.jsx";

// Success screens
import RegisterSuccessScreen from "./screens/RegisterSuccessScreen.jsx";

// Verify Screens
import VerifyEmail from "./screens/VerifyEmailScreen.jsx";
import TwoFaScreen from "./screens/TwoFaScreen.jsx";

// Protected routes
import ProtectedRoute from "./routes/ProtectedRoute.jsx";
import LoginVerificationRoute from "./routes/LoginVerificationRoute.jsx";

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route path="/" element={<App />}>
      <Route index element={<LoginScreen />} />
      <Route
        path="verify-2fa"
        element={
          <LoginVerificationRoute>
            <TwoFaScreen />
          </LoginVerificationRoute>
        }
      />
      <Route path="/Register" element={<RegisterScreen />} />
      <Route
        path="/verify-email"
        element={
          <ProtectedRoute>
            <VerifyEmail />
          </ProtectedRoute>
        }
      />
      <Route
        path="/Register-success"
        element={
          <ProtectedRoute>
            <RegisterSuccessScreen />
          </ProtectedRoute>
        }
      />
    </Route>
  )
);

ReactDOM.createRoot(document.getElementById("root")).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>
);
