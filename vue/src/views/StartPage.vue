<template>
  <div class="container">
    <!-- 导航栏 -->
    <el-menu
        mode="horizontal"
        :default-active="activeIndex"
        @select="handleSelect"
        class="nav-menu"
    >
      <!-- 添加Logo -->
      <div class="logo-container">
        <span class="logo-icon">AI</span>
        <span class="logo-text">智课助教</span>
      </div>
      
      <el-menu-item index="1">首页</el-menu-item>
      <el-menu-item index="2">系统特色</el-menu-item>
      <el-menu-item index="3">核心功能</el-menu-item>
      <el-menu-item index="4">应用展示</el-menu-item>
      <el-menu-item index="5">关于我们</el-menu-item>
      
      <!-- 添加登录/退出按钮 -->
      <div class="nav-right">
        <template v-if="isLoggedIn">
          <span class="user-info">
            <el-avatar :size="24" class="user-avatar" src="../assets/img/s1.jpg"></el-avatar>
            {{ userRole }}
          </span>
          <el-button class="nav-button logout-button" size="small" @click="handleLogout">退出登录</el-button>
        </template>
        <template v-else>
          <el-button class="nav-button login-button" size="small" @click="goToLogin">登录</el-button>
        </template>
      </div>
    </el-menu>

    <!-- 内容区块 -->
    <section id="home" class="page-section">
      <div class="hero">
        <!-- 视频背景 -->
        <video autoplay muted loop class="background-video" @error="handleVideoError">
          <source src="../assets/teach.mp4" type="video/mp4" />
          您的浏览器不支持视频标签。
        </video>
        <!-- 遮罩层 -->
        <div class="overlay"></div>
        
        <!-- 粒子效果 -->
        <div class="particles">
          <div class="particle particle-1"></div>
          <div class="particle particle-2"></div>
          <div class="particle particle-3"></div>
          <div class="particle particle-4"></div>
          <div class="particle particle-5"></div>
          <div class="particle particle-6"></div>
        </div>
        
        <!-- 文字内容 -->
        <div class="hero-content">
          <div class="hero-badge">
            <span class="badge-icon"><el-icon><Monitor /></el-icon></span>
            <span>AI 技术驱动</span>
        </div>
          <h1 class="title">智能教育助手<br><span class="highlight">全新教学体验</span></h1>
          <p class="slogan">让AI为您的教学赋能 · 重新定义备课体验</p>
          
          <!-- 特点介绍 -->
          <div class="hero-features">
            <div class="hero-feature">
              <div class="feature-icon">
                <el-icon><Monitor /></el-icon>
              </div>
              <div class="feature-text">
                <div class="feature-title">数字人助教</div>
                <div class="feature-desc">智能对话，实时辅助</div>
              </div>
            </div>
            <div class="hero-feature">
              <div class="feature-icon">
                <el-icon><DocumentCopy /></el-icon>
              </div>
              <div class="feature-text">
                <div class="feature-title">PPT智能生成</div>
                <div class="feature-desc">一键制作，精美呈现</div>
              </div>
            </div>
            <div class="hero-feature">
              <div class="feature-icon">
                <el-icon><Connection /></el-icon>
              </div>
              <div class="feature-text">
                <div class="feature-title">智能备课</div>
                <div class="feature-desc">高效备课，减轻负担</div>
              </div>
            </div>
          </div>
          
          <!-- 按钮组 -->
          <div class="hero-buttons">
            <el-button class="start-button" @click="handleStartExperience" size="large">
              <span class="button-text">开始体验</span>
              <el-icon class="button-icon"><ArrowRight /></el-icon>
            </el-button>
            <el-button class="learn-button" @click="scrollToSection('features')" size="large">
              <span class="button-text">了解更多</span>
              <el-icon class="button-icon"><ArrowDown /></el-icon>
            </el-button>
          </div>
        </div>
        
        <!-- 浮动元素装饰 -->
        <div class="floating-elements">
          <div class="floating-icon icon-1"><el-icon><DataAnalysis /></el-icon></div>
          <div class="floating-icon icon-2"><el-icon><VideoCameraFilled /></el-icon></div>
          <div class="floating-icon icon-3"><el-icon><EditPen /></el-icon></div>
          <div class="floating-icon icon-4"><el-icon><PictureFilled /></el-icon></div>
          <div class="floating-shape shape-1"></div>
          <div class="floating-shape shape-2"></div>
          <div class="floating-shape shape-3"></div>
        </div>
        
        <!-- 高光效果 -->
        <div class="hero-highlight"></div>
      </div>
    </section>

    <!-- 系统特色 -->
    <section id="features" class="page-section tech-section dark-section">
      <div class="tech-grid"></div>
      <div class="tech-circles">
        <div class="circle circle-1"></div>
        <div class="circle circle-2"></div>
      </div>
      
      <div class="section-header">
        <h2 class="section-title">
          <span class="title-highlight">智能赋能</span>・<span>高效备课</span>
        </h2>
        <p class="section-subtitle">专为教育工作者打造的智能化AI助教工具</p>
      </div>
      
      <div class="features-wrapper">
        <div class="feature-card">
          <div class="feature-icon-wrapper">
            <el-icon><Avatar /></el-icon>
              </div>
          <h3>智能助教</h3>
          <p>基于大语言模型的智能助教，能够回答问题、生成内容，为教师提供全方位支持</p>
          <div class="feature-hover-effect"></div>
            </div>
        
        <div class="feature-card">
          <div class="feature-icon-wrapper">
            <el-icon><Document /></el-icon>
          </div>
          <h3>即时生成</h3>
          <p>一键生成教案、教学素材、PPT幻灯片等，大幅提升备课效率，让教学更加灵活多样</p>
          <div class="feature-hover-effect"></div>
        </div>
        
        <div class="feature-card">
          <div class="feature-icon-wrapper">
            <el-icon><DataAnalysis /></el-icon>
          </div>
          <h3>学情分析</h3>
          <p>智能分析学生学习数据，生成个性化报告，助力教师精准把握学生学习状况</p>
          <div class="feature-hover-effect"></div>
        </div>
        
        <div class="feature-card">
          <div class="feature-icon-wrapper">
            <el-icon><Connection /></el-icon>
          </div>
          <h3>资源整合</h3>
          <p>自动整合优质教学资源，为教师提供丰富的参考素材，打造高质量教学内容</p>
          <div class="feature-hover-effect"></div>
        </div>
      </div>
      
      <div class="tech-stats">
        <div class="stat-item">
          <div class="stat-number">98<span class="stat-symbol">%</span></div>
          <div class="stat-label">用户满意度</div>
        </div>
        <div class="stat-item">
          <div class="stat-number">10<span class="stat-symbol">k+</span></div>
          <div class="stat-label">活跃教师</div>
        </div>
        <div class="stat-item">
          <div class="stat-number">24<span class="stat-symbol">/7</span></div>
          <div class="stat-label">智能服务</div>
        </div>
      </div>
    </section>
    
    <!-- 核心功能 -->
    <section id="core-features" class="page-section tech-section dark-section">
      <div class="tech-grid"></div>
      
      <div class="section-header">
        <h2 class="section-title">
          <span class="title-highlight">全方位</span>教学解决方案
        </h2>
        <p class="section-subtitle">为您提供从备课到课后的完整智能教学工具链</p>
      </div>
      
      <div class="core-features-container">
        <div class="core-feature">
          <div class="feature-number">01</div>
          <div class="feature-content">
            <h3>教学设计自动化</h3>
            <p>通过与大模型的互动，为教师自动生成高质量教学设计和教学内容，包括教学活动安排、时间分配、教学目标和预期成果等。系统会根据课程标准和教学内容智能推荐最佳教学方法。</p>
            <div class="feature-tag-list">
              <div class="feature-tag">智能互动</div>
              <div class="feature-tag">个性化推荐</div>
              <div class="feature-tag">教学优化</div>
            </div>
          </div>
          <div class="feature-image">
            <img src="../assets/img/s1.jpg" alt="教学设计自动化">
            <div class="image-overlay"></div>
          </div>
        </div>
        
        <div class="core-feature reverse">
          <div class="feature-number">02</div>
          <div class="feature-content">
            <h3>多媒体教学资源生成</h3>
            <p>根据教学设计的要求，系统能自动生成相关的图片、视频等多媒体材料，支持教师直接使用或作为参考资料。资源生成过程中会考虑教学对象的年龄、认知水平等因素，保证资源的适用性。</p>
            <div class="feature-tag-list">
              <div class="feature-tag">一键生成</div>
              <div class="feature-tag">多媒体资源</div>
              <div class="feature-tag">自定义调整</div>
            </div>
          </div>
          <div class="feature-image">
            <img src="../assets/img/s1.jpg" alt="多媒体资源生成">
            <div class="image-overlay"></div>
          </div>
        </div>
        
        <div class="core-feature">
          <div class="feature-number">03</div>
          <div class="feature-content">
            <h3>智能练习题生成</h3>
            <p>针对课程内容，系统能自动生成不同类型和难度的练习题目，包括选择题、填空题、简答题等，用于课后复习或在线测试。每道题目都配有详细的解析和参考答案，并支持自动判卷和学情分析。</p>
            <div class="feature-tag-list">
              <div class="feature-tag">多类型题目</div>
              <div class="feature-tag">难度可控</div>
              <div class="feature-tag">自动判卷</div>
            </div>
          </div>
          <div class="feature-image">
            <img src="../assets/img/s1.jpg" alt="练习题生成">
            <div class="image-overlay"></div>
          </div>
        </div>
        
        <div class="core-feature reverse">
          <div class="feature-number">04</div>
          <div class="feature-content">
            <h3>学情分析与个性化推荐</h3>
            <p>通过分析学生的历史学习记录（如作业成绩、在线学习行为等），评估学生对知识点的掌握情况，并推荐个性化的学习资源。系统还会自动生成学情报告，帮助教师了解班级整体状况和个体学习差异。</p>
            <div class="feature-tag-list">
              <div class="feature-tag">数据分析</div>
              <div class="feature-tag">个性化推荐</div>
              <div class="feature-tag">学情报告</div>
            </div>
          </div>
          <div class="feature-image">
            <img src="../assets/img/s1.jpg" alt="学情分析">
            <div class="image-overlay"></div>
          </div>
        </div>
      </div>
    </section>

    <!-- 应用展示 -->
    <section id="demo" class="page-section tech-section dark-section">
      <div class="tech-grid"></div>
      <div class="tech-circles">
        <div class="circle circle-1"></div>
        <div class="circle circle-2"></div>
      </div>
      
      <div class="section-header">
        <h2 class="section-title">
          <span class="title-highlight">应用</span>展示
        </h2>
        <p class="section-subtitle">体验我们的核心AI教学应用</p>
      </div>
      
      <!-- 数字人小助手演示 -->
      <div class="demo-wrapper">
        <div class="digital-assistant-demo">
          <div class="demo-header">
            <div class="demo-title">
              <el-icon><Avatar /></el-icon>
              <span>数字人小助手</span>
            </div>
            <div class="demo-controls">
              <el-tooltip content="运行程序" placement="top">
                <el-button type="primary" class="run-program-button" @click="runExe">
                  <el-icon><VideoPlay /></el-icon>
                  运行程序
                </el-button>
              </el-tooltip>
              <el-button type="text" class="demo-control-button">
                <el-icon><RefreshRight /></el-icon>
              </el-button>
              <el-button type="text" class="demo-control-button">
                <el-icon><FullScreen /></el-icon>
              </el-button>
            </div>
          </div>
          <div class="demo-content">
            <div class="digital-human">
              <div class="digital-human-wrapper">
                <img src="../assets/img/study.png" alt="数字人小助手">
                <div class="digital-human-status">
                  <div class="pulse"></div>
                  <span>AI助手在线</span>
                </div>
              </div>
            </div>
            <div class="assistant-chat">
              <div class="chat-messages">
                <div class="message assistant">
                  <div class="message-avatar">
                    <el-avatar :size="36" src="../assets/img/study.png"></el-avatar>
                  </div>
                  <div class="message-bubble">
                    <div class="message-content">您好，我是您的AI教学助手。我可以帮您设计课程、生成教学资源、分析学情数据。今天有什么可以帮助您的吗？</div>
                    <div class="message-time">09:30</div>
                  </div>
                </div>
                <div class="message user">
                  <div class="message-bubble">
                    <div class="message-content">请帮我设计一节关于光合作用的生物课</div>
                    <div class="message-time">09:31</div>
                  </div>
                  <div class="message-avatar">
                    <el-avatar :size="36" src="../assets/img/s1.jpg"></el-avatar>
                  </div>
                </div>
                <div class="message assistant typing">
                  <div class="message-avatar">
                    <el-avatar :size="36" src="../assets/img/study.png"></el-avatar>
                  </div>
                  <div class="message-bubble">
                    <div class="message-content">正在设计课程内容<span class="dot-typing"></span></div>
                  </div>
                </div>
              </div>
              <div class="chat-input">
                <el-input placeholder="输入您的问题..." class="message-input"></el-input>
                <el-button class="send-button" type="primary" circle>
                  <el-icon><Position /></el-icon>
                </el-button>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- PPT智能讲解演示 -->
      <div class="demo-wrapper reverse">
        <div class="ppt-demo">
          <div class="demo-header">
            <div class="demo-title">
              <el-icon><Document /></el-icon>
              <span>PPT智能讲解</span>
            </div>
            <div class="demo-controls">
              <el-button type="text" class="demo-control-button">
                <el-icon><RefreshRight /></el-icon>
              </el-button>
              <el-button type="text" class="demo-control-button">
                <el-icon><FullScreen /></el-icon>
              </el-button>
            </div>
          </div>
          <div class="demo-content">
            <div class="ppt-preview">
              <div class="ppt-slide">
                <img src="../assets/img/s1.jpg" alt="PPT幻灯片">
                <div class="slide-indicator">
                  <span class="current">1</span> / <span class="total">10</span>
                </div>
              </div>
              <div class="ppt-controls">
                <el-button class="control-button" size="small" circle>
                  <el-icon><ArrowLeft /></el-icon>
                </el-button>
                <el-button class="control-button primary" type="primary">
                  <el-icon><VideoPlay /></el-icon> 智能讲解
                </el-button>
                <el-button class="control-button" size="small" circle>
                  <el-icon><ArrowRight /></el-icon>
                </el-button>
              </div>
            </div>
            <div class="ppt-script">
              <div class="script-header">
                <el-icon><Reading /></el-icon>
                <span>AI生成讲稿</span>
              </div>
              <div class="script-content">
                <p>从这张幻灯片可以看出，光合作用是植物利用光能将二氧化碳和水转化为有机物和氧气的过程。这个过程主要分为光反应和暗反应两个阶段...</p>
                <p>光反应发生在叶绿体的类囊体膜上，需要光的参与，主要是将光能转化为化学能，并产生氧气；而暗反应则发生在叶绿体的基质中，不直接需要光，主要是利用光反应产生的ATP和NADPH，将二氧化碳转化为有机物。</p>
                <p>让我们一起来分析这个过程的关键步骤和影响因素...</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      

    </section>

    <!-- 关于我们 -->
    <section id="about" class="page-section tech-section dark-section">
      <div class="tech-grid"></div>
      <div class="tech-circles">
        <div class="circle circle-3"></div>
        <div class="circle circle-4"></div>
      </div>
      
      <div class="section-header">
        <h2 class="section-title">
          <span class="title-highlight">专业团队</span>・<span>用心服务</span>
        </h2>
        <p class="section-subtitle">AI教育创新团队，致力于为教育赋能</p>
      </div>
      
      <div class="about-container">
        <div class="about-card">
          <div class="about-icon-wrapper">
            <el-icon><School /></el-icon>
          </div>
          <h3>我们的团队</h3>
      <div class="about-description">
        <p>我们位于中国石油大学（华东）唐岛湾校区，是一家专注于教育AI技术研发的创新团队。</p>
            <p>团队由AI技术专家、教育学专家和资深教师组成，致力于将先进的AI技术应用到教育领域。</p>
          </div>
          <div class="card-decoration"></div>
      </div>
      
        <div class="about-card">
          <div class="about-icon-wrapper">
            <el-icon><Aim /></el-icon>
          </div>
          <h3>我们的使命</h3>
          <div class="about-description">
            <p>利用AI技术赋能教育，提升教师备课效率，丰富教学内容，精准分析学情。</p>
            <p>为师生创造更加高效、个性化的教与学体验，助力教育数字化转型。</p>
          </div>
          <div class="card-decoration"></div>
        </div>
      </div>
      
      <div class="map-container">
        <div class="map-header">
          <div class="map-title">
            <el-icon><Location /></el-icon>
            <span>公司地址</span>
          </div>
          <el-tooltip content="在新标签页打开地图" placement="top">
            <el-button class="map-button" size="small">
              <el-icon><Link /></el-icon>
            </el-button>
          </el-tooltip>
        </div>
        <div class="map-wrapper">
        <MapContainer />
        </div>
      </div>
      
      <div class="contact-info">
        <div class="contact-item">
          <el-icon><Phone /></el-icon>
          <span>联系电话: 010-12345678</span>
        </div>
        <div class="contact-item">
          <el-icon><Message /></el-icon>
          <span>邮箱: contact@aiteach.com</span>
        </div>
        <div class="contact-item">
          <el-icon><Link /></el-icon>
          <span>官网: www.aiteach.com</span>
        </div>
      </div>
      
      <div class="footer">
        <div class="footer-content">
          <div class="footer-logo">
            <span class="logo-icon">AI</span>
            <span class="logo-text">智课助教</span>
          </div>
          <div class="footer-text">Copyright © 2023-2024 AI智能教育. All Rights Reserved.</div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import MapContainer from '@/views/main/MapContainer.vue';

