<template>
  <div class="datav-container">
    <dv-full-screen-container>
      <!-- 头部装饰 -->
      <div class="header">
        <dv-decoration-8 :color="['#568aea', '#1c4683']" style="width:200px;height:30px;" />
        <dv-decoration-8 :reverse="true" :color="['#568aea', '#1c4683']" style="width:200px;height:30px;" />
      </div>
      
      <!-- 主体内容区域 -->
      <div class="main-content">
        <!-- 大屏边框装饰 -->
        <dv-border-box-11 title="教师数据可视化大屏" :color="['#564aa5', '#1a98f3']" class="dashboard-wrapper">
          <router-view />
        </dv-border-box-11>
      </div>
      
      <!-- 底部装饰 -->
      <div class="footer">
        <dv-decoration-5 style="width:100%;height:20px;" />
      </div>
    </dv-full-screen-container>
  </div>
</template>

<script>
export default {
  name: 'DataVContainer'
}
</script>

<style scoped>
.datav-container {
  width: 100%;
  height: 100vh;
  background-color: #030929;
  background-image: radial-gradient(at 50% 50%, #04105d 0%, #030929 100%);
  color: #fff;
  overflow: hidden;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 5px 20px;
  height: 40px;
  box-sizing: border-box;
}

.main-content {
  padding: 0 20px;
  height: calc(100vh - 70px);
  box-sizing: border-box;
}

.dashboard-wrapper {
  width: 100%;
  height: 100%;
}

.footer {
  height: 20px;
  padding: 0 20px;
  box-sizing: border-box;
}

:deep(.dv-border-box-11-title) {
  font-size: 24px !important;
  font-weight: bold;
}

:deep(.dv-full-screen-container) {
  transform-origin: left top;
  z-index: 999;
}
</style> 