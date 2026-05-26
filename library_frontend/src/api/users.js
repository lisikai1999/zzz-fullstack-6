import api from './index'

export const getUsers = (params) => api.get('/auth/users/', { params })
export const getUser = (id) => api.get(`/auth/users/${id}/`)
export const createUser = (data) => api.post('/auth/users/', data)
export const updateUser = (id, data) => api.put(`/auth/users/${id}/`, data)
export const deleteUser = (id) => api.delete(`/auth/users/${id}/`)
export const changeUserRole = (id, role) => api.put(`/auth/users/${id}/role/`, { role })
