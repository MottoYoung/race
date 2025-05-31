<template>
  <div class="home" :class="{ 'light-mode': isLightMode }">
    <h1>PPT转视频工具</h1>
    <div class="container">
      <!-- 步骤指示器 -->
      <div class="steps">
        <div class="step" :class="{ active: currentStep >= 1 }">1. 上传PPT</div>
        <div class="step" :class="{ active: currentStep >= 2 }">2. 设置参数</div>
        <div class="step" :class="{ active: currentStep >= 3 }">3. 生成视频</div>
      </div>
      
      <!-- 步骤1：文件上传 -->
      <div v-if="currentStep === 1" class="step-content">
        <!-- FileUpload组件内容 -->
        <div class="file-upload">
          <h2>上传PPT文件</h2>
          <div 
            class="upload-area" 
            :class="{ 'drag-over': isDragging }"
            @dragover.prevent="isDragging = true"
            @dragleave.prevent="isDragging = false"
            @drop.prevent="handleFileDrop"
          >
            <div v-if="!isUploading && !file">
              <i class="file-icon">📄</i>
              <p>拖放PPT文件到此处，或</p>
              <label class="upload-btn">
                选择文件
                <input type="file" accept=".ppt,.pptx" @change="handleFileChange" />
              </label>
              <p class="note">支持.ppt和.pptx格式，最大50MB</p>
            </div>
            
            <div v-else-if="isUploading" class="uploading">
              <div class="spinner"></div>
              <p>正在上传 {{ file.name }}</p>
              <p>{{ Math.round(uploadProgress) }}%</p>
            </div>
            
            <div v-else class="uploaded">
              <i class="file-icon">✅</i>
              <p>{{ file.name }}</p>
              <p>已上传</p>
            </div>
          </div>
          
          <div v-if="error" class="error-message">
            {{ error }}
          </div>
        </div>
      </div>
      
      <!-- 步骤2：参数配置 -->
      <div v-if="currentStep === 2" class="step-content">
        <!-- ConversionForm组件内容 -->
        <div class="conversion-form">
          <h2>设置转换参数</h2>
          <p class="file-info">文件: {{ uploadedFilename }}</p>
          
          <form @submit.prevent="submitForm">
            <div class="form-group">
              <label>使用AI生成演讲稿</label>
              <div class="toggle-switch">
                <input 
                  type="checkbox" 
                  id="use-script" 
                  v-model="formData.use_generated_script"
                  @change="toggleScriptOptions"
                />
                <label for="use-script" class="toggle-label"></label>
              </div>
            </div>
            
            <!-- 当选择使用AI生成演讲稿时显示的选项 -->
            <div v-if="formData.use_generated_script" class="script-options">
              <div class="form-group">
                <label for="script-style">演讲风格</label>
                <select id="script-style" v-model="formData.script_style">
                  <option value="标准">标准</option>
                  <option value="幽默">幽默</option>
                  <option value="严谨">严谨</option>
                  <option value="激励">激励</option>
                </select>
              </div>
              
              <div class="form-group">
                <label for="target-audience">目标受众</label>
                <select id="target-audience" v-model="formData.target_audience">
                  <option value="通用">通用</option>
                  <option value="小学生">小学生</option>
                  <option value="初中生">初中生</option>
                  <option value="高中生">高中生</option>
                  <option value="大学生">大学生</option>
                  <option value="专业人士">专业人士</option>
                </select>
              </div>
              
              <div class="form-group">
                <label for="total-duration">演讲时长</label>
                <select id="total-duration" v-model="formData.total_duration">
                  <option value="简短">简短 (3-5分钟)</option>
                  <option value="中等">中等 (5-10分钟)</option>
                  <option value="详细">详细 (10-15分钟)</option>
                </select>
              </div>
              
              <div class="form-group">
                <label for="subject">学科类型</label>
                <select id="subject" v-model="formData.subject">
                  <option value="通用">通用</option>
                  <option value="语文">语文</option>
                  <option value="数学">数学</option>
                  <option value="英语">英语</option>
                  <option value="物理">物理</option>
                  <option value="化学">化学</option>
                  <option value="生物">生物</option>
                  <option value="历史">历史</option>
                  <option value="地理">地理</option>
                  <option value="政治">政治</option>
                </select>
              </div>
            </div>
            
            <div class="form-group">
              <label for="slide-duration">默认幻灯片时长 (秒)</label>
              <input 
                type="number" 
                id="slide-duration" 
                v-model.number="formData.slide_duration"
                min="1"
                max="30"
                step="1"
              />
              <span class="note">当幻灯片没有语音时的默认显示时长</span>
            </div>
            
            <div class="form-group">
              <label for="lang">语音语言</label>
              <select id="lang" v-model="formData.lang">
                <option value="zh-cn">中文 (普通话)</option>
                <option value="en-us">英语 (美国)</option>
              </select>
            </div>
            
            <!-- 新增：语速选择 -->
            <div class="form-group">
              <label for="speed">语速</label>
              <div class="slider-container">
                <input 
                  type="range" 
                  id="speed" 
                  v-model.number="formData.speed" 
                  min="0" 
                  max="100" 
                  step="1" 
                  class="slider"
                />
                <span class="slider-value">{{ formData.speed }}</span>
              </div>
              <span class="note">0-慢速，50-正常，100-快速</span>
            </div>
            
            <!-- 新增：发音人选择 -->
            <div class="form-group">
              <label for="vcn">发音人</label>
              <select id="vcn" v-model="formData.vcn">
                <option value="x4_mingge">明哥 (男声)</option>
                <option value="x4_xiaoying">秀英 (老年女声)</option>
                <option value="x4_xiaoguo">小果 (女声)</option>
                <option value="x4_xiaozhong">小忠 (男声)</option>
                <option value="x4_qianxue">千雪 (女声)</option>
                <option value="x4_yeting">希涵 (女声)</option>
                <option value="x4_lingbosong">聆伯松 (老年男声)</option>
                <option value="x4_lingxiaoshan_profnews">聆小珊 (女声)</option>
                <option value="x4_doudou">豆豆 (男童声)</option>
                <option value="x4_chaoge">超哥 (男声)</option>
                <option value="x4_guanyijie">关山 (专题男声)</option>
                <option value="x4_feidie">飞碟哥 (男声)</option>
              </select>
            </div>
            
            <div class="form-actions">
              <button type="submit" class="btn-submit">开始转换</button>
            </div>
          </form>
          <button class="btn-secondary" @click="currentStep = 1">返回</button>
        </div>
      </div>
      
      <!-- 步骤3：处理中 -->
      <div v-if="currentStep === 3" class="step-content">
        <div class="processing">
          <h2>正在处理您的PPT...</h2>
          <div class="progress-bar">
            <div class="progress-animation"></div>
          </div>
          <p>请耐心等待，转换过程可能需要几分钟。</p>
          <p>处理状态: {{ processingStatus }}</p>
        </div>
      </div>
      
      <!-- 步骤4：结果 -->
      <div v-if="currentStep === 4" class="step-content">
        <div v-if="conversionSuccess" class="success">
          <h2>转换成功！</h2>
          <!-- VideoPlayer组件内容 -->
          <div class="video-player">
            <video
              ref="videoPlayer"
              class="video-js"
              controls
              preload="auto"
              width="100%"
              height="auto"
              :src="videoUrl"
              data-setup="{}"
              @error="handleVideoError"
            >
              <p class="vjs-no-js">
                要查看此视频，请启用JavaScript并考虑升级到支持HTML5视频的浏览器
              </p>
            </video>
            <div v-if="videoError" class="error-message">
              视频加载错误: {{ videoError }}
            </div>
          </div>
          <div class="actions">
            <button class="btn-primary" @click="downloadVideo">下载视频</button>
            <button class="btn-secondary" @click="resetForm">开始新的转换</button>
          </div>
        </div>
        <div v-else class="error">
          <h2>转换失败</h2>
          <p>{{ errorMessage }}</p>
          <button class="btn-secondary" @click="resetForm">重试</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

