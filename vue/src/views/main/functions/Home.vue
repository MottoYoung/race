<template>
  <div class="home-container" :class="{ 'light-mode': isLightMode }">
    <!-- 顶部横幅 -->
    <div class="banner-section">
      <h1 class="banner-title">AI教育助手</h1>
      <p class="banner-desc">智能辅助教学，提升教学效率</p>
      
      <div class="search-container">
        <el-input
          placeholder="搜索您需要的内容..."
          class="search-input"
          v-model="searchText"
          clearable
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
      </div>
      
      <div class="quick-links">
        <span class="quick-link" @click="navigateTo('prepare')">AI生成PPT</span>
        <span class="quick-link" @click="navigateTo('image')">智能对话</span>
        <span class="quick-link" @click="navigateTo('exercise')">文章创作</span>
      </div>
    </div>

    <!-- 主要功能区 - 8个按钮 -->
    <div class="ai-functions">
      <h2 class="section-title">AI创作中心</h2>
      
      <div class="function-grid">
        <!-- 第一行 -->
        <div class="function-card" @click="navigateTo('analysis')">
          <div class="function-icon">
            <el-icon><DataAnalysis /></el-icon>
          </div>
          <div class="function-content">
            <h3>学情分析</h3>
            <p>智能分析学习情况</p>
          </div>
        </div>
        
        <div class="function-card" @click="navigateTo('image')">
          <div class="function-icon">
            <el-icon><PictureFilled /></el-icon>
          </div>
          <div class="function-content">
            <h3>图像生成</h3>
            <p>智能创作图像内容</p>
          </div>
        </div>
        
        <div class="function-card" @click="navigateTo('PPT')">
          <div class="function-icon">
            <el-icon><Files /></el-icon>
          </div>
          <div class="function-content">
            <h3>PPT设计</h3>
            <p>智能生成精美PPT</p>
          </div>
        </div>
        
        <div class="function-card" @click="navigateTo('resource')">
          <div class="function-icon">
            <el-icon><VideoPlay /></el-icon>
          </div>
          <div class="function-content">
            <h3>视频制作</h3>
            <p>快速生成教学视频</p>
          </div>
        </div>
        
        <!-- 第二行 -->
        <div class="function-card" @click="navigateTo('prepare')">
          <div class="function-icon">
            <el-icon><Management /></el-icon>
          </div>
          <div class="function-content">
            <h3>个性化资源</h3>
            <p>智能推荐教学资源</p>
          </div>
        </div>
        
        <div class="function-card" @click="navigateTo('exercise')">
          <div class="function-icon">
            <el-icon><Reading /></el-icon>
          </div>
          <div class="function-content">
            <h3>试题生成</h3>
            <p>快速创建测验题目</p>
          </div>
        </div>
        
        <div class="function-card" @click="navigateTo('prepare')">
          <div class="function-icon">
            <el-icon><Notebook /></el-icon>
          </div>
          <div class="function-content">
            <h3>教案设计</h3>
            <p>智能生成教学方案</p>
          </div>
        </div>
        
        <div class="function-card" @click="navigateTo('resource')">
          <div class="function-icon">
            <el-icon><MoreFilled /></el-icon>
          </div>
          <div class="function-content">
            <h3>更多AI能力</h3>
            <p>更多新能力，敬请期待</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 精品内容区 -->
    <div class="content-rankings">
      <div class="ranking-tabs">
        <div class="tab-item active">精品内容榜</div>
        <div class="tab-item">专业作者榜</div>
        <div class="tab-item">权威机构榜</div>
      </div>
      
      <div class="ranking-content">
        <div class="ranking-category">
          <div class="category-header">
            <h3>教育</h3>
            <span class="more-link">更多 <el-icon><ArrowRight /></el-icon></span>
          </div>
          
          <div class="ranking-list">
            <div class="ranking-item">
              <span class="rank-number">1</span>
              <span class="item-title">武汉市2025届高中毕业生三月调研考试 数学试卷</span>
              <span class="view-count">25,447 次阅读</span>
            </div>
            
            <div class="ranking-item">
              <span class="rank-number">2</span>
              <span class="item-title">2025届高考考作文素材：《题记2》作文素材</span>
              <span class="view-count">12,557 次阅读</span>
            </div>
            
            <div class="ranking-item">
              <span class="rank-number">3</span>
              <span class="item-title">人教版2025-2026学年七年级历史下册教学计划</span>
              <span class="view-count">9,807 次阅读</span>
            </div>
          </div>
        </div>
        
        <div class="ranking-category">
          <div class="category-header">
            <h3>法律</h3>
            <span class="more-link">更多 <el-icon><ArrowRight /></el-icon></span>
          </div>
          
          <div class="ranking-list">
            <div class="ranking-item">
              <span class="rank-number">1</span>
              <span class="item-title">正当防卫、防卫过当的司法认定(案例)</span>
              <span class="view-count">17,337 次阅读</span>
            </div>
            
            <div class="ranking-item">
              <span class="rank-number">2</span>
              <span class="item-title">预内财产协议书范本(共5篇)</span>
              <span class="view-count">14,947 次阅读</span>
            </div>
            
            <div class="ranking-item">
              <span class="rank-number">3</span>
              <span class="item-title">房屋交接确认书</span>
              <span class="view-count">13,927 次阅读</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import {
  Search,
  Files,
  PictureFilled,
  MoreFilled,
  ArrowRight,
  DataAnalysis,
  Management,
  Reading,
  VideoPlay,
  Notebook
} from "@element-plus/icons-vue";

