<template>
  <div class="resource-recommend-container" :class="{ 'light-mode': isLightMode }">
    <div class="page-header">
      <h1>资源推荐</h1>
      <p>探索精选教学资源</p>
    </div>

    <div class="resource-filters">
      <el-select v-model="selectedSubject" placeholder="选择学科">
        <el-option v-for="item in subjects" :key="item" :label="item" :value="item"></el-option>
      </el-select>
      <el-select v-model="selectedGrade" placeholder="选择年级">
        <el-option v-for="item in grades" :key="item" :label="item" :value="item"></el-option>
      </el-select>
      <el-select v-model="selectedResourceType" placeholder="资源类型">
        <el-option v-for="item in resourceTypes" :key="item" :label="item" :value="item"></el-option>
      </el-select>
      <el-button type="primary" @click="searchResources">筛选</el-button>
    </div>

    <div class="resources-grid">
      <el-empty v-if="!resourcesList.length" description="暂无资源，请调整筛选条件"></el-empty>
      
      <el-card v-for="resource in resourcesList" :key="resource.id" class="resource-card">
        <template #header>
          <div class="resource-header">
            <span class="resource-title">{{ resource.title }}</span>
            <el-tag size="small" :type="getTagType(resource.type)">{{ resource.type }}</el-tag>
          </div>
        </template>
        
        <div class="resource-content">
          <div class="resource-info">
            <p><strong>学科：</strong>{{ resource.subject }}</p>
            <p><strong>年级：</strong>{{ resource.grade }}</p>
            <p><strong>上传者：</strong>{{ resource.uploader }}</p>
            <p><strong>上传时间：</strong>{{ formatDate(resource.uploadTime) }}</p>
            <p class="resource-description">{{ resource.description }}</p>
          </div>
          
          <div class="resource-actions">
            <el-button type="primary" @click="previewResource(resource)">预览</el-button>
            <el-button type="success" @click="downloadResource(resource)">下载</el-button>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 资源预览对话框 -->
    <el-dialog
      v-model="previewDialogVisible"
      title="资源预览"
      width="70%"
      :before-close="handleClose"
    >
      <div v-if="currentResource" class="preview-container">
        <h2>{{ currentResource.title }}</h2>
        
        <div class="preview-content">
          <iframe v-if="currentResource.type === '视频'" :src="currentResource.previewUrl" frameborder="0" allowfullscreen></iframe>
          <img v-else-if="currentResource.type === '图片'" :src="currentResource.previewUrl" alt="预览图片" />
          <div v-else class="document-preview">
            <p>此类型资源需要下载后查看</p>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted, onBeforeUnmount } from 'vue';
import { ElMessage } from 'element-plus';

