<template>
  <div class="auth-container">
    <div class="tech-bg"></div>
    <div class="tech-grid"></div>
    <div class="tech-circles">
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
      <div class="circle circle-3"></div>
    </div>
    <div class="auth-content">
      <div class="auth-left">
        <div class="tech-text">
          <h1>Empower your teaching journey with our AI-driven solution</h1>
          <p>Streamline your planning process and spark creativity</p>
        </div>
        
        <div class="tech-features">
          <div class="feature">
            <el-icon><Monitor /></el-icon>
            <span>智能备课系统</span>
          </div>
          <div class="feature">
            <el-icon><DataLine /></el-icon>
            <span>数据分析</span>
          </div>
          <div class="feature">
            <el-icon><Connection /></el-icon>
            <span>PPT讲解</span>
          </div>
          <div class="feature">
            <el-icon><Magic /></el-icon>
            <span>AI 辅助</span>
          </div>
        </div>
        
        <div class="tech-stats">
          <div class="stat-item">
            <div class="stat-number">10K+</div>
            <div class="stat-label">活跃用户</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">98%</div>
            <div class="stat-label">满意度</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">24/7</div>
            <div class="stat-label">技术支持</div>
          </div>
        </div>
      </div>
      
      <div class="auth-form">
        <div class="glow-effect"></div>
        <div class="tech-scanner"></div>
        
        <div class="logo">
          <img src="@/assets/img/登记.png" alt="SmartPrep.ai">
        </div>
        
        <h2 class="form-title">{{ isLogin ? 'Sign In' : 'Register' }}</h2>
        
        <el-alert
          v-if="errorMsg"
          :title="errorMsg"
          type="error"
          :closable="false"
          show-icon
          class="error-message"
        />
        
        <!-- 角色选择器 -->
        <div class="role-selector">
          <div class="role-label">选择身份</div>
          <div class="tech-role-selector">
            <div 
              class="role-option" 
              :class="{ active: role === 'student' }" 
              @click="role = 'student'"
            >
              <el-icon><User /></el-icon>
              <span>学生</span>
            </div>
            <div 
              class="role-option" 
              :class="{ active: role === 'teacher' }" 
              @click="role = 'teacher'"
            >
              <el-icon><Briefcase /></el-icon>
              <span>老师</span>
            </div>
            <div 
              class="role-option" 
              :class="{ active: role === 'admin' }" 
              @click="role = 'admin'"
            >
              <el-icon><Setting /></el-icon>
              <span>管理员</span>
            </div>
          </div>
        </div>
        
        <el-form 
          ref="formRef"
          :model="form"
          :rules="rules"
          @submit.prevent="submitForm"
          class="login-form"
        >
          <el-form-item 
            v-if="role !== 'admin' || !isLogin"
            prop="email"
            class="tech-form-item"
          >
            <el-input
              v-model="form.email"
              type="email"
              placeholder="name@example.com"
              :disabled="role === 'admin' && isLogin"
              class="tech-input"
            >
              <template #prefix>
                <el-icon><Message /></el-icon>
              </template>
            </el-input>
          </el-form-item>
          
          <el-form-item prop="password" class="tech-form-item">
            <el-input
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="********"
              show-password
              class="tech-input"
            >
              <template #prefix>
                <el-icon><Lock /></el-icon>
              </template>
            </el-input>
          </el-form-item>
          
          <div v-if="!isLogin && role !== 'admin'" class="password-requirements">
            <el-card shadow="never" class="tech-card">
              <template #header>
                <div class="card-header">
                  <span>密码要求</span>
                  <el-icon><InfoFilled /></el-icon>
                </div>
              </template>
              <ul>
                <li>至少8个字符</li>
                <li>包含大、小写字母</li>
                <li>包含数字</li>
              </ul>
            </el-card>
          </div>
          
          <el-button 
            type="primary" 
            native-type="submit" 
            :loading="isSubmitting"
            class="submit-btn glow-btn"
          >
            {{ isSubmitting ? '处理中...' : (isLogin ? '登录' : '注册') }}
          </el-button>
          
          <div class="login-options">
            <div class="switch-mode">
              <span @click="toggleMode">{{ isLogin ? '注册账号' : '返回登录' }}</span>
            </div>
          </div>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { loginUser, registerUser } from '@/api/auth'
import { 
  Monitor, DataLine, Connection, Magic, Message, Lock, 
  InfoFilled, User, Briefcase, Setting 
} from '@element-plus/icons-vue'

