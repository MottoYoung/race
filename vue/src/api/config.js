// 如果在生产环境，使用环境变量中的API URL
// 否则使用相对路径 (在同一个域名下)
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? process.env.VUE_APP_API_URL 
  : '';

export default API_BASE_URL;
