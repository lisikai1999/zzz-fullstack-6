<template>
  <el-container class="app-layout">
    <el-aside width="220px" class="sidebar">
      <div class="logo">
        <h1>图书馆管理</h1>
      </div>
      <el-menu
        :default-active="$route.path"
        router
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409eff"
      >
        <el-menu-item index="/dashboard">
          <el-icon><Monitor /></el-icon>
          <span>仪表盘</span>
        </el-menu-item>
        <el-menu-item index="/books">
          <el-icon><Reading /></el-icon>
          <span>图书管理</span>
        </el-menu-item>
        <el-menu-item index="/borrowing">
          <el-icon><Document /></el-icon>
          <span>{{ isAdminOrLibrarian ? '借阅管理' : '我的借阅' }}</span>
        </el-menu-item>
        <el-menu-item v-if="isAdminOrLibrarian" index="/readers">
          <el-icon><User /></el-icon>
          <span>读者管理</span>
        </el-menu-item>
        <el-menu-item v-if="isAdminOrLibrarian" index="/reports">
          <el-icon><DataAnalysis /></el-icon>
          <span>统计报表</span>
        </el-menu-item>
        <el-menu-item v-if="isAdminOrLibrarian" index="/import-export">
          <el-icon><Upload /></el-icon>
          <span>导入导出</span>
        </el-menu-item>
        <el-sub-menu v-if="isAdmin" index="admin">
          <template #title>
            <el-icon><Setting /></el-icon>
            <span>系统管理</span>
          </template>
          <el-menu-item index="/admin/users">用户管理</el-menu-item>
          <el-menu-item index="/admin/settings">系统设置</el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="header">
        <div class="header-left">
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>{{ $route.name }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        <div class="header-right">
          <el-badge :value="overdueCount" :hidden="overdueCount === 0" class="overdue-badge">
            <el-button text @click="$router.push('/borrowing')">逾期提醒</el-button>
          </el-badge>
          <el-dropdown @command="handleCommand">
            <span class="user-info">
              {{ user?.username }}
              <el-tag size="small" type="info">{{ roleLabel }}</el-tag>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { Monitor, Reading, Document, User, DataAnalysis, Upload, Setting } from '@element-plus/icons-vue'
import { getOverdueList } from '@/api/borrowing'

const authStore = useAuthStore()
const user = computed(() => authStore.user)
const isAdmin = computed(() => authStore.isAdmin)
const isAdminOrLibrarian = computed(() => authStore.isAdminOrLibrarian)
const overdueCount = ref(0)

const roleLabel = computed(() => {
  const map = { admin: '管理员', librarian: '图书管理员', reader: '读者' }
  return map[authStore.userRole] || '读者'
})

function handleCommand(cmd) {
  if (cmd === 'logout') authStore.logout()
}

onMounted(async () => {
  if (authStore.isAdminOrLibrarian) {
    try {
      const res = await getOverdueList()
      overdueCount.value = res.data.length
    } catch {}
  }
})
</script>

<style scoped>
.app-layout {
  height: 100vh;
}
.sidebar {
  background-color: #304156;
  overflow-y: auto;
}
.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}
.logo h1 {
  font-size: 18px;
  white-space: nowrap;
}
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #fff;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
}
.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}
.user-info {
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
}
.main-content {
  background: #f5f7fa;
  min-height: 0;
}
.overdue-badge {
  margin-right: 8px;
}
</style>
