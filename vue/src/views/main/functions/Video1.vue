<template>
  <div class="resource-container" :class="{ 'light-mode': isLightMode }">
    <div class="resource-layout">
      <!-- 左侧控制面板 -->
      <div class="control-panel">
        <h2 class="panel-title">
          AI <span class="highlight">视频生成</span>
        </h2>
        
        <!-- 视频描述输入 -->
        <div class="form-section">
          <div class="section-label">视频描述</div>
          <el-input
            v-model="prompt"
            type="textarea"
            :rows="6"
            placeholder="请描述您想要生成的视频内容..."
            class="prompt-input"
            :disabled="isGenerating"
          />
        </div>

        <!-- 参考图片上传 -->
        <div class="form-section">
          <div class="section-label">参考图片</div>
          <el-upload
            class="upload-area"
            drag
            action=""
            :auto-upload="false"
            :show-file-list="false"
            :on-change="handleFileUpload"
          >
            <div class="upload-content" v-if="!image">
              <el-icon class="upload-icon">
                <UploadFilled />
              </el-icon>
              <div class="upload-text">
                拖放文件到此处或<em>点击上传</em>
              </div>
              <div class="upload-tip">
                支持JPG, PNG格式，推荐分辨率1024x1024
              </div>
            </div>
          </el-upload>
          
          <!-- 上传预览 -->
          <div class="upload-preview" v-if="image">
            <img :src="image" class="preview-image" alt="Preview" />
            <div class="remove-btn">
              <el-button
                type="danger"
                plain
                icon="Delete"
                circle
                @click="removeImage"
              />
            </div>
          </div>
        </div>

        <!-- 视频选项 -->
        <div class="form-section">
          <div class="section-label">生成选项</div>
          <div class="options-grid">
            <div class="option-item">
              <div class="option-label">生成质量</div>
              <el-select
                v-model="quality"
                class="option-select"
                placeholder="选择质量"
              >
                <el-option label="高质量" value="quality" />
                <el-option label="速度优先" value="speed" />
              </el-select>
            </div>
            
            <div class="option-item">
              <div class="option-label">分辨率</div>
              <el-select
                v-model="size"
                class="option-select"
                placeholder="选择分辨率"
              >
                <el-option
                  v-for="res in resolutions"
                  :key="res"
                  :label="res"
                  :value="res"
                />
              </el-select>
            </div>
            
            <div class="option-item">
              <div class="option-label">帧率</div>
              <el-select
                v-model="fps"
                class="option-select"
                placeholder="选择帧率"
              >
                <el-option label="24 FPS" value="24" />
                <el-option label="30 FPS" value="30" />
                <el-option label="60 FPS" value="60" />
              </el-select>
            </div>
            
            <div class="option-item">
              <div class="option-label">生成音频</div>
              <el-switch
                v-model="with_audio"
                class="option-switch"
                active-text="是"
                inactive-text="否"
              />
            </div>
          </div>
        </div>

        <!-- 生成按钮 -->
        <div class="form-action">
          <el-button
            :loading="isGenerating"
            @click="generateVideo"
            class="generate-btn"
          >
            <el-icon v-if="!isGenerating">
              <VideoCamera />
            </el-icon>
            {{ isGenerating ? '生成中...' : '生成视频' }}
          </el-button>
        </div>
      </div>

      <!-- 右侧预览区域 -->
      <div class="preview-panel">
        <div class="preview-header">
          <h2 class="preview-title">视频预览</h2>
          <div class="preview-actions">
            <el-tooltip
              effect="dark"
              content="清除所有数据"
              placement="top"
            >
              <el-button
                v-if="hasStoredData"
                type="danger"
                plain
                icon="Delete"
                @click="confirmClear"
              >清除</el-button>
            </el-tooltip>
          </div>
        </div>
        
        <div class="preview-content">
          <!-- 无结果时的空状态 -->
          <div v-if="!result" class="empty-state">
            <el-icon class="empty-icon">
              <VideoCamera />
            </el-icon>
            <div class="empty-text">尚未生成视频</div>
            <div class="empty-tip">
              请在左侧填写视频描述和参数，然后点击"生成视频"
            </div>
            
            <div class="session-info" v-if="hasStoredData">
              已加载上一次的会话数据
            </div>
          </div>
          
          <!-- 有结果时的视频展示 -->
          <div v-else class="video-result">
            <video
              :src="result.result"
              controls
              class="video-player"
            ></video>
            
            <div class="video-actions">
              <el-button
                type="primary"
                class="action-btn download-btn"
                @click="downloadVideo"
              >
                <el-icon><Download /></el-icon>
                下载视频
              </el-button>
              
              <el-button
                type="danger"
                plain
                class="action-btn"
                @click="clearVideo"
              >
                <el-icon><Delete /></el-icon>
                清除视频
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onBeforeUnmount, watch, computed } from "vue";
import axios from "axios";
import { UploadFilled, Download, Delete, VideoCamera } from "@element-plus/icons-vue";
import { ElMessage, ElMessageBox } from "element-plus";

