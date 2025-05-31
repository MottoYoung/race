<template>
  <div id="app" class="ppt-generator" :class="{ 'light-mode': isLightMode }">
    <!-- 新的标题设计 -->
    <div class="title-section">
      <h2 class="gradient-title">
        一键生成<span class="ppt-text">PPT</span
        ><span class="star-icon">✨</span>
      </h2>
      <p class="subtitle">支持导入文档、利用个性化模板创作PPT</p>
    </div>

    <!-- 内容输入区 (置于顶部) -->
    <div class="main-content">
      <!-- 文件上传与文本输入区域 -->
      <div class="input-area">
        <div class="input-container">
          <!-- 如果有文件，显示文件信息 -->
          <div class="file-upload-container" v-if="selectedFile">
            <div class="file-info">
              <i class="file-icon">📄</i>
              <span class="file-name-display">{{ selectedFile.name }}</span>
              <button class="clear-file-btn" @click="clearFile">×</button>
            </div>
          </div>

          <!-- 如果没有文件，显示文本输入框 -->
          <textarea
            v-if="!selectedFile"
            v-model="description"
            placeholder="试试输入一点点的小小的需求即可生成PPT"
          ></textarea>

          <div class="input-actions">
            <div class="action-buttons">
              <input
                type="file"
                ref="fileInput"
                @change="handleFileUpload"
                accept=".pdf,.doc,.docx,.txt,.md"
                hidden
              />
              <button @click="triggerFileUpload" class="action-btn upload-btn">
                <i class="action-icon">📄</i
                >{{ selectedFile ? "重新上传" : "上传文档" }}
              </button>
            </div>
            <button
              class="create-btn"
              :disabled="
                loading || (!selectedFile && !description) || !selectedTemplate
              "
              @click="generatePPT"
            >
              {{ loading ? "生成中..." : "立即创作" }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 模板选择区域 (移到下方) -->
    <div class="template-section">
      <!-- 模板筛选区域 -->
      <div class="section-header">
        <h3 class="section-title">选择模板</h3>
        <div class="filter-group">
          <select v-model="selectedStyle" @change="handleFilterChange">
            <option value="">所有风格</option>
            <option v-for="style in styleOptions" :key="style" :value="style">
              {{ style }}
            </option>
          </select>

          <select v-model="selectedColor" @change="handleFilterChange">
            <option value="">所有颜色</option>
            <option v-for="color in colorOptions" :key="color" :value="color">
              {{ color }}
            </option>
          </select>
        </div>
      </div>

      <div class="template-grid">
        <div v-if="loadingTemplates" class="loading-tip">模板加载中...</div>
        <div
          v-if="!loadingTemplates && templates.length === 0"
          class="empty-tip"
        >
          {{
            hasActiveFilters
              ? "当前筛选条件下暂无模板，请尝试其他条件"
              : "暂无可用模板"
          }}
          <span
            v-if="hasActiveFilters"
            class="clear-filter"
            @click="clearFilters"
          >
            （清空筛选条件）
          </span>
        </div>
        <div
          v-for="template in templates"
          :key="template.id"
          class="template-item"
          :class="{ selected: selectedTemplate === template.id }"
          @click="selectTemplate(template.id)"
        >
          <img
            :src="template.cover || '/default-cover.png'"
            :alt="template.name"
            class="template-cover"
            @error="handleImageError"
          />
          <div class="template-selected-indicator">
            <span class="checkmark">✓</span>
          </div>
        </div>
      </div>

      <!-- 分页控件 -->
      <div class="pagination">
        <button
          @click="changePage(1)"
          :disabled="currentPage === 1 || totalPages === 0"
        >
          首页
        </button>
        <button
          @click="changePage(currentPage - 1)"
          :disabled="currentPage === 1 || totalPages === 0"
        >
          上一页
        </button>

        <span
          v-for="page in visiblePages"
          :key="page"
          @click="changePage(page)"
          :class="{ active: currentPage === page }"
        >
          {{ page }}
        </span>

        <button
          @click="changePage(currentPage + 1)"
          :disabled="currentPage === totalPages || totalPages === 0"
        >
          下一页
        </button>
        <button
          @click="changePage(totalPages)"
          :disabled="currentPage === totalPages || totalPages === 0"
        >
          尾页
        </button>
      </div>
    </div>

    <!-- 结果展示 -->
    <div v-if="resultUrl" class="result">
      <p>生成完成！<a :href="resultUrl" download>点击下载PPT</a></p>
    </div>

    <!-- 错误提示 -->
    <div v-if="error" class="error">
      {{ error }}
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from "vue";
import axios from "axios";

export default {
  name: "App",
  setup() {
    // 配置axios基础路径
    axios.defaults.baseURL = "/api/ppt";

    // 响应式数据
    const description = ref("");
    const loading = ref(false);
    const resultUrl = ref("");
    const error = ref("");
    const selectedTemplate = ref(null);
    const templates = ref([]);
    const loadingTemplates = ref(true);
    const taskId = ref(null);
    const fileInput = ref(null);
    const selectedFile = ref(null);

    // 分页相关
    const currentPage = ref(1);
    const totalPages = ref(0);
    const pageSize = ref(8);

    // 筛选相关
    const selectedStyle = ref("");
    const selectedColor = ref("");
    const styleOptions = ref([
      "简约",
      "卡通",
      "商务",
      "创意",
      "国风",
      "清新",
      "扁平",
      "插画",
      "节日",
    ]);
    const colorOptions = ref([
      "蓝色",
      "绿色",
      "红色",
      "紫色",
      "黑色",
      "灰色",
      "黄色",
      "粉色",
      "橙色",
    ]);

    // 计算属性
    const visiblePages = computed(() => {
      if (totalPages.value <= 5) {
        return Array.from({ length: totalPages.value }, (_, i) => i + 1);
      }
      const start = Math.max(1, currentPage.value - 2);
      const end = Math.min(totalPages.value, currentPage.value + 2);
      return Array.from({ length: end - start + 1 }, (_, i) => start + i);
    });

    const hasActiveFilters = computed(() => {
      return selectedStyle.value || selectedColor.value;
    });

    // 方法
    const triggerFileUpload = () => {
      fileInput.value.click();
    };

    const handleFileUpload = (e) => {
      const files = e.target.files;
      if (files && files[0]) {
        selectedFile.value = files[0];
        description.value = "";
      } else {
        selectedFile.value = null;
      }
    };

    const fetchTemplates = async () => {
      try {
        loadingTemplates.value = true;
        templates.value = [];
        const response = await axios.get("/templates", {
          params: {
            currentPage: currentPage.value,
            pageSize: pageSize.value,
            style: selectedStyle.value,
            color: selectedColor.value,
          },
        });

        if (response.data.code === 0) {
          templates.value = response.data.data.list;
          totalPages.value = Math.ceil(
            response.data.data.total / pageSize.value
          );
        } else {
          error.value = "模板加载失败：" + response.data.error;
        }
      } catch (err) {
        error.value = `模板加载失败: ${err.message}`;
      } finally {
        loadingTemplates.value = false;
      }
    };

    const changePage = (newPage) => {
      newPage = Math.max(1, Math.min(newPage, totalPages.value));
      if (newPage !== currentPage.value) {
        currentPage.value = newPage;
        fetchTemplates();
      }
    };

    const handleImageError = (e) => {
      e.target.src = "/default-cover.png";
    };

    const selectTemplate = (templateId) => {
      selectedTemplate.value = templateId;
    };

    const handleFilterChange = () => {
      currentPage.value = 1;
      fetchTemplates();
    };

    const clearFilters = () => {
      selectedStyle.value = "";
      selectedColor.value = "";
      handleFilterChange();
    };

    const clearFile = () => {
      selectedFile.value = null;
      fileInput.value.value = "";
    };

    const checkStatus = async () => {
      try {
        const response = await axios.get(`/status/${taskId.value}`);
        const data = response.data.data;

        if (!data) throw new Error("无效的响应格式");
        if (
          data.pptStatus === "build_failed" ||
          data.aiImageStatus === "build_failed" ||
          data.cardNoteStatus === "build_failed"
        ) {
          throw new Error(data.errMsg || "PPT生成失败");
        }

        if (
          data.pptStatus === "done" &&
          data.aiImageStatus === "done" &&
          data.cardNoteStatus === "done"
        ) {
          resultUrl.value = data.pptUrl;
          loading.value = false;
        } else {
          setTimeout(checkStatus, 2000);
        }
      } catch (err) {
        error.value = `生成失败：${err.message}`;
        loading.value = false;
        taskId.value = null;
      }
    };

    const generatePPT = async () => {
      if (!selectedTemplate.value) {
        error.value = "请先选择模板";
        return;
      }

      try {
        loading.value = true;
        error.value = "";
        resultUrl.value = "";
        const formData = new FormData();
        formData.append("templateId", selectedTemplate.value);

        if (selectedFile.value) {
          formData.append("file", selectedFile.value);
          formData.append("fileName", selectedFile.value.name);
        } else {
          if (!description.value.trim()) {
            throw new Error("请输入内容描述或选择文件");
          }
          formData.append("query", description.value);
        }

        const response = await axios.post("/generate", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });

        if (response.data?.code === 0) {
          taskId.value = response.data.task_id;
          checkStatus();
        } else {
          error.value = response.data?.error || "生成请求失败";
          loading.value = false;
        }
      } catch (err) {
        error.value = `请求失败：${err.message}`;
        if (err.response) {
          error.value += ` (状态码：${err.response.status})`;
        }
        loading.value = false;
      }
    };

    onMounted(fetchTemplates);

    return {
      description,
      loading,
      resultUrl,
      error,
      templates,
      selectedTemplate,
      selectTemplate,
      loadingTemplates,
      visiblePages,
      currentPage,
      totalPages,
      changePage,
      handleImageError,
      selectedStyle,
      selectedColor,
      styleOptions,
      colorOptions,
      handleFilterChange,
      hasActiveFilters,
      clearFilters,
      fileInput,
      selectedFile,
      triggerFileUpload,
      handleFileUpload,
      generatePPT,
      clearFile,
    };
  },
  data() {
    return {
      isLightMode: localStorage.getItem("theme-mode") === "light",
    };
  },
  mounted() {
    this.checkThemeMode();
    window.addEventListener("storage", this.checkThemeMode);
    window.addEventListener("themeChange", this.checkThemeMode);
  },
  beforeUnmount() {
    window.removeEventListener("storage", this.checkThemeMode);
    window.removeEventListener("themeChange", this.checkThemeMode);
  },
  methods: {
    checkThemeMode() {
      this.isLightMode = localStorage.getItem("theme-mode") === "light";
    },
  },
};
</script>

