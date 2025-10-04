import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

// Interceptor para manejar errores
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

// Endpoints de Asteroides
export const getAsteroids = async () => {
  const response = await api.get('/api/asteroids');
  return response.data;
};

export const getAsteroid = async (asteroidId) => {
  const response = await api.get(`/api/asteroids/${asteroidId}`);
  return response.data;
};

// Endpoints de Simulación
export const runSimulation = async (simulationData) => {
  const response = await api.post('/api/simulation', simulationData);
  return response.data;
};

// Endpoints de Análisis de Riesgos
export const getRiskAnalysis = async (asteroidId) => {
  const response = await api.get(`/api/risk-analysis/${asteroidId}`);
  return response.data;
};

export const getMitigationStrategies = async (asteroidId) => {
  const response = await api.get(`/api/mitigation-strategies/${asteroidId}`);
  return response.data;
};

export default api;