export default {
  name: 'ResourceRecommend',
  setup() {
    // 添加夜间模式状态
    const isLightMode = ref(localStorage.getItem("theme-mode") === "light");

    const selectedSubject = ref('');
    const selectedGrade = ref('');
    const selectedResourceType = ref('');
    const resourcesList = ref([]);
    const previewDialogVisible = ref(false);
    const currentResource = ref(null);
    
    // 模拟数据
    const subjects = ['语文', '数学', '英语', '物理', '化学', '生物', '历史', '地理', '政治'];
    const grades = ['一年级', '二年级', '三年级', '四年级', '五年级', '六年级', '初一', '初二', '初三', '高一', '高二', '高三'];
    const resourceTypes = ['视频', '文档', '图片', 'PPT', '习题'];
    
    // 加载资源列表
    const loadResources = async () => {
      try {
        // 这里应该调用API获取资源列表
        // const response = await api.get('/resources', {
        //   params: {
        //     subject: selectedSubject.value,
        //     grade: selectedGrade.value,
        //     type: selectedResourceType.value
        //   }
        // });
        // resourcesList.value = response.data;
        
        // 模拟数据
        resourcesList.value = [
          {
            id: 1,
            title: '高中物理力学知识点总结',
            type: '文档',
            subject: '物理',
            grade: '高一',
            uploader: '王老师',
            uploadTime: '2023-06-15',
            description: '本资源包含高中物理力学部分的重要知识点和解题技巧，适合高一学生复习使用。',
            previewUrl: '#'
          },
          {
            id: 2,
            title: '初中英语语法大全',
            type: 'PPT',
            subject: '英语',
            grade: '初三',
            uploader: '李老师',
            uploadTime: '2023-05-20',
            description: '系统总结初中英语所有重要语法点，配有丰富例句和练习。',
            previewUrl: '#'
          },
          {
            id: 3,
            title: '小学数学思维训练视频课',
            type: '视频',
            subject: '数学',
            grade: '五年级',
            uploader: '张老师',
            uploadTime: '2023-07-01',
            description: '培养小学生数学思维能力的精品视频课程，通过生动有趣的例子讲解数学概念。',
            previewUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ'
          }
        ];
      } catch (error) {
        console.error('加载资源失败:', error);
        ElMessage.error('加载资源失败，请稍后重试');
      }
    };
    
    // 搜索资源
    const searchResources = () => {
      loadResources();
    };
    
    // 预览资源
    const previewResource = (resource) => {
      currentResource.value = resource;
      previewDialogVisible.value = true;
    };
    
    // 下载资源
    const downloadResource = (resource) => {
      // 实际应用中应调用API下载资源
      ElMessage.success(`开始下载: ${resource.title}`);
    };
    
    // 关闭预览对话框
    const handleClose = () => {
      previewDialogVisible.value = false;
      currentResource.value = null;
    };
    
    // 格式化日期
    const formatDate = (dateString) => {
      return dateString; // 简单实现，实际应用中可能需要更复杂的格式化
    };
    
    // 根据资源类型获取标签类型
    const getTagType = (type) => {
      const types = {
        '视频': 'danger',
        '文档': '',
        '图片': 'success',
        'PPT': 'warning',
        '习题': 'info'
      };
      return types[type] || '';
    };

    // 添加主题监听
    const checkThemeMode = () => {
      isLightMode.value = localStorage.getItem("theme-mode") === "light";
    };
    
    onMounted(() => {
      loadResources();
      
      // 添加主题监听
      checkThemeMode();
      window.addEventListener("storage", checkThemeMode);
      window.addEventListener("themeChange", checkThemeMode);
    });
    
    onBeforeUnmount(() => {
      // 移除主题监听
      window.removeEventListener("storage", checkThemeMode);
      window.removeEventListener("themeChange", checkThemeMode);
    });
    
    return {
      selectedSubject,
      selectedGrade,
      selectedResourceType,
      subjects,
      grades,
      resourceTypes,
      resourcesList,
      previewDialogVisible,
      currentResource,
      searchResources,
      previewResource,
      downloadResource,
      handleClose,
      formatDate,
      getTagType,
      isLightMode // 添加到返回值
    };
  }
}
</script>

<style scoped>
/* 夜间模式(默认) */
.resource-recommend-container {
  padding: 20px;
  height: 100%;
  overflow-y: auto;
  background-color: #0f1629;
  color: #e6ecf5;
  transition: background-color 0.3s, color 0.3s;
}

/* 日间模式 */
.resource-recommend-container.light-mode {
  background-color: #f0f5ff;
  color: #1a2980;
}

.page-header {
  margin-bottom: 24px;
}

.page-header h1 {
  font-size: 24px;
  margin-bottom: 8px;
  color: #64ffda; /* 夜间模式主色 */
  transition: color 0.3s;
}

.light-mode .page-header h1 {
  color: #26d0ce; /* 日间模式主色 */
}

.page-header p {
  color: #8a94b8; /* 夜间模式文本色 */
  font-size: 14px;
  transition: color 0.3s;
}

.light-mode .page-header p {
  color: #4b6cb7; /* 日间模式文本色 */
}