export default {
  name: "StartPage",
  components: {
    MapContainer
  },
  setup() {
    const router = useRouter();
    const activeIndex = ref('1');
    const isLoggedIn = ref(false);
    const userRole = ref("教师用户");
    const videoPlayers = ref([]);
    const currentVideoIndex = ref(0);
    
    
    
    // 导航菜单选择
    const handleSelect = (key) => {
      switch(key) {
        case '1':
          scrollToSection('home');
          break;
        case '2':
          scrollToSection('features');
          break;
        case '3':
          scrollToSection('core-features');
          break;
        case '4':
          scrollToSection('demo');
          break;
        case '5':
          scrollToSection('about');
          break;
      }
    };
    
    // 滚动到指定区域
    const scrollToSection = (sectionId) => {
      const section = document.getElementById(sectionId);
      if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
      }
    };
    
    // 处理开始体验按钮
    const handleStartExperience = () => {
      router.push('/auth/login');
    };
    
    // 跳转到登录页面
    const goToLogin = () => {
      router.push('/auth/login');
    };
    
    // 退出登录
    const handleLogout = () => {
      // 实际项目中这里会清除token等登录信息
      isLoggedIn.value = false;
      ElMessage.success('退出登录成功');
      router.push('/auth/login');
    };
    
    // 运行程序功能
    const runExe = async () => {
      try {
        ElMessage.info('正在执行程序，请稍后...');
        
        // 使用变量定义API基础URL，便于修改
        const apiBaseUrl = 'http://localhost:3000';
        
        const response = await axios.post(`${apiBaseUrl}/api/run-exe`, {
          path: 'D:/Desktop/比赛/服务外包+网络技术挑战赛/最新版工程2/server/test2/AI.exe'  // 使用正斜杠替代反斜杠
        });
        
        console.log('程序执行成功:', response.data);
        
        if (response.data.success) {
          ElMessage.success('程序执行成功');
        } else {
          ElMessage.warning('程序执行完成，但可能有警告');
        }
      } catch (error) {
        console.error('执行失败:', error);
        ElMessage.error('程序执行失败: ' + (error.response?.data?.error || error.message));
      }
    };
    
    return {
      activeIndex,
      isLoggedIn,
      userRole,
      videoPlayers,
      handleSelect,
      scrollToSection,
      handleStartExperience,
      goToLogin,
      handleLogout,
      runExe
    };
  }
};
</script>

