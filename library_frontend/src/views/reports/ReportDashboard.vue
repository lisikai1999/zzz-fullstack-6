<template>
  <div>
    <div class="page-header">
      <h2>统计报表</h2>
    </div>

    <el-row :gutter="16" style="margin-bottom: 24px">
      <el-col :span="12">
        <el-card>
          <template #header>借阅趋势 (近12个月)</template>
          <div ref="trendChartRef" style="height: 320px"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>分类分布</template>
          <div ref="categoryChartRef" style="height: 320px"></div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="16" style="margin-bottom: 24px">
      <el-col :span="12">
        <el-card>
          <template #header>热门图书 Top 10</template>
          <div ref="topBooksRef" style="height: 320px"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>逾期统计</template>
          <div class="overdue-info">
            <div class="stat-card"><div class="value">{{ overdueStats.total_overdue }}</div><div class="label">逾期总数</div></div>
            <div class="stat-card"><div class="value" style="color:#e6a23c">{{ overdueStats.total_fine }}</div><div class="label">预计罚款(元)</div></div>
          </div>
          <div ref="overdueChartRef" style="height: 220px"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import * as echarts from 'echarts'
import { getBorrowingTrend, getCategoryStats, getTopBooks, getOverdueStats } from '@/api/reports'

const trendChartRef = ref(null)
const categoryChartRef = ref(null)
const topBooksRef = ref(null)
const overdueChartRef = ref(null)
const overdueStats = reactive({ total_overdue: 0, total_fine: 0 })

onMounted(async () => {
  try {
    const trendRes = await getBorrowingTrend()
    const chart1 = echarts.init(trendChartRef.value)
    const trendData = trendRes.data
    chart1.setOption({
      xAxis: { type: 'category', data: trendData.map(d => d.month?.substring(0, 7)) },
      yAxis: { type: 'value' },
      series: [{ data: trendData.map(d => d.count), type: 'line', smooth: true, areaStyle: {} }],
      tooltip: { trigger: 'axis' },
      grid: { left: 40, right: 20, bottom: 30, top: 20 },
    })
  } catch {}

  try {
    const catRes = await getCategoryStats()
    const chart2 = echarts.init(categoryChartRef.value)
    chart2.setOption({
      series: [{ type: 'pie', radius: ['40%', '70%'], data: catRes.data.map(d => ({ name: d.name, value: d.book_count })) }],
      tooltip: { trigger: 'item' },
    })
  } catch {}

  try {
    const topRes = await getTopBooks()
    const chart3 = echarts.init(topBooksRef.value)
    const topData = topRes.data.reverse()
    chart3.setOption({
      xAxis: { type: 'value' },
      yAxis: { type: 'category', data: topData.map(d => d.title.length > 10 ? d.title.substring(0, 10) + '...' : d.title) },
      series: [{ type: 'bar', data: topData.map(d => d.borrow_count) }],
      tooltip: { trigger: 'axis' },
      grid: { left: 100, right: 20, bottom: 30, top: 20 },
    })
  } catch {}

  try {
    const overdueRes = await getOverdueStats()
    Object.assign(overdueStats, overdueRes.data)
    const chart4 = echarts.init(overdueChartRef.value)
    const byDays = overdueRes.data.by_days || {}
    chart4.setOption({
      series: [{
        type: 'pie', radius: '60%',
        data: Object.entries(byDays).map(([name, value]) => ({ name, value })),
      }],
      tooltip: { trigger: 'item' },
    })
  } catch {}
})
</script>

<style scoped>
.overdue-info {
  display: flex;
  gap: 24px;
  margin-bottom: 12px;
}
</style>