// 创建自定义的axios实例，替代vue.config.js中的代理配置
const apiClient = axios.create({
  baseURL: '/api/pptvideo',
  headers: {
    'Content-Type': 'application/json'
  }
});

export default {
  name: 'CombinedComponent',
  data() {
    return {
      // 添加夜间模式属性
      isLightMode: localStorage.getItem("theme-mode") === "light",
      
      // Home组件数据
      currentStep: 1,
      taskId: null,
      uploadedFilename: '',
      processingStatus: '初始化中...',
      statusInterval: null,
      conversionSuccess: false,
      videoUrl: '',
      errorMessage: '',
      videoError: null,
      
      // FileUpload组件数据
      file: null,
      isDragging: false,
      isUploading: false,
      uploadProgress: 0,
      error: null,
      
      // ConversionForm组件数据
      formData: {
        use_generated_script: true,
        script_style: '标准',
        target_audience: '通用',
        total_duration: '中等',
        subject: '通用',
        slide_duration: 5,
        lang: 'zh-cn',
        // 新增参数
        speed: 50,
        vcn: 'x4_mingge'
      }
    };
  },
  mounted() {
    // 添加主题监听
    this.checkThemeMode();
    window.addEventListener("storage", this.checkThemeMode);
    window.addEventListener("themeChange", this.checkThemeMode);
  },
  beforeUnmount() {
    // 清理interval
    if (this.statusInterval) {
      clearInterval(this.statusInterval);
    }
    
    // 移除主题监听
    window.removeEventListener("storage", this.checkThemeMode);
    window.removeEventListener("themeChange", this.checkThemeMode);
  },
  methods: {
    // 添加主题检测方法
    checkThemeMode() {
      this.isLightMode = localStorage.getItem("theme-mode") === "light";
    },
    
    // 下载视频方法
    downloadVideo() {
      if (!this.videoUrl) return;
      
      // 创建一个临时的隐藏a标签
      const downloadLink = document.createElement('a');
      downloadLink.href = `${this.videoUrl}?download=true`;
      downloadLink.setAttribute('download', `${this.uploadedFilename.split('.')[0]}.mp4`);
      downloadLink.setAttribute('target', '_blank');
      
      // 添加到文档中并触发点击
      document.body.appendChild(downloadLink);
      downloadLink.click();
      
      // 移除临时元素
      setTimeout(() => {
        document.body.removeChild(downloadLink);
      }, 100);
    },
    
    // FileUpload组件方法
    handleFileChange(event) {
      const selectedFile = event.target.files[0];
      if (selectedFile) {
        this.validateAndSetFile(selectedFile);
      }
    },
    handleFileDrop(event) {
      this.isDragging = false;
      const droppedFile = event.dataTransfer.files[0];
      if (droppedFile) {
        this.validateAndSetFile(droppedFile);
      }
    },
    validateAndSetFile(file) {
      // 检查文件类型
      const validTypes = ['application/vnd.ms-powerpoint', 'application/vnd.openxmlformats-officedocument.presentationml.presentation'];
      const fileExtension = file.name.split('.').pop().toLowerCase();
      
      if (!validTypes.includes(file.type) && !['ppt', 'pptx'].includes(fileExtension)) {
        this.error = '只支持PPT文件(.ppt 或 .pptx)';
        return;
      }
      
      // 检查文件大小 (50MB限制)
      if (file.size > 50 * 1024 * 1024) {
        this.error = '文件大小不能超过50MB';
        return;
      }
      
      this.file = file;
      this.error = null;
      this.uploadFile();
    },
    uploadFile() {
      this.isUploading = true;
      this.uploadProgress = 0;
      
      const formData = new FormData();
      formData.append('file', this.file);
      
      apiClient.post('/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        onUploadProgress: progressEvent => {
          this.uploadProgress = (progressEvent.loaded / progressEvent.total) * 100;
        }
      })
      .then(response => {
        this.isUploading = false;
        // 处理上传成功
        this.handleFileUploaded({
          task_id: response.data.task_id,
          filename: this.file.name
        });
      })
      .catch(error => {
        this.isUploading = false;
        this.error = error.response?.data?.error || '上传失败，请重试';
        this.file = null;
      });
    },
    
    // ConversionForm组件方法
    toggleScriptOptions() {
      // 当切换AI生成选项时，可以在这里添加额外逻辑
    },
    submitForm() {
      this.startConversion(this.formData);
    },
    
    // Home组件方法
    handleFileUploaded(response) {
      this.taskId = response.task_id;
      this.uploadedFilename = response.filename;
      this.currentStep = 2;
    },
    startConversion(params) {
      this.currentStep = 3;
      
      // 发送转换请求
      apiClient.post(`/convert/${this.taskId}`, params)
        .then(() => {
          // 启动状态轮询
          this.checkTaskStatus();
        })
        .catch(error => {
          this.handleError(error);
        });
    },
    checkTaskStatus() {
      // 清除之前的interval
      if (this.statusInterval) {
        clearInterval(this.statusInterval);
      }
      
      // 设置新的轮询
      this.statusInterval = setInterval(() => {
        apiClient.get(`/tasks/${this.taskId}`)
          .then(response => {
            this.processingStatus = response.data.status;
            
            if (response.data.status === 'completed') {
              clearInterval(this.statusInterval);
              this.conversionSuccess = true;
              // 修复：解决URL中路径重复问题
              let videoUrl = response.data.video_url || '';
              
              // 检查是否已包含基础路径
              const baseURLWithoutSlash = apiClient.defaults.baseURL.replace(/\/$/, '');
              if (videoUrl.includes('/api/pptvideo') && videoUrl.startsWith('/')) {
                // 如果URL已经包含基础路径且以斜杠开头，直接使用
                this.videoUrl = videoUrl;
              } else if (videoUrl.startsWith('http')) {
                // 如果是完整的HTTP URL，直接使用
                this.videoUrl = videoUrl;
              } else if (videoUrl.startsWith('/')) {
                // 如果以斜杠开头但不包含基础路径
                this.videoUrl = `${baseURLWithoutSlash}${videoUrl}`;
              } else if (videoUrl) {
                // 如果不以斜杠开头且不为空
                this.videoUrl = `${baseURLWithoutSlash}/${videoUrl}`;
              }
              
              this.currentStep = 4;
            } else if (response.data.status === 'failed') {
              clearInterval(this.statusInterval);
              this.conversionSuccess = false;
              this.errorMessage = response.data.error || '转换过程中出现错误';
              this.currentStep = 4;
            }
          })
          .catch(error => {
            clearInterval(this.statusInterval);
            this.handleError(error);
          });
      }, 3000); // 每3秒检查一次
    },
    handleError(error) {
      this.conversionSuccess = false;
      this.errorMessage = error.response?.data?.error || '发生未知错误';
      this.currentStep = 4;
    },
    resetForm() {
      this.currentStep = 1;
      this.taskId = null;
      this.uploadedFilename = '';
      this.processingStatus = '初始化中...';
      this.conversionSuccess = false;
      this.videoUrl = '';
      this.errorMessage = '';
      this.file = null;
      this.isDragging = false;
      this.isUploading = false;
      this.uploadProgress = 0;
      this.error = null;
      this.formData = {
        use_generated_script: true,
        script_style: '标准',
        target_audience: '通用',
        total_duration: '中等',
        subject: '通用',
        slide_duration: 5,
        lang: 'zh-cn',
        // 新增参数
        speed: 50,
        vcn: 'x4_mingge'
      };
      
      if (this.statusInterval) {
        clearInterval(this.statusInterval);
        this.statusInterval = null;
      }
    },
    // 新增：处理视频错误
    handleVideoError(e) {
      this.videoError = `视频无法播放 (错误代码: ${e.target.error ? e.target.error.code : '未知'})`;
      console.error('视频加载错误:', e);
    }
  }
};
</script>