<style lang="scss" scoped>
.container {
  scroll-behavior: smooth;
  background: linear-gradient(135deg, #f5f7fa, #e9ecef); /* 更柔和的背景色 */
  color: #333;
  overflow-x: hidden;
  font-family: 'Nunito', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

// 导航栏样式优化
.nav-menu {
  position: fixed;
  width: 100%;
  z-index: 1000;
  background-color: rgba(255, 255, 255, 0.95); /* 更柔和的背景色 */
  backdrop-filter: blur(15px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  display: flex;
  justify-content: flex-start;
  height: 68px;
  padding: 0 20px;
  box-shadow: 0 5px 25px rgba(0, 0, 0, 0.05);
}

// Logo 样式
.logo-container {
  display: flex;
  align-items: center;
  margin-right: 40px;
  margin-left: 20px;
  padding: 0 10px;
}

.logo-icon {
  background: linear-gradient(135deg, #4a55a2, #7895cb); /* 较醒目但不刺眼的渐变 */
  color: #ffffff;
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 18px;
  margin-right: 12px;
  box-shadow: 0 0 20px rgba(120, 149, 203, 0.3);
}

.logo-text {
  font-size: 22px;
  font-weight: 700;
  letter-spacing: 1px;
  background: linear-gradient(135deg, #2c3e50, #4a55a2); /* 更鲜明的文字渐变 */
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

// 右侧导航
.nav-right {
  position: absolute;
  right: 20px;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  align-items: center;
  gap: 15px;
}

.user-info {
  color: #4a55a2;
  font-size: 14px;
  background: rgba(120, 149, 203, 0.1);
  padding: 6px 14px 6px 6px;
  border-radius: 50px;
  display: flex;
  align-items: center;
  gap: 8px;
  border: 1px solid rgba(120, 149, 203, 0.2);
  transition: all 0.3s ease;
  
  &:hover {
    background: rgba(120, 149, 203, 0.15);
    border-color: rgba(120, 149, 203, 0.3);
  }
  
  .user-avatar {
    border: 2px solid rgba(120, 149, 203, 0.5);
  }
}

.nav-button {
  border-radius: 50px;
  padding: 10px 20px;
  font-weight: 500;
  transition: all 0.3s ease;
  border: none;
}

.login-button {
  background: linear-gradient(135deg, #4a55a2, #7895cb); /* 品牌色调的按钮渐变 */
  color: #ffffff;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(120, 149, 203, 0.3);
  }
  
  &:active {
    transform: translateY(0);
  }
}

.logout-button {
  background: rgba(255, 78, 78, 0.1);
  color: #ff4e4e;
  border: 1px solid rgba(255, 78, 78, 0.3);
  
  &:hover {
    background: rgba(255, 78, 78, 0.2);
    transform: translateY(-2px);
  }
}

// 菜单项样式增强
:deep(.el-menu-item) {
  font-size: 16px;
  margin: 0 5px;
  color: #4a55a2; /* 品牌色调 */
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  height: 68px;
  line-height: 68px;
  padding: 0 16px;

  &:hover {
    color: #7895cb;
    background: transparent !important;
    transform: translateY(-2px);

    &::after {
      width: 30%;
      opacity: 1;
    }
  }

  // 激活状态指示器
  &.is-active {
    color: #4a55a2;
    font-weight: 500;

    &::after {
      content: '';
      position: absolute;
      bottom: 15px;
      left: 50%;
      transform: translateX(-50%);
      width: 60%;
      height: 3px;
      background: linear-gradient(90deg, transparent, #4a55a2, transparent);
      border-radius: 3px;
      opacity: 1;
      transition: all 0.3s ease;
    }
  }
  
  &::after {
    content: '';
    position: absolute;
    bottom: 15px;
    left: 50%;
    transform: translateX(-50%);
    width: 0;
    height: 3px;
    background: linear-gradient(90deg, transparent, #7895cb, transparent);
    border-radius: 3px;
    opacity: 0;
    transition: all 0.3s ease;
  }
}

// 英雄区样式优化
.hero {
  position: relative;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  overflow: hidden;

  .background-video {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    z-index: 0;
  }
  
  .overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, rgba(41, 65, 122, 0.8), rgba(20, 30, 70, 0.75)); /* 深沉大气的蓝色渐变 */
    z-index: 1;
    
    &::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: url('data:image/svg+xml;utf8,<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><rect width="100" height="100" fill-opacity="0"/><rect width="1" height="1" fill="%23ffffff" fill-opacity="0.03" x="30" y="40"/><rect width="1" height="1" fill="%23ffffff" fill-opacity="0.03" x="70" y="60"/><rect width="1" height="1" fill="%23ffffff" fill-opacity="0.03" x="45" y="30"/><rect width="1" height="1" fill="%23ffffff" fill-opacity="0.03" x="60" y="80"/><rect width="1" height="1" fill="%23ffffff" fill-opacity="0.03" x="20" y="75"/><rect width="1" height="1" fill="%23ffffff" fill-opacity="0.03" x="80" y="20"/><rect width="1" height="1" fill="%23ffffff" fill-opacity="0.03" x="22" y="22"/><rect width="1" height="1" fill="%23ffffff" fill-opacity="0.03" x="90" y="40"/><rect width="1" height="1" fill="%23ffffff" fill-opacity="0.03" x="10" y="60"/><rect width="1" height="1" fill="%23ffffff" fill-opacity="0.03" x="50" y="50"/></svg>');
      background-size: 500px 500px;
      opacity: 0.4;
      z-index: -1;
    }
  }

  .hero-highlight {
    position: absolute;
    top: -200px;
    left: -200px;
    width: 400px;
    height: 400px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(118, 203, 255, 0.15) 0%, rgba(118, 203, 255, 0) 70%); /* 柔和的蓝色高光 */
    z-index: 1;
    animation: pulse-highlight 8s ease-in-out infinite alternate;
  }
  
  &::after {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    width: 100%;
    height: 100%;
    background: radial-gradient(circle at top right, rgba(97, 205, 255, 0.07) 0%, transparent 60%); /* 淡雅的顶部光晕 */
    z-index: 0;
  }
  
  &::before {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: radial-gradient(circle at bottom left, rgba(76, 145, 255, 0.07) 0%, transparent 60%); /* 协调的底部光晕 */
    z-index: 0;
  }
}

.hero-content {
  text-align: center;
  color: white;
  z-index: 2;
  animation: fadeInUp 1.2s ease-out;
  max-width: 1000px;
  padding: 0 20px;
  position: relative;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3); /* 添加文字阴影增强可读性 */
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.15); /* 高雅的徽章背景 */
  color: #ffffff; /* 明亮的徽章文字颜色 */
  font-size: 16px;
  font-weight: 600;
  padding: 8px 24px 8px 16px;
  border-radius: 50px;
  margin-bottom: 30px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.15);
  transform: translateY(-20px);
  opacity: 0;
  animation: fadeInDown 0.8s ease forwards;
  animation-delay: 0.2s;
  
  .badge-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.2); /* 协调的图标背景 */
    width: 28px;
    height: 28px;
    border-radius: 50%;
    margin-right: 10px;
    
    i {
      font-size: 16px;
    }
  }
}

