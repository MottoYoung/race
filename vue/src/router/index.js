import { createRouter, createWebHistory } from 'vue-router'

// 正确导入
import { FullScreen } from '@element-plus/icons-vue'

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes: [
    // 管理员数据可视化大屏 - 放在最前面确保优先匹配
    {
      path: '/admin-dashboard',
      name: 'AdminDashboard',
      component: () => import('@/views/charts1/index.vue'),
      meta: {title:'管理员数据监控中心', requiresAuth: true}
    },

    {
      path: '/',
      name: 'StartPage',
      meta: {title:'开始页面'},
      component: () => import('@/views/StartPage.vue')
    },

    // 认证相关
    {
      path: '/auth',
      redirect: '/auth/login',
      children: [
        {
          path: 'login',
          name: 'Login',
          meta: {title:'登录页面'},
          component: () => import('@/views/auth/Login.vue')
        },
      ]
    },

    {
      path: '/main',
      component: () => import('@/views/main/MainLayout.vue'),
      meta: { title: '主页面', requiresAuth: true },
      redirect: '/main/home',
      children: [
        {
          path: 'home',
          name: 'home',
          component: () => import('@/views/main/functions/Home.vue')
        },
        {
          path: 'prepare', name: 'prepare', component: () => import('@/views/main/functions/app-jiaoan-ok.vue')
        },
        {
          path: 'image',
          name: 'image',
          component: () => import('@/views/main/functions/Image.vue')
        },
        {
          path: 'resource',
          name: 'resource',
          component: () => import('@/views/main/functions/Video1.vue')
        },
        {
          path: 'exercise',
          name: 'exercise',
          component: () => import('@/views/main/functions/mainExercise.vue')
        },
        // {
        //   path: 'analysis',
        //   name: 'analysis',
        //   component: () => import('@/views/main/chart.vue')
        // },
        {
          path: 'PPT',
          name: 'PPT',
          component: () => import('@/views/main/functions/PPTmaker.vue')
        },
        {
          path: 'pptvideo',
          name: 'pptvideo',
          component: () => import('@/views/main/functions/CombinedComponent.vue')
        },
        {
          path: 'resource-recommend',
          name: 'resource-recommend',
          // component: () => import('@/components/ExternalRedirect.vue')
        },
        {
          path: 'homework',
          name: 'homework',
          component: () => import('@/views/main/functions/Homework.vue')
        }
      ]
    },
    {
      path: '/analysis',
      name: 'analysis',
      component: () => import('@/views/main/functions/Analysis.vue')
    },
    
    // 教师数据可视化大屏
    {
      path: '/dashboard',
      component: () => import('@/views/charts/index.vue'),
      meta: {title:'教师端数据可视化'},
      children: [
        {
          path: '',
          name: 'TeacherDashboard',
          component: () => import('@/views/charts/TeacherDashboard.vue')
        }
      ]
    },
    
    // 进错页面
    { 
      path: '/404', 
      name: 'NotFound', 
      meta: {title:'404找不到页面'},
      component: () => import('../views/404.vue'),
    },
    { 
      path: '/:pathMatch(.*)', 
      redirect: (to) => {
        // 避免将 admin-dashboard 相关的路径重定向到 404
        if (to.path.startsWith('/admin-dashboard')) {
          return '/admin-dashboard';
        }
        return '/404';
      } 
    }
  ]
})
// beforeEach表示跳转之前的一些操作
router.beforeEach((to, from, next) => {
  // 设置页面标题
  if (to.meta.title) {
    document.title = to.meta.title;
  }
  
  // 特殊处理：确保管理员路径不会错误跳转
  if (to.path.startsWith('/admin-dashboard')) {
    const userJson = localStorage.getItem('user');
    if (userJson) {
      const user = JSON.parse(userJson);
      if (user.role === 'admin') {
        // 管理员访问管理员大屏，正常通过
        return next();
      }
    }
    // 如果非管理员或未登录尝试访问管理员页面，重定向到登录
    return next({ path: '/auth/login' });
  }
  
  // 检查是否需要登录权限
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // 检查用户是否已登录
    const userJson = localStorage.getItem('user');
    if (!userJson) {
      // 未登录，重定向到登录页面
      next({ path: '/auth/login' });
    } else {
      // 已登录，继续
      next();
    }
  } else if (to.path === '/auth/login') {
    // 如果用户已登录并试图访问登录页面，根据角色重定向到相应页面
    const userJson = localStorage.getItem('user');
    if (userJson) {
      const user = JSON.parse(userJson);
      if (user.role === 'student') {
        next({ path: '/main' });
      } else if (user.role === 'teacher') {
        next({ path: '/main' });
      } else if (user.role === 'admin') {
        // 确保管理员角色正确跳转到管理员大屏
        next({ path: '/admin-dashboard', replace: true });
      } else {
        next();
      }
    } else {
      next();
    }
  } else {
    // 不需要登录权限的路由
    next();
  }
})

export default router
