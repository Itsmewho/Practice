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
import VerifyEmail from "./screens/VerifyEmailScreen.jsx";
import RegisterSuccessScreen from "./screens/RegisterSuccessScreen.jsx";

// Protected routes
import ProtectedRoute from "./routes/ProtectedRoute.jsx";

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route path="/" element={<App />}>
      <Route index element={<LoginScreen />} />
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
