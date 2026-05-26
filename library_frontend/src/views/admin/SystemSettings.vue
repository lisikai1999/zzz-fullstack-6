<template>
  <div>
    <div class="page-header">
      <h2>系统设置 - 借阅配置</h2>
      <el-button type="primary" @click="showAdd">新增配置</el-button>
    </div>

    <el-table :data="configs" v-loading="loading" stripe>
      <el-table-column label="会员类型" width="120">
        <template #default="{ row }">{{ membershipMap[row.membership_type] || row.membership_type }}</template>
      </el-table-column>
      <el-table-column prop="max_borrow_days" label="最大借阅天数" width="130" align="center" />
      <el-table-column prop="max_renew_times" label="最大续借次数" width="130" align="center" />
      <el-table-column prop="fine_per_day" label="每日罚款(元)" width="130" align="center" />
      <el-table-column prop="max_borrow_count" label="最大借阅数量" width="130" align="center" />
      <el-table-column label="操作" width="100">
        <template #default="{ row }">
          <el-button text type="primary" @click="showEdit(row)">编辑</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" :title="editingId ? '编辑配置' : '新增配置'" width="500px">
      <el-form :model="form" label-width="120px">
        <el-form-item label="会员类型">
          <el-select v-model="form.membership_type" :disabled="!!editingId">
            <el-option label="标准" value="standard" />
            <el-option label="高级" value="premium" />
            <el-option label="学生" value="student" />
          </el-select>
        </el-form-item>
        <el-form-item label="最大借阅天数">
          <el-input-number v-model="form.max_borrow_days" :min="1" />
        </el-form-item>
        <el-form-item label="最大续借次数">
          <el-input-number v-model="form.max_renew_times" :min="0" />
        </el-form-item>
        <el-form-item label="每日罚款(元)">
          <el-input-number v-model="form.fine_per_day" :min="0" :step="0.1" :precision="2" />
        </el-form-item>
        <el-form-item label="最大借阅数量">
          <el-input-number v-model="form.max_borrow_count" :min="1" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getBorrowingConfigs, createBorrowingConfig, updateBorrowingConfig } from '@/api/borrowing'
import { ElMessage } from 'element-plus'

const configs = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const editingId = ref(null)
const membershipMap = { standard: '标准', premium: '高级', student: '学生' }

const form = reactive({
  membership_type: 'standard',
  max_borrow_days: 30,
  max_renew_times: 2,
  fine_per_day: 0.5,
  max_borrow_count: 5,
})

async function fetchConfigs() {
  loading.value = true
  try {
    const res = await getBorrowingConfigs()
    configs.value = res.data.results || res.data
  } catch {} finally {
    loading.value = false
  }
}

function showAdd() {
  editingId.value = null
  Object.assign(form, { membership_type: 'standard', max_borrow_days: 30, max_renew_times: 2, fine_per_day: 0.5, max_borrow_count: 5 })
  dialogVisible.value = true
}

function showEdit(row) {
  editingId.value = row.id
  Object.assign(form, row)
  dialogVisible.value = true
}

async function handleSave() {
  try {
    if (editingId.value) {
      await updateBorrowingConfig(editingId.value, form)
    } else {
      await createBorrowingConfig(form)
    }
    ElMessage.success('保存成功')
    dialogVisible.value = false
    fetchConfigs()
  } catch (e) {
    ElMessage.error('保存失败')
  }
}

onMounted(fetchConfigs)
</script>