<style scoped>
/* Home组件样式 - 夜间模式(默认) */
.home {
  width: 100%;
  height: 100%;
  padding: 20px;
  overflow-y: auto;
  box-sizing: border-box;
  background-color: #2d2339; /* 更改为深紫色背景 */
  color: #e6ecf5; /* 亮色文本 */
  transition: background-color 0.3s, color 0.3s;
}

/* 日间模式 */
.home.light-mode {
  background-color: #fff9f0; /* 更改为温暖米色背景 */
  color: #593618; /* 深棕色文字 */
}

h1 {
  text-align: center;
  margin-bottom: 30px;
  color: #ff9e5e; /* 更改为橙色标题 - 夜间模式 */
  transition: color 0.3s;
}

.light-mode h1 {
  color: #d86500; /* 更改为深橙色标题 - 日间模式 */
}

.container {
  background: #3d2d4e; /* 更改为深紫色 - 夜间模式 */
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  padding: 30px;
  margin-bottom: 20px;
  transition: background-color 0.3s, box-shadow 0.3s;
}

.light-mode .container {
  background: #ffffff;
  box-shadow: 0 4px 12px rgba(244, 162, 89, 0.08); /* 更改为金黄色阴影 */
}

/* 其他样式保持不变 */
.steps {
  display: flex;
  justify-content: space-between;
  margin-bottom: 30px;
  position: relative;
}