<style scoped>
/* 确保占满整个可用空间 */
:deep(.el-card__body) {
  height: 100%;
  padding: 0 !important;
  background: #2d2339; /* 更改为深紫色背景 */
  transition: background-color 0.5s ease;
}

.light-mode :deep(.el-card__body) {
  background: #fff9f0; /* 更改为温暖米色背景 */
}

.ppt-generator {
  width: 100%;
  height: 100%;
  padding: 20px;
  background-color: #2d2339; /* 更改为深紫色背景 */
  color: #e6ecf5;
  overflow-y: auto;
  box-sizing: border-box;
  transition: background-color 0.5s ease, color 0.5s ease;
  background-image: 
    radial-gradient(circle at 15% 15%, rgba(255, 158, 94, 0.03) 0%, transparent 25%),
    radial-gradient(circle at 85% 85%, rgba(255, 158, 94, 0.03) 0%, transparent 25%);
}

.ppt-generator.light-mode {
  background-color: #fff9f0; /* 更改为温暖米色背景 */
  color: #593618; /* 深棕色文字 */
  background-image: none;
}

/* 标题部分样式 */
.title-section {
  margin-bottom: 30px;
  text-align: center;
}

.gradient-title {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 10px;
  position: relative;
  display: inline-block;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.ppt-text {
  background: linear-gradient(90deg, #ff9e5e, #f4a259); /* 更改为橙金色渐变 */
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin: 0 5px;
  filter: drop-shadow(0 2px 4px rgba(255, 158, 94, 0.3)); /* 更改为橙色阴影 */
}

.star-icon {
  font-size: 24px;
  color: #ff9e5e; /* 更改为橙色 */
  margin-left: 5px;
  display: inline-block;
  animation: twinkle 4s ease-in-out infinite;
  filter: drop-shadow(0 0 5px rgba(255, 158, 94, 0.5)); /* 更改为橙色阴影 */
}

@keyframes twinkle {
  0%, 100% {
    opacity: 0.9;
    transform: scale(1);
    filter: brightness(1);
  }
  50% {
    opacity: 0.7;
    transform: scale(1.1);
    filter: brightness(1.2);
  }
}

.subtitle {
  color: #a8b8d5;
  font-size: 16px;
  margin-top: 5px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.light-mode .subtitle {
  color: #d86500; /* 更改为深橙色 */
  text-shadow: none;
}

/* 主内容区域 */
.main-content {
  margin-bottom: 30px;
}

.input-area {
  background-color: #3d2d4e; /* 更改为深紫色 */
  border-radius: 12px;
  padding: 25px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15), 0 0 0 1px rgba(255, 255, 255, 0.05) inset;
  transition: background-color 0.5s ease, box-shadow 0.5s ease;
}

.light-mode .input-area {
  background-color: #ffffff;
  box-shadow: 0 4px 20px rgba(244, 162, 89, 0.08); /* 更改为金黄色阴影 */
}

.input-container {
  width: 100%;
}

textarea {
  width: 100%;
  height: 120px;
  padding: 15px;
  border: 1px solid rgba(255, 158, 94, 0.15); /* 更改为半透明橙色边框 */
  border-radius: 8px;
  background: rgba(61, 45, 78, 0.4); /* 更改为半透明紫色 */
  color: #e6ecf5;
  font-size: 16px;
  resize: vertical;
  transition: all 0.3s ease;
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) inset;
}

.light-mode textarea {
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(244, 162, 89, 0.2); /* 更改为半透明金黄色 */
  color: #593618; /* 深棕色文字 */
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03) inset;
}