export default {
  components: {
    UploadFilled,
    Download,
    Delete,
    VideoCamera
  },
  data() {
    return {
      prompt: "",
      image: null,
      quality: "speed",
      with_audio: false,
      size: "1920x1080",
      fps: "30",
      result: null,
      isGenerating: false,
      resolutions: [
        "720x480",
        "1024x1024",
        "1280x960",
        "960x1280",
        "1920x1080",
        "1080x1920",
        "2048x1080",
        "3840x2160",
      ],
      isLightMode: localStorage.getItem("theme-mode") === "light",
    };
  },
  computed: {
    hasStoredData() {
      return localStorage.getItem('video_generator_form') !== null || 
             localStorage.getItem('video_generator_result') !== null;
    }
  },
  mounted() {
    this.checkThemeMode();
    window.addEventListener("storage", this.checkThemeMode);
    window.addEventListener("themeChange", this.checkThemeMode);
    
    // 加载保存的状态
    this.loadSavedState();
    
    // 监听状态变化，自动保存
    this.setupStateWatchers();
  },
  beforeUnmount() {
    window.removeEventListener("storage", this.checkThemeMode);
    window.removeEventListener("themeChange", this.checkThemeMode);
  },
  methods: {
    handleFileUpload(file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        this.image = e.target.result;
      };
      reader.readAsDataURL(file.raw);
    },
    removeImage() {
      this.image = null;
    },
    async generateVideo() {
      if (!this.prompt) {
        ElMessage.warning("请输入视频描述");
        return;
      }

      this.isGenerating = true;

      const data = {
        prompt: this.prompt,
        image: this.image,
        quality: this.quality,
        with_audio: this.with_audio,
        size: this.size,
        fps: parseInt(this.fps),
      };

      try {
        const response = await axios.post(
          "/api/videomaker/generate-video",
          data
        );
        this.result = response.data;
        ElMessage.success("视频生成成功！");
        
        // 保存生成结果到本地存储
        this.saveState();
      } catch (error) {
        console.error("生成视频失败:", error);
        ElMessage.error("生成视频失败，请稍后重试");
      } finally {
        this.isGenerating = false;
      }
    },
    downloadVideo() {
      if (this.result && this.result.result) {
        const link = document.createElement("a");
        link.href = this.result.result;
        link.download = "generated_video.mp4";
        link.click();
      }
    },
    checkThemeMode() {
      this.isLightMode = localStorage.getItem("theme-mode") === "light";
    },
    
    // 状态持久化相关方法
    loadSavedState() {
      try {
        // 加载表单数据
        const savedForm = localStorage.getItem('video_generator_form');
        if (savedForm) {
          const formData = JSON.parse(savedForm);
          this.prompt = formData.prompt || "";
          this.quality = formData.quality || "speed";
          this.with_audio = formData.with_audio || false;
          this.size = formData.size || "1920x1080";
          this.fps = formData.fps || "30";
          this.image = formData.image || null;
        }
        
        // 加载视频结果
        const savedResult = localStorage.getItem('video_generator_result');
        if (savedResult) {
          this.result = JSON.parse(savedResult);
        }
      } catch (error) {
        console.error('加载保存的状态失败:', error);
      }
    },
    
    saveState() {
      try {
        // 保存表单数据
        const formData = {
          prompt: this.prompt,
          quality: this.quality,
          with_audio: this.with_audio,
          size: this.size,
          fps: this.fps,
          image: this.image
        };
        localStorage.setItem('video_generator_form', JSON.stringify(formData));
        
        // 保存视频结果
        if (this.result) {
          localStorage.setItem('video_generator_result', JSON.stringify(this.result));
        } else {
          localStorage.removeItem('video_generator_result');
        }
      } catch (error) {
        console.error('保存状态失败:', error);
      }
    },
    
    setupStateWatchers() {
      // 监听表单字段变化
      this.$watch(
        () => ({
          prompt: this.prompt,
          quality: this.quality,
          with_audio: this.with_audio,
          size: this.size,
          fps: this.fps,
          image: this.image
        }),
        () => {
          this.saveState();
        },
        { deep: true }
      );
      
      // 监听结果变化
      this.$watch('result', () => {
        this.saveState();
      }, { deep: true });
    },
    
    clearState() {
      // 清空本地存储和当前状态
      this.prompt = "";
      this.image = null;
      this.quality = "speed";
      this.with_audio = false;
      this.size = "1920x1080";
      this.fps = "30";
      this.result = null;
      
      localStorage.removeItem('video_generator_form');
      localStorage.removeItem('video_generator_result');
      
      ElMessage.success('已清空所有数据');
    },
    
    confirmClear() {
      ElMessageBox.confirm(
        '确定要清除所有数据吗？此操作将清空表单内容和生成的视频。',
        '确认清除',
        {
          confirmButtonText: '确定清除',
          cancelButtonText: '取消',
          type: 'warning',
        }
      )
        .then(() => {
          this.clearState();
        })
        .catch(() => {
          // 用户取消清除操作
        });
    },
    
    clearVideo() {
      this.result = null;
      localStorage.removeItem('video_generator_result');
      ElMessage.success('已清除视频');
    },
  },
};
</script>