.steps::before {
  content: '';
  position: absolute;
  top: 15px;
  left: 0;
  right: 0;
  height: 2px;
  background: rgba(255, 255, 255, 0.1); /* 夜间模式的淡线条 */
  z-index: 1;
  transition: background-color 0.3s;
}

.light-mode .steps::before {
  background: rgba(244, 162, 89, 0.2); /* 更改为半透明金黄色 */
}

.step {
  background: #3d2d4e; /* 更改为深紫色 - 夜间模式 */
  padding: 5px 15px;
  border-radius: 20px;
  border: 2px solid rgba(255, 255, 255, 0.1);
  position: relative;
  z-index: 2;
  color: #a0b0d0; /* 淡灰蓝色文字 */
  transition: all 0.3s;
}

.light-mode .step {
  background: #ffffff;
  border: 2px solid rgba(244, 162, 89, 0.2); /* 更改为半透明金黄色边框 */
  color: rgba(89, 54, 24, 0.6); /* 半透明深棕色 */
}

.step.active {
  border-color: #ff9e5e; /* 更改为橙色 */
  color: #ff9e5e; /* 更改为橙色 */
  font-weight: bold;
}

.light-mode .step.active {
  border-color: #d86500; /* 更改为深橙色 */
  color: #d86500; /* 更改为深橙色 */
}

