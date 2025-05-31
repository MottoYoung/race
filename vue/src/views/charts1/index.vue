<template>
  <div class="dashboard-container">
    <div class="light-beam beam1"></div>
    <div class="light-beam beam2"></div>
    <div class="light-beam beam3"></div>
    <div class="connector c1"></div>
    <div class="connector c2"></div>
    <div class="connector c3"></div>
    
    <div class="dashboard-header">
      <div class="header-title">
        <div class="tech-icon"></div>
        <span class="title-text" data-text="AI辅助教师智能备课系统">AI辅助教师智能备课系统</span>
        <span class="title-sub">管理员数据监控中心</span>
      </div>
      <div class="header-actions">
        <button class="logout-btn" @click="handleLogout">退出登录</button>
        <div class="header-time">
          <div class="time">{{ currentTime }}</div>
          <div class="date">{{ currentDate }}</div>
        </div>
      </div>
    </div>

    <div class="dashboard-content">
      <!-- 左侧内容区 -->
      <div class="content-left">
        <div class="panel panel-resources">
          <div class="panel-header">
            <span>教学资源统计</span>
            <div class="panel-tags">
              <div class="tag tag-today">今日</div>
              <div class="tag tag-total">总量</div>
            </div>
          </div>
          <div class="panel-body">
            <resources-total-chart ref="resourcesTotalChart" v-if="componentsLoaded.resourcesTotal" />
            <div v-else class="chart-loading">加载中...</div>
          </div>
          <div class="panel-corner-br"></div>
          <div class="panel-id">SYS-001</div>
          <div class="panel-digits" data-digits="10110101">01101011</div>
        </div>

        <div class="panel panel-user">
          <div class="panel-header">用户活跃度分析</div>
          <div class="panel-body">
            <user-activity-chart ref="userActivityChart" v-if="componentsLoaded.userActivity" />
            <div v-else class="chart-loading">加载中...</div>
          </div>
          <div class="panel-corner-br"></div>
          <div class="panel-id">SYS-002</div>
          <div class="panel-digits" data-digits="10110010">01011010</div>
        </div>
      </div>

      <!-- 右侧内容区 -->
      <div class="content-right">
        <div class="panel-group top-group">
          <div class="panel panel-sm">
            <div class="panel-header">今日教案生成概况</div>
            <div class="panel-body">
              <lessons-chart ref="lessonsChart" v-if="componentsLoaded.lessons" />
              <div v-else class="chart-loading">加载中...</div>
            </div>
            <div class="panel-corner-br"></div>
            <div class="panel-id">SYS-003</div>
            <div class="panel-digits" data-digits="11001010">10110010</div>
          </div>
          <div class="panel panel-sm">
            <div class="panel-header">今日习题生成统计</div>
            <div class="panel-body">
              <exercises-chart ref="exercisesChart" v-if="componentsLoaded.exercises" />
              <div v-else class="chart-loading">加载中...</div>
            </div>
            <div class="panel-corner-br"></div>
            <div class="panel-id">SYS-004</div>
            <div class="panel-digits" data-digits="01110101">01101010</div>
          </div>
          <div class="panel panel-sm">
            <div class="panel-header">多媒体资源生成量</div>
            <div class="panel-body">
              <media-chart ref="mediaChart" v-if="componentsLoaded.media" />
              <div v-else class="chart-loading">加载中...</div>
            </div>
            <div class="panel-corner-br"></div>
            <div class="panel-id">SYS-005</div>
            <div class="panel-digits" data-digits="11010011">10101001</div>
          </div>
        </div>

        <div class="panel panel-api">
          <div class="panel-header">大模型API调用统计</div>
          <div class="panel-body">
            <api-calls-chart ref="apiCallsChart" v-if="componentsLoaded.apiCalls" />
            <div v-else class="chart-loading">加载中...</div>
          </div>
          <div class="panel-corner-br"></div>
          <div class="panel-id">SYS-006</div>
          <div class="panel-digits" data-digits="10110111">01101110</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, onBeforeUnmount, defineAsyncComponent } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: 'Dashboard',
  components: {
    LessonsChart: defineAsyncComponent(() => import('./components/LessonsChart.vue')
      .catch(err => {
        console.error('Failed to load LessonsChart:', err);
        return import('./components/EmptyChart.vue');
      })),
    ExercisesChart: defineAsyncComponent(() => import('./components/ExercisesChart.vue')
      .catch(err => {
        console.error('Failed to load ExercisesChart:', err);
        return import('./components/EmptyChart.vue');
      })),
    MediaChart: defineAsyncComponent(() => import('./components/MediaChart.vue')
      .catch(err => {
        console.error('Failed to load MediaChart:', err);
        return import('./components/EmptyChart.vue');
      })),
    ResourcesTotalChart: defineAsyncComponent(() => import('./components/ResourcesTotalChart.vue')
      .catch(err => {
        console.error('Failed to load ResourcesTotalChart:', err);
        return import('./components/EmptyChart.vue');
      })),
    ApiCallsChart: defineAsyncComponent(() => import('./components/ApiCallsChart.vue')
      .catch(err => {
        console.error('Failed to load ApiCallsChart:', err);
        console.log('尝试加载简化版API图表组件');
        return import('./components/ApiCallsChartSimple.vue')
          .catch(simpleErr => {
            console.error('简化版API图表也无法加载:', simpleErr);
            return import('./components/EmptyChart.vue');
          });
      })),
    UserActivityChart: defineAsyncComponent(() => import('./components/UserActivityChart.vue')
      .catch(err => {
        console.error('Failed to load UserActivityChart:', err);
        return import('./components/EmptyChart.vue');
      })),
  },
  setup() {
    const router = useRouter();
    const lessonsChart = ref(null);
    const exercisesChart = ref(null);
    const mediaChart = ref(null);
    const resourcesTotalChart = ref(null);
    const apiCallsChart = ref(null);
    const userActivityChart = ref(null);

    // 组件加载状态跟踪
    const componentsLoaded = reactive({
      lessons: false,
      exercises: false,
      media: false,
      resourcesTotal: false,
      apiCalls: false,
      userActivity: false
    });

    const currentTime = ref('');
    const currentDate = ref('');

    const updateDateTime = () => {
      const now = new Date();
      currentTime.value = now.toLocaleTimeString('zh-CN', { hour12: false });
      currentDate.value = now.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        weekday: 'long'
      });
    };

    const handleLogout = () => {
      // 清除用户数据
      localStorage.removeItem('user');
      // 跳转到登录页面
      router.push('/auth/login');
    };

    let timer = null;

    onMounted(() => {
      updateDateTime();
      timer = setInterval(updateDateTime, 1000);
      
      // 延迟设置组件加载状态，确保异步组件有时间加载
      setTimeout(() => {
        Object.keys(componentsLoaded).forEach(key => {
          componentsLoaded[key] = true;
        });
      }, 1000);
    });

    onBeforeUnmount(() => {
      if (timer) clearInterval(timer);
    });

    return {
      lessonsChart,
      exercisesChart,
      mediaChart,
      resourcesTotalChart,
      apiCallsChart,
      userActivityChart,
      componentsLoaded,
      currentTime,
      currentDate,
      handleLogout
    };
  }
};
</script>