<style scoped>
/* 主容器 */
:deep(.el-card__body) {
  height: 100%;
  padding: 0 !important;
  background: #2d2339; /* 更改为深紫色背景 */
  transition: background-color 0.5s ease;
  overflow: auto;
}

.resource-container {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  background-color: #2d2339; /* 更改为深紫色背景 */
  color: #e6ecf5;
  overflow-y: auto;
  transition: background-color 0.3s, color 0.3s;
}

/* 日间模式 */
.resource-container.light-mode {
  background-color: #fff9f0; /* 更改为温暖米色背景 */
  color: #593618; /* 深棕色文字 */
}

/* 布局结构 */
.resource-layout {
  display: flex;
  width: 100%;
  min-height: 100%; /* 设置为最小高度 */
  flex: 1; /* 添加flex属性确保填充空间 */
}

/* 左侧控制面板 */
.control-panel {
  flex: 0 0 380px;
  background-color: #3d2d4e; /* 更改为深紫色 */
  padding: 24px;
  overflow-y: auto; /* 修改为auto允许滚动 */
  border-right: 1px solid rgba(255, 255, 255, 0.05);
  display: flex;
  flex-direction: column;
  max-height: 100vh; /* 限制最大高度 */
}

.light-mode .control-panel {
  background-color: #ffffff;
  border-right: 1px solid rgba(244, 162, 89, 0.1); /* 更改为半透明金黄色 */
}

/* 标题样式 */
.panel-title {
  margin: 0 0 30px;
  font-size: 24px;
  font-weight: 600;
  text-align: center;
  padding-bottom: 15px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  position: relative;
}