.resource-filters {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

/* 资源卡片 */
.resources-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.resource-card {
  transition: all 0.3s;
  height: 100%;
  background-color: #131b30; /* 夜间模式卡片背景 */
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.light-mode .resource-card {
  background-color: #ffffff;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.resource-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
}

.light-mode .resource-card:hover {
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.resource-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  padding-bottom: 10px;
  transition: border-color 0.3s;
}

.light-mode .resource-header {
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.resource-title {
  font-weight: bold;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 200px;
  color: #e6ecf5; /* 夜间模式文本色 */
  transition: color 0.3s;
}

.light-mode .resource-title {
  color: #1a2980; /* 日间模式文本色 */
}

.resource-content {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.resource-info {
  flex: 1;
  margin-bottom: 15px;
}

.resource-description {
  margin-top: 10px;
  color: #8a94b8; /* 夜间模式文本色 */
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  transition: color 0.3s;
}

.light-mode .resource-description {
  color: #4b6cb7; /* 日间模式文本色 */
}

.resource-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

/* 预览容器 */
.preview-container {
  padding: 10px;
}

.preview-container h2 {
  margin-bottom: 20px;
  text-align: center;
  color: #64ffda; /* 夜间模式主色 */
}

.light-mode .preview-container h2 {
  color: #26d0ce; /* 日间模式主色 */
}

.preview-content {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
  background-color: rgba(15, 22, 41, 0.3); /* 夜间模式背景色 */
}

.light-mode .preview-content {
  background-color: rgba(240, 245, 255, 0.5); /* 日间模式背景色 */
}

.preview-content iframe,
.preview-content img {
  max-width: 100%;
  max-height: 500px;
}

.document-preview {
  padding: 50px;
  text-align: center;
  background-color: rgba(15, 22, 41, 0.5); /* 夜间模式背景色 */
  border-radius: 4px;
}

.light-mode .document-preview {
  background-color: #f5f7fa; /* 日间模式背景色 */
}

/* 滚动条美化 */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: rgba(15, 22, 41, 0.2);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb {
  background: rgba(100, 255, 218, 0.2);
  border-radius: 3px;
  transition: background 0.3s;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(100, 255, 218, 0.3);
}

.light-mode ::-webkit-scrollbar-track {
  background: rgba(240, 245, 255, 0.5);
}

.light-mode ::-webkit-scrollbar-thumb {
  background: rgba(38, 208, 206, 0.2);
}

.light-mode ::-webkit-scrollbar-thumb:hover {
  background: rgba(38, 208, 206, 0.3);
}

/* Element Plus组件夜间模式样式 */
:deep(.el-select) {
  width: 100%;
}

:deep(.el-input__wrapper) {
  background-color: rgba(15, 22, 41, 0.4) !important;
  border: 1px solid rgba(100, 255, 218, 0.2) !important;
  box-shadow: none !important;
}

.light-mode :deep(.el-input__wrapper) {
  background-color: rgba(240, 245, 255, 0.5) !important;
  border: 1px solid rgba(38, 208, 206, 0.2) !important;
}

:deep(.el-input__wrapper.is-focus) {
  border-color: #64ffda !important;
  box-shadow: 0 0 0 2px rgba(100, 255, 218, 0.1) !important;
}

.light-mode :deep(.el-input__wrapper.is-focus) {
  border-color: #26d0ce !important;
  box-shadow: 0 0 0 2px rgba(38, 208, 206, 0.1) !important;
}

:deep(.el-input__inner) {
  color: #e6ecf5 !important;
}

.light-mode :deep(.el-input__inner) {
  color: #1a2980 !important;
}

:deep(.el-select__popper.el-popper) {
  background-color: #131b30 !important;
  border: 1px solid rgba(100, 255, 218, 0.2) !important;
}

.light-mode :deep(.el-select__popper.el-popper) {
  background-color: #ffffff !important;
  border: 1px solid rgba(38, 208, 206, 0.2) !important;
}

:deep(.el-select-dropdown__item) {
  color: #e6ecf5 !important;
}

:deep(.el-select-dropdown__item:hover) {
  background-color: rgba(100, 255, 218, 0.1) !important;
}

.light-mode :deep(.el-select-dropdown__item) {
  color: #1a2980 !important;
}

.light-mode :deep(.el-select-dropdown__item:hover) {
  background-color: rgba(38, 208, 206, 0.1) !important;
}

:deep(.el-select-dropdown__item.selected) {
  color: #64ffda !important;
  background-color: rgba(100, 255, 218, 0.1) !important;
}

.light-mode :deep(.el-select-dropdown__item.selected) {
  color: #26d0ce !important;
  background-color: rgba(38, 208, 206, 0.1) !important;
}

:deep(.el-tag) {
  background-color: rgba(15, 22, 41, 0.4) !important;
  border-color: rgba(100, 255, 218, 0.2) !important;
  color: #e6ecf5 !important;
}

.light-mode :deep(.el-tag) {
  background-color: rgba(240, 245, 255, 0.5) !important;
  border-color: rgba(38, 208, 206, 0.2) !important;
  color: #1a2980 !important;
}

/* 按钮样式 */
:deep(.el-button) {
  background: linear-gradient(135deg, #64ffda, #26d0ce) !important;
  color: #0f1629 !important;
  border: none !important;
  box-shadow: 0 4px 15px rgba(100, 255, 218, 0.3);
  transition: all 0.3s !important;
}

.light-mode :deep(.el-button) {
  box-shadow: 0 4px 15px rgba(38, 208, 206, 0.3);
}

:deep(.el-button:hover) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(100, 255, 218, 0.5);
}

/* 预览弹窗样式 */
:deep(.el-dialog) {
  background-color: #131b30 !important;
  border: 1px solid rgba(100, 255, 218, 0.1) !important;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3) !important;
}

.light-mode :deep(.el-dialog) {
  background-color: #ffffff !important;
biorder: 1px solid rgba(38, 208, 206, 0.1) !important;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1) !important;
}

:deep(.el-dialog__header) {
  border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
}

.light-mode :deep(.el-dialog__header) {
  border-bottom: 1px solid rgba(0, 0, 0, 0.05) !important;
}

:deep(.el-dialog__title) {
  color: #64ffda !important;
}

.light-mode :deep(.el-dialog__title) {
  color: #26d0ce !important;
}

:deep(.el-dialog__close) {
  color: #e6ecf5 !important;
}

.light-mode :deep(.el-dialog__close) {
  color: #1a2980 !important;
}

/* 空状态样式 */
:deep(.el-empty__description) {
  color: #8a94b8 !important;
}

.light-mode :deep(.el-empty__description) {
  color: #4b6cb7 !important;
}

:deep(.el-empty__image) {
  opacity: 0.5;
}

/* 修复下拉框样式问题 */
:deep(.el-select__wrapper),
:deep(.el-select__wrapper.el-tooltip__trigger) {
  background-color: rgba(15, 22, 41, 0.4) !important;
  border: 1px solid rgba(100, 255, 218, 0.2) !important;
  box-shadow: none !important;
  color: #e6ecf5 !important;
  transition: all 0.3s;
}

.light-mode :deep(.el-select__wrapper),
.light-mode :deep(.el-select__wrapper.el-tooltip__trigger) {
  background-color: rgba(240, 245, 255, 0.5) !important;
  border: 1px solid rgba(38, 208, 206, 0.2) !important;
  color: #1a2980 !important;
}

:deep(.el-select__wrapper:hover),
:deep(.el-select__wrapper.el-tooltip__trigger:hover) {
  border-color: rgba(100, 255, 218, 0.4) !important;
}

.light-mode :deep(.el-select__wrapper:hover),
.light-mode :deep(.el-select__wrapper.el-tooltip__trigger:hover) {
  border-color: rgba(38, 208, 206, 0.4) !important;
}

:deep(.el-select-dropdown) {
  background-color: #131b30 !important;
  border: 1px solid rgba(100, 255, 218, 0.2) !important;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3) !important;
}

.light-mode :deep(.el-select-dropdown) {
  background-color: #ffffff !important;
  border: 1px solid rgba(38, 208, 206, 0.2) !important;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1) !important;
}
</style>