export default {
  name: 'AuthPage',
  components: {
    Monitor,
    DataLine,
    Connection,
    Magic,
    Message,
    Lock,
    InfoFilled,
    User,
    Briefcase,
    Setting
  },
  setup() {
    const router = useRouter()
    const formRef = ref(null)
    const isLogin = ref(true)
    const role = ref('student')
    const errorMsg = ref('')
    const isSubmitting = ref(false)
    const showPassword = ref(false)
    
    const form = reactive({
      email: '',
      password: ''
    })
    
    const roles = [
      { label: '学生', value: 'student' },
      { label: '老师', value: 'teacher' },
      { label: '管理员', value: 'admin' }
    ]
    
    const rules = {
      email: [
        { required: true, message: '请输入邮箱地址', trigger: 'blur' },
        { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 8, message: '密码长度不能小于8位', trigger: 'blur' }
      ]
    }

    // 测试API连接
    onMounted(() => {
      // 检查用户是否已登录
      const userJson = localStorage.getItem('user');
      if (userJson) {
        try {
          const user = JSON.parse(userJson);
          // 如果用户已登录，根据角色自动跳转
          if (user.role === 'student') {
            router.push('/image-process');
          } else if (user.role === 'teacher') {
            router.push('/main');
          } else if (user.role === 'admin') {
            router.push('/admin-dashboard');
          }
        } catch (e) {
          console.error('解析用户数据失败:', e);
          // 出错时清除localStorage中的用户数据
          localStorage.removeItem('user');
        }
      }
      
      // 测试API是否可用
      fetch('/api/auth/test')
        .then(res => res.json())
        .then(data => {
          console.log('API测试结果:', data);
        })
        .catch(err => {
          console.error('API测试失败:', err);
          errorMsg.value = '无法连接到服务器，请确保后端服务已启动';
        });
    });

    // 监听角色变化
    watch(role, (newRole) => {
      // 当选择管理员角色且在登录模式时，自动填充admin
      if (newRole === 'admin' && isLogin.value) {
        form.email = 'admin';
        form.password = 'admin';
      } else if (newRole !== 'admin') {
        // 如果切换到其他角色，清空字段
        if (form.email === 'admin') {
          form.email = '';
        }
        if (form.password === 'admin') {
          form.password = '';
        }
      }
    });

    const toggleMode = () => {
      isLogin.value = !isLogin.value
      form.email = ''
      form.password = ''
      errorMsg.value = ''
      
      // 切换到登录模式时，如果是管理员，自动填充admin
      if (isLogin.value && role.value === 'admin') {
        form.email = 'admin'
        form.password = 'admin'
      }
    }

    const submitForm = async () => {
      if (formRef.value) {
        await formRef.value.validate(async (valid) => {
          if (valid) {
            try {
              errorMsg.value = ''
              isSubmitting.value = true
              
              // 检查管理员特殊情况
              if (role.value === 'admin' && isLogin.value) {
                form.email = 'admin'
                form.password = 'admin'
              }
              
              if (isLogin.value) {
                // 登录逻辑
                console.log('尝试登录:', { email: form.email, password: form.password, role: role.value });
                
                const response = await loginUser(form.email, form.password, role.value);
                
                console.log('登录响应:', response.data);
                
                if (response.data.success) {
                  // 存储用户信息到 localStorage
                  localStorage.setItem('user', JSON.stringify(response.data.user))
                  // 根据角色跳转到不同页面
                  if (role.value === 'student') {
                    router.push('/image-process')
                  } else if (role.value === 'teacher') {
                    router.push('/main')
                  } else if (role.value === 'admin') {
                    router.push('/admin-dashboard')
                  } else {
                    router.push('/main')
                  }
                } else {
                  errorMsg.value = response.data.message || '登录失败，请检查账号和密码'
                }
              } else {
                // 注册逻辑
                if (role.value === 'admin') {
                  errorMsg.value = '管理员账号不允许注册'
                  isSubmitting.value = false
                  return
                }
                
                // 验证密码强度
                if (form.password.length < 8 ||
                    !/[A-Z]/.test(form.password) ||
                    !/[a-z]/.test(form.password) ||
                    !/[0-9]/.test(form.password)) {
                  errorMsg.value = '密码必须包含大小写字母和数字，且长度至少为8位'
                  isSubmitting.value = false
                  return
                }
                
                console.log('尝试注册:', { email: form.email, password: form.password, role: role.value });
                
                const response = await registerUser(form.email, form.password, role.value);
                
                console.log('注册响应:', response.data);
                
                if (response.data.success) {
                  alert('注册成功，请登录')
                  isLogin.value = true
                  form.email = ''
                  form.password = ''
                } else {
                  errorMsg.value = response.data.message || '注册失败，请重试'
                }
              }
            } catch (error) {
              console.error('操作错误:', error)
              errorMsg.value = error.response?.data?.message || '操作失败，请检查网络连接并重试'
            } finally {
              isSubmitting.value = false
            }
          }
        });
      }
    }

    return {
      formRef,
      form,
      rules,
      isLogin,
      email: form.email,
      password: form.password,
      role,
      roles,
      showPassword,
      errorMsg,
      isSubmitting,
      toggleMode,
      submitForm
    }
  }
}
</script>

