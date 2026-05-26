<template>
  <div>
    <div class="page-header">
      <h2>图书管理</h2>
      <el-button v-if="isAdminOrLibrarian" type="primary" @click="$router.push('/books/create')">新增图书</el-button>
    </div>

    <div class="filter-bar">
      <el-input v-model="search" placeholder="搜索书名/作者/ISBN" clearable style="width: 250px" @clear="fetchBooks" @keyup.enter="fetchBooks" />
      <el-select v-model="filterCategory" placeholder="选择分类" clearable @change="fetchBooks">
        <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.id" />
      </el-select>
      <el-select v-model="filterStatus" placeholder="状态" clearable @change="fetchBooks">
        <el-option label="可借" value="available" />
        <el-option label="已借出" value="borrowed" />
        <el-option label="维护中" value="maintenance" />
      </el-select>
      <el-button type="primary" @click="fetchBooks">搜索</el-button>
    </div>

    <el-table :data="books" v-loading="loading" stripe>
      <el-table-column prop="isbn" label="ISBN" width="140" />
      <el-table-column prop="title" label="书名" min-width="180" />
      <el-table-column prop="author" label="作者" width="120" />
      <el-table-column prop="publisher" label="出版社" width="140" />
      <el-table-column label="分类" width="160">
        <template #default="{ row }">
          <el-tag v-for="cat in row.categories" :key="cat.id" size="small" style="margin: 2px">{{ cat.name }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="available_copies" label="可借" width="70" align="center" />
      <el-table-column prop="total_copies" label="总数" width="70" align="center" />
      <el-table-column label="状态" width="80" align="center">
        <template #default="{ row }">
          <el-tag :type="row.status === 'available' ? 'success' : 'warning'" size="small">
            {{ statusMap[row.status] }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180" fixed="right">
        <template #default="{ row }">
          <el-button text type="primary" @click="$router.push(`/books/${row.id}`)">详情</el-button>
          <el-button v-if="isAdminOrLibrarian" text type="primary" @click="$router.push(`/books/${row.id}/edit`)">编辑</el-button>
          <el-popconfirm v-if="isAdmin" title="确认删除?" @confirm="handleDelete(row.id)">
            <template #reference>
              <el-button text type="danger">删除</el-button>
            </template>
          </el-popconfirm>
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
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { getBooks, deleteBook, getCategories } from '@/api/books'
import { ElMessage } from 'element-plus'

const authStore = useAuthStore()
const isAdmin = computed(() => authStore.isAdmin)
const isAdminOrLibrarian = computed(() => authStore.isAdminOrLibrarian)

const books = ref([])
const categories = ref([])
const loading = ref(false)
const search = ref('')
const filterCategory = ref('')
const filterStatus = ref('')
const page = ref(1)
const total = ref(0)

const statusMap = { available: '可借', borrowed: '已借出', reserved: '已预约', maintenance: '维护中' }

async function fetchBooks() {
  loading.value = true
  try {
    const params = { page: page.value, search: search.value }
    if (filterCategory.value) params.category = filterCategory.value
    if (filterStatus.value) params.status = filterStatus.value
    const res = await getBooks(params)
    books.value = res.data.results || res.data
    total.value = res.data.count || books.value.length
  } catch {
    ElMessage.error('加载图书列表失败')
  } finally {
    loading.value = false
  }
}

async function fetchCategories() {
  try {
    const res = await getCategories()
    categories.value = res.data.results || res.data
  } catch {}
}

async function handleDelete(id) {
  await deleteBook(id)
  ElMessage.success('删除成功')
  fetchBooks()
}

function handlePageChange(p) {
  page.value = p
  fetchBooks()
}

onMounted(() => {
  fetchBooks()
  fetchCategories()
})
</script>
