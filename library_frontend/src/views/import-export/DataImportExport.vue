<template>
  <div>
    <div class="page-header">
      <h2>数据导入导出</h2>
    </div>

    <el-tabs type="border-card">
      <el-tab-pane label="图书数据">
        <el-row :gutter="24">
          <el-col :span="12">
            <el-card>
              <template #header>导入图书</template>
              <el-upload
                ref="bookUploadRef"
                :auto-upload="false"
                :limit="1"
                accept=".xlsx,.xls"
                :on-change="handleBookFileChange"
              >
                <template #trigger>
                  <el-button type="primary">选择文件</el-button>
                </template>
              </el-upload>
              <el-button style="margin-top: 12px" type="success" :loading="importing" @click="handleImportBooks">
                开始导入
              </el-button>
              <el-button style="margin-top: 12px" @click="handleDownloadBookTemplate">下载模板</el-button>
              <div v-if="importResult" style="margin-top: 12px">
                <el-alert :title="`成功导入 ${importResult.created} 条，共 ${importResult.total_rows} 行`" type="success" />
                <div v-if="importResult.errors?.length" style="margin-top: 8px">
                  <el-alert v-for="(err, i) in importResult.errors" :key="i" :title="err" type="warning" :closable="false" />
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="12">
            <el-card>
              <template #header>导出图书</template>
              <p style="margin-bottom: 12px; color: #606266">导出所有图书数据为 Excel 文件</p>
              <el-button type="primary" :loading="exporting" @click="handleExportBooks">导出图书</el-button>
            </el-card>
          </el-col>
        </el-row>
      </el-tab-pane>

      <el-tab-pane label="读者数据" v-if="isAdmin">
        <el-row :gutter="24">
          <el-col :span="12">
            <el-card>
              <template #header>导入读者</template>
              <el-upload
                ref="readerUploadRef"
                :auto-upload="false"
                :limit="1"
                accept=".xlsx,.xls"
                :on-change="handleReaderFileChange"
              >
                <template #trigger>
                  <el-button type="primary">选择文件</el-button>
                </template>
              </el-upload>
              <el-button style="margin-top: 12px" type="success" :loading="importingReaders" @click="handleImportReaders">
                开始导入
              </el-button>
              <el-button style="margin-top: 12px" @click="handleDownloadReaderTemplate">下载模板</el-button>
              <div v-if="readerImportResult" style="margin-top: 12px">
                <el-alert :title="`成功导入 ${readerImportResult.created} 条`" type="success" />
                <div v-if="readerImportResult.errors?.length" style="margin-top: 8px">
                  <el-alert v-for="(err, i) in readerImportResult.errors" :key="i" :title="err" type="warning" :closable="false" />
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="12">
            <el-card>
              <template #header>导出读者</template>
              <p style="margin-bottom: 12px; color: #606266">导出所有读者数据为 Excel 文件</p>
              <el-button type="primary" :loading="exportingReaders" @click="handleExportReaders">导出读者</el-button>
            </el-card>
          </el-col>
        </el-row>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { exportBooks, importBooks, exportReaders, importReaders, downloadBookTemplate, downloadReaderTemplate } from '@/api/dataIO'
import { ElMessage } from 'element-plus'

const authStore = useAuthStore()
const isAdmin = computed(() => authStore.isAdmin)

const bookFile = ref(null)
const readerFile = ref(null)
const importing = ref(false)
const exporting = ref(false)
const importingReaders = ref(false)
const exportingReaders = ref(false)
const importResult = ref(null)
const readerImportResult = ref(null)

function handleBookFileChange(file) {
  bookFile.value = file.raw
}

function handleReaderFileChange(file) {
  readerFile.value = file.raw
}

function downloadBlob(data, filename) {
  const url = window.URL.createObjectURL(new Blob([data]))
  const link = document.createElement('a')
  link.href = url
  link.setAttribute('download', filename)
  document.body.appendChild(link)
  link.click()
  link.remove()
  window.URL.revokeObjectURL(url)
}

async function handleImportBooks() {
  if (!bookFile.value) {
    ElMessage.warning('请先选择文件')
    return
  }
  importing.value = true
  try {
    const res = await importBooks(bookFile.value)
    importResult.value = res.data
    ElMessage.success(`导入完成，成功 ${res.data.created} 条`)
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '导入失败')
  } finally {
    importing.value = false
  }
}

async function handleExportBooks() {
  exporting.value = true
  try {
    const res = await exportBooks()
    downloadBlob(res.data, 'books_export.xlsx')
    ElMessage.success('导出成功')
  } catch {
    ElMessage.error('导出失败')
  } finally {
    exporting.value = false
  }
}

async function handleImportReaders() {
  if (!readerFile.value) {
    ElMessage.warning('请先选择文件')
    return
  }
  importingReaders.value = true
  try {
    const res = await importReaders(readerFile.value)
    readerImportResult.value = res.data
    ElMessage.success(`导入完成，成功 ${res.data.created} 条`)
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '导入失败')
  } finally {
    importingReaders.value = false
  }
}

async function handleExportReaders() {
  exportingReaders.value = true
  try {
    const res = await exportReaders()
    downloadBlob(res.data, 'readers_export.xlsx')
    ElMessage.success('导出成功')
  } catch {
    ElMessage.error('导出失败')
  } finally {
    exportingReaders.value = false
  }
}

async function handleDownloadBookTemplate() {
  try {
    const res = await downloadBookTemplate()
    downloadBlob(res.data, 'books_template.xlsx')
  } catch {
    ElMessage.error('下载失败')
  }
}

async function handleDownloadReaderTemplate() {
  try {
    const res = await downloadReaderTemplate()
    downloadBlob(res.data, 'readers_template.xlsx')
  } catch {
    ElMessage.error('下载失败')
  }
}
</script>