export default {
  name: 'HomeView',
  components: {
    Search,
    Files,
    PictureFilled,
    MoreFilled,
    ArrowRight,
    DataAnalysis,
    Management,
    Reading,
    VideoPlay,
    Notebook
  },
  setup() {
    const searchText = ref('');
    const isLightMode = ref(false);
    const router = useRouter();
    
    const checkThemeMode = () => {
      isLightMode.value = localStorage.getItem("theme-mode") === "light";
    };
    
    const navigateTo = (path) => {
      router.push({ path: `/main/${path}` });
    };
    
    onMounted(() => {
      checkThemeMode();
      window.addEventListener("storage", checkThemeMode);
      window.addEventListener("themeChange", checkThemeMode);
    });
    
    onBeforeUnmount(() => {
      window.removeEventListener("storage", checkThemeMode);
      window.removeEventListener("themeChange", checkThemeMode);
    });
    
    return {
      searchText,
      isLightMode,
      navigateTo
    };
  }
};
</script>

<style scoped>
.home-container {
  height: 100%;
  width: 100%;
  overflow-y: auto;
  background-color: #2d2339; /* 更新为深紫色背景 */
  color: #e6ecf5;
  transition: background-color 0.3s, color 0.3s;
  padding-bottom: 40px;
}

.light-mode {
  background-color: #fff9f0; /* 更新为温暖米色背景 */
  color: #593618; /* 深棕色文字 */
}

