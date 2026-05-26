import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as loginApi, getMe } from '@/api/auth'
import router from '@/router'

export const useAuthStore = defineStore('auth', () => {
  const accessToken = ref(localStorage.getItem('access_token') || '')
  const refreshToken = ref(localStorage.getItem('refresh_token') || '')
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))

  const isAuthenticated = computed(() => !!accessToken.value)
  const userRole = computed(() => user.value?.profile?.role || 'reader')
  const isAdmin = computed(() => userRole.value === 'admin')
  const isLibrarian = computed(() => userRole.value === 'librarian')
  const isAdminOrLibrarian = computed(() => ['admin', 'librarian'].includes(userRole.value))

  function setTokens(access, refresh) {
    accessToken.value = access
    refreshToken.value = refresh || refreshToken.value
    localStorage.setItem('access_token', access)
    if (refresh) localStorage.setItem('refresh_token', refresh)
  }

  async function login(username, password) {
    const res = await loginApi({ username, password })
    setTokens(res.data.access, res.data.refresh)
    await fetchUser()
  }

  async function fetchUser() {
    const res = await getMe()
    user.value = res.data
    localStorage.setItem('user', JSON.stringify(res.data))
  }

  function logout() {
    accessToken.value = ''
    refreshToken.value = ''
    user.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
    router.push('/login')
  }

  return {
    accessToken, refreshToken, user,
    isAuthenticated, userRole, isAdmin, isLibrarian, isAdminOrLibrarian,
    setTokens, login, fetchUser, logout,
  }
})
