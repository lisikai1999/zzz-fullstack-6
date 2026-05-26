import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import router from '@/router'

const api = axios.create({
  baseURL: '/api/v1',
  timeout: 15000,
})

api.interceptors.request.use(config => {
  const authStore = useAuthStore()
  if (authStore.accessToken) {
    config.headers.Authorization = `Bearer ${authStore.accessToken}`
  }
  return config
})

api.interceptors.response.use(
  response => response,
  async error => {
    if (error.response?.status === 401 && !error.config._retry) {
      const authStore = useAuthStore()
      if (authStore.refreshToken) {
        error.config._retry = true
        try {
          const res = await axios.post('/api/v1/auth/token/refresh/', {
            refresh: authStore.refreshToken,
          })
          authStore.setTokens(res.data.access, res.data.refresh)
          error.config.headers.Authorization = `Bearer ${res.data.access}`
          return api(error.config)
        } catch {
          authStore.logout()
          router.push('/login')
        }
      } else {
        authStore.logout()
        router.push('/login')
      }
    }
    return Promise.reject(error)
  }
)

export default api