textarea:focus {
  outline: none;
  border-color: rgba(255, 158, 94, 0.3); /* 更改为半透明橙色 */
  box-shadow: 0 0 0 2px rgba(255, 158, 94, 0.08), 0 2px 8px rgba(0, 0, 0, 0.1) inset;
}

.light-mode textarea:focus {
  border-color: rgba(244, 162, 89, 0.4); /* 更改为半透明金黄色 */
  box-shadow: 0 0 0 2px rgba(244, 162, 89, 0.08), 0 2px 8px rgba(0, 0, 0, 0.03) inset;
}

textarea::placeholder {
  color: #8a9cc0;
}

.light-mode textarea::placeholder {
  color: rgba(89, 54, 24, 0.6); /* 半透明深棕色 */
}

/* 文件上传区域 */
.file-upload-container {
  margin-bottom: 20px;
}

.file-info {
  display: flex;
  align-items: center;
  background: rgba(61, 45, 78, 0.4); /* 更改为半透明紫色 */
  border-radius: 8px;
  padding: 15px;
  border: 1px solid rgba(255, 158, 94, 0.15); /* 更改为半透明橙色边框 */
  margin-bottom: 20px;
  position: relative;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) inset;
}

.light-mode .file-info {
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(244, 162, 89, 0.2); /* 更改为半透明金黄色 */
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03) inset;
}

