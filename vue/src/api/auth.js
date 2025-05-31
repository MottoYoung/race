import axios from 'axios'

// 设置基础URL
const API_URL = '/api/auth'

// 创建axios实例
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 添加请求拦截器
api.interceptors.request.use(
  config => {
    // 从localStorage获取用户信息
    const user = JSON.parse(localStorage.getItem('user') || '{}')
    
    // 如果有token，在header中添加Authentication
    if (user && user.token) {
      config.headers.Authorization = `Bearer ${user.token}`
    }
    
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 获取登录页面信息（如果需要的话）
export const getLoginPage = () => {
  return api.get('/login')
    .catch(error => {
      console.warn('获取登录页面失败，这可能是预期行为，如果后端不支持GET /login：', error);
      // 静默失败，因为这可能是预期的行为
      return { data: null };
    });
}

export const loginUser = (email, password, role) => {
  return api.post('/login', { email, password, role })
    .then(response => {
      // Save user data including role to localStorage
      if (response.data.success) {
        localStorage.setItem('user', JSON.stringify(response.data.user));
      }
      return response;
    });
}

export const registerUser = (email, password, role) => {
  return api.post('/register', { email, password, role })
}

export const logoutUser = () => {
  localStorage.removeItem('user')
}

// 获取当前用户信息
export const getCurrentUser = () => {
  const userJson = localStorage.getItem('user')
  if (userJson) {
    return JSON.parse(userJson)
  }
  return null
}

// 检查用户是否已登录
export const isAuthenticated = () => {
  return localStorage.getItem('user') !== null
}

export default api