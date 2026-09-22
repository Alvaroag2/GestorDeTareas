import { useEffect, useState } from 'react';
import api from '../api';
import styles from './tareasPage.module.css';

// Recibimos 'tareaId' y 'onVolver' como props directamente desde App.jsx
export default function TareaDetallePage({ tareaId, onVolver }) {
  const [tarea, setTarea] = useState(null);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Verificamos que tengamos un ID antes de llamar a la API
    if (!tareaId) {
      // eslint-disable-next-line react-hooks/set-state-in-effect
      setError("No se ha proporcionado un ID de tarea válido.");
      setCargando(false);
      return;
    }

    setCargando(true);
    setError(null);

    // Hacemos la petición con el tareaId recibido por props
    api.get(`/tareas/${tareaId}/`)
      .then((res) => {
        setTarea(res.data);
        setCargando(false);
      })
      .catch((err) => {
        console.error("Error al cargar la tarea:", err);
        setError("No se pudo obtener la información de la tarea.");
        setCargando(false);
      });
  }, [tareaId]);

  if (cargando) {
    return <p style={{ color: '#ffffff', padding: '2rem' }}>Cargando detalles de la tarea...</p>;
  }

  if (error) {
    return (
      <div style={{ padding: '2rem' }}>
        <p style={{ color: '#ef4444', marginBottom: '1rem' }}>{error}</p>
        <button onClick={onVolver} style={{ padding: '0.5rem 1rem', cursor: 'pointer' }}>
          ← Volver a Tareas
        </button>
      </div>
    );
  }

  return (
    <div className={styles.wrapper}>
      <div className={styles.container}>
        <button 
          className={styles.btnIcon} 
          onClick={onVolver}
          style={{ marginBottom: '1rem', padding: '0.5rem 1rem', cursor: 'pointer' }}
        >
          ← Volver atrás
        </button>

        <div className={styles.card} style={{ flexDirection: 'column', alignItems: 'flex-start', padding: '1.5rem' }}>
          <h1 className={styles.title}>{tarea.titulo}</h1>
          <p style={{ color: '#9ca3af', marginTop: '0.5rem' }}>
            {tarea.descripcion || 'Sin descripción asignada.'}
          </p>

          <div style={{ marginTop: '1.5rem', width: '100%' }}>
            {Object.entries(tarea).map(([clave, valor]) => {
              let valorMostrar = valor;

              if (typeof valor === 'object' && valor !== null) {
                valorMostrar = valor.nombre || valor.username || JSON.stringify(valor);
              } else if (typeof valor === 'boolean') {
                valorMostrar = valor ? 'Sí' : 'No';
              } else if (valor === null || valor === '') {
                valorMostrar = 'N/A';
              }

              return (
                <div 
                  key={clave} 
                  style={{ 
                    display: 'flex', 
                    justifyContent: 'space-between', 
                    padding: '0.6rem 0', 
                    borderBottom: '1px solid #374151' 
                  }}
                >
                  <strong style={{ color: '#9ca3af', textTransform: 'capitalize' }}>
                    {clave.replace('_', ' ')}:
                  </strong>
                  <span style={{ color: '#ffffff' }}>{String(valorMostrar)}</span>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}