/* 顶部横幅 */
.banner-section {
  background: linear-gradient(135deg, #352941, #5e3a6e); /* 深紫色渐变 */
  padding: 40px 20px;
  margin-bottom: 40px;
  text-align: center;
  border-radius: 0 0 20px 20px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.light-mode .banner-section {
  background: linear-gradient(135deg, #f4a259, #f7cb87); /* 橙金色渐变 */
}

.banner-title {
  font-size: 36px;
  font-weight: 700;
  color: white;
  margin-bottom: 10px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.banner-desc {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 30px;
}

.search-container {
  max-width: 600px;
  margin: 0 auto 20px;
}

.search-input {
  width: 100%;
  border-radius: 30px;
  overflow: hidden;
}

:deep(.el-input__wrapper) {
  padding: 0 15px;
  border-radius: 30px;
  background-color: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

:deep(.el-input__inner) {
  height: 44px;
  color: white;
}

:deep(.el-input__inner::placeholder) {
  color: rgba(255, 255, 255, 0.7);
}

.light-mode :deep(.el-input__wrapper) {
  background-color: rgba(255, 255, 255, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.light-mode :deep(.el-input__inner) {
  color: #593618; /* 深棕色文字 */
}

.light-mode :deep(.el-input__inner::placeholder) {
  color: rgba(89, 54, 24, 0.7); /* 半透明深棕色 */
}

.quick-links {
  display: flex;
  justify-content: center;
  gap: 30px;
  flex-wrap: wrap;
}

.quick-link {
  color: white;
  background-color: rgba(255, 255, 255, 0.15);
  padding: 8px 16px;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 14px;
}

.quick-link:hover {
  background-color: rgba(255, 158, 94, 0.3); /* 半透明橙色 */
  transform: translateY(-2px);
}

.light-mode .quick-link {
  background-color: rgba(89, 54, 24, 0.1); /* 半透明深棕色 */
  color: #593618;
}

.light-mode .quick-link:hover {
  background-color: rgba(216, 101, 0, 0.2); /* 半透明深橙色 */
}

@media (max-width: 768px) {
  .banner-title {
    font-size: 28px;
  }
  
  .banner-desc {
    font-size: 14px;
    margin-bottom: 20px;
  }
  
  .quick-links {
    gap: 15px;
  }
}

@media (max-width: 480px) {
  .banner-title {
    font-size: 24px;
  }
  
  .quick-link {
    padding: 6px 12px;
    font-size: 12px;
  }
}

/* 功能区样式 */
.ai-functions {
  max-width: 1200px;
  margin: 0 auto 40px;
  padding: 0 20px;
}

.section-title {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 30px;
  color: #ff9e5e; /* 橙色标题 */
  display: flex;
  align-items: center;
}

.light-mode .section-title {
  color: #d86500; /* 深橙色标题 */
}

.function-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-template-rows: repeat(2, auto);
  gap: 24px;
  margin-bottom: 40px;
}

.function-card {
  background-color: rgba(45, 35, 57, 0.8); /* 半透明深紫色 */
  border-radius: 16px;
  padding: 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s;
  border: 1px solid rgba(255, 158, 94, 0.1); /* 橙色边框 */
  text-align: center;
  height: 100%;
}

.light-mode .function-card {
  background-color: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(244, 162, 89, 0.2); /* 金黄色边框 */
}

.function-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
  border-color: rgba(255, 158, 94, 0.3); /* 深一点的橙色边框 */
}

.light-mode .function-card:hover {
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.08);
  border-color: rgba(216, 101, 0, 0.3); /* 深橙色边框 */
}

.function-icon {
  font-size: 32px;
  color: #ff9e5e; /* 橙色图标 */
  background-color: rgba(255, 158, 94, 0.1); /* 半透明橙色背景 */
  width: 70px;
  height: 70px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
  transition: all 0.3s;
}

.light-mode .function-icon {
  color: #d86500; /* 深橙色图标 */
  background-color: rgba(244, 162, 89, 0.1); /* 半透明金黄色背景 */
}

.function-card:hover .function-icon {
  background-color: rgba(255, 158, 94, 0.2); /* 深一点的半透明橙色背景 */
  transform: scale(1.1);
}

.light-mode .function-card:hover .function-icon {
  background-color: rgba(244, 162, 89, 0.2); /* 深一点的半透明金黄色背景 */
}

.function-content h3 {
  font-size: 18px;
  margin-bottom: 8px;
  font-weight: 500;
}

.function-content p {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.6);
  line-height: 1.4;
}

.light-mode .function-content p {
  color: rgba(89, 54, 24, 0.6); /* 半透明深棕色 */
}

@media (max-width: 992px) {
  .function-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
  }
}

@media (max-width: 576px) {
  .function-grid {
    grid-template-columns: 1fr;
  }
  
  .function-card {
    padding: 20px;
  }
  
  .function-icon {
    width: 60px;
    height: 60px;
    font-size: 28px;
  }
}

/* 内容排行榜 */
.content-rankings {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.ranking-tabs {
  display: flex;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  margin-bottom: 20px;
}

.light-mode .ranking-tabs {
  border-bottom: 1px solid rgba(89, 54, 24, 0.1); /* 半透明深棕色 */
}

.tab-item {
  padding: 12px 20px;
  font-size: 16px;
  cursor: pointer;
  position: relative;
  color: rgba(255, 255, 255, 0.7);
}

.light-mode .tab-item {
  color: rgba(89, 54, 24, 0.7); /* 半透明深棕色 */
}

.tab-item.active {
  color: #ff9e5e; /* 橙色 */
  font-weight: 500;
}

.light-mode .tab-item.active {
  color: #d86500; /* 深橙色 */
}

.tab-item.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 20%;
  width: 60%;
  height: 3px;
  background-color: #ff9e5e; /* 橙色 */
  border-radius: 3px 3px 0 0;
}

.light-mode .tab-item.active::after {
  background-color: #d86500; /* 深橙色 */
}

.ranking-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
}

.category-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.category-header h3 {
  font-size: 20px;
  font-weight: 500;
}

.more-link {
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 5px;
  cursor: pointer;
}

.light-mode .more-link {
  color: rgba(89, 54, 24, 0.6); /* 半透明深棕色 */
}

.more-link:hover {
  color: #ff9e5e; /* 橙色 */
}

.light-mode .more-link:hover {
  color: #f4a259; /* 金黄色 */
}

.ranking-list {
  background-color: rgba(61, 45, 78, 0.5); /* 半透明紫色背景 */
  border-radius: 12px;
  overflow: hidden;
}

.light-mode .ranking-list {
  background-color: rgba(255, 255, 255, 0.6);
}

.ranking-item {
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  transition: background-color 0.3s;
  cursor: pointer;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.light-mode .ranking-item {
  border-bottom: 1px solid rgba(89, 54, 24, 0.05); /* 半透明深棕色 */
}

.ranking-item:last-child {
  border-bottom: none;
}

.ranking-item:hover {
  background-color: rgba(255, 255, 255, 0.05);
}

.light-mode .ranking-item:hover {
  background-color: rgba(244, 162, 89, 0.05); /* 半透明金黄色 */
}

.rank-number {
  font-size: 16px;
  font-weight: 600;
  color: #ff9e5e; /* 橙色 */
  width: 24px;
  height: 24px;
  background-color: rgba(255, 158, 94, 0.1); /* 半透明橙色背景 */
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.light-mode .rank-number {
  color: #d86500; /* 深橙色 */
  background-color: rgba(244, 162, 89, 0.1); /* 半透明金黄色背景 */
}

.item-title {
  flex: 1;
  font-size: 14px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.view-count {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.5);
  white-space: nowrap;
}

.light-mode .view-count {
  color: rgba(89, 54, 24, 0.5); /* 半透明深棕色 */
}

@media (max-width: 768px) {
  .ranking-content {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .quick-actions {
    gap: 12px;
  }
  
  .tab-item {
    padding: 10px 15px;
    font-size: 14px;
  }
}
</style>