.title {
  font-size: 4.8rem;
  line-height: 1.2;
  margin-bottom: 30px;
  font-weight: 800;
  color: #ffffff;
  text-shadow: 0 5px 30px rgba(0, 0, 0, 0.4); /* 增强文字阴影 */
  transform: translateY(-20px);
  opacity: 0;
  animation: fadeInDown 0.8s ease forwards;
  animation-delay: 0.4s;
  letter-spacing: -1px;
  
  @media (max-width: 768px) {
    font-size: 3.5rem;
  }
  
  @media (max-width: 576px) {
    font-size: 2.8rem;
  }
  
  .highlight {
    color: #a8d1ff; /* 高亮文字颜色 */
    position: relative;
    text-shadow: 0 0 20px rgba(118, 203, 255, 0.8); /* 增强高亮部分的发光效果 */
    
    &::after {
      content: '';
      position: absolute;
      bottom: 5px;
      left: 0;
      width: 100%;
      height: 10px;
      background: rgba(118, 203, 255, 0.3); /* 增加高亮下划线的不透明度 */
      z-index: -1;
      border-radius: 10px;
    }
  }
}

.slogan {
  font-size: 1.5rem;
  margin-bottom: 40px;
  opacity: 0;
  transform: translateY(-20px);
  animation: fadeInDown 0.8s ease forwards;
  animation-delay: 0.6s;
  color: rgba(255, 255, 255, 0.95);
  letter-spacing: 1px;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3); /* 添加文字阴影增强可读性 */
}
  
.hero-features {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin: 50px 0;
  flex-wrap: wrap;
  opacity: 0;
  transform: translateY(20px);
  animation: fadeInUp 0.8s ease forwards;
  animation-delay: 0.8s;
}
  
.hero-feature {
  display: flex;
  align-items: center;
  gap: 16px;
  background: rgba(41, 65, 122, 0.35); /* 更协调的特性卡片背景 */
  padding: 20px;
  border-radius: 20px;
  border: 1px solid rgba(118, 203, 255, 0.2);
  transition: all 0.4s ease;
  backdrop-filter: blur(10px);
  min-width: 240px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  text-align: left;
  
  &:hover {
    transform: translateY(-5px);
    background: rgba(52, 82, 150, 0.4); /* 更深沉的悬停背景 */
    border-color: rgba(118, 203, 255, 0.4);
    box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2), 0 0 15px rgba(118, 203, 255, 0.2);
    
    .feature-icon {
      background: rgba(118, 203, 255, 0.2);
      border-color: rgba(118, 203, 255, 0.6);
      transform: scale(1.1) rotate(10deg);
    }
  }
  
  .feature-icon {
    width: 50px;
    height: 50px;
    border-radius: 15px;
    background: rgba(118, 203, 255, 0.1);
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid rgba(118, 203, 255, 0.3);
    transition: all 0.4s ease;
    
    i {
      font-size: 24px;
      color: #ffffff;
    }
  }
  
  .feature-text {
    flex: 1;
  }
  
  .feature-title {
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 5px;
    color: #ffffff;
  }
  
  .feature-desc {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.7);
  }
}
  
.hero-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 20px;
  opacity: 0;
  transform: translateY(20px);
  animation: fadeInUp 0.8s ease forwards;
  animation-delay: 1s;
  
  @media (max-width: 576px) {
    flex-direction: column;
    align-items: center;
  }
}
  
.start-button {
  background: linear-gradient(135deg, #7895cb, #4a55a2); /* 更柔和的按钮渐变 */
  border: none;
  color: #ffffff;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  padding: 16px 32px;
  font-size: 18px;
  font-weight: 700;
  border-radius: 50px;
  box-shadow: 0 10px 30px rgba(120, 149, 203, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  position: relative;
  overflow: hidden;
    
  &::before {
      content: '';
      position: absolute;
      top: -50%;
      left: -50%;
      width: 200%;
      height: 200%;
    background: linear-gradient(
      transparent,
      rgba(255, 255, 255, 0.3),
      transparent
    );
      transform: rotate(45deg);
    transition: all 0.5s ease;
    opacity: 0;
  }
  
  .button-text {
    position: relative;
    z-index: 1;
  }
  
  .button-icon {
    position: relative;
    z-index: 1;
    transition: transform 0.4s ease;
    }
    
    &:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 40px rgba(97, 174, 201, 0.4); /* 更柔和的悬停阴影 */
    
    &::before {
      animation: button-shine 1.5s ease;
    }
    
    .button-icon {
      transform: translateX(5px);
    }
    }

    &:active {
    transform: scale(0.98);
    box-shadow: 0 5px 15px rgba(97, 174, 201, 0.3);
  }
}
  
.learn-button {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: #ffffff;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  padding: 16px 32px;
  font-size: 18px;
  font-weight: 700;
  border-radius: 50px;
  box-shadow: none;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  
  .button-text {
    position: relative;
    z-index: 1;
  }
  
  .button-icon {
    position: relative;
    z-index: 1;
    transition: transform 0.4s ease;
  }
  
  &:hover {
    background: rgba(255, 255, 255, 0.1);
    color: #ffffff;
    transform: translateY(-5px);
    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
    
    .button-icon {
      transform: translateY(5px);
    }
  }

  &:active {
    transform: scale(0.98);
  }
}

// 粒子效果
.particles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
  overflow: hidden;
  pointer-events: none;
}

