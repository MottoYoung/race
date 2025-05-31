<template>
  <div
    id="app"
    class="ai-image-generator"
    :class="{ 'light-mode': isLightMode }"
  >
    <div class="container">
      <h1 class="main-title">AI <span class="highlight">图像生成</span>工具</h1>

      <!-- 模式选择 -->
      <div class="mode-select">
        <button
          @click="setMode('normal')"
          :class="{ active: mode === 'normal' }"
        >
          普通绘图
        </button>
        <button @click="setMode('math')" :class="{ active: mode === 'math' }">
          数学绘图
        </button>
      </div>

      <div class="input-group">
        <textarea
          v-model="inputText"
          :placeholder="placeholderText"
          maxlength="1000"
        ></textarea>
        <div class="char-count">{{ inputText.length }}/1000</div>
      </div>

      <!-- 普通绘图选项 -->
      <div v-if="mode === 'normal'" class="controls">
        <select v-model="selectedResolution" class="resolution-select">
          <option
            v-for="res in resolutions"
            :key="res.value"
            :value="res.value"
          >
            {{ res.label }} ({{ res.points }}点数)
          </option>
        </select>
      </div>

      <button @click="generateImage" :disabled="isLoading" class="generate-btn">
        <span v-if="isLoading">生成中...</span>
        <span v-else>{{ generateButtonText }}</span>
      </button>

      <div v-if="errorMsg" class="error-message">{{ errorMsg }}</div>

      <div v-if="imageUrl" class="result-container">
        <div class="image-wrapper">
          <img :src="imageUrl" alt="生成的图片" class="generated-image" />
        </div>
        <div class="action-buttons">
          <button @click="downloadImage" class="download-btn">下载图片</button>
          <button @click="regenerate" class="regenerate-btn">重新生成</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      mode: "normal", // 'normal' 或 'math'
      inputText: "",
      selectedResolution: "512x512",
      resolutions: [
        { label: "512x512", value: "512x512", points: 6 },
        { label: "768x768", value: "768x768", points: 8 },
        { label: "1024x1024", value: "1024x1024", points: 14 },
      ],
      imageUrl: "",
      isLoading: false,
      errorMsg: "",
      isLightMode: localStorage.getItem("theme-mode") === "light",
    };
  },
  computed: {
    placeholderText() {
      return this.mode === "normal"
        ? "请输入图片描述，例如：雪山脚下的蓝色湖泊..."
        : "请输入数学绘图需求，例如：绘制三维正弦函数图像，添加颜色渐变";
    },
    generateButtonText() {
      return this.mode === "normal" ? "生成图片" : "生成数学图表";
    },
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
    setMode(newMode) {
      this.mode = newMode;
      this.resetState();
    },
    resetState() {
      this.inputText = "";
      this.imageUrl = "";
      this.errorMsg = "";
    },
    async generateImage() {
      if (!this.inputText.trim()) {
        this.errorMsg = "请输入内容";
        return;
      }

      this.isLoading = true;
      this.errorMsg = "";

      try {
        const payload = {
          text: this.inputText,
          mode: this.mode,
        };

        if (this.mode === "normal") {
          payload.resolution = this.selectedResolution;
        }

        const response = await axios.post(
          "/api/picturegenerater/generate",
          payload
        );
        this.imageUrl = `data:image/png;base64,${response.data.image}`;
      } catch (err) {
        this.errorMsg =
          err.response?.data?.error || "生成失败，请检查网络或重试";
      } finally {
        this.isLoading = false;
      }
    },
    downloadImage() {
      const link = document.createElement("a");
      link.href = this.imageUrl;
      link.download = `generated_${Date.now()}.png`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    },
    regenerate() {
      this.generateImage();
    },
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

.ai-image-generator {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  background-color: #2d2339; /* 更改为深紫色背景 */
  color: #e6ecf5;
  overflow-y: auto;
  padding: 20px;
  box-sizing: border-box;
  transition: background-color 0.5s ease, color 0.5s ease;
  background-image: 
    radial-gradient(circle at 10% 20%, rgba(255, 158, 94, 0.03) 0%, transparent 25%),
    radial-gradient(circle at 90% 80%, rgba(255, 158, 94, 0.03) 0%, transparent 25%);
}

.ai-image-generator.light-mode {
  background-color: #fff9f0; /* 更改为温暖米色背景 */
  color: #593618; /* 深棕色文字 */
  background-image: none;
}

.container {
  max-width: 1000px;
  width: 100%;
  margin: 0 auto;
  padding: 30px;
  background: #3d2d4e; /* 更改为深紫色 */
  border-radius: 12px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2), 0 0 0 1px rgba(255, 255, 255, 0.05) inset;
  transition: background-color 0.5s ease, box-shadow 0.5s ease;
}