.file-icon {
  font-size: 20px;
  margin-right: 15px;
  color: #ff9e5e; /* 更改为橙色 */
  text-shadow: 0 0 5px rgba(255, 158, 94, 0.3); /* 更改为橙色阴影 */
}

.light-mode .file-icon {
  color: #d86500; /* 更改为深橙色 */
  text-shadow: none;
}

.file-name-display {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-right: 15px;
}

.clear-file-btn {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: rgba(255, 76, 76, 0.08);
  border: 1px solid rgba(255, 76, 76, 0.15);
  color: #ff8080;
  font-size: 16px;
  line-height: 1;
  cursor: pointer;
  transition: all 0.3s ease;
}

.clear-file-btn:hover {
  background: rgba(255, 76, 76, 0.15);
  transform: scale(1.05);
}

/* 操作按钮 */
.input-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 15px;
}

.action-buttons {
  display: flex;
  gap: 10px;
}

.action-btn {
  padding: 10px 15px;
  background: rgba(255, 158, 94, 0.08); /* 更改为半透明橙色 */
  color: #ff9e5e; /* 更改为橙色 */
  border: 1px solid rgba(255, 158, 94, 0.15); /* 更改为半透明橙色边框 */
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.light-mode .action-btn {
  background: rgba(244, 162, 89, 0.08); /* 更改为半透明金黄色 */
  color: #d86500; /* 更改为深橙色 */
  border: 1px solid rgba(244, 162, 89, 0.15); /* 更改为半透明金黄色 */
}

.action-btn:hover {
  background: rgba(255, 158, 94, 0.15); /* 更改为半透明橙色 */
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.light-mode .action-btn:hover {
  background: rgba(244, 162, 89, 0.15); /* 更改为半透明金黄色 */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.action-icon {
  font-size: 16px;
}

.create-btn {
  padding: 12px 30px;
  background: linear-gradient(135deg, #ff9e5e, #f4a259); /* 更改为橙金色渐变 */
  color: #ffffff;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(255, 158, 94, 0.25), 0 0 0 1px rgba(255, 255, 255, 0.1) inset;
}

.light-mode .create-btn {
  color: #ffffff;
  box-shadow: 0 4px 15px rgba(244, 162, 89, 0.25); /* 更改为金黄色阴影 */
}

.create-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 158, 94, 0.35), 0 0 0 1px rgba(255, 255, 255, 0.2) inset;
}

.light-mode .create-btn:hover:not(:disabled) {
  box-shadow: 0 6px 20px rgba(244, 162, 89, 0.35); /* 更改为金黄色阴影 */
}

.create-btn:disabled {
  background: #53416e; /* 更改为紫色 */
  color: #8a9cc0;
  cursor: not-allowed;
  box-shadow: none;
}

.light-mode .create-btn:disabled {
  background: #f7cb87; /* 更改为浅金黄色 */
  color: rgba(89, 54, 24, 0.4); /* 半透明深棕色 */
}

/* 模板选择区域 */
.template-section {
  background-color: #3d2d4e; /* 更改为深紫色 */
  border-radius: 12px;
  padding: 25px;
  margin-bottom: 30px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15), 0 0 0 1px rgba(255, 255, 255, 0.05) inset;
  transition: background-color 0.5s ease, box-shadow 0.5s ease;
}

.light-mode .template-section {
  background-color: #ffffff;
  box-shadow: 0 4px 20px rgba(244, 162, 89, 0.08); /* 更改为金黄色阴影 */
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 15px;
}

.section-title {
  color: #ff9e5e; /* 更改为橙色 */
  font-size: 20px;
  font-weight: 600;
  text-shadow: 0 0 10px rgba(255, 158, 94, 0.3); /* 更改为橙色阴影 */
}

.light-mode .section-title {
  color: #d86500; /* 更改为深橙色 */
  text-shadow: none;
}

.filter-group {
  display: flex;
  gap: 15px;
}

.filter-group select {
  padding: 8px 12px;
  border-radius: 6px;
  background: rgba(61, 45, 78, 0.4); /* 更改为半透明紫色 */
  border: 1px solid rgba(255, 158, 94, 0.15); /* 更改为半透明橙色边框 */
  color: #e6ecf5;
  appearance: none;
  background-position: right 8px center;
  background-size: 12px;
  padding-right: 30px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) inset;
}