.particle {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.5), 0 0 20px rgba(255, 255, 255, 0.3);
  
  &::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(255, 255, 255, 0.8) 0%, rgba(137, 114, 255, 0.5) 20%, transparent 70%);
  }
}

.particle-1 {
  width: 8px;
  height: 8px;
  top: 20%;
  left: 10%;
  animation: particle-float 20s linear infinite;
}

.particle-2 {
  width: 12px;
  height: 12px;
  top: 40%;
  left: 15%;
  animation: particle-float 25s linear infinite;
  animation-delay: -5s;
}

.particle-3 {
  width: 6px;
  height: 6px;
  top: 70%;
  left: 20%;
  animation: particle-float 15s linear infinite;
  animation-delay: -7s;
}

.particle-4 {
  width: 10px;
  height: 10px;
  top: 30%;
  right: 15%;
  animation: particle-float 22s linear infinite;
  animation-delay: -10s;
}

.particle-5 {
  width: 7px;
  height: 7px;
  top: 60%;
  right: 10%;
  animation: particle-float 18s linear infinite;
  animation-delay: -3s;
}

.particle-6 {
  width: 9px;
  height: 9px;
  top: 80%;
  right: 20%;
  animation: particle-float 23s linear infinite;
  animation-delay: -15s;
}

// 浮动形状
.floating-shape {
  position: absolute;
  border-radius: 30%;
  background: linear-gradient(135deg, rgba(137, 114, 255, 0.1), rgba(101, 87, 236, 0.05));
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(3px);
    opacity: 0;
  animation: fadeIn 0.5s ease forwards, floatShape 20s ease-in-out infinite;
  z-index: 1;
}

.shape-1 {
  width: 200px;
  height: 200px;
  top: 15%;
  left: 5%;
  transform: rotate(45deg);
  animation-delay: 2s, 2s;
}

.shape-2 {
  width: 150px;
  height: 150px;
  bottom: 20%;
  left: 10%;
  transform: rotate(30deg);
  animation-delay: 2.2s, 2.2s;
}

.shape-3 {
  width: 180px;
  height: 180px;
  top: 25%;
  right: 5%;
  transform: rotate(15deg);
  animation-delay: 2.4s, 2.4s;
}

// 波浪效果优化
.wave-container {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 120px;
  overflow: hidden;
  z-index: 3;
}

.wave {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 200%;
  height: 120px;
  background: url('data:image/svg+xml;utf8,<svg viewBox="0 0 1200 120" xmlns="http://www.w3.org/2000/svg"><path d="M0 0v46.29c47.79 22.2 103.59 32.17 158 28 70.36-5.37 136.33-33.31 206.8-37.5 73.84-4.36 147.54 16.88 218.2 35.26 69.27 18 138.3 24.88 209.4 13.08 36.15-6 69.85-17.84 104.45-29.34 22.11-7.35 42.65-17 68.26-17.09 16.83-.07 37.04 5.55 52.12 13.47V0z" fill-opacity=".15" fill="%2349F6DC"/></svg>');
  background-size: 1200px 120px;
  animation: waveAnimation 20s linear infinite;
}

.wave1 {
  animation-delay: 0s;
  z-index: 3;
  opacity: 0.7;
  height: 120px;
}

.wave2 {
  animation-delay: -5s;
  bottom: 10px;
  z-index: 2;
  opacity: 0.5;
  height: 100px;
}

// 浮动元素动画增强
.floating-elements {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1;
  pointer-events: none;
}

.floating-icon {
  position: absolute;
  width: 60px;
  height: 60px;
  background: rgba(17, 34, 64, 0.6);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(73, 246, 220, 0.15);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(5px);
  animation: floatIcon 10s ease-in-out infinite;
  opacity: 0;
  
  i {
    font-size: 28px;
    color: #49F6DC;
  }
}

.icon-1 {
  top: 20%;
  left: 15%;
  animation-delay: 0s;
  animation: floatIcon 10s ease-in-out infinite, fadeIn 0.5s ease forwards 1.2s;
}

.icon-2 {
  top: 60%;
  left: 10%;
  animation-delay: -3s;
  width: 50px;
  height: 50px;
  animation: floatIcon 12s ease-in-out infinite, fadeIn 0.5s ease forwards 1.4s;
}

.icon-3 {
  top: 25%;
  right: 15%;
  animation-delay: -5s;
  animation: floatIcon 9s ease-in-out infinite, fadeIn 0.5s ease forwards 1.6s;
}

.icon-4 {
  top: 70%;
  right: 10%;
  animation-delay: -7s;
  width: 50px;
  height: 50px;
  animation: floatIcon 11s ease-in-out infinite, fadeIn 0.5s ease forwards 1.8s;
}

// 新增动画关键帧
@keyframes button-shine {
  0% {
    opacity: 0;
    left: -50%;
  }
  50% {
    opacity: 0.5;
  }
  100% {
    opacity: 0;
    left: 150%;
  }
}

@keyframes scroll {
  0% {
    opacity: 1;
    top: 8px;
  }
  90% {
    opacity: 0;
    top: 25px;
  }
  100% {
    opacity: 0;
    top: 8px;
  }
}

@keyframes pulse-highlight {
  0% {
    transform: scale(1);
    opacity: 0.1;
  }
  50% {
    transform: scale(1.5);
    opacity: 0.15;
  }
  100% {
    transform: scale(1);
    opacity: 0.1;
  }
}

@keyframes particle-float {
  0% {
    transform: translateY(0) translateX(0) scale(1);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: translateY(-700px) translateX(300px) scale(0.2);
    opacity: 0;
  }
}

@keyframes floatShape {
  0% {
    transform: translateY(0) rotate(0deg);
  }
  25% {
    transform: translateY(-20px) rotate(5deg);
  }
  50% {
    transform: translateY(0) rotate(10deg);
  }
  75% {
    transform: translateY(20px) rotate(5deg);
  }
  100% {
    transform: translateY(0) rotate(0deg);
  }
}

@keyframes gradientShift {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

@keyframes shimmer {
  0% {
    box-shadow: 0 0 10px rgba(73, 246, 220, 0.3);
  }
  50% {
    box-shadow: 0 0 30px rgba(73, 246, 220, 0.5);
  }
  100% {
    box-shadow: 0 0 10px rgba(73, 246, 220, 0.3);
  }
}

.section-header {
  text-align: center;
  margin-bottom: 60px;
  position: relative;
}

.section-badge {
  display: none; /* 隐藏section-badge */
}

.section-title {
  font-size: 3.2rem;
  margin-bottom: 20px;
  color: #2c3e50; /* 深灰色为基础色 */
  display: inline-block;
  position: relative;
  padding-bottom: 15px;
  font-weight: 800;
  letter-spacing: -1px;
  text-transform: uppercase;

  .title-highlight {
    color: #4a55a2; /* 品牌蓝色作为强调色 */
    position: relative;
    
    &::after {
      content: '';
      position: absolute;
      bottom: 5px;
      left: 0;
      width: 100%;
      height: 8px;
      background: rgba(74, 85, 162, 0.1);
      z-index: -1;
      border-radius: 10px;
    }
  }

  &::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 100px;
    height: 4px;
    background: linear-gradient(90deg, rgba(74, 85, 162, 0.3), rgba(74, 85, 162, 0.8), rgba(74, 85, 162, 0.3));
    border-radius: 2px;
    animation: shimmer 4s infinite;
  }
  
  &::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    z-index: -1;
    color: rgba(74, 85, 162, 0.08); /* 淡蓝色的文字阴影效果 */
    transform: translateX(5px) translateY(5px);
    filter: blur(8px);
  }
}

