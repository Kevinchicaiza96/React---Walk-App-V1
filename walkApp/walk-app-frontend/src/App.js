import { Routes, Route } from "react-router-dom";
import PrivateRoute from "./components/PrivateRoute";
import Home from "./pages/Home";
import Comunidad from "./pages/Comunidad";
import Juegos from "./pages/Juegos";
import Rutas from "./pages/Rutas";
import Ranking from "./pages/Ranking";
import Login from "./pages/Login";
import Registro from "./pages/Registro";
import Perfil from "./pages/Perfil";
import DetalleRuta from "./pages/DetalleRuta";
import RecorridoActivo from "./pages/RecorridoActivo";
import NotFound from "./pages/NotFound";
import AdminPanel from "./pages/AdminPanel";
import SOSButton from "./components/SOSButton";
import ActivarCuenta from "./pages/ActivarCuenta";
import PoliticaPrivacidad from "./pages/PoliticaPrivacidad";
import TerminosCondiciones from "./pages/TerminosCondiciones";
import Contacto from "./pages/Contacto";
import RecuperarContrasena from "./pages/RecuperarContrasena";

function App() {
  const isAuthenticated = !!localStorage.getItem("access_token");

  return (
    <>
      {isAuthenticated && <SOSButton />}
      <Routes>
        {/* Públicas */}
        <Route path="/"                      element={<Home />} />
        <Route path="/login"                 element={<Login />} />
        <Route path="/registro"              element={<Registro />} />
        <Route path="/activar/:uidb64/:token" element={<ActivarCuenta />} />
        <Route path="/recuperar-contrasena"  element={<RecuperarContrasena />} />
        <Route path="/privacidad"            element={<PoliticaPrivacidad />} />
        <Route path="/terminos"              element={<TerminosCondiciones />} />
        <Route path="/contacto"              element={<Contacto />} />

        {/* Privadas — requieren login */}
        <Route path="/perfil"                element={<PrivateRoute><Perfil /></PrivateRoute>} />
        <Route path="/comunidad"             element={<PrivateRoute><Comunidad /></PrivateRoute>} />
        <Route path="/rutas"                 element={<PrivateRoute><Rutas /></PrivateRoute>} />
        <Route path="/rutas/:id"             element={<PrivateRoute><DetalleRuta /></PrivateRoute>} />
        <Route path="/rutas/:id/recorrido"   element={<PrivateRoute><RecorridoActivo /></PrivateRoute>} />
        <Route path="/ranking"              element={<PrivateRoute><Ranking /></PrivateRoute>} />
        <Route path="/juegos"               element={<PrivateRoute><Juegos /></PrivateRoute>} />

        {/* Solo admin */}
        <Route path="/dashboard"            element={<PrivateRoute adminOnly><AdminPanel /></PrivateRoute>} />

        <Route path="*" element={<NotFound />} />
      </Routes>
    </>
  );
}

export default App;