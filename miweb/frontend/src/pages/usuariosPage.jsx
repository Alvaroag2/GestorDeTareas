import { useEffect, useState, useContext } from 'react';
import api from '../api';
import { AuthContext } from '../context/AuthContext';
import styles from './tareasPage.module.css';

function IconPlus() {
  return (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
      <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
    </svg>
  );
}

function IconEdit() {
  return (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
      <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
    </svg>
  );
}

function IconTrash() {
  return (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/>
      <path d="M10 11v6"/><path d="M14 11v6"/>
      <path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/>
    </svg>
  );
}

export default function UsuariosPage() {

const [usuarios, setUsuario] = useState([]);
const [error, setError] = useState(null);
const [mostrarFormulario, setMostrarFormulario] = useState(false);
const [formulario, setFormulario] = useState({
  nombre:'',
  email:'',
  password:'',
  rol:''

});
const [editandoId, setEditandoId] = useState(null);
const { usuario } = useContext(AuthContext);

const [filtros, setFiltros] = useState({
    rol: ''
  });


useEffect(() => {
    api.get('/usuarios/')
    .then((response) => setUsuario(response.data))
    .catch((err) => setError(err.message));
  }, []);


const manejarCambioFiltro = (e) => {
  const { name, value } = e.target;
  setFiltros({
    ...filtros,
    [name]: value
  });
};

const manejador = (e) => {

  const { name, value, type, checked } = e.target;
    
  setFormulario({
    ...formulario, //Sin esta línea, si editas la descripción, perderías el título, la prioridad y el resto de campos que ya habías rellenado.
    [name]: type === 'checkbox' ? checked : value //Operador ternario si es un checkbox guarda checked (true o false) si no es guarda valor osea el texto o numero de los inputs normales
  });
    
  
};

const rolActual = (usuario?.rol || usuario?.perfil?.rol || usuario?.perfil_rol || '').toUpperCase();
console.log("Rol Detectado:", rolActual);


const esComun = rolActual === 'COMUN';

const activarEdicion = (usuario) => {
  if(esComun){
    alert("No tienes permisos para editar usuarios.");
      return;
  }
    setEditandoId(usuario.id);
    setFormulario({
      nombre: usuario.nombre,
      email: usuario.email,
      password: '', // La dejamos vacía por seguridad
      rol: usuario.rol
    });
    setMostrarFormulario(true);
  };

  // Cancela la edición y limpia el formulario
  const cancelarEdicion = () => {
    setEditandoId(null);
    setFormulario({ nombre: '', email: '', password: '', rol: 'COMUN' });
    setMostrarFormulario(false);
  };

const aplicarFiltro = () => {
  // Construimos un objeto solo con los filtros que no estén vacíos
  const params = {};
  if (filtros.rol) params.rol = filtros.rol;

  api.get('/usuarios/', { params })
    .then((response) => setUsuario(response.data))
    .catch((err) => setError("Error al filtrar los usuarios: " + err.message));
};


const limpiarFiltros = () => {
  setFiltros({ rol: ''});
  api.get('/usuarios/')
    .then((response) => setUsuario(response.data))
    .catch((err) => setError(err.message));
};

const eliminarUsuario = async (id) => {
  if(esComun){
    alert("No tienes permisos para eliminar usuarios.");
      return;
  }
  // Confirmación previa antes de borrar
  const confirmar = window.confirm("¿Estas seguro de que deseas eliminar este usuario?");
  if (!confirmar) return;

  try {
    // 1. Petición DELETE a Django enviando la ID
    await api.delete(`/usuarios/${id}/`);

    // 2. Filtramos el estado local eliminando la tarea con esa ID
    setUsuario(usuarios.filter(usuario => usuario.id !== id));

    alert("Usuario eliminado con éxito");
    
    // Si la categoria que se borra estaba siendo editada, cancelamos la edición
    if (editandoId === id) {
      cancelarEdicion();
    }
  } catch (error) {
    console.error("Error al eliminar el usuario:", error.response?.data || error);
    alert("Error al intentar eliminar el usuario");
  }
};

  const botonForm = async (e) => {
  e.preventDefault();

  if (esComun) {
      alert("No tienes permisos para crear o modificar usuarios.");
      return;
    }
  // 1. Mapeamos los datos del formulario local
  const datosEnvio = {
    username: formulario.nombre.trim(),
    email: formulario.email.trim(),
    password: formulario.password,
    rol: formulario.rol || 'COMUN',
  };

  try {
      if (editandoId) {
        // --- MODO EDICIÓN (PUT) ---
        const response = await api.put(`/usuarios/${editandoId}/`, datosEnvio);
        
        // Reemplazamos el usuario actualizado en la lista local
        setUsuario(usuarios.map(u => u.id === editandoId ? response.data : u));
        alert("Usuario actualizado correctamente");
        cancelarEdicion();
      } else {
        // --- MODO CREACIÓN (POST) ---
        const response = await api.post('/usuarios/', datosEnvio);
        setUsuario([...usuarios, response.data]);
        alert("Usuario creado correctamente");
        cancelarEdicion();
      }
    } catch (error) {
      console.error("Error al guardar:", error.response?.data || error);
      alert("Error: " + (error.response?.data?.error || "Ocurrió un fallo"));
    }
  };


  return (
    <div className={styles.wrapper}>
      <div className={styles.container}>
        <div className={styles.header}>
          <div>
            <h2 className={styles.title}>Gestión de Usuarios</h2>
            <p className={styles.subtitle}>{usuarios.length} usuarios en total</p>
          </div>
                    {!mostrarFormulario && (
                      <button className={`${styles.btn} ${styles.btnPrimary}`} onClick={() =>{
                if (esComun) {
                  alert("No tienes permisos para crear usuarios.");
                  return;
                }
                       setMostrarFormulario(true);}}>
                        <IconPlus /> Nuevo usuario
                      </button>
                    )}
                  </div>

        {error && <p style={{ color: '#ef4444', marginBottom: '1rem' }}>Error: {error}</p>}

                {/* Barra de Filtros */}
        <div style={{ display: 'flex', gap: '1rem', marginBottom: '1.5rem', alignItems: 'center', background: '#1f2937', padding: '1rem', borderRadius: '0.5rem' }}>
          <div>
            <label style={{ color: '#9ca3af', fontSize: '0.875rem', display: 'block' }}>Rol:</label>
            <select 
              name="rol" 
              value={filtros.rol} 
              onChange={manejarCambioFiltro}
              className={styles.input}
            >
              <option value="">Todos los roles</option>
              <option value="COMUN">Usuario Común</option>
              <option value="JEFE">Jefe de Equipo</option>
              <option value="ADMIN">Administrador</option>
            </select>
          </div>
        
          
        
          <div style={{ display: 'flex', gap: '0.5rem', alignSelf: 'flex-end' }}>
            <button className={`${styles.btn} ${styles.btnPrimary}`} onClick={aplicarFiltro}>
              Filtrar
            </button>
            <button className={styles.btnIcon} style={{ padding: '0.5rem 1rem' }} onClick={limpiarFiltros}>
              Limpiar
            </button>
          </div>
          </div>
        </div>
        

        {mostrarFormulario && (
          <form className={styles.form} onSubmit={botonForm}>
            <div className={styles.grid}>
              
              <div>
                <label className={styles.label} htmlFor="nombre">Nombre: </label>
                <input
                  className={styles.input}
                  type="text"
                  id="nombre"
                  name="nombre"
                  value={formulario.nombre}
                  onChange={manejador}
                  required
                />
              </div>

              <div>
                <label className={styles.label} htmlFor="email">Correo electrónico: </label>
                <input
                  className={styles.input}
                  type="email"
                  id="email"
                  name="email"
                  value={formulario.email}
                  onChange={manejador}
                  required
                />
              </div>

              <div>
                <label className={styles.label} htmlFor="password">Contraseña: </label>
                <input
                  className={styles.input}
                  type="password"
                  id="password"
                  name="password"
                  value={formulario.password}
                  onChange={manejador}
                  required={!editandoId}
                />
              </div>

              <div>
                <label className={styles.label} htmlFor="rol">Rol: </label>
                <select
                  className={styles.input}
                  id="rol"
                  name="rol"
                  value={formulario.rol}
                  onChange={manejador}
                >
                  <option value="COMUN">Usuario estandar</option>
                  <option value="JEFE">Jefe de proyecto</option>
                  <option value="ADMIN">Administrador</option>
                </select>
              </div>

            </div>

            <div style={{ marginTop: '1.25rem', display: 'flex', gap: '0.5rem' }}>
              <button type="submit" className={`${styles.btn} ${styles.btnPrimary}`}>
                Enviar
              </button>
              <button type="button" className={styles.btnIcon} style={{ padding: '0.5rem 1rem' }} onClick={cancelarEdicion}>
                Cancelar
              </button>
            </div>
          </form>
        )}

        <div className={styles.list}>
          {usuarios.map((usuario) => (
            <div key={usuario.id} className={styles.card}>
              <div className={styles.cardBody}>
                <div className={styles.headerRow}>
                  <strong className={styles.tareaTitulo}>{usuario.nombre}</strong>
                  <span className={`${styles.badge} ${styles.badgePro}`}>{usuario.rol}</span>
                </div>
              </div>

              <div className={styles.actions}>
                <button className={styles.btnIcon} onClick={() => activarEdicion(usuario)}>
                  <IconEdit />
                </button>
                <button className={styles.btnIcon} style={{ color: '#ef4444' }} onClick={() => eliminarUsuario(usuario.id)}>
                  <IconTrash />
                </button>
              </div>
            </div>
          ))}
        </div>

      </div>
    
  );

}