.section-subtitle {
  font-size: 1.2rem;
  color: #666666; /* 更深的灰色 */
  max-width: 700px;
  margin: 0 auto;
}

.features-wrapper {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 30px;
  max-width: 1200px;
  margin: 0 auto 60px;
  padding: 0 20px;
}

.feature-card {
  background: #ffffff; /* 纯白色背景 */
  border: 1px solid rgba(0, 0, 0, 0.08); /* 极浅的灰色边框 */
  border-radius: 20px;
  padding: 30px;
  text-align: center;
  transition: all 0.4s ease;
  color: #333333;
  position: relative;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05); /* 轻微阴影 */
  z-index: 1;
  
  &:hover {
    transform: translateY(-10px);
    border-color: rgba(120, 149, 203, 0.3);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1), 0 0 20px rgba(120, 149, 203, 0.2); /* 更柔和的阴影 */
    
    .feature-icon-wrapper {
      background: rgba(74, 85, 162, 0.1);
      transform: scale(1.1);
      border-color: rgba(74, 85, 162, 0.3);
      
      i {
        color: #4a55a2;
        transform: scale(1.2);
      }
    }
    
    .feature-hover-effect {
      transform: scale(2.5);
      opacity: 0.1;
    }
  }
  
  h3 {
    font-size: 1.5rem;
    color: #2c3e50;
    margin: 20px 0 15px;
    position: relative;
    z-index: 2;
  }

  p {
    color: #666666;
    line-height: 1.6;
    margin-bottom: 0;
    position: relative;
    z-index: 2;
  }
}

.feature-icon-wrapper {
  width: 80px;
  height: 80px;
  border-radius: 20px;
  background: rgba(74, 85, 162, 0.08);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  transition: all 0.4s ease;
  border: 1px solid rgba(74, 85, 162, 0.15);
  position: relative;
  z-index: 2;
  
  i {
    font-size: 40px;
    color: #4a55a2;
    transition: all 0.4s ease;
  }
}

.feature-hover-effect {
  position: absolute;
  bottom: -50px;
  right: -50px;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.8) 0%, rgba(255, 255, 255, 0) 70%);
  opacity: 0;
  transition: all 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  z-index: 1;
}

.tech-stats {
  display: flex;
  justify-content: center;
  gap: 80px;
  margin: 70px 0 40px;
  flex-wrap: wrap;
}

.stat-item {
  text-align: center;
  position: relative;
  z-index: 1;
  background: #ffffff;
  padding: 25px 35px;
  border-radius: 20px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-10px);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
    border-color: rgba(74, 85, 162, 0.3);
    
    .stat-number {
      transform: translateY(-5px);
      color: #4a55a2;
    }
  }
}

.stat-number {
  font-size: 3.5rem;
  font-weight: 800;
  color: #4a55a2; /* 品牌蓝色 */
  margin-bottom: 10px;
  position: relative;
  display: inline-block;
  transition: all 0.3s ease;
  
  .stat-symbol {
    font-size: 2rem;
    font-weight: 400;
    color: #7895cb; /* 浅一点的蓝色 */
  }
}

.stat-label {
  color: #666666;
  font-size: 1.1rem;
  font-weight: 500;
}

.content-image {
  margin-top: 60px;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(64, 224, 208, 0.3);
  position: relative;
  
  .tech-image {
    width: 100%;
    height: auto;
    display: block;
    transition: transform 0.5s ease;
    
    &:hover {
      transform: scale(1.03);
    }
  }
}


.map-container {
  max-width: 1200px;
  margin: 0 auto 50px;
  padding: 0 20px;
  background: #ffffff;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(0, 0, 0, 0.08);
}

.map-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0;
  padding: 15px 20px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.map-title {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #2c3e50;
  font-size: 1.5rem;
  font-weight: 600;
  
  i {
    color: #4a55a2;
    font-size: 24px;
  }
}

.map-button {
  background: rgba(74, 85, 162, 0.08);
  color: #4a55a2;
  border: 1px solid rgba(74, 85, 162, 0.15);
  transition: all 0.3s ease;
  
  &:hover {
    background: rgba(74, 85, 162, 0.12);
    transform: translateY(-2px);
  }
}

.map-wrapper {
  overflow: hidden;
  height: 400px;
}

.contact-info {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 30px;
  margin: 50px 0;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #2c3e50;
  background: #ffffff;
  padding: 15px 25px;
  border-radius: 50px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
  
  i {
    color: #4a55a2;
    font-size: 20px;
  }
  
  &:hover {
    background: #ffffff;
    transform: translateY(-5px);
    border-color: rgba(74, 85, 162, 0.3);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  }
}

