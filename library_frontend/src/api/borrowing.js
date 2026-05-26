import api from './index'

export const getBorrowingRecords = (params) => api.get('/borrowing/records/', { params })
export const borrowBook = (data) => api.post('/borrowing/borrow/', data)
export const returnBook = (id, data) => api.post(`/borrowing/return/${id}/`, data)
export const renewBook = (id) => api.post(`/borrowing/renew/${id}/`)
export const getOverdueList = () => api.get('/borrowing/overdue/')
export const getMyRecords = () => api.get('/borrowing/my-records/')

export const getBorrowingConfigs = () => api.get('/borrowing/config/')
export const createBorrowingConfig = (data) => api.post('/borrowing/config/', data)
export const updateBorrowingConfig = (id, data) => api.put(`/borrowing/config/${id}/`, data)