.step-content {
  min-height: 300px;
}

.processing {
  text-align: center;
  padding: 40px 0;
}

.progress-bar {
  width: 100%;
  height: 10px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 5px;
  overflow: hidden;
  margin: 20px 0;
  transition: background-color 0.3s;
}

.light-mode .progress-bar {
  background: rgba(244, 162, 89, 0.1); /* 更改为半透明金黄色 */
}

.progress-animation {
  height: 100%;
  width: 30%;
  background: linear-gradient(90deg, #ff9e5e, #f4a259); /* 更改为橙金色渐变 */
  border-radius: 5px;
  animation: progressAnim 1.5s infinite ease-in-out;
}

@keyframes progressAnim {
  0% { margin-left: -30%; }
  100% { margin-left: 100%; }
}

.actions {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 20px;
}

.btn-primary, .btn-secondary, .btn-submit {
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  text-decoration: none;
  display: inline-block;
  transition: all 0.3s;
}

.btn-primary, .btn-submit {
  background: linear-gradient(135deg, #ff9e5e, #f4a259) !important; /* 更改为橙金色渐变 */
  color: #ffffff !important; /* 白色文字更可读 */
  border: none !important;
  box-shadow: 0 4px 15px rgba(255, 158, 94, 0.3); /* 更改为橙色阴影 */
}

.light-mode .btn-primary, .light-mode .btn-submit {
  box-shadow: 0 4px 15px rgba(244, 162, 89, 0.3); /* 更改为金黄色阴影 */
}

.btn-primary:hover, .btn-submit:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 158, 94, 0.5); /* 更改为橙色阴影 */
}

.light-mode .btn-primary:hover, .light-mode .btn-submit:hover {
  box-shadow: 0 6px 20px rgba(244, 162, 89, 0.5); /* 更改为金黄色阴影 */
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.1);
  color: #a0b0d0;
  border: 1px solid rgba(255, 158, 94, 0.2); /* 更改为半透明橙色边框 */
}

