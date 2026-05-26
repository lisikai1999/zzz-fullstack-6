import api from './index'

export const exportBooks = () => api.get('/data/export/books/', { responseType: 'blob' })
export const importBooks = (file) => {
  const formData = new FormData()
  formData.append('file', file)
  return api.post('/data/import/books/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}
export const exportReaders = () => api.get('/data/export/readers/', { responseType: 'blob' })
export const importReaders = (file) => {
  const formData = new FormData()
  formData.append('file', file)
  return api.post('/data/import/readers/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}
export const downloadBookTemplate = () => api.get('/data/template/books/', { responseType: 'blob' })
export const downloadReaderTemplate = () => api.get('/data/template/readers/', { responseType: 'blob' })
