<template>
  <div class="bg content body">
    <div class="header-actions">
      <span class="user-role">当前身份: 管理员</span>
      <el-button type="danger" size="small" @click="handleLogout">退出登录</el-button>
    </div>
    <dv-full-screen-container>
      <!-- 标题 -->
      <moduleTitle />
      <!-- 第一行 -->
      <module-first />
      <!-- 第二行 -->
      <module-second />
    </dv-full-screen-container>
  </div>
</template>

<script setup>
import {ref,reactive} from "vue";
import moduleTitle from "./Charts/moduleTitle.vue";
import moduleFirst from "./Charts/moduleFirst.vue";
import moduleSecond from "./Charts/moduleSecond.vue"; 
import { logoutUser } from '@/api/auth';
import { ElMessage } from 'element-plus';
import { useRouter } from 'vue-router';

const router = useRouter();

const handleLogout = () => {
  logoutUser();
  ElMessage.success('退出登录成功');
  router.push('/');
};
</script>

<style scoped>
.header-actions {
  position: absolute;
  top: 10px;
  right: 20px;
  z-index: 1000;
  display: flex;
  align-items: center;
  gap: 15px;
}

.user-role {
  color: #40e0d0;
  font-size: 14px;
  text-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
}
</style>