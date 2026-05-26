<template>
  <div>
    <div class="page-header">
      <h2>读者管理</h2>
    </div>

    <div class="filter-bar">
      <el-input v-model="search" placeholder="搜索用户名/姓名" clearable style="width: 250px" @keyup.enter="fetchReaders" />
      <el-button type="primary" @click="fetchReaders">搜索</el-button>
    </div>

    <el-table :data="readers" v-loading="loading" stripe>
      <el-table-column prop="username" label="用户名" width="120" />
      <el-table-column label="姓名" width="120">
        <template #default="{ row }">{{ row.last_name }}{{ row.first_name }}</template>
      </el-table-column>
      <el-table-column prop="email" label="邮箱" width="180" />
      <el-table-column label="电话" width="130">
        <template #default="{ row }">{{ row.profile?.phone }}</template>
      </el-table-column>
      <el-table-column label="会员类型" width="100">
        <template #default="{ row }">
          <el-tag size="small">{{ membershipMap[row.profile?.membership_type] }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="借书证号" width="120">
        <template #default="{ row }">{{ row.profile?.id_card }}</template>
      </el-table-column>
      <el-table-column label="最大借阅" width="90" align="center">
        <template #default="{ row }">{{ row.profile?.max_borrow_count }}</template>
      </el-table-column>
      <el-table-column label="操作" width="120" fixed="right">
        <template #default="{ row }">
          <el-button text type="primary" @click="$router.push(`/readers/${row.id}`)">详情</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      v-if="total > 0"
      style="margin-top: 16px; justify-content: flex-end"
      :current-page="page"
      :page-size="20"
      :total="total"
      layout="total, prev, pager, next"
      @current-change="handlePageChange"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getUsers } from '@/api/users'
import { ElMessage } from 'element-plus'

const readers = ref([])
const loading = ref(false)
const search = ref('')
const page = ref(1)
const total = ref(0)

const membershipMap = { standard: '标准', premium: '高级', student: '学生' }

async function fetchReaders() {
  loading.value = true
  try {
    const params = { page: page.value }
    if (search.value) params.search = search.value
    const res = await getUsers(params)
    readers.value = res.data.results || res.data
    total.value = res.data.count || readers.value.length
  } catch {
    ElMessage.error('加载读者列表失败')
  } finally {
    loading.value = false
  }
}

function handlePageChange(p) {
  page.value = p
  fetchReaders()
}

onMounted(fetchReaders)
</script>
