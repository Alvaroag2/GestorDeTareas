import axios from 'axios';

// Función para leer el token CSRF que envía Django en las cookies
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

/*const api = axios.create({
  baseURL: 'http://localhost:8000/api', // Servidor de Django
  withCredentials: true, // VITAL: Permite enviar cookies de sesión
});*/

const api = axios.create({
  // Si existe la variable en Vercel la usa; si no, usa localhost
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
  withCredentials: true, // Importante para sesiones/cookies
});

// Interceptor para adjuntar el Token CSRF en POST, PUT y DELETE
api.interceptors.request.use((config) => {
  const token = getCookie('csrftoken');
  if (token) {
    config.headers['X-CSRFToken'] = token;
  }
  return config;
});

export default api;