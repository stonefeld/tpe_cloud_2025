import axios from 'axios'

// Create axios instance with base configuration
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Types for our API responses
export interface Product {
  id: number
  name: string
  description: string
  unit_price: number
  created_at: string
  updated_at: string
}

export interface Pool {
  id: number
  product: number
  start_at: string
  end_at: string
  min_quantity: number
  created_at: string
  updated_at: string
}

export interface Request {
  id: number
  pool: number
  email: string
  quantity: number
  created_at: string
}

// Product API
export const productApi = {
  getAll: () => api.get<Product[]>('/products/'),
  getById: (id: number) => api.get<Product>(`/products/${id}/`),
  create: (data: Omit<Product, 'id' | 'created_at' | 'updated_at'>) =>
    api.post<Product>('/products/', data),
  update: (
    id: number,
    data: Partial<Omit<Product, 'id' | 'created_at' | 'updated_at'>>,
  ) => api.put<Product>(`/products/${id}/`, data),
  delete: (id: number) => api.delete(`/products/${id}/`),
}

// Pool API
export const poolApi = {
  getAll: () => api.get<Pool[]>('/pools/'),
  getById: (id: number) => api.get<Pool>(`/pools/${id}/`),
  create: (data: Omit<Pool, 'id' | 'created_at' | 'updated_at'>) =>
    api.post<Pool>('/pools/', data),
  update: (
    id: number,
    data: Partial<Omit<Pool, 'id' | 'created_at' | 'updated_at'>>,
  ) => api.put<Pool>(`/pools/${id}/`, data),
  delete: (id: number) => api.delete(`/pools/${id}/`),
}

// Request API
export const requestApi = {
  getByPool: (poolId: number) =>
    api.get<Request[]>(`/pools/${poolId}/requests/`),
  create: (poolId: number, data: Omit<Request, 'id' | 'pool' | 'created_at'>) =>
    api.post<Request>(`/pools/${poolId}/requests/`, data),
  update: (
    poolId: number,
    requestId: number,
    data: Partial<Omit<Request, 'id' | 'pool' | 'created_at'>>,
  ) => api.put<Request>(`/pools/${poolId}/requests/${requestId}/`, data),
  delete: (poolId: number, requestId: number) =>
    api.delete(`/pools/${poolId}/requests/${requestId}/`),
}

export default api
