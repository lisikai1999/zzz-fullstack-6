import api from './index'

export const getBooks = (params) => api.get('/books/', { params })
export const getBook = (id) => api.get(`/books/${id}/`)
export const createBook = (data) => api.post('/books/', data)
export const updateBook = (id, data) => api.put(`/books/${id}/`, data)
export const deleteBook = (id) => api.delete(`/books/${id}/`)

export const getCategories = (params) => api.get('/books/categories/', { params })
export const createCategory = (data) => api.post('/books/categories/', data)
export const updateCategory = (id, data) => api.put(`/books/categories/${id}/`, data)
export const deleteCategory = (id) => api.delete(`/books/categories/${id}/`)