<style lang="scss" scoped>
.dashboard-container {
  width: 100%;
  height: 100vh;
  min-height: 768px;
  background-color: #030929;
  color: #fff;
  overflow: auto;
  padding: 20px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  background-image: 
    radial-gradient(circle at 50% 50%, rgba(59, 141, 255, 0.1) 0%, transparent 80%),
    linear-gradient(to bottom, rgba(2, 5, 31, 0.9), rgba(2, 5, 31, 0.9));
  background-size: cover;
  position: relative;
  
  .light-beam {
    position: absolute;
    width: 100px;
    height: 1000px;
    background: linear-gradient(to bottom, transparent, rgba(59, 141, 255, 0.02), transparent);
    transform-origin: top center;
    transform: rotate(45deg);
    filter: blur(3px);
    opacity: 0.6;
    z-index: 0;
    pointer-events: none;
    animation: moveBeam 20s linear infinite;
    
    &.beam1 {
      left: 20%;
      top: -400px;
      animation-delay: 0s;
    }
    
    &.beam2 {
      left: 50%;
      top: -300px;
      animation-delay: 6s;
      transform: rotate(30deg);
      opacity: 0.5;
    }
    
    &.beam3 {
      right: 20%;
      top: -350px;
      animation-delay: 13s;
      transform: rotate(-40deg);
      opacity: 0.4;
    }
  }
  
  @keyframes moveBeam {
    0% {
      opacity: 0.1;
    }
    25% {
      opacity: 0.6;
    }
    50% {
      opacity: 0.2;
    }
    75% {
      opacity: 0.5;
    }
    100% {
      opacity: 0.1;
    }
  }
  
  .connector {
    position: absolute;
    z-index: 0;
    border-top: 1px dashed rgba(54, 209, 220, 0.2);
    width: 60px;
    pointer-events: none;
    
    &.c1 {
      top: 240px;
      left: 38.5%;
      width: 40px;
      transform: rotate(-30deg);
    }
    
    &.c2 {
      top: 480px;
      left: 38.5%;
      width: 40px;
      transform: rotate(-30deg);
    }
    
    &.c3 {
      top: 250px;
      right: 59%;
      width: 40px;
      transform: rotate(30deg);
    }
  }
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: 
      linear-gradient(rgba(59, 141, 255, 0.05) 1px, transparent 1px),
      linear-gradient(90deg, rgba(59, 141, 255, 0.05) 1px, transparent 1px);
    background-size: 20px 20px;
    pointer-events: none;
    z-index: 0;
  }
  
  &::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: 
      radial-gradient(circle at 10% 20%, rgba(59, 141, 255, 0.02) 0%, transparent 20%),
      radial-gradient(circle at 80% 60%, rgba(54, 209, 220, 0.03) 0%, transparent 30%),
      radial-gradient(circle at 40% 80%, rgba(91, 134, 229, 0.02) 0%, transparent 25%);
    z-index: 0;
  }
}