.panel-title::after {
  content: "";
  position: absolute;
  bottom: -1px;
  left: 50%;
  transform: translateX(-50%);
  width: 80px;
  height: 2px;
  background: linear-gradient(90deg, #ff9e5e, #f4a259); /* 更改为橙金色渐变 */
}

.light-mode .panel-title {
  border-bottom: 1px solid rgba(244, 162, 89, 0.2); /* 更改为半透明金黄色 */
}

.highlight {
  background: linear-gradient(90deg, #ff9e5e, #f4a259); /* 更改为橙金色渐变 */
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* 表单部分 */
.form-section {
  margin-bottom: 24px;
}

.section-label {
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 12px;
  color: #ff9e5e; /* 更改为橙色 */
}

.light-mode .section-label {
  color: #d86500; /* 更改为深橙色 */
}

/* 输入区域 */
.prompt-input {
  width: 100%;
}

:deep(.el-textarea__inner) {
  background-color: rgba(61, 45, 78, 0.4); /* 更改为半透明紫色 */
  border: 1px solid rgba(255, 158, 94, 0.2); /* 更改为半透明橙色边框 */
  border-radius: 8px;
  color: #e6ecf5;
  transition: all 0.3s;
}

.light-mode :deep(.el-textarea__inner) {
  background-color: rgba(255, 249, 240, 0.5); /* 更改为半透明米色 */
  border: 1px solid rgba(244, 162, 89, 0.2); /* 更改为半透明金黄色边框 */
  color: #593618; /* 深棕色文字 */
}

:deep(.el-textarea__inner:focus) {
  border-color: #ff9e5e; /* 更改为橙色 */
  box-shadow: 0 0 0 2px rgba(255, 158, 94, 0.1); /* 更改为半透明橙色 */
}

.light-mode :deep(.el-textarea__inner:focus) {
  border-color: #f4a259; /* 更改为金黄色 */
  box-shadow: 0 0 0 2px rgba(244, 162, 89, 0.1); /* 更改为半透明金黄色 */
}

/* 上传区域 */
.upload-area {
  width: 100%;
}

:deep(.el-upload-dragger) {
  width: 100%;
  background-color: rgba(61, 45, 78, 0.4); /* 更改为半透明紫色 */
  border: 1px dashed rgba(255, 158, 94, 0.3); /* 更改为半透明橙色边框 */
  border-radius: 8px;
  transition: all 0.3s;
}

.light-mode :deep(.el-upload-dragger) {
  background-color: rgba(255, 249, 240, 0.5); /* 更改为半透明米色 */
  border: 1px dashed rgba(244, 162, 89, 0.3); /* 更改为半透明金黄色边框 */
}

:deep(.el-upload-dragger:hover) {
  border-color: #ff9e5e; /* 更改为橙色 */
  background-color: rgba(255, 158, 94, 0.05); /* 更改为半透明橙色 */
}

.light-mode :deep(.el-upload-dragger:hover) {
  border-color: #f4a259; /* 更改为金黄色 */
  background-color: rgba(244, 162, 89, 0.05); /* 更改为半透明金黄色 */
}

.upload-content {
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.upload-icon {
  font-size: 40px;
  color: #ff9e5e; /* 更改为橙色 */
  margin-bottom: 10px;
}

.light-mode .upload-icon {
  color: #f4a259; /* 更改为金黄色 */
}

.upload-text {
  color: #a0b0d0;
  margin-bottom: 5px;
}

.light-mode .upload-text {
  color: #593618; /* 深棕色文字 */
}

.upload-text em {
  color: #ff9e5e; /* 更改为橙色 */
  font-style: normal;
  font-weight: 600;
}

.light-mode .upload-text em {
  color: #d86500; /* 更改为深橙色 */
}

.upload-tip {
  font-size: 12px;
  color: #8a94b8;
}

.light-mode .upload-tip {
  color: rgba(89, 54, 24, 0.7); /* 半透明深棕色 */
}

/* 上传预览 */
.upload-preview {
  margin-top: 15px;
  display: flex;
  align-items: center;
  gap: 15px;
  background: rgba(61, 45, 78, 0.3); /* 更改为半透明紫色 */
  border-radius: 8px;
  padding: 10px;
}

.light-mode .upload-preview {
  background: rgba(255, 249, 240, 0.5); /* 更改为半透明米色 */
}

.preview-image {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 6px;
  border: 2px solid rgba(255, 158, 94, 0.3); /* 更改为半透明橙色边框 */
}

.light-mode .preview-image {
  border: 2px solid rgba(244, 162, 89, 0.3); /* 更改为半透明金黄色边框 */
}

.remove-btn {
  margin-left: auto;
}

/* 选项网格 */
.options-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.option-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.option-label {
  font-size: 14px;
  color: #a0b0d0;
}

.light-mode .option-label {
  color: rgba(89, 54, 24, 0.7); /* 半透明深棕色 */
}

.option-select {
  width: 100%;
}

:deep(.el-select .el-input__inner) {
  background-color: rgba(61, 45, 78, 0.4); /* 更改为半透明紫色 */
  border: 1px solid rgba(255, 158, 94, 0.2); /* 更改为半透明橙色边框 */
  color: #e6ecf5;
}

.light-mode :deep(.el-select .el-input__inner) {
  background-color: rgba(255, 249, 240, 0.5); /* 更改为半透明米色 */
  border: 1px solid rgba(244, 162, 89, 0.2); /* 更改为半透明金黄色边框 */
  color: #593618; /* 深棕色文字 */
}

:deep(.el-select .el-input.is-focus .el-input__inner) {
  border-color: #ff9e5e; /* 更改为橙色 */
}

.light-mode :deep(.el-select .el-input.is-focus .el-input__inner) {
  border-color: #f4a259; /* 更改为金黄色 */
}

:deep(.el-select-dropdown__item.selected) {
  color: #ff9e5e; /* 更改为橙色 */
}

.light-mode :deep(.el-select-dropdown__item.selected) {
  color: #d86500; /* 更改为深橙色 */
}

/* 生成按钮 */
.form-action {
  margin-top: auto;
  padding-top: 5px;
  display: flex;
  justify-content: center;
}

.generate-btn {
  width: 100%;
  height: 48px;
  font-size: 16px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  background: linear-gradient(135deg, #ff9e5e, #f4a259) !important; /* 更改为橙金色渐变 */
  color: #ffffff !important;
  border: none !important;
  border-radius: 24px !important;
  box-shadow: 0 4px 15px rgba(255, 158, 94, 0.3); /* 更改为橙色阴影 */
  transition: all 0.3s !important;
}

.generate-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 158, 94, 0.5); /* 更改为橙色阴影 */
}

.generate-btn:active {
  transform: translateY(1px);
}

.generate-btn.is-loading {
  background: rgba(61, 45, 78, 0.5) !important; /* 更改为半透明紫色 */
  color: #8a94b8 !important;
}

/* 右侧预览面板 */
.preview-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow-y: auto; /* 修改为auto允许滚动 */
  max-height: 100vh; /* 限制最大高度 */
}

.preview-header {
  padding: 20px 30px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.light-mode .preview-header {
  border-bottom: 1px solid rgba(244, 162, 89, 0.1); /* 更改为半透明金黄色 */
}

.preview-title {
  margin: 0;
  font-size: 20px;
  font-weight: 500;
}

.preview-actions {
  display: flex;
  gap: 10px;
}

.preview-content {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 30px;
  overflow: auto; /* 修改为auto允许滚动 */
  min-height: 400px; /* 确保最小高度 */
}

/* 空状态 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  max-width: 400px;
  animation: fadeIn 0.5s ease-out;
}

.empty-icon {
  font-size: 80px;
  color: #ff9e5e; /* 更改为橙色 */
  margin-bottom: 20px;
  opacity: 0.5;
}

.light-mode .empty-icon {
  color: #f4a259; /* 更改为金黄色 */
}

.empty-text {
  font-size: 18px;
  margin-bottom: 10px;
  color: #a0b0d0;
}

.light-mode .empty-text {
  color: rgba(89, 54, 24, 0.7); /* 半透明深棕色 */
}

.empty-tip {
  font-size: 14px;
  color: #8a94b8;
  opacity: 0.8;
  margin-bottom: 16px;
}

.light-mode .empty-tip {
  color: rgba(89, 54, 24, 0.6); /* 半透明深棕色 */
}

.session-info {
  margin-top: 10px;
  padding: 8px 16px;
  background-color: rgba(255, 158, 94, 0.1); /* 更改为半透明橙色 */
  border-radius: 20px;
  font-size: 14px;
  color: #ff9e5e; /* 更改为橙色 */
  display: flex;
  align-items: center;
  animation: pulse 2s infinite;
}

.light-mode .session-info {
  background-color: rgba(244, 162, 89, 0.1); /* 更改为半透明金黄色 */
  color: #d86500; /* 更改为深橙色 */
}

@keyframes pulse {
  0% { opacity: 0.7; }
  50% { opacity: 1; }
  100% { opacity: 0.7; }
}

/* 视频结果 */
.video-result {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  animation: fadeIn 0.5s ease-out;
}

.video-player {
  max-width: 90%;
  max-height: calc(100% - 100px);
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  background-color: #000;
}

.video-actions {
  margin-top: 24px;
  display: flex;
  gap: 15px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  font-weight: 600;
}

.download-btn {
  background: linear-gradient(135deg, #ff9e5e, #f4a259) !important; /* 更改为橙金色渐变 */
  border: none !important;
  color: #ffffff !important;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 响应式适配 */
@media (max-width: 1200px) {
  .resource-layout {
    flex-direction: column;
  }
  
  .control-panel {
    flex: 0 0 auto;
    border-right: none;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    max-height: 50vh; /* 修改为视口高度的一半 */
    overflow-y: auto; /* 确保可滚动 */
  }
  
  .light-mode .control-panel {
    border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  }
  
  .preview-panel {
    max-height: 50vh; /* 修改为视口高度的一半 */
    overflow-y: auto; /* 确保可滚动 */
  }
}

@media (max-width: 768px) {
  .options-grid {
    grid-template-columns: 1fr;
  }
  
  .preview-content {
    padding: 15px;
  }
}

/* 添加滚动条美化样式 */
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
  transition: background 0.3s;
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
