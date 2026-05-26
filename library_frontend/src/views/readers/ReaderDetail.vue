<template>
  <div v-loading="loading">
    <div class="page-header">
      <h2>读者详情</h2>
      <el-button @click="$router.back()">返回</el-button>
    </div>

    <el-descriptions :column="2" border>
      <el-descriptions-item label="用户名">{{ reader.username }}</el-descriptions-item>
      <el-descriptions-item label="姓名">{{ reader.last_name }}{{ reader.first_name }}</el-descriptions-item>
      <el-descriptions-item label="邮箱">{{ reader.email }}</el-descriptions-item>
      <el-descriptions-item label="电话">{{ reader.profile?.phone }}</el-descriptions-item>
      <el-descriptions-item label="会员类型">{{ membershipMap[reader.profile?.membership_type] }}</el-descriptions-item>
      <el-descriptions-item label="借书证号">{{ reader.profile?.id_card }}</el-descriptions-item>
      <el-descriptions-item label="最大借阅数量">{{ reader.profile?.max_borrow_count }}</el-descriptions-item>
      <el-descriptions-item label="地址">{{ reader.profile?.address }}</el-descriptions-item>
    </el-descriptions>

    <h3 style="margin: 24px 0 12px">借阅记录</h3>
    <el-table :data="borrowRecords" stripe>
      <el-table-column prop="book_title" label="图书" />
      <el-table-column label="借阅日期" width="110">
        <template #default="{ row }">{{ row.borrow_date?.substring(0, 10) }}</template>
      </el-table-column>
      <el-table-column label="应还日期" width="110">
        <template #default="{ row }">{{ row.due_date?.substring(0, 10) }}</template>
      </el-table-column>
      <el-table-column label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="row.status === 'returned' ? 'success' : 'warning'" size="small">
            {{ statusMap[row.status] }}
          </el-tag>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getUser } from '@/api/users'
import { getBorrowingRecords } from '@/api/borrowing'

const route = useRoute()
const reader = ref({})
const borrowRecords = ref([])
const loading = ref(false)

const membershipMap = { standard: '标准', premium: '高级', student: '学生' }
const statusMap = { borrowed: '借出', returned: '已还', overdue: '逾期', lost: '丢失' }

onMounted(async () => {
  loading.value = true
  try {
    const [userRes, recordsRes] = await Promise.all([
      getUser(route.params.id),
      getBorrowingRecords({ user_id: route.params.id }),
    ])
    reader.value = userRes.data
    borrowRecords.value = recordsRes.data.results || recordsRes.data
  } catch {} finally {
    loading.value = false
  }
})
</script>