.dashboard-header, .dashboard-content {
  position: relative;
  z-index: 1;
}

.dashboard-header {
  height: 70px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  position: relative;
  padding: 0 10px;
  
  &::before {
    content: '';
    position: absolute;
    left: 0;
    top: 50%;
    transform: translateY(-50%);
    width: 100%;
    height: 1px;
    background: linear-gradient(90deg, 
      rgba(54, 209, 220, 0), 
      rgba(54, 209, 220, 0.3), 
      rgba(91, 134, 229, 0.5), 
      rgba(54, 209, 220, 0.3), 
      rgba(54, 209, 220, 0)
    );
  }
  
  &::after {
    content: '01010111';
    position: absolute;
    right: -10px;
    top: -10px;
    font-size: 10px;
    color: rgba(54, 209, 220, 0.2);
    font-family: monospace;
    letter-spacing: 2px;
    opacity: 0.6;
    animation: digitFlicker 4s infinite;
  }

  .header-title {
    display: flex;
    flex-direction: column;
    position: relative;
    z-index: 1;

    .tech-icon {
      position: absolute;
      left: -50px;
      top: 50%;
      transform: translateY(-50%);
      width: 40px;
      height: 40px;
      border-radius: 50%;
      background: rgba(3, 19, 57, 0.8);
      border: 1px solid rgba(59, 141, 255, 0.3);
      box-shadow: 0 0 15px rgba(59, 141, 255, 0.2);
      display: flex;
      justify-content: center;
      align-items: center;
      overflow: hidden;
      
      &::before {
        content: '';
        position: absolute;
        width: 30px;
        height: 30px;
        border: 2px solid transparent;
        border-top-color: #36d1dc;
        border-right-color: #5b86e5;
        border-radius: 50%;
        animation: iconSpin 3s linear infinite;
      }
      
      &::after {
        content: '';
        position: absolute;
        width: 15px;
        height: 15px;
        background: linear-gradient(90deg, #36d1dc, #5b86e5);
        border-radius: 50%;
        opacity: 0.8;
        filter: blur(1px);
        animation: iconPulse 2s ease-in-out infinite;
      }
    }

    @keyframes iconSpin {
      0% {
        transform: rotate(0deg);
      }
      100% {
        transform: rotate(360deg);
      }
    }

    @keyframes iconPulse {
      0%, 100% {
        transform: scale(0.8);
        opacity: 0.8;
      }
      50% {
        transform: scale(1.2);
        opacity: 1;
      }
    }

    .title-text {
      position: relative;
      font-weight: bold;
      font-size: 32px;
      background: linear-gradient(90deg, #36d1dc, #5b86e5, #5654de);
      background-size: 400% 100%;
      -webkit-background-clip: text;
      background-clip: text;
      -webkit-text-fill-color: transparent;
      color: transparent;
      text-shadow: 0 0 10px rgba(54, 209, 220, 0.3);
      letter-spacing: 2px;
      animation: textShine 6s linear infinite;
      
      @keyframes textShine {
        0% {
          background-position: 0% center;
        }
        100% {
          background-position: 400% center;
        }
      }
      
      &::before {
        content: attr(data-text);
        position: absolute;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        background: linear-gradient(90deg, #36d1dc, #5b86e5);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        color: transparent;
        filter: blur(8px);
        opacity: 0.7;
        animation: glowPulse 3s infinite alternate;
      }
      
      &::after {
        content: attr(data-text);
        position: absolute;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        z-index: 1;
        background: white;
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        color: transparent;
        opacity: 0;
        animation: textHighlight 8s ease-in-out infinite;
      }
      
      @keyframes textHighlight {
        0%, 100% { 
          opacity: 0;
          filter: blur(0px);
        }
        15% { 
          opacity: 0.7;
          filter: blur(2px);
        }
        30% { 
          opacity: 0;
          filter: blur(0px);
        }
      }
    }

    @keyframes glowPulse {
      0% {
        filter: blur(8px);
        opacity: 0.7;
      }
      50% {
        filter: blur(12px);
        opacity: 0.9;
      }
      100% {
        filter: blur(8px);
        opacity: 0.7;
      }
    }

    .title-sub {
      font-size: 16px;
      background: linear-gradient(90deg, rgba(54, 209, 220, 0.8), rgba(91, 134, 229, 0.8));
      -webkit-background-clip: text;
      background-clip: text;
      color: transparent;
      margin-top: 5px;
      letter-spacing: 1px;
      position: relative;
      padding-left: 15px;
      
      &::before {
        content: '';
        position: absolute;
        left: 0;
        top: 50%;
        transform: translateY(-50%);
        width: 8px;
        height: 8px;
        background: linear-gradient(90deg, #36d1dc, #5b86e5);
        border-radius: 50%;
        box-shadow: 0 0 10px rgba(54, 209, 220, 0.5);
      }
    }
  }

  .header-actions {
    display: flex;
    align-items: center;
    gap: 20px;
  }

  .logout-btn {
    padding: 8px 16px;
    background: rgba(3, 19, 57, 0.8);
    border: 1px solid rgba(54, 209, 220, 0.5);
    border-radius: 4px;
    color: #36d1dc;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s;
    position: relative;
    overflow: hidden;
    letter-spacing: 1px;
    
    &::before {
      content: '';
      position: absolute;
      top: 0;
      left: -100%;
      width: 100%;
      height: 100%;
      background: linear-gradient(90deg, 
        transparent, 
        rgba(54, 209, 220, 0.2), 
        transparent
      );
      transition: all 0.5s;
    }
    
    &:hover {
      border-color: rgba(54, 209, 220, 0.8);
      box-shadow: 0 0 15px rgba(54, 209, 220, 0.3);
      
      &::before {
        left: 100%;
      }
    }
  }

  .header-time {
    text-align: right;
    position: relative;
    z-index: 1;
    display: flex;
    flex-direction: column;
    align-items: flex-end;

    .time {
      font-size: 28px;
      font-weight: bold;
      color: transparent;
      background: linear-gradient(90deg, #36d1dc, #5b86e5);
      -webkit-background-clip: text;
      background-clip: text;
      text-shadow: 0 0 10px rgba(54, 209, 220, 0.3);
      font-family: 'Orbitron', sans-serif;
      letter-spacing: 1px;
      position: relative;
    }

    .date {
      font-size: 14px;
      color: rgba(91, 134, 229, 0.9);
      margin-top: 5px;
      letter-spacing: 1px;
      padding-right: 10px;
      position: relative;
      
      &::after {
        content: '';
        position: absolute;
        right: 0;
        top: 50%;
        transform: translateY(-50%);
        width: 6px;
        height: 6px;
        background: #5b86e5;
        border-radius: 50%;
        box-shadow: 0 0 8px rgba(91, 134, 229, 0.7);
      }
    }
  }
}

@keyframes digitFlicker {
  0%, 100% {
    opacity: 0.2;
  }
  50% {
    opacity: 0.6;
  }
  55% {
    opacity: 0.2;
  }
  60% {
    opacity: 0.6;
  }
}

.dashboard-content {
  flex: 1;
  display: flex;
  gap: 20px;
  min-height: 0;
  position: relative;
  
  &::before {
    content: '';
    position: absolute;
    width: 2px;
    height: 100px;
    background: linear-gradient(to bottom, transparent, rgba(54, 209, 220, 0.8), transparent);
    left: 39.5%;
    top: 0;
    z-index: 0;
    animation: dataFlowLine 8s infinite;
    opacity: 0.6;
  }
  
  &::after {
    content: '';
    position: absolute;
    width: 2px;
    height: 120px;
    background: linear-gradient(to bottom, transparent, rgba(91, 134, 229, 0.8), transparent);
    left: 39.5%;
    top: 40%;
    z-index: 0;
    animation: dataFlowLine 12s infinite;
    opacity: 0.6;
    animation-delay: 4s;
  }
}

@keyframes dataFlowLine {
  0% {
    transform: translateY(-100%);
    opacity: 0;
  }
  10% {
    opacity: 0.6;
  }
  90% {
    opacity: 0.6;
  }
  100% {
    transform: translateY(100%);
    opacity: 0;
  }
}

.content-left, .content-right {
  display: flex;
  flex-direction: column;
  gap: 20px;
  min-height: 0;
}

.content-left {
  width: 40%;
}

.content-right {
  width: 60%;
}

.top-group {
  display: flex;
  gap: 20px;
  height: 260px;
}

.panel {
  background: rgba(3, 19, 57, 0.8);
  border: 1px solid rgba(59, 141, 255, 0.2);
  box-shadow: 0 0 15px rgba(59, 141, 255, 0.1);
  border-radius: 8px;
  overflow: hidden;
  backdrop-filter: blur(10px);
  transition: all 0.3s;
  display: flex;
  flex-direction: column;
  position: relative;
  
  &::before {
    content: '';
    position: absolute;
    top: -1px;
    left: -1px;
    right: -1px;
    bottom: -1px;
    background: linear-gradient(135deg, rgba(59, 141, 255, 0.3) 0%, transparent 50%, rgba(54, 209, 220, 0.3) 100%);
    border-radius: 9px;
    z-index: -1;
    opacity: 0;
    transition: opacity 0.3s;
  }
  
  .panel-digits {
    position: absolute;
    left: 12px;
    bottom: 8px;
    font-size: 8px;
    color: rgba(59, 141, 255, 0.4);
    font-family: monospace;
    letter-spacing: 1px;
    user-select: none;
    z-index: 0;
    
    &::after {
      content: attr(data-digits);
      position: absolute;
      left: 0;
      top: 0;
      opacity: 0;
      animation: digitBlink 8s linear infinite;
    }
  }
  
  @keyframes digitBlink {
    0%, 98% {
      opacity: 0;
    }
    98.5% {
      opacity: 1;
    }
    99% {
      opacity: 0;
    }
    99.5% {
      opacity: 1;
    }
    100% {
      opacity: 0;
    }
  }

  &::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 15px;
    height: 15px;
    border-top: 2px solid rgba(54, 209, 220, 0.7);
    border-left: 2px solid rgba(54, 209, 220, 0.7);
    border-top-left-radius: 4px;
  }
  
  .panel-corner-br {
    position: absolute;
    right: 0;
    bottom: 0;
    width: 15px;
    height: 15px;
    border-bottom: 2px solid rgba(91, 134, 229, 0.7);
    border-right: 2px solid rgba(91, 134, 229, 0.7);
    border-bottom-right-radius: 4px;
  }
  
  .panel-id {
    position: absolute;
    right: 10px;
    bottom: 5px;
    font-size: 10px;
    color: rgba(59, 141, 255, 0.5);
    font-family: monospace;
    z-index: 1;
  }

  &:hover {
    border-color: rgba(59, 141, 255, 0.5);
    box-shadow: 0 0 20px rgba(59, 141, 255, 0.3);
    
    &::before {
      opacity: 1;
    }
  }

  .panel-header {
    height: 40px;
    line-height: 40px;
    padding: 0 20px;
    background: linear-gradient(90deg, rgba(27, 54, 123, 0.5), rgba(5, 25, 70, 0.5));
    font-size: 16px;
    font-weight: bold;
    color: #5b86e5;
    border-bottom: 1px solid rgba(59, 141, 255, 0.1);
    position: relative;
    display: flex;
    justify-content: space-between;
    align-items: center;
    overflow: hidden;

    &::before {
      content: '';
      position: absolute;
      left: 0;
      top: 50%;
      transform: translateY(-50%);
      width: 4px;
      height: 16px;
      background: linear-gradient(to bottom, #36d1dc, #5b86e5);
    }
    
    &::after {
      content: '';
      position: absolute;
      top: 0;
      left: -100%;
      width: 100%;
      height: 100%;
      background: linear-gradient(90deg, 
        transparent, 
        rgba(54, 209, 220, 0.2), 
        transparent
      );
      animation: scanLine 10s infinite;
    }

    .panel-tags {
      display: flex;
      gap: 10px;
      
      .tag {
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: normal;
        
        &.tag-today {
          background: rgba(54, 209, 220, 0.2);
          color: #36d1dc;
        }
        
        &.tag-total {
          background: rgba(91, 134, 229, 0.2);
          color: #5b86e5;
        }
      }
    }
  }

  @keyframes scanLine {
    0% {
      left: -100%;
    }
    40%, 60% {
      left: 100%;
    }
    100% {
      left: 100%;
    }
  }

  .panel-body {
    flex: 1;
    padding: 10px;
    display: flex;
    overflow: hidden;
  }
}

.panel-sm {
  flex: 1;
  min-width: 0;
}

.panel-resources {
  height: 45%;
  min-height: 340px;
  overflow: visible;
  background: rgba(3, 19, 57, 0.9);
  box-shadow: 0 5px 25px rgba(0, 0, 0, 0.2), 0 0 15px rgba(59, 141, 255, 0.15);
  
  .panel-body {
    padding: 0;
  }
}

.panel-user {
  height: 52%;
  overflow: visible;
  box-shadow: 0 5px 25px rgba(0, 0, 0, 0.2), 0 0 15px rgba(59, 141, 255, 0.15);
}

.panel-api {
  height: calc(100% - 280px);
  min-height: 350px;
  display: flex;
  flex-direction: column;
}

.panel-api .panel-body {
  flex: 1;
  min-height: 300px;
  display: flex;
  padding: 10px;
  overflow: hidden;
}

.chart-loading {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  color: rgba(91, 134, 229, 0.7);
  font-size: 14px;
  position: relative;
  
  &::after {
    content: '';
    position: absolute;
    width: 20px;
    height: 20px;
    border: 2px solid transparent;
    border-top-color: #36d1dc;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-left: 10px;
  }
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style> 