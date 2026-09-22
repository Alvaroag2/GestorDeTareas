import { useEffect, useContext, useState } from 'react';
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

export default function CategoriasPage() {

const [categorias, setCategorias] = useState([]);
const [error, setError] = useState(null);
const [mostrarFormulario, setMostrarFormulario] = useState(false);
const [formulario, setFormulario] = useState({
  nombre:'',
  descripcion:'',
});

const { usuario } = useContext(AuthContext);

const [editandoId, setEditandoId] = useState(null);

useEffect(() => {
    api.get('/categorias/')
    .then((response) => setCategorias(response.data))
    .catch((err) => setError(err.message));
  }, []);

  const manejador = (e) => {

  const { name, value, type, checked } = e.target;
    
  setFormulario({
    ...formulario, //Sin esta línea, si editas la descripción, perderías el título, la prioridad y el resto de campos que ya habías rellenado.
    [name]: type === 'checkbox' ? checked : value //Operador ternario si es un checkbox guarda checked (true o false) si no es guarda valor osea el texto o numero de los inputs normales
  });
    
  



};

const rolActual = (usuario?.rol || usuario?.perfil?.rol || usuario?.perfil_rol || '').toUpperCase();
  const esComun = rolActual === 'COMUN';

const activarEdicion = (categoria) => {
  if (esComun) {
      alert("No tienes permisos para editar categorias.");
      return;
    }

    setEditandoId(categoria.id);
    setFormulario({
      nombre: categoria.nombre,
      descripcion: categoria.descripcion
    });
    setMostrarFormulario(true);
  };

  // Cancela la edición y limpia el formulario
  const cancelarEdicion = () => {
    setEditandoId(null);
    setFormulario({ nombre: '', descripcion: ''});
    setMostrarFormulario(false);
  };


const eliminarCategoria = async (id) => {

  if (esComun) {
      alert("No tienes permisos para eliminar categorias.");
      return;
    }
  // Confirmación previa antes de borrar
  const confirmar = window.confirm("¿Estas seguro de que deseas eliminar esta categoria?");
  if (!confirmar) return;

  try {
    // 1. Petición DELETE a Django enviando la ID
    await api.delete(`/categorias/${id}/`);

    // 2. Filtramos el estado local eliminando la tarea con esa ID
    setCategorias(categorias.filter(categoria => categoria.id !== id));

    alert("Categoria eliminada con éxito");
    
    // Si la categoria que se borra estaba siendo editada, cancelamos la edición
    if (editandoId === id) {
      cancelarEdicion();
    }
  } catch (error) {
    console.error("Error al eliminar la categoria:", error.response?.data || error);
    alert("Error al intentar eliminar la categoria");
  }
};

   const botonForm = async (e) => {
    e.preventDefault();

    if (esComun) {
      alert("No tienes permisos para crear categorias.");
      return;
    }
  
    // 1. Mapeamos los datos del formulario local
    const datosEnvio = {
      nombre: formulario.nombre.trim(),
      descripcion: formulario.descripcion.trim(),
    };
  
    try {
      if (editandoId) {
        // --- MODO EDICIÓN (PUT) ---
        const response = await api.put(`/categorias/${editandoId}/`, datosEnvio);
        
        // Reemplazamos el usuario actualizado en la lista local
        setCategorias(categorias.map(c => c.id === editandoId ? response.data : c));
        alert("Categoria actualizada correctamente");
        cancelarEdicion();
       } else {
      // 2. Enviamos el POST a la API
      const response = await api.post('/categorias/', datosEnvio);
  
      // 3. Añadimos el nuevo usuario a la lista local
      setCategorias([...categorias, response.data]);
  
      // 4. Limpiamos el formulario
      setFormulario({
        nombre: '',
        descripcion: '',
      });
      setMostrarFormulario(false);
      
      alert("Categoria " + formulario.nombre + " creada correctamente");
    }
    } catch (error) {
      console.error("Error al crear la categoria:", error.response?.data || error);
      alert("Hubo un error al crear la categoria");
    }
  };

  return (
    <div className={styles.wrapper}>
      <div className={styles.container}>
        <div className={styles.header}>
          <div>
            <h2 className={styles.title}>Gestión de Categorías</h2>
            <p className={styles.subtitle}>{categorias.length} categorías en total</p>
          </div>
          {!mostrarFormulario && (
            <button className={`${styles.btn} ${styles.btnPrimary}`} onClick={() =>{
      if (esComun) {
        alert("No tienes permisos para crear categorías.");
        return;
      }
             setMostrarFormulario(true);}}>
              <IconPlus /> Nueva categoría
            </button>
          )}
        </div>

        {error && <p style={{ color: '#ef4444', marginBottom: '1rem' }}>Error: {error}</p>}

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
                <label className={styles.label} htmlFor="descripcion">Descripción: </label>
                <input
                  className={styles.input}
                  type="text"
                  id="descripcion"
                  name="descripcion"
                  value={formulario.descripcion}
                  onChange={manejador}
                  required
                />
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
          {categorias.map((categoria) => (
            <div key={categoria.id} className={styles.card}>
              <div className={styles.cardBody}>
                <div className={styles.headerRow}>
                  <strong className={styles.tareaTitulo}>{categoria.nombre}</strong>
                </div>
                {categoria.descripcion && (
                  <p className={styles.tareaDesc} style={{ margin: '0.5rem 0 0 0', color: '#9ca3af', fontSize: '0.875rem' }}>
                    {categoria.descripcion}
                  </p>
                )}
              </div>

              <div className={styles.actions}>
                <button className={styles.btnIcon} onClick={() => activarEdicion(categoria)}>
                  <IconEdit />
                </button>
                <button className={styles.btnIcon} style={{ color: '#ef4444' }} onClick={() => eliminarCategoria(categoria.id)}>
                  <IconTrash />
                </button>
              </div>
            </div>
          ))}
        </div>

      </div>
    </div>
  );
}