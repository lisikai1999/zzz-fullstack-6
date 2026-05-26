<template>
  <div>
    <div class="page-header">
      <h2>{{ isAdminOrLibrarian ? '借阅管理' : '我的借阅记录' }}</h2>
      <el-button v-if="isAdminOrLibrarian" type="primary" @click="$router.push('/borrowing/borrow')">新增借阅</el-button>
    </div>

    <div class="filter-bar">
      <el-select v-model="filterStatus" placeholder="状态筛选" clearable @change="fetchRecords">
        <el-option label="借出" value="borrowed" />
        <el-option label="已还" value="returned" />
        <el-option label="逾期" value="overdue" />
      </el-select>
      <el-button type="warning" v-if="isAdminOrLibrarian" @click="showOverdue">查看逾期</el-button>
    </div>

    <el-table :data="records" v-loading="loading" stripe>
      <el-table-column prop="book_title" label="图书" min-width="180" />
      <el-table-column prop="book_isbn" label="ISBN" width="140" />
      <el-table-column prop="username" label="借阅人" width="100" />
      <el-table-column label="借阅日期" width="110">
        <template #default="{ row }">{{ row.borrow_date?.substring(0, 10) }}</template>
      </el-table-column>
      <el-table-column label="应还日期" width="110">
        <template #default="{ row }">{{ row.due_date?.substring(0, 10) }}</template>
      </el-table-column>
      <el-table-column label="归还日期" width="110">
        <template #default="{ row }">{{ row.return_date?.substring(0, 10) || '-' }}</template>
      </el-table-column>
      <el-table-column label="状态" width="80" align="center">
        <template #default="{ row }">
          <el-tag :type="statusType(row)" size="small">{{ displayStatus(row) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="fine_amount" label="罚款" width="80" align="center" />
      <el-table-column label="操作" width="160" fixed="right">
        <template #default="{ row }">
          <template v-if="row.status === 'borrowed'">
            <el-button v-if="isAdminOrLibrarian" text type="primary" @click="handleReturn(row)">归还</el-button>
            <el-button text type="success" @click="handleRenew(row)">续借</el-button>
          </template>
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

    <el-dialog v-model="returnDialogVisible" title="归还图书" width="400px">
      <el-form>
        <el-form-item label="备注">
          <el-input v-model="returnNotes" type="textarea" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="returnDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmReturn">确认归还</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { getBorrowingRecords, returnBook, renewBook, getOverdueList } from '@/api/borrowing'
import { ElMessage, ElMessageBox } from 'element-plus'

const authStore = useAuthStore()
const isAdminOrLibrarian = computed(() => authStore.isAdminOrLibrarian)

const records = ref([])
const loading = ref(false)
const filterStatus = ref('')
const page = ref(1)
const total = ref(0)

const returnDialogVisible = ref(false)
const returnNotes = ref('')
const currentRecord = ref(null)

const statusMap = { borrowed: '借出', returned: '已还', overdue: '逾期', lost: '丢失' }

function statusType(row) {
  if (row.is_overdue || row.status === 'overdue') return 'danger'
  if (row.status === 'returned') return 'success'
  return 'warning'
}

function displayStatus(row) {
  if (row.is_overdue && row.status === 'borrowed') return '逾期'
  return statusMap[row.status]
}

async function fetchRecords() {
  loading.value = true
  try {
    const params = { page: page.value }
    if (filterStatus.value) params.status = filterStatus.value
    const res = await getBorrowingRecords(params)
    records.value = res.data.results || res.data
    total.value = res.data.count || records.value.length
  } catch {
    ElMessage.error('加载借阅记录失败')
  } finally {
    loading.value = false
  }
}

async function showOverdue() {
  loading.value = true
  try {
    const res = await getOverdueList()
    records.value = res.data
    total.value = res.data.length
  } catch {} finally {
    loading.value = false
  }
}

function handleReturn(row) {
  currentRecord.value = row
  returnNotes.value = ''
  returnDialogVisible.value = true
}

async function confirmReturn() {
  try {
    await returnBook(currentRecord.value.id, { notes: returnNotes.value })
    ElMessage.success('归还成功')
    returnDialogVisible.value = false
    fetchRecords()
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '操作失败')
  }
}

async function handleRenew(row) {
  try {
    await ElMessageBox.confirm('确认续借该图书?', '续借确认')
    await renewBook(row.id)
    ElMessage.success('续借成功')
    fetchRecords()
  } catch (e) {
    if (e !== 'cancel') {
      ElMessage.error(e.response?.data?.detail || '续借失败')
    }
  }
}

function handlePageChange(p) {
  page.value = p
  fetchRecords()
}

onMounted(fetchRecords)
</script>
