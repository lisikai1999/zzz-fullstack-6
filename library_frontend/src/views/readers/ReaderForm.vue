<template>
  <div>
    <div class="page-header">
      <h2>{{ isEdit ? '编辑读者' : '新增读者' }}</h2>
      <el-button @click="$router.back()">返回</el-button>
    </div>

    <el-form ref="formRef" :model="form" :rules="rules" label-width="100px" style="max-width: 600px">
      <el-form-item label="用户名" prop="username">
        <el-input v-model="form.username" :disabled="isEdit" />
      </el-form-item>
      <el-form-item label="姓" prop="last_name">
        <el-input v-model="form.last_name" />
      </el-form-item>
      <el-form-item label="名" prop="first_name">
        <el-input v-model="form.first_name" />
      </el-form-item>
      <el-form-item label="邮箱">
        <el-input v-model="form.email" />
      </el-form-item>
      <el-form-item label="电话">
        <el-input v-model="form.phone" />
      </el-form-item>
      <el-form-item label="会员类型">
        <el-select v-model="form.membership_type">
          <el-option label="标准" value="standard" />
          <el-option label="高级" value="premium" />
          <el-option label="学生" value="student" />
        </el-select>
      </el-form-item>
      <el-form-item label="借书证号">
        <el-input v-model="form.id_card" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleSubmit">保存</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const isEdit = computed(() => !!route.params.id)
const formRef = ref()

const form = reactive({
  username: '',
  last_name: '',
  first_name: '',
  email: '',
  phone: '',
  membership_type: 'standard',
  id_card: '',
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
}

function handleSubmit() {
  ElMessage.info('功能开发中')
}
</script>
