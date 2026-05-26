<template>
  <div>
    <div class="page-header">
      <h2>新增借阅</h2>
      <el-button @click="$router.back()">返回</el-button>
    </div>

    <el-form ref="formRef" :model="form" :rules="rules" label-width="100px" style="max-width: 600px">
      <el-form-item label="读者" prop="user_id">
        <el-select v-model="form.user_id" filterable placeholder="搜索读者" style="width: 100%">
          <el-option v-for="u in readers" :key="u.id" :label="`${u.username} (${u.last_name}${u.first_name})`" :value="u.id" />
        </el-select>
      </el-form-item>
      <el-form-item label="图书" prop="book_id">
        <el-select v-model="form.book_id" filterable placeholder="搜索图书(ISBN/书名)" style="width: 100%">
          <el-option v-for="b in books" :key="b.id" :label="`${b.title} (${b.isbn})`" :value="b.id" :disabled="b.available_copies === 0" />
        </el-select>
      </el-form-item>
      <el-form-item label="备注">
        <el-input v-model="form.notes" type="textarea" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">确认借阅</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getBooks } from '@/api/books'
import { getUsers } from '@/api/users'
import { borrowBook } from '@/api/borrowing'
import { ElMessage } from 'element-plus'

const router = useRouter()
const formRef = ref()
const submitting = ref(false)
const readers = ref([])
const books = ref([])

const form = reactive({ user_id: '', book_id: '', notes: '' })
const rules = {
  user_id: [{ required: true, message: '请选择读者', trigger: 'change' }],
  book_id: [{ required: true, message: '请选择图书', trigger: 'change' }],
}

async function handleSubmit() {
  await formRef.value.validate()
  submitting.value = true
  try {
    await borrowBook(form)
    ElMessage.success('借阅成功')
    router.push('/borrowing')
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '借阅失败')
  } finally {
    submitting.value = false
  }
}

onMounted(async () => {
  try {
    const [usersRes, booksRes] = await Promise.all([
      getUsers({ page_size: 1000 }),
      getBooks({ page_size: 1000, status: 'available' }),
    ])
    readers.value = usersRes.data.results || usersRes.data
    books.value = booksRes.data.results || booksRes.data
  } catch {}
})
</script>
