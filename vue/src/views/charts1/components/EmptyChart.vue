<template>
  <div class="empty-chart">
    <div class="chart-error-message">
      <div class="error-icon">!</div>
      <div class="error-text">图表加载失败</div>
      <div class="error-details">请尝试刷新页面或联系管理员</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EmptyChart'
}
</script>

<style scoped>
.empty-chart {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background: rgba(3, 19, 57, 0.5);
  border-radius: 6px;
}

.chart-error-message {
  text-align: center;
}

.error-icon {
  width: 40px;
  height: 40px;
  margin: 0 auto 10px;
  background: rgba(255, 110, 118, 0.2);
  border: 1px solid rgba(255, 110, 118, 0.5);
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 24px;
  font-weight: bold;
  color: #ff6e76;
}

.error-text {
  font-size: 16px;
  font-weight: bold;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 5px;
}

.error-details {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.5);
}
</style> 