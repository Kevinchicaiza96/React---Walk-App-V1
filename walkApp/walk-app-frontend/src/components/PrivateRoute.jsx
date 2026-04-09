import { Navigate, useLocation } from "react-router-dom";

export default function PrivateRoute({ children, adminOnly = false }) {
  const token = localStorage.getItem("access_token");
  const location = useLocation();

  if (!token) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  if (adminOnly) {
    try {
      const user = JSON.parse(localStorage.getItem("user") || "{}");
      if (!user.is_staff && user.rol !== "admin") {
        return <Navigate to="/" replace />;
      }
    } catch {
      return <Navigate to="/login" replace />;
    }
  }

  return children;
}