.light-mode .filter-group select {
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(244, 162, 89, 0.2); /* 更改为半透明金黄色 */
  color: #593618; /* 深棕色文字 */
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03) inset;
}

.filter-group select:focus {
  outline: none;
  border-color: rgba(255, 158, 94, 0.3); /* 更改为半透明橙色 */
  box-shadow: 0 0 0 2px rgba(255, 158, 94, 0.08), 0 2px 8px rgba(0, 0, 0, 0.1) inset;
}

.light-mode .filter-group select:focus {
  border-color: rgba(244, 162, 89, 0.4); /* 更改为半透明金黄色 */
  box-shadow: 0 0 0 2px rgba(244, 162, 89, 0.08), 0 2px 8px rgba(0, 0, 0, 0.03) inset;
}

/* 优化select下拉菜单样式 */
.filter-group select option {
  background-color: #3d2d4e; /* 更改为深紫色 */
  color: #e6ecf5;
  padding: 8px;
}

.light-mode .filter-group select option {
  background-color: #ffffff;
  color: #593618; /* 深棕色文字 */
}

/* 模板网格 */
.template-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 25px;
  min-height: 200px;
}

.template-item {
  position: relative;
  aspect-ratio: 16/9;
  overflow: hidden;
  border-radius: 8px;
  border: 2px solid transparent;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.template-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.25);
}