.light-mode .btn-secondary {
  background: rgba(244, 162, 89, 0.05); /* 更改为半透明金黄色背景 */
  color: #593618; /* 深棕色文字 */
  border: 1px solid rgba(244, 162, 89, 0.2); /* 更改为半透明金黄色边框 */
}

.success, .error {
  text-align: center;
  padding: 20px;
}

.error {
  color: #D32F2F;
}

/* FileUpload组件样式 */
.file-upload {
  margin-bottom: 20px;
}

h2 {
  margin-bottom: 15px;
  color: #ff9e5e; /* 更改为橙色 */
}

.light-mode h2 {
  color: #d86500; /* 更改为深橙色 */
}

.upload-area {
  border: 2px dashed rgba(255, 158, 94, 0.3); /* 更改为半透明橙色边框 */
  border-radius: 8px;
  padding: 40px;
  text-align: center;
  cursor: pointer;
  background-color: rgba(61, 45, 78, 0.4); /* 更改为半透明紫色背景 */
  transition: all 0.3s;
}

.light-mode .upload-area {
  border: 2px dashed rgba(244, 162, 89, 0.3); /* 更改为半透明金黄色边框 */
  background-color: rgba(255, 249, 240, 0.5); /* 更改为半透明米色背景 */
}

.upload-area:hover, .drag-over {
  border-color: #ff9e5e; /* 更改为橙色 */
  background-color: rgba(255, 158, 94, 0.05); /* 更改为半透明橙色背景 */
}

.light-mode .upload-area:hover, .light-mode .drag-over {
  border-color: #f4a259; /* 更改为金黄色 */
  background-color: rgba(244, 162, 89, 0.05); /* 更改为半透明金黄色背景 */
}

.file-icon {
  font-size: 48px;
  margin-bottom: 10px;
  display: block;
}

.upload-btn {
  background: linear-gradient(135deg, #ff9e5e, #f4a259); /* 更改为橙金色渐变 */
  color: #ffffff;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  display: inline-block;
  margin: 10px 0;
  font-weight: bold;
  transition: all 0.3s;
  border: none;
}

.upload-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(255, 158, 94, 0.3); /* 更改为橙色阴影 */
}

.light-mode .upload-btn:hover {
  box-shadow: 0 4px 15px rgba(244, 162, 89, 0.3); /* 更改为金黄色阴影 */
}

.upload-btn input {
  display: none;
}

.note {
  color: #a0b0d0;
  font-size: 14px;
  margin-top: 10px;
  transition: color 0.3s;
}

.light-mode .note {
  color: rgba(89, 54, 24, 0.7); /* 半透明深棕色 */
}

.uploading {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top-color: #ff9e5e; /* 更改为橙色 */
  animation: spin 1s ease infinite;
  margin-bottom: 15px;
}

