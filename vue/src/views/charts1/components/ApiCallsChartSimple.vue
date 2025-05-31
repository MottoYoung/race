<template>
  <div class="simple-chart">
    <div class="chart-placeholder">
      <div class="chart-icon">📊</div>
      <div class="chart-text">API调用数据统计</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ApiCallsChartSimple'
}
</script>

<style scoped>
.simple-chart {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background: rgba(3, 19, 57, 0.5);
  border-radius: 6px;
}

.chart-placeholder {
  text-align: center;
}

.chart-icon {
  font-size: 40px;
  margin-bottom: 10px;
}

.chart-text {
  font-size: 16px;
  font-weight: bold;
  color: rgba(54, 209, 220, 0.8);
}
</style> 