.light-mode .template-item:hover {
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.template-item.selected {
  border-color: #ff9e5e; /* 更改为橙色 */
  box-shadow: 0 0 0 4px rgba(255, 158, 94, 0.15), 0 8px 25px rgba(0, 0, 0, 0.2);
}

.light-mode .template-item.selected {
  border-color: #d86500; /* 更改为深橙色 */
  box-shadow: 0 0 0 4px rgba(244, 162, 89, 0.15), 0 8px 25px rgba(0, 0, 0, 0.1);
}

.template-cover {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.template-item:hover .template-cover {
  transform: scale(1.05);
}

.template-selected-indicator {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 24px;
  height: 24px;
  background: rgba(255, 158, 94, 0.9); /* 更改为半透明橙色 */
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transform: scale(0);
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.light-mode .template-selected-indicator {
  background: rgba(244, 162, 89, 0.9); /* 更改为半透明金黄色 */
}

.template-item.selected .template-selected-indicator {
  opacity: 1;
  transform: scale(1);
}

.checkmark {
  color: white;
  font-weight: bold;
  font-size: 14px;
}

.loading-tip, .empty-tip {
  grid-column: 1 / -1;
  text-align: center;
  padding: 40px 0;
  color: #a8b8d5;
}

.light-mode .loading-tip, .light-mode .empty-tip {
  color: rgba(89, 54, 24, 0.7); /* 半透明深棕色 */
}

.clear-filter {
  color: #ff9e5e; /* 更改为橙色 */
  cursor: pointer;
  margin-left: 5px;
  text-decoration: underline;
}

.light-mode .clear-filter {
  color: #d86500; /* 更改为深橙色 */
}

/* 分页控件 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
  margin-top: 20px;
}

.pagination button, .pagination span {
  padding: 8px 12px;
  border-radius: 6px;
  background: rgba(61, 45, 78, 0.4); /* 更改为半透明紫色 */
  border: 1px solid rgba(255, 158, 94, 0.15); /* 更改为半透明橙色边框 */
  color: #e6ecf5;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 40px;
  text-align: center;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.light-mode .pagination button, .light-mode .pagination span {
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(244, 162, 89, 0.15); /* 更改为半透明金黄色边框 */
  color: #593618; /* 深棕色文字 */
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
}

.pagination button:hover:not(:disabled), .pagination span:hover {
  background: rgba(255, 158, 94, 0.1); /* 更改为半透明橙色 */
  border-color: rgba(255, 158, 94, 0.25); /* 更改为半透明橙色边框 */
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
}

.light-mode .pagination button:hover:not(:disabled), .light-mode .pagination span:hover {
  background: rgba(244, 162, 89, 0.1); /* 更改为半透明金黄色 */
  border-color: rgba(244, 162, 89, 0.25); /* 更改为半透明金黄色边框 */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
}

.pagination button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.pagination span.active {
  background: linear-gradient(135deg, #ff9e5e, #f4a259); /* 更改为橙金色渐变 */
  color: #ffffff;
  border-color: transparent;
  font-weight: bold;
  box-shadow: 0 4px 10px rgba(255, 158, 94, 0.25); /* 更改为橙色阴影 */
}

.light-mode .pagination span.active {
  color: #ffffff;
  box-shadow: 0 4px 10px rgba(244, 162, 89, 0.25); /* 更改为金黄色阴影 */
}

/* 结果和错误信息样式 */
.result, .error {
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  text-align: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.result {
  background: rgba(255, 158, 94, 0.08); /* 更改为半透明橙色 */
  border: 1px solid rgba(255, 158, 94, 0.2); /* 更改为半透明橙色边框 */
}

.light-mode .result {
  background: rgba(244, 162, 89, 0.08); /* 更改为半透明金黄色 */
  border: 1px solid rgba(244, 162, 89, 0.2); /* 更改为半透明金黄色边框 */
}

.result a {
  color: #ff9e5e; /* 更改为橙色 */
  font-weight: bold;
  text-decoration: underline;
  transition: color 0.3s ease;
}

.light-mode .result a {
  color: #d86500; /* 更改为深橙色 */
}

.result a:hover {
  color: #f7cb87; /* 更改为浅金黄色 */
  text-decoration: none;
}

.light-mode .result a:hover {
  color: #f4a259; /* 更改为金黄色 */
}

.error {
  background: rgba(255, 76, 76, 0.08);
  border: 1px solid rgba(255, 76, 76, 0.2);
  color: #ff8080;
}

/* 响应式布局调整 */
@media (max-width: 768px) {
  .ppt-generator {
    padding: 15px;
  }
  
  .section-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .filter-group {
    width: 100%;
  }
  
  .filter-group select {
    flex: 1;
  }
  
  .template-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 15px;
  }
  
  .input-actions {
    flex-direction: column;
  }
  
  .action-buttons {
    width: 100%;
  }
  
  .create-btn {
    width: 100%;
    margin-top: 10px;
  }
}

/* 自定义滚动条 - 更柔和的样式 */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: rgba(61, 45, 78, 0.2); /* 更改为半透明紫色 */
  border-radius: 3px;
}

::-webkit-scrollbar-thumb {
  background: rgba(255, 158, 94, 0.2); /* 更改为半透明橙色 */
  border-radius: 3px;
  transition: background 0.3s ease;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 158, 94, 0.3); /* 更改为半透明橙色 */
}

.light-mode ::-webkit-scrollbar-track {
  background: rgba(255, 249, 240, 0.5); /* 更改为半透明米色 */
}

.light-mode ::-webkit-scrollbar-thumb {
  background: rgba(244, 162, 89, 0.2); /* 更改为半透明金黄色 */
}

.light-mode ::-webkit-scrollbar-thumb:hover {
  background: rgba(244, 162, 89, 0.3); /* 更改为半透明金黄色 */
}
</style>