<style scoped>
.auth-container {
  display: flex;
  min-height: 100vh;
  background: #162654;
  position: relative;
  overflow: hidden;
}

.tech-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1;
}

.tech-grid {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    linear-gradient(rgba(126, 192, 255, 0.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(126, 192, 255, 0.06) 1px, transparent 1px);
  background-size: 30px 30px;
  animation: gridMove 20s linear infinite;
}

.tech-circles {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.circle {
  position: absolute;
  border-radius: 50%;
  background: linear-gradient(45deg, rgba(142, 198, 255, 0.07), rgba(158, 206, 255, 0.07));
  animation: float 8s ease-in-out infinite;
}

.circle-1 {
  width: 300px;
  height: 300px;
  top: -100px;
  left: -100px;
  animation-delay: 0s;
}

.circle-2 {
  width: 200px;
  height: 200px;
  top: 50%;
  right: -50px;
  animation-delay: -2s;
}

.circle-3 {
  width: 150px;
  height: 150px;
  bottom: -50px;
  left: 50%;
  animation-delay: -4s;
}

.auth-content {
  display: flex;
  width: 100%;
  max-width: 1400px;
  margin: auto;
  padding: 2rem;
  position: relative;
  z-index: 2;
  min-height: calc(100vh - 4rem); /* Adjusted to account for padding */
}

.auth-left {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  color: #e6f1ff;
  padding: 0 4rem;
  position: relative;
}

.tech-text h1 {
  font-size: 3.5rem;
  line-height: 1.2;
  margin-bottom: 1.5rem;
  background: linear-gradient(45deg, #7ecaff, #9ed0ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: glow 2s ease-in-out infinite alternate;
}

.tech-features {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  margin-top: 3rem;
}

.feature {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  background: rgba(142, 198, 255, 0.04);
  border-radius: 16px;
  border: 1px solid rgba(142, 198, 255, 0.08);
  transition: all 0.3s ease;
}

.feature:hover {
  transform: translateY(-5px);
  background: rgba(142, 198, 255, 0.06);
  border-color: rgba(142, 198, 255, 0.15);
  box-shadow: 0 10px 30px rgba(142, 198, 255, 0.08);
}

.feature .el-icon {
  font-size: 2rem;
  color: #9ed0ff;
  background: rgba(142, 198, 255, 0.06);
  padding: 1rem;
  border-radius: 12px;
}

.feature span {
  font-size: 1.2rem;
  font-weight: 500;
  color: #e6f1ff;
}

.tech-stats {
  display: flex;
  gap: 2rem;
  margin-top: 3rem;
  position: relative;
  z-index: 2;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 700;
  color: #9ed0ff;
  margin-bottom: 0.5rem;
  background: linear-gradient(45deg, #7ecaff, #9ed0ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.stat-label {
  color: #bbc8e3;
  font-size: 1rem;
}

.auth-form {
  flex: 1;
  max-width: 450px;
  background: rgba(35, 53, 100, 0.6);
  border-radius: 24px;
  padding: 3rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(15px);
  border: 1px solid rgba(142, 198, 255, 0.12);
  margin-left: auto;
  position: relative;
  overflow: visible;
  transition: all 0.3s ease;
}

.auth-form:hover {
  box-shadow: 0 12px 40px rgba(142, 198, 255, 0.1);
  border-color: rgba(142, 198, 255, 0.2);
}

.glow-effect {
  position: absolute;
  width: 150px;
  height: 150px;
  background: radial-gradient(circle, rgba(142, 198, 255, 0.25) 0%, rgba(142, 198, 255, 0) 70%);
  border-radius: 50%;
  top: -75px;
  right: -75px;
  z-index: 0;
  filter: blur(30px);
  animation: pulse 4s infinite;
}

.tech-scanner {
  position: absolute;
  width: 100%;
  height: 3px;
  background: linear-gradient(90deg, transparent, rgba(142, 198, 255, 0.6), transparent);
  top: 0;
  left: 0;
  z-index: 1;
  animation: scan 4s ease-in-out infinite;
}

@keyframes scan {
  0% {
    top: 0;
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  80% {
    opacity: 0.5;
  }
  100% {
    top: 100%;
    opacity: 0;
  }
}

@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 0.3;
  }
  50% {
    transform: scale(1.2);
    opacity: 0.5;
  }
  100% {
    transform: scale(1);
    opacity: 0.3;
  }
}

.form-title {
  font-size: 1.8rem;
  color: #e6f1ff;
  margin-bottom: 1.5rem;
  text-align: center;
  background: linear-gradient(45deg, #7ecaff, #9ed0ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: 1px;
}

.logo {
  text-align: center;
  margin-bottom: 1.5rem;
}

.logo img {
  height: 60px;
  animation: glow 3s ease-in-out infinite alternate;
}

.role-selector {
  margin-bottom: 2rem;
}

.role-label {
  color: #bbc8e3;
  margin-bottom: 0.8rem;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  text-align: center;
}

.tech-role-selector {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  width: 100%;
}

.role-option {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 12px;
  background: rgba(45, 67, 121, 0.6);
  border: 1px solid rgba(142, 198, 255, 0.12);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.role-option:hover {
  transform: translateY(-2px);
  border-color: rgba(142, 198, 255, 0.25);
  box-shadow: 0 5px 15px rgba(142, 198, 255, 0.06);
}

.role-option.active {
  background: rgba(142, 198, 255, 0.07);
  border-color: rgba(142, 198, 255, 0.25);
  box-shadow: 0 0 15px rgba(142, 198, 255, 0.12);
}

.role-option .el-icon {
  font-size: 22px;
  color: #9ed0ff;
  background: rgba(142, 198, 255, 0.07);
  padding: 8px;
  border-radius: 8px;
}

.role-option span {
  color: #bbc8e3;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.role-option:hover span,
.role-option.active span {
  color: #9ed0ff;
}

.login-form {
  position: relative;
  z-index: 2;
}

.tech-form-item {
  margin-bottom: 1.5rem;
}

.tech-input :deep(.el-input__wrapper) {
  background: rgba(45, 67, 121, 0.4);
  border: 1px solid rgba(142, 198, 255, 0.12);
  box-shadow: none;
  transition: all 0.3s ease;
  border-radius: 12px;
  padding: 0 15px;
  height: 52px;
}

.tech-input :deep(.el-input__wrapper:hover),
.tech-input :deep(.el-input__wrapper.is-focus) {
  border-color: rgba(142, 198, 255, 0.25);
  box-shadow: 0 0 10px rgba(142, 198, 255, 0.12);
}

.tech-input :deep(.el-input__prefix) {
  color: #9ed0ff;
  margin-right: 10px;
}

.tech-input :deep(.el-input__inner) {
  color: #e6f1ff;
}

.tech-input :deep(.el-input__inner::placeholder) {
  color: #7d8db6;
}

.submit-btn {
  width: 100%;
  height: 50px;
  border: none;
  background: linear-gradient(45deg, #7ecaff, #9ed0ff);
  margin-top: 1rem;
  font-size: 1.1rem;
  letter-spacing: 1px;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.glow-btn:before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(45deg, transparent, rgba(255,255,255,0.2), transparent);
  transform: rotate(45deg);
  animation: shine 3s infinite;
}

@keyframes shine {
  0% {
    left: -100%;
  }
  20%, 100% {
    left: 100%;
  }
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 7px 15px rgba(142, 198, 255, 0.2);
}

.password-requirements {
  margin: 1rem 0;
}

.tech-card {
  background: rgba(45, 67, 121, 0.5);
  border: 1px solid rgba(142, 198, 255, 0.12);
  border-radius: 12px;
}

.tech-card :deep(.el-card__header) {
  border-bottom: 1px solid rgba(142, 198, 255, 0.08);
  padding: 0.6rem 1rem;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: #9ed0ff;
  font-size: 0.85rem;
}

.tech-card ul {
  list-style: none;
  padding: 0.4rem 1rem;
  margin: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tech-card li {
  color: #bbc8e3;
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  width: calc(50% - 0.25rem);
}

.tech-card li:before {
  content: '•';
  color: #9ed0ff;
  margin-right: 8px;
}

.login-options {
  display: flex;
  justify-content: flex-end;
  margin-top: 1.5rem;
}

.switch-mode span {
  color: #9ed0ff;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s ease;
  position: relative;
}

.switch-mode span:hover {
  color: #b6dfff;
}

.switch-mode span:after {
  content: '';
  position: absolute;
  width: 0;
  height: 1px;
  bottom: -2px;
  left: 0;
  background-color: #b6dfff;
  transition: width 0.3s ease;
}

.switch-mode span:hover:after {
  width: 100%;
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
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
  }
}

@keyframes glow {
  from {
    text-shadow: 0 0 10px rgba(142, 198, 255, 0.3);
  }
  to {
    text-shadow: 0 0 20px rgba(142, 198, 255, 0.6);
  }
}

@media (max-width: 992px) {
  .auth-content {
    flex-direction: column;
    padding: 1rem;
  }
  
  .auth-left {
    padding: 2rem 0;
    text-align: center;
  }
  
  .tech-features {
    grid-template-columns: 1fr;
    max-width: 400px;
    margin: 2rem auto;
  }
  
  .tech-stats {
    justify-content: center;
  }
  
  .auth-form {
    margin: 0 auto;
    padding: 2rem;
  }
}
</style>