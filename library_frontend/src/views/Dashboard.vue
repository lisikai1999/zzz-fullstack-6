<template>
  <div class="dashboard">
    <div class="stat-cards">
      <div class="stat-card">
        <div class="value">{{ stats.total_books }}</div>
        <div class="label">图书总数</div>
      </div>
      <div class="stat-card">
        <div class="value">{{ stats.total_readers }}</div>
        <div class="label">读者总数</div>
      </div>
      <div class="stat-card">
        <div class="value">{{ stats.active_borrows }}</div>
        <div class="label">当前借出</div>
      </div>
      <div class="stat-card" :class="{ warning: stats.overdue_count > 0 }">
        <div class="value">{{ stats.overdue_count }}</div>
        <div class="label">逾期未还</div>
      </div>
      <div class="stat-card">
        <div class="value">{{ stats.total_categories }}</div>
        <div class="label">图书分类</div>
      </div>
      <div class="stat-card">
        <div class="value">{{ stats.returned_today }}</div>
        <div class="label">今日归还</div>
      </div>
    </div>

    <el-row :gutter="16" v-if="isAdminOrLibrarian">
      <el-col :span="12">
        <el-card>
          <template #header>借阅趋势</template>
          <div ref="trendChart" style="height: 300px"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>分类分布</template>
          <div ref="categoryChart" style="height: 300px"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { getDashboard, getBorrowingTrend, getCategoryStats } from '@/api/reports'
import * as echarts from 'echarts'

const authStore = useAuthStore()
const isAdminOrLibrarian = computed(() => authStore.isAdminOrLibrarian)

const stats = reactive({
  total_books: 0,
  total_readers: 0,
  active_borrows: 0,
  overdue_count: 0,
  total_categories: 0,
  returned_today: 0,
})

const trendChart = ref(null)
const categoryChart = ref(null)

onMounted(async () => {
  if (!isAdminOrLibrarian.value) return
  try {
    const res = await getDashboard()
    Object.assign(stats, res.data)
  } catch {}

  try {
    const trendRes = await getBorrowingTrend()
    if (trendChart.value) {
      const chart = echarts.init(trendChart.value)
      const data = trendRes.data
      chart.setOption({
        xAxis: {
          type: 'category',
          data: data.map(d => d.month?.substring(0, 7) || ''),
        },
        yAxis: { type: 'value' },
        series: [{ data: data.map(d => d.count), type: 'line', smooth: true, areaStyle: {} }],
        tooltip: { trigger: 'axis' },
      })
    }
  } catch {}

  try {
    const catRes = await getCategoryStats()
    if (categoryChart.value) {
      const chart = echarts.init(categoryChart.value)
      chart.setOption({
        series: [{
          type: 'pie',
          radius: ['40%', '70%'],
          data: catRes.data.map(d => ({ name: d.name, value: d.book_count })),
        }],
        tooltip: { trigger: 'item' },
      })
    }
  } catch {}
})
</script>

<style scoped>
.dashboard {
  padding: 0;
}
.stat-card.warning .value {
  color: #e6a23c;
}
</style>
