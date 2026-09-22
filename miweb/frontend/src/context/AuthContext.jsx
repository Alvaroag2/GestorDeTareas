import { createContext, useState} from 'react';
import api from '../api';
// 1. Creación del contexto
// eslint-disable-next-line react-refresh/only-export-components
export const AuthContext = createContext();

export function AuthProvider({ children }) {
  // Inicializamos el estado intentando leer la sesión guardada previamente
  const [usuario, setUsuario] = useState(() => {
    const usuarioGuardado = localStorage.getItem('usuario');
    return usuarioGuardado ? JSON.parse(usuarioGuardado) : null;
  });

  // Función para guardar los datos al hacer login exitoso
  const login = (datosUsuario) => {
    setUsuario(datosUsuario);
    localStorage.setItem('usuario', JSON.stringify(datosUsuario));
  };

 


  const logout = async () => {
    try {
      // 1. Llama a tu vista api_logout en Django
      await api.post('/logout/');
    } catch (error) {
      console.error('Error al cerrar sesión en el servidor:', error);
    } finally {
      // 2. Independientemente de la respuesta, limpiamos React y localStorage
      setUsuario(null);
      localStorage.removeItem('usuario');
    }
  };

  return (
    <AuthContext.Provider value={{ usuario, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}