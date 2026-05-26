import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { guest: true },
  },
  {
    path: '/',
    component: () => import('@/components/layout/AppLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      { path: '', redirect: '/dashboard' },
      { path: 'dashboard', name: 'Dashboard', component: () => import('@/views/Dashboard.vue') },
      { path: 'books', name: 'BookList', component: () => import('@/views/books/BookList.vue') },
      { path: 'books/create', name: 'BookCreate', component: () => import('@/views/books/BookForm.vue'), meta: { roles: ['admin', 'librarian'] } },
      { path: 'books/:id', name: 'BookDetail', component: () => import('@/views/books/BookDetail.vue') },
      { path: 'books/:id/edit', name: 'BookEdit', component: () => import('@/views/books/BookForm.vue'), meta: { roles: ['admin', 'librarian'] } },
      { path: 'borrowing', name: 'BorrowingList', component: () => import('@/views/borrowing/BorrowingList.vue') },
      { path: 'borrowing/borrow', name: 'BorrowForm', component: () => import('@/views/borrowing/BorrowForm.vue'), meta: { roles: ['admin', 'librarian'] } },
      { path: 'readers', name: 'ReaderList', component: () => import('@/views/readers/ReaderList.vue'), meta: { roles: ['admin', 'librarian'] } },
      { path: 'readers/:id', name: 'ReaderDetail', component: () => import('@/views/readers/ReaderDetail.vue'), meta: { roles: ['admin', 'librarian'] } },
      { path: 'reports', name: 'Reports', component: () => import('@/views/reports/ReportDashboard.vue'), meta: { roles: ['admin', 'librarian'] } },
      { path: 'admin/users', name: 'UserManagement', component: () => import('@/views/admin/UserManagement.vue'), meta: { roles: ['admin'] } },
      { path: 'admin/settings', name: 'SystemSettings', component: () => import('@/views/admin/SystemSettings.vue'), meta: { roles: ['admin'] } },
      { path: 'import-export', name: 'DataImportExport', component: () => import('@/views/import-export/DataImportExport.vue'), meta: { roles: ['admin', 'librarian'] } },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.meta.guest && authStore.isAuthenticated) {
    next('/dashboard')
  } else if (to.meta.roles && !to.meta.roles.includes(authStore.userRole)) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
