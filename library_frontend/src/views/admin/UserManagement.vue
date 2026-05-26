<template>
  <div>
    <div class="page-header">
      <h2>用户管理</h2>
    </div>

    <el-table :data="users" v-loading="loading" stripe>
      <el-table-column prop="username" label="用户名" width="120" />
      <el-table-column label="姓名" width="120">
        <template #default="{ row }">{{ row.last_name }}{{ row.first_name }}</template>
      </el-table-column>
      <el-table-column prop="email" label="邮箱" width="180" />
      <el-table-column label="角色" width="130">
        <template #default="{ row }">
          <el-select v-model="row.profile.role" size="small" @change="handleRoleChange(row)">
            <el-option label="管理员" value="admin" />
            <el-option label="图书管理员" value="librarian" />
            <el-option label="读者" value="reader" />
          </el-select>
        </template>
      </el-table-column>
      <el-table-column label="会员类型" width="100">
        <template #default="{ row }">{{ membershipMap[row.profile?.membership_type] }}</template>
      </el-table-column>
      <el-table-column label="状态" width="80" align="center">
        <template #default="{ row }">
          <el-tag :type="row.is_active ? 'success' : 'danger'" size="small">
            {{ row.is_active ? '正常' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="100" fixed="right">
        <template #default="{ row }">
          <el-popconfirm title="确认删除?" @confirm="handleDelete(row.id)">
            <template #reference>
              <el-button text type="danger" size="small">删除</el-button>
            </template>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getUsers, deleteUser, changeUserRole } from '@/api/users'
import { ElMessage } from 'element-plus'

const users = ref([])
const loading = ref(false)
const membershipMap = { standard: '标准', premium: '高级', student: '学生' }

async function fetchUsers() {
  loading.value = true
  try {
    const res = await getUsers({ page_size: 1000 })
    users.value = res.data.results || res.data
  } catch {} finally {
    loading.value = false
  }
}

async function handleRoleChange(user) {
  try {
    await changeUserRole(user.id, user.profile.role)
    ElMessage.success('角色已更新')
  } catch (e) {
    ElMessage.error('更新失败')
    fetchUsers()
  }
}

async function handleDelete(id) {
  try {
    await deleteUser(id)
    ElMessage.success('已删除')
    fetchUsers()
  } catch {}
}

onMounted(fetchUsers)
</script>