.light-mode .spinner {
  border-top-color: #f4a259; /* 更改为金黄色 */
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-message {
  color: #ff8080;
  margin-top: 10px;
  padding: 10px;
  background: rgba(255, 0, 0, 0.1);
  border-radius: 4px;
  transition: all 0.3s;
}

.light-mode .error-message {
  color: #D32F2F;
  background: #FFEBEE;
}

/* ConversionForm组件样式 */
.conversion-form {
  margin-bottom: 30px;
}
.file-info{
  color: #a0b0d0;
  font-size: 14px;
  margin-bottom: 10px;
  transition: color 0.3s;
}

.light-mode .file-info {
  color: rgba(89, 54, 24, 0.7); /* 半透明深棕色 */
  background: rgba(244, 162, 89, 0.05); /* 更改为半透明金黄色背景 */
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 20px;
  font-weight: bold;
}

.form-group {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

.form-group label {
  flex: 0 0 180px;
  font-weight: bold;
  color: #a0b0d0;
  transition: color 0.3s;
}

.light-mode .form-group label {
  color: rgba(89, 54, 24, 0.8); /* 深一点的半透明深棕色 */
}

select, input[type="number"] {
  flex: 1;
  padding: 10px;
  background-color: rgba(61, 45, 78, 0.4); /* 更改为半透明紫色背景 */
  border: 1px solid rgba(255, 158, 94, 0.2); /* 更改为半透明橙色边框 */
  border-radius: 8px;
  color: #e6ecf5;
  font-size: 16px;
  transition: all 0.3s;
}

.light-mode select, .light-mode input[type="number"] {
  background-color: #ffffff;
  border: 1px solid rgba(244, 162, 89, 0.2); /* 更改为半透明金黄色边框 */
  color: #593618; /* 深棕色文字 */
}

select:focus, input[type="number"]:focus {
  border-color: #ff9e5e; /* 更改为橙色 */
  box-shadow: 0 0 0 2px rgba(255, 158, 94, 0.1); /* 更改为半透明橙色阴影 */
}

.light-mode select:focus, .light-mode input[type="number"]:focus {
  border-color: #f4a259; /* 更改为金黄色 */
  box-shadow: 0 0 0 2px rgba(244, 162, 89, 0.1); /* 更改为半透明金黄色阴影 */
}

.toggle-switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-label {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(61, 45, 78, 0.6); /* 更改为半透明紫色背景 */
  transition: .4s;
  border-radius: 34px;
}

.light-mode .toggle-label {
  background-color: rgba(244, 162, 89, 0.2); /* 更改为半透明金黄色背景 */
}

.toggle-label:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

input:checked + .toggle-label {
  background-color: #ff9e5e; /* 更改为橙色 */
}

.light-mode input:checked + .toggle-label {
  background-color: #f4a259; /* 更改为金黄色 */
}

input:checked + .toggle-label:before {
  transform: translateX(26px);
}

.script-options {
  border-left: 3px solid #ff9e5e; /* 更改为橙色 */
  padding-left: 20px;
  margin: 20px 0 20px 180px;
}

.light-mode .script-options {
  border-left: 3px solid #f4a259; /* 更改为金黄色 */
}

.form-actions {
  margin-top: 30px;
  text-align: center;
}

.btn-submit {
  background: linear-gradient(135deg, #ff9e5e, #f4a259); /* 更改为橙金色渐变 */
  color: white;
  padding: 12px 30px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  font-weight: bold;
}

.btn-submit:hover {
  background: linear-gradient(135deg, #f4a259, #ff9e5e); /* 反向渐变效果 */
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(255, 158, 94, 0.3); /* 更改为橙色阴影 */
}

.light-mode .btn-submit:hover {
  box-shadow: 0 4px 15px rgba(244, 162, 89, 0.3); /* 更改为金黄色阴影 */
}

/* VideoPlayer组件样式 */
.video-player {
  max-width: 800px;
  margin: 0 auto;
  margin-bottom: 20px;
}

video {
  width: 100%;
  border-radius: 8px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  background-color: #000;
  transition: box-shadow 0.3s;
}

.light-mode video {
  box-shadow: 0 10px 30px rgba(244, 162, 89, 0.1); /* 更改为金黄色阴影 */
}

/* 新增样式 */
.slider-container {
  display: flex;
  align-items: center;
  flex: 1;
}

.slider {
  flex: 1;
  height: 10px;
  -webkit-appearance: none;
  appearance: none;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 5px;
  outline: none;
  transition: background-color 0.3s;
}

.light-mode .slider {
  background: rgba(244, 162, 89, 0.1); /* 更改为半透明金黄色背景 */
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #ff9e5e; /* 更改为橙色 */
  cursor: pointer;
  transition: background-color 0.3s;
}

.light-mode .slider::-webkit-slider-thumb {
  background: #f4a259; /* 更改为金黄色 */
}

.slider-value {
  margin-left: 10px;
  min-width: 30px;
  text-align: center;
  font-weight: bold;
}

/* 添加自定义滚动条样式 */
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

/* 亮色模式滚动条(当父组件为亮色模式时) */
:deep(.light-mode) .home::-webkit-scrollbar-track {
  background: rgba(255, 249, 240, 0.5); /* 更改为半透明米色 */
}

:deep(.light-mode) .home::-webkit-scrollbar-thumb {
  background: rgba(244, 162, 89, 0.2); /* 更改为半透明金黄色 */
}

:deep(.light-mode) .home::-webkit-scrollbar-thumb:hover {
  background: rgba(244, 162, 89, 0.3); /* 更改为半透明金黄色 */
}
</style>