.light-mode .container {
  background: #ffffff;
  box-shadow: 0 8px 30px rgba(244, 162, 89, 0.08);
}

.main-title {
  text-align: center;
  color: #e6ecf5;
  font-size: 2.2rem;
  margin-bottom: 30px;
  font-weight: 700;
  position: relative;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.main-title::after {
  content: "";
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 80px;
  height: 2px;
  background: linear-gradient(90deg, #ff9e5e, #f4a259); /* 更改为橙金色渐变 */
  box-shadow: 0 0 10px rgba(255, 158, 94, 0.5); /* 更改为橙色阴影 */
}

.light-mode .main-title {
  color: #593618; /* 深棕色文字 */
  text-shadow: none;
}

.highlight {
  background: linear-gradient(90deg, #ff9e5e, #f4a259); /* 更改为橙金色渐变 */
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  filter: drop-shadow(0 2px 4px rgba(255, 158, 94, 0.3)); /* 更改为橙色阴影 */
}

/* 模式选择 */
.mode-select {
  margin: 25px 0;
  display: flex;
  gap: 15px;
  justify-content: center;
}

.mode-select button {
  padding: 12px 25px;
  border: 2px solid rgba(255, 158, 94, 0.15); /* 更改为半透明橙色边框 */
  border-radius: 30px;
  background: rgba(61, 45, 78, 0.4); /* 更改为半透明紫色背景 */
  color: #e6ecf5;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.light-mode .mode-select button {
  background: rgba(255, 255, 255, 0.8);
  border: 2px solid rgba(244, 162, 89, 0.3); /* 更改为半透明金黄色边框 */
  color: #593618; /* 深棕色文字 */
}

.mode-select button.active {
  background: linear-gradient(135deg, #ff9e5e, #f4a259); /* 更改为橙金色渐变 */
  border-color: transparent;
  color: #ffffff; /* 白色文字更好看 */
  font-weight: 600;
  box-shadow: 0 4px 15px rgba(255, 158, 94, 0.35); /* 更改为橙色阴影 */
  transform: translateY(-2px);
}

.light-mode .mode-select button.active {
  color: #ffffff;
  box-shadow: 0 4px 15px rgba(244, 162, 89, 0.35); /* 更改为金黄色阴影 */
}

.mode-select button:hover:not(.active) {
  background: rgba(255, 158, 94, 0.1); /* 更改为半透明橙色背景 */
  border-color: rgba(255, 158, 94, 0.25); /* 更改为半透明橙色边框 */
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.light-mode .mode-select button:hover:not(.active) {
  background: rgba(244, 162, 89, 0.1); /* 更改为半透明金黄色背景 */
  border-color: rgba(244, 162, 89, 0.25); /* 更改为半透明金黄色边框 */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.input-group {
  margin: 20px 0;
  position: relative;
}

textarea {
  width: 100%;
  height: 150px;
  padding: 15px;
  border: 1px solid rgba(255, 158, 94, 0.15); /* 更改为半透明橙色边框 */
  border-radius: 8px;
  background: rgba(61, 45, 78, 0.4); /* 更改为半透明紫色背景 */
  color: #e6ecf5;
  font-size: 16px;
  resize: vertical;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) inset;
}

.light-mode textarea {
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(244, 162, 89, 0.2); /* 更改为半透明金黄色边框 */
  color: #593618; /* 深棕色文字 */
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03) inset;
}

textarea:focus {
  outline: none;
  border-color: rgba(255, 158, 94, 0.3); /* 更改为半透明橙色边框 */
  box-shadow: 0 0 0 2px rgba(255, 158, 94, 0.08), 0 2px 8px rgba(0, 0, 0, 0.1) inset;
}

.light-mode textarea:focus {
  border-color: rgba(244, 162, 89, 0.4); /* 更改为半透明金黄色边框 */
  box-shadow: 0 0 0 2px rgba(244, 162, 89, 0.08), 0 2px 8px rgba(0, 0, 0, 0.03) inset;
}

textarea::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.light-mode textarea::placeholder {
  color: rgba(89, 54, 24, 0.6); /* 半透明深棕色 */
}

.char-count {
  text-align: right;
  color: rgba(255, 255, 255, 0.6);
  margin-top: 5px;
  font-size: 0.85rem;
}

.light-mode .char-count {
  color: rgba(89, 54, 24, 0.6); /* 半透明深棕色 */
}

.controls {
  display: flex;
  gap: 15px;
  margin: 25px 0;
}

.resolution-select {
  flex: 1;
  padding: 12px 15px;
  border: 1px solid rgba(255, 158, 94, 0.15); /* 更改为半透明橙色边框 */
  border-radius: 8px;
  background: rgba(61, 45, 78, 0.4); /* 更改为半透明紫色背景 */
  color: #e6ecf5;
  font-size: 16px;
  appearance: none;
  background-repeat: no-repeat;
  background-position: right 15px center;
  background-size: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) inset;
}

.light-mode .resolution-select {
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(244, 162, 89, 0.2); /* 更改为半透明金黄色边框 */
  color: #593618; /* 深棕色文字 */
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03) inset;
}

.resolution-select:focus {
  outline: none;
  border-color: rgba(255, 158, 94, 0.3); /* 更改为半透明橙色边框 */
  box-shadow: 0 0 0 2px rgba(255, 158, 94, 0.08), 0 2px 8px rgba(0, 0, 0, 0.1) inset;
}

.light-mode .resolution-select:focus {
  border-color: rgba(244, 162, 89, 0.4); /* 更改为半透明金黄色边框 */
  box-shadow: 0 0 0 2px rgba(244, 162, 89, 0.08), 0 2px 8px rgba(0, 0, 0, 0.03) inset;
}

.generate-btn {
  width: 100%;
  padding: 16px;
  margin: 10px 0 20px;
  background: linear-gradient(135deg, #ff9e5e, #f4a259); /* 更改为橙金色渐变 */
  color: #ffffff;
  border: none;
  border-radius: 8px;
  font-size: 18px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(255, 158, 94, 0.25), 0 0 0 1px rgba(255, 255, 255, 0.1) inset;
}

.light-mode .generate-btn {
  color: #ffffff;
  box-shadow: 0 4px 15px rgba(244, 162, 89, 0.25); /* 更改为金黄色阴影 */
}

.generate-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 158, 94, 0.35), 0 0 0 1px rgba(255, 255, 255, 0.2) inset;
}

.light-mode .generate-btn:hover:not(:disabled) {
  box-shadow: 0 6px 20px rgba(244, 162, 89, 0.35); /* 更改为金黄色阴影 */
}

.generate-btn:disabled {
  background: #53416e; /* 更改为紫色 */
  color: rgba(255, 255, 255, 0.4);
  cursor: not-allowed;
  box-shadow: none;
}

.light-mode .generate-btn:disabled {
  background: #f7cb87; /* 更改为浅金黄色 */
  color: rgba(89, 54, 24, 0.4); /* 半透明深棕色 */
}

.error-message {
  color: #ff8080;
  padding: 12px;
  margin: 15px 0;
  border-radius: 8px;
  background: rgba(255, 76, 76, 0.08);
  border-left: 3px solid #ff8080;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.result-container {
  margin-top: 30px;
  text-align: center;
  animation: fadeIn 0.6s ease-out;
}

.image-wrapper {
  border: 2px dashed rgba(255, 158, 94, 0.2); /* 更改为半透明橙色边框 */
  border-radius: 8px;
  padding: 15px;
  display: inline-block;
  background: rgba(61, 45, 78, 0.4); /* 更改为半透明紫色背景 */
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

.image-wrapper:hover {
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
  transform: translateY(-3px);
}

.light-mode .image-wrapper {
  background: rgba(255, 255, 255, 0.8);
  border: 2px dashed rgba(244, 162, 89, 0.2); /* 更改为半透明金黄色边框 */
  box-shadow: 0 4px 15px rgba(244, 162, 89, 0.08); /* 更改为金黄色阴影 */
}

.light-mode .image-wrapper:hover {
  box-shadow: 0 8px 25px rgba(244, 162, 89, 0.12); /* 更改为金黄色阴影 */
}

.generated-image {
  max-width: 100%;
  max-height: 60vh;
  border-radius: 4px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease;
}

.generated-image:hover {
  transform: scale(1.02);
}

.light-mode .generated-image {
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
}

.action-buttons {
  margin-top: 20px;
  display: flex;
  gap: 15px;
  justify-content: center;
}

.download-btn,
.regenerate-btn {
  padding: 12px 25px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.download-btn {
  background: rgba(255, 158, 94, 0.08); /* 更改为半透明橙色背景 */
  color: #ff9e5e; /* 更改为橙色 */
  border: 1px solid rgba(255, 158, 94, 0.15); /* 更改为半透明橙色边框 */
}

.light-mode .download-btn {
  background: rgba(244, 162, 89, 0.08); /* 更改为半透明金黄色背景 */
  color: #d86500; /* 更改为深橙色 */
  border: 1px solid rgba(244, 162, 89, 0.15); /* 更改为半透明金黄色边框 */
}

.download-btn:hover {
  background: rgba(255, 158, 94, 0.15); /* 更改为半透明橙色背景 */
  border-color: rgba(255, 158, 94, 0.25); /* 更改为半透明橙色边框 */
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.light-mode .download-btn:hover {
  background: rgba(244, 162, 89, 0.15); /* 更改为半透明金黄色背景 */
  border-color: rgba(244, 162, 89, 0.25); /* 更改为半透明金黄色边框 */
  box-shadow: 0 4px 12px rgba(244, 162, 89, 0.08); /* 更改为金黄色阴影 */
}

.regenerate-btn {
  background: rgba(255, 158, 94, 0.08); /* 更改为半透明橙色背景 */
  color: #ff9e5e; /* 更改为橙色 */
  border: 1px solid rgba(255, 158, 94, 0.15); /* 更改为半透明橙色边框 */
}

.light-mode .regenerate-btn {
  background: rgba(244, 162, 89, 0.08); /* 更改为半透明金黄色背景 */
  color: #d86500; /* 更改为深橙色 */
  border: 1px solid rgba(244, 162, 89, 0.15); /* 更改为半透明金黄色边框 */
}

.regenerate-btn:hover {
  background: rgba(255, 158, 94, 0.15); /* 更改为半透明橙色背景 */
  border-color: rgba(255, 158, 94, 0.25); /* 更改为半透明橙色边框 */
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.light-mode .regenerate-btn:hover {
  background: rgba(244, 162, 89, 0.15); /* 更改为半透明金黄色背景 */
  border-color: rgba(244, 162, 89, 0.25); /* 更改为半透明金黄色边框 */
  box-shadow: 0 4px 12px rgba(244, 162, 89, 0.08); /* 更改为金黄色阴影 */
}

/* 动画效果 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 自定义滚动条 */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: rgba(61, 45, 78, 0.2); /* 更改为半透明紫色背景 */
  border-radius: 3px;
}

::-webkit-scrollbar-thumb {
  background: rgba(255, 158, 94, 0.2); /* 更改为半透明橙色背景 */
  border-radius: 3px;
  transition: background 0.3s ease;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 158, 94, 0.3); /* 更改为半透明橙色背景 */
}

.light-mode ::-webkit-scrollbar-track {
  background: rgba(255, 249, 240, 0.5); /* 更改为半透明米色背景 */
}

.light-mode ::-webkit-scrollbar-thumb {
  background: rgba(244, 162, 89, 0.2); /* 更改为半透明金黄色背景 */
}

.light-mode ::-webkit-scrollbar-thumb:hover {
  background: rgba(244, 162, 89, 0.3); /* 更改为半透明金黄色背景 */
}

/* 响应式调整 */
@media (max-width: 768px) {
  .container {
    padding: 20px;
  }
  
  .main-title {
    font-size: 1.8rem;
  }
  
  .mode-select {
    flex-direction: column;
    gap: 10px;
    align-items: center;
  }
  
  .mode-select button {
    width: 100%;
    max-width: 300px;
  }
  
  .action-buttons {
    flex-direction: column;
    align-items: center;
    gap: 10px;
  }
  
  .download-btn, .regenerate-btn {
    width: 100%;
    max-width: 300px;
  }
}
</style>