.footer {
  margin-top: 80px;
  padding: 30px 0;
  background: #2c3e50;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  color: #ffffff;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.footer-logo {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  
  .logo-icon {
    width: 32px;
    height: 32px;
    font-size: 16px;
    box-shadow: 0 0 15px rgba(255, 255, 255, 0.1);
  }
  
  .logo-text {
    background: linear-gradient(135deg, #ffffff, #d8e3f2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 20px;
  }
}

.footer-text {
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
}

.about-container {
  display: flex;
  justify-content: center;
  gap: 40px;
  max-width: 1200px;
  margin: 0 auto 60px;
  padding: 0 20px;
  
  @media (max-width: 992px) {
    flex-direction: column;
    align-items: center;
  }
}

.about-card {
  background: #ffffff; /* 纯白色背景 */
  border: 1px solid rgba(0, 0, 0, 0.08); /* 极浅的灰色边框 */
  border-radius: 20px;
  padding: 40px;
  flex: 1;
  max-width: 500px;
  position: relative;
  color: #333333;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05); /* 轻微阴影 */
  overflow: hidden;
  
  &:hover {
    transform: translateY(-10px);
    border-color: rgba(120, 149, 203, 0.3);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1), 0 0 20px rgba(120, 149, 203, 0.2); /* 更柔和的阴影 */
    
    .about-icon-wrapper {
      background: rgba(74, 85, 162, 0.1);
      border-color: rgba(74, 85, 162, 0.3);
      transform: translateY(-5px);
      
      i {
        color: #4a55a2;
        transform: scale(1.2);
      }
    }
    
    .card-decoration {
      transform: rotate(45deg) scale(1.2);
      opacity: 0.08;
    }
  }
  
  h3 {
    font-size: 1.8rem;
    margin: 20px 0;
    color: #2c3e50;
    position: relative;
    
    &::after {
      content: '';
      position: absolute;
      bottom: -10px;
      left: 0;
      width: 40px;
      height: 3px;
      background: linear-gradient(90deg, #4a55a2, transparent);
      border-radius: 3px;
    }
  }
}

.about-icon-wrapper {
  width: 70px;
  height: 70px;
  border-radius: 20px;
  background: rgba(74, 85, 162, 0.08);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(74, 85, 162, 0.15);
  transition: all 0.4s ease;
  
  i {
    font-size: 32px;
    color: #4a55a2;
    transition: all 0.4s ease;
  }
}

.about-description {
  margin-top: 30px;
  
  p {
    color: #666666;
    line-height: 1.7;
    margin-bottom: 15px;
    position: relative;
    z-index: 2;
  }
}

.card-decoration {
  position: absolute;
  top: -50px;
  right: -50px;
  width: 200px;
  height: 200px;
  background: #4a55a2;
  border-radius: 30px;
  transform: rotate(45deg);
  opacity: 0.05;
  transition: all 0.6s ease;
  z-index: 1;
}


@keyframes dotTyping {
  0% { content: '.'; }
  25% { content: '..'; }
  50% { content: '...'; }
  75% { content: ''; }
}

.chat-input {
  padding: 15px;
  border-top: 1px solid rgba(73, 246, 220, 0.15);
  display: flex;
  gap: 10px;
  background: rgba(10, 25, 47, 0.5);
}

.message-input {
  :deep(.el-input__wrapper) {
    background: rgba(62, 73, 156, 0.6) !important; /* 更柔和的输入框背景 */
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 30px !important;
    box-shadow: none !important;
    padding: 0 15px !important;
    
    &:hover, &:focus {
      border-color: rgba(255, 255, 255, 0.4) !important;
    }
    
    .el-input__inner {
      color: #ffffff !important;
      
      &::placeholder {
        color: rgba(255, 255, 255, 0.5) !important;
      }
    }
  }
}

.send-button {
  background: linear-gradient(135deg, #7895cb, #4a55a2) !important; /* 更柔和的发送按钮渐变 */
  color: #ffffff !important;
  boimportanter: none !important;
  transition: all 0.3s ease !important;
  
  &:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 5px 15px rgba(120, 149, 203, 0.3) !important; /* 更柔和的悬停阴影 */
  }
}

// PPT演示样式优化
.ppt-preview {
  flex: 1;
  min-width: 300px;
  display: flex;
  flex-direction: column;
}

.ppt-slide {
  position: relative;
  border-radius: 16px;
  overflow: hidden;
  border: 2px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
  margin-bottom: 20px;
  
  img {
    width: 100%;
    height: auto;
    display: block;
  }
  
  .slide-indicator {
    position: absolute;
    bottom: 15px;
    right: 15px;
    background: rgba(78, 67, 206, 0.7);
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 14px;
    color: #ffffff;
    border: 1px solid rgba(255, 255, 255, 0.3);
    backdrop-filter: blur(5px);
    
    .current {
      color: #ffffff;
      font-weight: 600;
    }
  }
}

.ppt-controls {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-top: 20px;
}

.control-button {
  &.primary {
    background: linear-gradient(135deg, #8972ff, #6557ec) !important;
    color: #ffffff !important;
    border: none !important;
    padding: 10px 20px !important;
    border-radius: 30px !important;
    font-weight: 600 !important;
    
    i {
      margin-right: 5px;
    }
    
    &:hover {
      transform: translateY(-2px) !important;
      box-shadow: 0 5px 15px rgba(137, 114, 255, 0.3) !important;
    }
  }
  
  &:not(.primary) {
    background: rgba(255, 255, 255, 0.1) !important;
    color: #ffffff !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
    
    &:hover {
      background: rgba(255, 255, 255, 0.2) !important;
      transform: translateY(-2px) !important;
    }
  }
}

// 核心功能样式优化
.core-features-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.core-feature {
  display: flex;
  gap: 50px;
  margin-bottom: 100px;
  position: relative;
  background: #ffffff;
  border-radius: 30px;
  padding: 40px;
  overflow: hidden;
  border: 1px solid rgba(0, 0, 0, 0.08);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
  transition: all 0.4s ease;
  
  &:hover {
    transform: translateY(-10px);
    border-color: rgba(120, 149, 203, 0.3);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1), 0 0 20px rgba(120, 149, 203, 0.2);
    
    .feature-number {
      color: rgba(74, 85, 162, 0.15);
      transform: scale(1.1);
    }
    
    .image-overlay {
      opacity: 0.2;
    }
    
    .feature-tag {
      background: rgba(74, 85, 162, 0.1);
      border-color: rgba(74, 85, 162, 0.3);
    }
  }
  
  &.reverse {
    flex-direction: row-reverse;
    
    .feature-number {
      left: auto;
      right: -20px;
    }
  }
  
  @media (max-width: 992px) {
    flex-direction: column;
    
    &.reverse {
      flex-direction: column;
    }
    
    .feature-number {
      top: -10px;
      left: 50%;
      transform: translateX(-50%);
    }
    
    &.reverse .feature-number {
      left: 50%;
      right: auto;
    }
  }
}

.feature-number {
  position: absolute;
  top: -20px;
  left: -20px;
  font-size: 5rem;
  font-weight: 900;
  color: rgba(74, 85, 162, 0.1);
  z-index: 1;
  transition: all 0.4s ease;
}

.feature-content {
  flex: 1;
  z-index: 2;
  
  h3 {
    font-size: 1.8rem;
    color: #2c3e50;
    margin-bottom: 20px;
    padding-bottom: 15px;
    position: relative;
    
    &::after {
      content: '';
      position: absolute;
      bottom: 0;
      left: 0;
      width: 60px;
      height: 3px;
      background: linear-gradient(90deg, #4a55a2, transparent);
      border-radius: 3px;
    }
  }
  
  p {
    color: #666666;
    line-height: 1.7;
    margin-bottom: 25px;
    font-size: 1.05rem;
  }
}

.feature-tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 20px;
}

.feature-tag {
  background: rgba(74, 85, 162, 0.08);
  color: #4a55a2;
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
  border: 1px solid rgba(74, 85, 162, 0.15);
  transition: all 0.3s ease;
}

.feature-image {
  flex: 1;
  min-width: 300px;
  border-radius: 20px;
  overflow: hidden;
  position: relative;
  
  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: all 0.6s ease;
    transform: scale(1.05);
  }
  
  .image-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, #8972ff, #6557ec);
    opacity: 0;
    mix-blend-mode: color;
    transition: opacity 0.4s ease;
  }
}

// 页面区块通用样式
.page-section {
  min-height: 100vh;
  padding: 88px 20px 20px;
  scroll-margin-top: 68px;
  position: relative;
  overflow: hidden;
  
  &:not(#home) {
    padding-top: 120px;
  }
}

// 科技风格部分
.tech-section {
  position: relative;
  background: linear-gradient(135deg, #f5f7fa, #e9ecef); /* 浅灰色渐变背景 */
  z-index: 1;
  color: #333;
  
  .section-title {
    color: #2c3e50; /* 深色标题 */
  }
  
  .section-subtitle {
    color: #666666; /* 中等灰色副标题 */
  }
}

// 为渐变背景上的部分修改颜色
.tech-section.dark-section {
  background: linear-gradient(135deg, #2c3e50, #4a55a2); /* 深色渐变背景 */
  color: #ffffff;
  
  .section-title {
    color: #ffffff;
    
    &::after {
      background: linear-gradient(90deg, rgba(255, 255, 255, 0.3), rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0.3));
    }
  }
  
  .section-subtitle {
    color: rgba(255, 255, 255, 0.8);
  }
  
  .title-highlight {
    color: #a8d1ff;
    
    &::after {
      background: rgba(255, 255, 255, 0.2);
    }
  }
  
  .feature-card {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border-color: rgba(255, 255, 255, 0.2);
    
    h3 {
      color: #ffffff;
    }
    
    p {
      color: rgba(255, 255, 255, 0.8);
    }
  }
  
  .feature-icon-wrapper {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.2);
    
    i {
      color: #ffffff;
    }
  }
  
  .stat-item {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border-color: rgba(255, 255, 255, 0.2);
  }
  
  .stat-number {
    color: #ffffff;
    
    .stat-symbol {
      color: rgba(255, 255, 255, 0.8);
    }
  }
  
  .stat-label {
    color: rgba(255, 255, 255, 0.8);
  }
}

.tech-grid {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    linear-gradient(rgba(255, 255, 255, 0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.05) 1px, transparent 1px);
  background-size: 30px 30px;
  animation: gridMove 20s linear infinite;
  z-index: -1;
}

.tech-circles {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: -1;
}

.circle {
  position: absolute;
  border-radius: 50%;
  background: linear-gradient(45deg, rgba(255, 255, 255, 0.05), rgba(216, 227, 242, 0.05)); /* 更柔和的圆形渐变 */
  animation: float 15s ease-in-out infinite;
}

.circle-1 {
  width: 500px;
  height: 500px;
  top: -100px;
  left: -100px;
  animation-delay: 0s;
}

.circle-2 {
  width: 400px;
  height: 400px;
  top: 50%;
  right: -150px;
  animation-delay: -5s;
}

.circle-3 {
  width: 350px;
  height: 350px;
  bottom: -100px;
  left: 30%;
  animation-delay: -10s;
}

.circle-4 {
  width: 280px;
  height: 280px;
  bottom: 30%;
  right: 10%;
  animation-delay: -7s;
}

