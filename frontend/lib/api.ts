import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

/**
 * Standard Axios client for API requests.
 * Configured with base URL and interceptors for consistent error handling and auth.
 */
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add auth token if available (Feature 3)
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Standardized error handling following ADR-0004
    const message = error.response?.data?.error?.message || 'An unexpected error occurred';
    console.error(`[API Error] ${message}`, error);
    return Promise.reject(error);
  }
);

export default api;
