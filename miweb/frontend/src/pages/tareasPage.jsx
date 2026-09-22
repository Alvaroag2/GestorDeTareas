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

export default function TareasPage({onVerDetalle}) {
  
  const [tareas, setTareas] = useState([]);
  const [usuarios, setUsuarios] = useState([]);
  const [categorias, setCategorias] = useState([]);
  const [error, setError] = useState(null);
  const [mostrarFormulario, setMostrarFormulario] = useState(false);
  
  
  
  const [filtros, setFiltros] = useState({
    categoria: '',
    usuario: ''
  });

  const [formulario, setFormulario] = useState({
    titulo: '',
    descripcion: '',
    prioridad: 'M',
    estado: 'PEN',
    realizada: false,
    fecha_limite: '',
    tiempo_estimado: 0.0,
    usuario: '',
    categoria: ''
  });

  const [editandoId, setEditandoId] = useState(null);
  const { usuario } = useContext(AuthContext);

  useEffect(() => {
    api.get('/tareas/')
      .then((response) => setTareas(response.data))
      .catch((err) => setError(err.message));

    api.get('/usuarios/')
      .then((response) => setUsuarios(response.data))
      .catch((err) => console.error("Error al cargar usuarios:", err));

    api.get('/categorias/')
      .then((response) => setCategorias(response.data))
      .catch((err) => console.error("Error al cargar categorías:", err));
  }, []);

  const rolActual = (usuario?.rol || usuario?.perfil?.rol || usuario?.perfil_rol || '').toUpperCase();
  const esComun = rolActual === 'COMUN';

  const activarEdicion = (tarea) => {
    if (esComun) {
      alert("No tienes permisos para editar tareas.");
      return;
    }

    let idUsuario = '';
    if (tarea.usuario) {
      if (typeof tarea.usuario === 'object') {
        idUsuario = tarea.usuario.id;
      } else {
        idUsuario = tarea.usuario;
      }
    }

    let idCategoria = '';
    if (tarea.categoria) {
      if (typeof tarea.categoria === 'object') {
        idCategoria = tarea.categoria.id;
      } else {
        idCategoria = tarea.categoria;
      }
    }

    setEditandoId(tarea.id);
    setFormulario({
      titulo: tarea.titulo,
      descripcion: tarea.descripcion || '',
      prioridad: tarea.prioridad || 'M',
      estado: tarea.estado || 'PEN',
      realizada: tarea.realizada || false,
      fecha_limite: tarea.fecha_limite || '',
      tiempo_estimado: tarea.tiempo_estimado || 0,
      usuario: idUsuario,
      categoria: idCategoria
    });
    setMostrarFormulario(true);
  };



  const cancelarEdicion = () => {
    setEditandoId(null);
    setFormulario({
      titulo: '',
      descripcion: '',
      prioridad: 'M',
      estado: 'PEN',
      realizada: false,
      fecha_limite: '',
      tiempo_estimado: 0,
      usuario: '',
      categoria: ''
    });
    setMostrarFormulario(false);
  };

  // Función genérica para actualizar el estado del filtro al cambiar un select
const manejarCambioFiltro = (e) => {
  const { name, value } = e.target;
  setFiltros({
    ...filtros,
    [name]: value
  });
};

  const manejador = (e) => {
    const { name, value, type, checked } = e.target;
    let valorFinal = value;
    if (type === 'checkbox') {
      valorFinal = checked;
    }

    setFormulario({
      ...formulario,
      [name]: valorFinal
    });
  };

  const eliminarTarea = async (id) => {
    if (esComun) {
      alert("No tienes permisos para eliminar tareas.");
      return;
    }
    if (!window.confirm("¿Estás seguro de que deseas eliminar esta tarea?")) return;

    try {
      await api.delete(`/tareas/${id}/`);
      setTareas(tareas.filter(tarea => tarea.id !== id));
      if (editandoId === id) cancelarEdicion();
    } catch (error) {
      console.error("Error al eliminar la tarea:", error);
      alert("Error al intentar eliminar la tarea");
    }
  };

  const botonForm = async (e) => {
    e.preventDefault();

    if (esComun) {
      alert("No tienes permisos para crear o modificar tareas.");
      return;
    }

    const datosEnvio = {
      titulo: formulario.titulo,
      descripcion: formulario.descripcion,
      prioridad: formulario.prioridad,
      estado: formulario.estado,
      realizada: formulario.realizada,
      fecha_limite: formulario.fecha_limite || null,
      tiempo_estimado: formulario.tiempo_estimado || 0,
      categoria_id: formulario.categoria || null,
      usuario_id: formulario.usuario || null,
    };

    try {
      if (editandoId) {
        const response = await api.put(`/tareas/${editandoId}/`, datosEnvio);
        setTareas(tareas.map(t => {
          if (t.id === editandoId) {
            return response.data;
          } else {
            return t;
          }
        }));
        cancelarEdicion();
      } else {
        const response = await api.post('/tareas/', datosEnvio);
        setTareas([...tareas, response.data]);
        cancelarEdicion();
      }
    } catch (error) {
      console.error("Error al guardar la tarea:", error);
      alert("Error al guardar la tarea");
    }
  };

  const aplicarFiltro = () => {
  // Construimos un objeto solo con los filtros que no estén vacíos
  const params = {};
  if (filtros.categoria) params.categoria = filtros.categoria;
  if (filtros.usuario) params.usuario = filtros.usuario;

  api.get('/tareas/', { params })
    .then((response) => setTareas(response.data))
    .catch((err) => setError("Error al filtrar las tareas: " + err.message));
};

// Función para limpiar los filtros y traer todas las tareas de nuevo
const limpiarFiltros = () => {
  setFiltros({ categoria: '', usuario: '' });
  api.get('/tareas/')
    .then((response) => setTareas(response.data))
    .catch((err) => setError(err.message));
};

  const getEstadoBadge = (estado) => {
    switch (estado) {
      case 'COM': return <span className={`${styles.badge} ${styles.badgeCom}`}>Completada</span>;
      case 'PRO': return <span className={`${styles.badge} ${styles.badgePro}`}>En progreso</span>;
      default: return <span className={`${styles.badge} ${styles.badgePen}`}>Pendiente</span>;
    }
  };

  let tituloFormulario = "Nueva tarea";
  let textoBotonSubmit = "Crear tarea";

  if (editandoId) {
    tituloFormulario = "Editar tarea";
    textoBotonSubmit = "Guardar cambios";
  }

  return (
    <div className={styles.wrapper}>
      <div className={styles.container}>
        <div className={styles.header}>
          <div>
            <h1 className={styles.title}>Gestión de Tareas</h1>
            <p className={styles.subtitle}>{tareas.length} tareas en total</p>
          </div>
          
                    {!mostrarFormulario && (
                      <button className={`${styles.btn} ${styles.btnPrimary}`} onClick={() =>{
                if (esComun) {
                  alert("No tienes permisos para crear tareas.");
                  return;
                }
                       setMostrarFormulario(true);}}>
                        <IconPlus /> Nueva Tarea
                      </button>
                    )}
                  </div>

        {error && <div style={{ color: '#ef4444', marginBottom: '1rem' }}>Error: {error}</div>}
        {/* Barra de Filtros */}
<div style={{ display: 'flex', gap: '1rem', marginBottom: '1.5rem', alignItems: 'center', background: '#1f2937', padding: '1rem', borderRadius: '0.5rem' }}>
  <div>
    <label style={{ color: '#9ca3af', fontSize: '0.875rem', display: 'block' }}>Categoría:</label>
    <select 
      name="categoria" 
      value={filtros.categoria} 
      onChange={manejarCambioFiltro}
      className={styles.input}
    >
      <option value="">Todas las categorías</option>
      {categorias.map(c => (
        <option key={c.id} value={c.id}>{c.nombre}</option>
      ))}
    </select>
  </div>

  <div>
    <label style={{ color: '#9ca3af', fontSize: '0.875rem', display: 'block' }}>Usuario:</label>
    <select 
      name="usuario" 
      value={filtros.usuario} 
      onChange={manejarCambioFiltro}
      className={styles.input}
    >
      <option value="">Todos los usuarios</option>
      {usuarios.map(u => (
        <option key={u.id} value={u.id}>{u.nombre || u.username}</option>
      ))}
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

        {mostrarFormulario && (
          <form className={styles.form} onSubmit={botonForm}>
            <h2 style={{ fontSize: '0.875rem', color: '#ffffff', marginTop: 0, marginBottom: '1rem' }}>
              {tituloFormulario}
            </h2>

            <div className={styles.grid}>
              <div className={styles.full}>
                <label className={styles.label} htmlFor="titulo">Título</label>
                <input className={styles.input} id="titulo" name="titulo" value={formulario.titulo} onChange={manejador} required />
              </div>

              <div className={styles.full}>
                <label className={styles.label} htmlFor="descripcion">Descripción</label>
                <textarea className={styles.input} id="descripcion" name="descripcion" value={formulario.descripcion} onChange={manejador} rows="2" />
              </div>

              <div>
                <label className={styles.label} htmlFor="estado">Estado</label>
                <select className={styles.input} id="estado" name="estado" value={formulario.estado} onChange={manejador}>
                  <option value="PEN">Pendiente</option>
                  <option value="PRO">En progreso</option>
                  <option value="COM">Completada</option>
                </select>
              </div>

              <div>
                <label className={styles.label} htmlFor="categoria">Categoría</label>
                <select className={styles.input} id="categoria" name="categoria" value={formulario.categoria} onChange={manejador} required>
                  <option value="">Seleccionar categoría</option>
                  {categorias.map(c => <option key={c.id} value={c.id}>{c.nombre}</option>)}
                </select>
              </div>

              <div>
                <label className={styles.label} htmlFor="usuario">Usuario</label>
                <select className={styles.input} id="usuario" name="usuario" value={formulario.usuario} onChange={manejador} required>
                  <option value="">Seleccionar usuario</option>
                  {usuarios.map(u => <option key={u.id} value={u.id}>{u.nombre}</option>)}
                </select>
              </div>

              <div>
                <label className={styles.label} htmlFor="fecha_limite">Fecha límite</label>
                <input type="date" className={styles.input} id="fecha_limite" name="fecha_limite" value={formulario.fecha_limite} onChange={manejador} />
              </div>
            </div>

            <div style={{ display: 'flex', gap: '0.5rem', marginTop: '1.25rem' }}>
              <button type="submit" className={`${styles.btn} ${styles.btnPrimary}`}>
                {textoBotonSubmit}
              </button>
              <button type="button" className={styles.btnIcon} style={{ padding: '0.5rem 1rem' }} onClick={cancelarEdicion}>
                Cancelar
              </button>
            </div>
          </form>
        )}

        <div className={styles.list}>
          {tareas.map((tarea) => {
            let nombreUsuario = '';
            if (typeof tarea.usuario === 'object') {
              nombreUsuario = tarea.usuario?.nombre;
            } else {
              const uEncontrado = usuarios.find(u => u.id === tarea.usuario);
              if (uEncontrado) {
                nombreUsuario = uEncontrado.nombre;
              }
            }

            let nombreCategoria = '';
            if (typeof tarea.categoria === 'object') {
              nombreCategoria = tarea.categoria?.nombre;
            } else {
              const cEncontrada = categorias.find(c => c.id === tarea.categoria);
              if (cEncontrada) {
                nombreCategoria = cEncontrada.nombre;
              }
            }

            return (
              <div key={tarea.id} className={styles.card}>
                <div className={styles.cardBody}>
                  <div className={styles.headerRow}>
                   <span 
                    className={styles.tareaTitulo}
                    style={{ cursor: 'pointer', color: '#60a5fa' }}
                    onClick={() => onVerDetalle(tarea.id)}
                  >
                    {tarea.titulo}
                  </span>
                  {getEstadoBadge(tarea.estado)}
                </div>

                  {tarea.descripcion && <p className={styles.tareaDesc}>{tarea.descripcion}</p>}

                  <div className={styles.tareaMeta}>
                    {nombreCategoria && <span>{nombreCategoria}</span>}
                    {nombreCategoria && nombreUsuario && <span>·</span>}
                    {nombreUsuario && <span>{nombreUsuario}</span>}
                  </div>
                </div>

                <div className={styles.actions}>
                  <button className={styles.btnIcon} onClick={() => activarEdicion(tarea)}>
                    <IconEdit />
                  </button>
                  <button className={styles.btnIcon} style={{ color: '#ef4444' }} onClick={() => eliminarTarea(tarea.id)}>
                    <IconTrash />
                  </button>
                </div>
              </div>
            );
          })}
        </div>

      </div>
    </div>
  );
}