@keyframes gridMove {
  0% {
    transform: translateY(0);
  }
  100% {
    transform: translateY(30px);
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  50% {
    transform: translateY(-30px) rotate(5deg);
  }
}

// 应用展示部分样式优化
.demo-wrapper {
  display: flex;
  justify-content: center;
  margin-bottom: 80px;
  
  &.reverse {
    flex-direction: row-reverse;
  }
  
  @media (max-width: 992px) {
    flex-direction: column;
    
    &.reverse {
      flex-direction: column;
    }
  }
}

.digital-assistant-demo, .ppt-demo {
  max-width: 1200px;
  width: 100%;
  background: #ffffff; /* 纯白色背景 */
  border-radius: 20px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  overflow: hidden;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1); /* 轻微阴影 */
  transition: all 0.4s ease;
  position: relative;
  
  &:hover {
    transform: translateY(-10px);
    border-color: rgba(120, 149, 203, 0.3);
    box-shadow: 0 30px 60px rgba(0, 0, 0, 0.15), 0 0 30px rgba(120, 149, 203, 0.15); /* 更柔和的悬停阴影 */
  }
}

.demo-header {
  background: rgba(74, 85, 162, 0.08);
  padding: 15px 20px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.demo-title {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #2c3e50;
  font-size: 18px;
  font-weight: 600;
  
  i {
    color: #4a55a2;
    font-size: 22px;
  }
}

.demo-controls {
  display: flex;
  gap: 10px;
}

.demo-control-button {
  color: #4a55a2;
  transition: all 0.3s ease;
  
  &:hover {
    color: #7895cb;
    transform: scale(1.1);
  }
}

.demo-content {
  padding: 30px;
  display: flex;
  gap: 30px;
  align-items: stretch;
  
  @media (max-width: 992px) {
    flex-direction: column;
  }
}

// 数字人助手样式优化
.digital-human {
  flex: 1;
  min-width: 300px;
}

.digital-human-wrapper {
  position: relative;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(120, 149, 203, 0.2);
  
  img {
    width: 100%;
    height: auto;
    display: block;
    transition: transform 0.5s ease, filter 0.5s ease;
    
    &:hover {
      transform: scale(1.03);
      filter: brightness(1.05);
    }
  }
}

.digital-human-status {
  position: absolute;
  bottom: 15px;
  right: 15px;
  background: rgba(255, 255, 255, 0.9);
  padding: 8px 15px;
  border-radius: 30px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  color: #2c3e50;
  border: 1px solid rgba(0, 0, 0, 0.08);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
}

.pulse {
  width: 10px;
  height: 10px;
  background: #2ecc71;
  border-radius: 50%;
  position: relative;
  
  &:before {
    content: '';
    position: absolute;
    top: -5px;
    left: -5px;
    right: -5px;
    bottom: -5px;
    border-radius: 50%;
    border: 2px solid #2ecc71;
    animation: pulse 1.5s linear infinite;
  }
}

// 助手对话样式优化
.assistant-chat {
  flex: 1;
  min-width: 300px;
  background: rgba(74, 85, 162, 0.03);
  border-radius: 16px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  height: 400px;
}

.chat-messages {
  flex: 1;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  overflow-y: auto;
}

.message {
  display: flex;
  gap: 12px;
  max-width: 85%;
  
  &.assistant {
    align-self: flex-start;
  }
  
  &.user {
    align-self: flex-end;
    flex-direction: row-reverse;
    
    .message-bubble {
      background: rgba(74, 85, 162, 0.08);
      border-color: rgba(74, 85, 162, 0.15);
      
      &:before {
        left: auto;
        right: -8px;
        border-width: 8px 0 8px 8px;
        border-color: transparent transparent transparent rgba(74, 85, 162, 0.15);
      }
    }
    
    .message-time {
      text-align: right;
    }
  }
  
  &.typing .message-content {
    display: flex;
    align-items: center;
  }
}

.message-avatar {
  margin-top: 5px;
}

.message-bubble {
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(0, 0, 0, 0.05);
  border-radius: 18px;
  padding: 12px 16px;
  position: relative;
  
  &:before {
    content: '';
    position: absolute;
    left: -8px;
    top: 15px;
    border-style: solid;
    border-width: 8px 8px 8px 0;
    border-color: transparent rgba(0, 0, 0, 0.05) transparent transparent;
  }
}

.message-content {
  color: #2c3e50;
  font-size: 15px;
  line-height: 1.5;
}

.message-time {
  font-size: 12px;
  color: #999999;
  margin-top: 5px;
}

.chat-input {
  padding: 15px;
  border-top: 1px solid rgba(0, 0, 0, 0.05);
  display: flex;
  gap: 10px;
  background: #ffffff;
}

.message-input {
  :deep(.el-input__wrapper) {
    background: rgba(74, 85, 162, 0.03) !important;
    border: 1px solid rgba(0, 0, 0, 0.05) !important;
    border-radius: 30px !important;
    box-shadow: none !important;
    padding: 0 15px !important;
    
    &:hover, &:focus {
      border-color: rgba(74, 85, 162, 0.2) !important;
    }
    
    .el-input__inner {
      color: #2c3e50 !important;
      
      &::placeholder {
        color: #999999 !important;
      }
    }
  }
}

.send-button {
  background: linear-gradient(135deg, #4a55a2, #7895cb) !important;
  color: #ffffff !important;
  border: none !important;
  transition: all 0.3s ease !important;
  
  &:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 5px 15px rgba(120, 149, 203, 0.3) !important;
  }
}

// PPT演示样式优化
.ppt-preview {
  flex: 1;
  min-width: 300px;
  display: flex;
  flex-direction: column;
}

.ppt-slide {
  position: relative;
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid rgba(0, 0, 0, 0.08);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
  
  img {
    width: 100%;
    height: auto;
    display: block;
  }
  
  .slide-indicator {
    position: absolute;
    bottom: 15px;
    right: 15px;
    background: rgba(255, 255, 255, 0.9);
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 14px;
    color: #2c3e50;
    border: 1px solid rgba(0, 0, 0, 0.08);
  }
}

.ppt-controls {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-top: 20px;
}

.ppt-script {
  flex: 1;
  min-width: 300px;
  background: rgba(74, 85, 162, 0.03);
  border-radius: 16px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  height: 400px;
}

.script-header {
  padding: 12px 20px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  gap: 10px;
  color: #2c3e50;
  font-size: 16px;
  font-weight: 500;
  background: rgba(74, 85, 162, 0.05);
}

.script-content {
  flex: 1;
  padding: 20px;
  color: #2c3e50;
  font-size: 15px;
  line-height: 1.7;
  overflow-y: auto;
  
  p {
    margin-bottom: 15px;
    text-align: justify;
  }
}

.run-program-button {
  background: linear-gradient(135deg, #4a55a2, #7895cb) !important;
  color: #ffffff !important;
  border: none !important;
  padding: 8px 16px !important;
  border-radius: 30px !important;
  font-weight: 600 !important;
  display: flex;
  align-items: center;
  gap: 6px;
  box-shadow: 0 5px 15px rgba(120, 149, 203, 0.2);
  transition: all 0.3s ease;
  margin-right: 10px;
  
  i {
    font-size: 16px;
  }
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(120, 149, 203, 0.3);
  }
  
  &:active {
    transform: translateY(0);
    box-shadow: 0 2px 10px rgba(120, 149, 203, 0.2);
  }
}

.dot-typing {
  position: relative;
  margin-left: 10px;
  
  &:after {
    content: '...';
    animation: dotTyping 1.5s infinite;
    letter-spacing: 2px;
  }
}

// ... existing code ...

@keyframes pulse {
  0% {
    transform: scale(0.5);
    opacity: 1;
  }
  100% {
    transform: scale(2);
    opacity: 0;
  }
}

@keyframes waveAnimation {
  0% {
    transform: translateX(0);
  }
  100% {
    transform: translateX(-50%);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes floatIcon {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  25% {
    transform: translateY(-15px) rotate(5deg);
  }
  50% {
    transform: translateY(0) rotate(0deg);
  }
  75% {
    transform: translateY(15px) rotate(-5deg);
  }
}

@keyframes dotTyping {
  0% { content: '.'; }
  25% { content: '..'; }
  50% { content: '...'; }
  75% { content: ''; }
}
</style>


