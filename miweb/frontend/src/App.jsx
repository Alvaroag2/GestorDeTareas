import { useState } from 'react';
import TareasPage from './pages/tareasPage';
import UsuariosPage from './pages/usuariosPage'
import CategoriasPage from './pages/categoriasPage'
import TareaDetallePage from './pages/tareaDetallePage';
import LoginPage from './pages/loginPage'
import { AuthContext } from './context/AuthContext';
import { useContext } from 'react';

function App() {
const [tareaIdSeleccionada, setTareaIdSeleccionada] = useState(null);
const [paginaActual, setPaginaActual] = useState('tareas');
const { usuario, logout } = useContext(AuthContext);

const verDetalleTarea = (id) => {
    setTareaIdSeleccionada(id);
    setPaginaActual('tarea-detalle');
  };

return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>
      
      <nav style={{ marginBottom: '20px', display: 'flex', gap: '10px', alignItems: 'center' }}>
    <button onClick={() => setPaginaActual('tareas')}>Tareas</button>
    <button onClick={() => setPaginaActual('usuarios')}>Usuarios</button>
    <button onClick={() => setPaginaActual('categorias')}>Categorias</button>
    
    
    {!usuario && (
      <button onClick={() => setPaginaActual('login')}>Login</button>
    )}

    {usuario ? (
      <div>
        <span>
          Sesión activa como: <strong>{usuario.nombre}</strong> (Rol: {usuario.rol})
        </span>
        <button onClick={logout} style={{ marginLeft: '10px' }}>
          Cerrar Sesión
        </button>
      </div>
    ) : (
      <span>No has iniciado sesión</span>
    )}
  </nav>

      {/* Renderizado condicional de las páginas */}
      {paginaActual === 'tareas' && <TareasPage onVerDetalle={verDetalleTarea} />}
      {paginaActual === 'tarea-detalle' && (
        <TareaDetallePage 
          tareaId={tareaIdSeleccionada} 
          onVolver={() => setPaginaActual('tareas')} 
        />
      )}
      {paginaActual === 'usuarios' && <UsuariosPage/>}
      {paginaActual === 'categorias' && <CategoriasPage/>}
      {paginaActual === 'login' && <LoginPage/>}
    </div>
  );




}

export default App;