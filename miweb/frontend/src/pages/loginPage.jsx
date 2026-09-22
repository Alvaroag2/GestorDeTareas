import { useState, useContext, useEffect } from 'react';
import api from '../api';
import { AuthContext } from '../context/AuthContext';
import styles from './tareasPage.module.css';

export default function LoginPage() {

const [error, setError] = useState(null);
const [formulario, setFormulario] = useState({
  username:'',
  password:'',

});

const { login } = useContext(AuthContext);

// Carga inicial para asegurar que Django establezca la cookie CSRF
  useEffect(() => {
    api.get('/csrf/').catch((err) => console.error("Error al obtener CSRF:", err));
    }, []);

const manejador = (e) => {

  const { name, value, type, checked } = e.target;
    
  setFormulario({
    ...formulario, //Sin esta línea, si editas la descripción, perderías el título, la prioridad y el resto de campos que ya habías rellenado.
    [name]: type === 'checkbox' ? checked : value //Operador ternario si es un checkbox guarda checked (true o false) si no es guarda valor osea el texto o numero de los inputs normales
  });
    
  
};

  const botonForm = async (e) => {
    e.preventDefault();
    setError(null);

    try {
      // 1. Pedimos explícitamente el token fresco justo antes del login
      const csrfRes = await api.get('/csrf/');
      const csrfToken = csrfRes.data.csrf_token;

      // 2. Enviamos la petición de login asegurando la cabecera X-CSRFToken
      const response = await api.post('/login/', formulario, {
        headers: {
          'X-CSRFToken': csrfToken,
        },
      });

      login(response.data);
      alert(`¡Bienvenido ${response.data.nombre}!`);
    } catch (err) {
      if (err.response && err.response.data.error) {
        setError(err.response.data.error);
      } else {
        setError('Error al iniciar sesión');
      }
    }
  };

  return (
    <div className={styles.wrapper}>
      <div className={styles.container}>
        <form className={styles.form} onSubmit={botonForm}>
          <h2 className={styles.title} style={{ marginBottom: '1.5rem' }}>Login</h2>

          {error && <p style={{ color: '#ef4444', fontWeight: 'bold', marginBottom: '1rem' }}>{error}</p>}

          <div className={styles.grid}>
            <div className={styles.full}>
              <label className={styles.label} htmlFor="username">Nombre: </label>
              <input
                className={styles.input}
                type="text"
                id="username"
                name="username"
                value={formulario.username}
                onChange={manejador}
                required
              />
            </div>

            <div className={styles.full}>
              <label className={styles.label} htmlFor="password">Contraseña: </label>
              <input
                className={styles.input}
                type="password"
                id="password"
                name="password"
                value={formulario.password}
                onChange={manejador}
                required
              />
            </div>
          </div>

          <div style={{ marginTop: '1.5rem' }}>
            <button type="submit" className={`${styles.btn} ${styles.btnPrimary}`} style={{ width: '100%', justifyContent: 'center' }}>
              Iniciar Sesión
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}