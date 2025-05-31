<template>
  <div class="redirect-loading">
    <p>正在跳转到资源推荐系统...</p>
  </div>
</template>

<script>
export default {
  name: 'ExternalRedirect',
  created() {
    // 在组件创建时直接跳转到外部URL
    window.location.href = '/api/recommend/login';
  }
}
</script>

<style scoped>
.redirect-loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  font-size: 16px;
  color: #666;
}
</style>
