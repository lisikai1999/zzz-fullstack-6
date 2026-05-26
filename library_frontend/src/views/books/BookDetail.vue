<template>
  <div v-loading="loading">
    <div class="page-header">
      <h2>{{ book.title }}</h2>
      <div>
        <el-button v-if="isAdminOrLibrarian" type="primary" @click="$router.push(`/books/${book.id}/edit`)">编辑</el-button>
        <el-button @click="$router.back()">返回</el-button>
      </div>
    </div>

    <el-descriptions :column="2" border>
      <el-descriptions-item label="ISBN">{{ book.isbn }}</el-descriptions-item>
      <el-descriptions-item label="作者">{{ book.author }}</el-descriptions-item>
      <el-descriptions-item label="出版社">{{ book.publisher }}</el-descriptions-item>
      <el-descriptions-item label="出版日期">{{ book.publish_date }}</el-descriptions-item>
      <el-descriptions-item label="分类">
        <el-tag v-for="cat in book.categories" :key="cat.id" style="margin-right: 4px">{{ cat.name }}</el-tag>
      </el-descriptions-item>
      <el-descriptions-item label="馆藏位置">{{ book.location }}</el-descriptions-item>
      <el-descriptions-item label="总册数">{{ book.total_copies }}</el-descriptions-item>
      <el-descriptions-item label="可借册数">{{ book.available_copies }}</el-descriptions-item>
      <el-descriptions-item label="状态">
        <el-tag :type="book.status === 'available' ? 'success' : 'warning'">{{ statusMap[book.status] }}</el-tag>
      </el-descriptions-item>
      <el-descriptions-item label="简介" :span="2">{{ book.description || '暂无' }}</el-descriptions-item>
    </el-descriptions>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { getBook } from '@/api/books'

const route = useRoute()
const authStore = useAuthStore()
const isAdminOrLibrarian = computed(() => authStore.isAdminOrLibrarian)
const book = ref({})
const loading = ref(false)

const statusMap = { available: '可借', borrowed: '已借出', reserved: '已预约', maintenance: '维护中' }

onMounted(async () => {
  loading.value = true
  try {
    const res = await getBook(route.params.id)
    book.value = res.data
  } catch {} finally {
    loading.value = false
  }
})
</script>
