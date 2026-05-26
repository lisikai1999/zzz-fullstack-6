<template>
  <div>
    <div class="page-header">
      <h2>{{ isEdit ? '编辑图书' : '新增图书' }}</h2>
      <el-button @click="$router.back()">返回</el-button>
    </div>

    <el-form ref="formRef" :model="form" :rules="rules" label-width="100px" style="max-width: 700px">
      <el-form-item label="ISBN" prop="isbn">
        <el-input v-model="form.isbn" />
      </el-form-item>
      <el-form-item label="书名" prop="title">
        <el-input v-model="form.title" />
      </el-form-item>
      <el-form-item label="作者" prop="author">
        <el-input v-model="form.author" />
      </el-form-item>
      <el-form-item label="出版社">
        <el-input v-model="form.publisher" />
      </el-form-item>
      <el-form-item label="出版日期">
        <el-date-picker v-model="form.publish_date" type="date" value-format="YYYY-MM-DD" />
      </el-form-item>
      <el-form-item label="分类">
        <el-select v-model="form.category_ids" multiple placeholder="选择分类">
          <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.id" />
        </el-select>
      </el-form-item>
      <el-form-item label="总册数">
        <el-input-number v-model="form.total_copies" :min="1" />
      </el-form-item>
      <el-form-item label="可借册数">
        <el-input-number v-model="form.available_copies" :min="0" :max="form.total_copies" />
      </el-form-item>
      <el-form-item label="馆藏位置">
        <el-input v-model="form.location" />
      </el-form-item>
      <el-form-item label="简介">
        <el-input v-model="form.description" type="textarea" :rows="4" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">{{ isEdit ? '保存' : '创建' }}</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getBook, createBook, updateBook, getCategories } from '@/api/books'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const isEdit = computed(() => !!route.params.id)
const formRef = ref()
const submitting = ref(false)
const categories = ref([])

const form = reactive({
  isbn: '',
  title: '',
  author: '',
  publisher: '',
  publish_date: '',
  category_ids: [],
  total_copies: 1,
  available_copies: 1,
  location: '',
  description: '',
})

const rules = {
  isbn: [{ required: true, message: '请输入ISBN', trigger: 'blur' }],
  title: [{ required: true, message: '请输入书名', trigger: 'blur' }],
  author: [{ required: true, message: '请输入作者', trigger: 'blur' }],
}

async function fetchCategories() {
  try {
    const res = await getCategories()
    categories.value = res.data.results || res.data
  } catch {}
}

async function handleSubmit() {
  await formRef.value.validate()
  submitting.value = true
  try {
    if (isEdit.value) {
      await updateBook(route.params.id, form)
      ElMessage.success('保存成功')
    } else {
      await createBook(form)
      ElMessage.success('创建成功')
    }
    router.push('/books')
  } catch (e) {
    ElMessage.error(e.response?.data?.isbn?.[0] || '操作失败')
  } finally {
    submitting.value = false
  }
}

onMounted(async () => {
  fetchCategories()
  if (isEdit.value) {
    const res = await getBook(route.params.id)
    Object.assign(form, {
      ...res.data,
      category_ids: res.data.categories?.map(c => c.id) || [],
    })
  }
})
</script>
