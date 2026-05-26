import api from './index'

export const getDashboard = () => api.get('/reports/dashboard/')
export const getBorrowingTrend = (params) => api.get('/reports/borrowing-trend/', { params })
export const getCategoryStats = () => api.get('/reports/category-stats/')
export const getOverdueStats = () => api.get('/reports/overdue-stats/')
export const getTopBooks = (params) => api.get('/reports/top-books/', { params })
export const getActiveReaders = (params) => api.get('/reports/active-readers/', { params })
