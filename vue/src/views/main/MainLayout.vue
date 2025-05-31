<template>
  <div class="app-container" :class="{ 'light-mode': isLightMode }">
    <!-- 侧边栏 -->
    <el-menu
      :collapse="isSidebarCollapsed"
      class="sidebar"
      :default-active="activeMenu"
      background-color="transparent"
      :text-color="
        isLightMode ? 'rgba(89, 54, 24, 0.8)' : 'rgba(255, 255, 255, 0.8)'
      "
      :active-text-color="isLightMode ? '#d86500' : '#ff9e5e'"
      :collapse-transition="false"
    >
      <!-- 顶部Logo和系统名称 -->
      <div class="sidebar-header">
        <div class="logo-container">
          <img src="../../assets/img/study.png" alt="Logo" class="logo" />
          <span class="system-name" v-if="!isSidebarCollapsed"
            >智教双擎</span
          >
        </div>
      </div>

      <!-- 搜索框 -->
      <div class="search-container" v-if="!isSidebarCollapsed">
        <div class="search-wrapper">
          <el-icon class="search-icon-input"><Search /></el-icon>
          <input
            type="text"
            class="search-input"
            placeholder="搜索功能..."
            v-model="searchQuery"
          />
        </div>
      </div>
      <div class="search-icon-container" v-else>
        <el-tooltip content="搜索" placement="right" effect="light">
          <el-button circle class="search-icon-btn">
            <el-icon><Search /></el-icon>
          </el-button>
        </el-tooltip>
      </div>

      <!-- 导航菜单 - 修改为垂直展开的二级菜单结构 -->
      <div
        v-for="(item, index) in filteredNavItems"
        :key="index"
        class="menu-item-wrapper"
      >
        <!-- 父菜单项 -->
        <div
          class="parent-nav-item"
          :class="{ 'is-active': isActiveParent(item) }"
        >
          <el-menu-item
            :index="getDefaultSubItemPath(item)"
            @click="item.children ? toggleSubMenu(item.id) : handleSubItemClick(item.path, item)"
            class="nav-item parent-item"
          >
            <div class="nav-item-content">
              <el-icon>
                <component :is="item.icon"></component>
              </el-icon>
              <span class="nav-text" v-show="!isSidebarCollapsed">{{
                item.name
              }}</span>
              <el-icon
                v-if="!isSidebarCollapsed && item.children"
                class="submenu-indicator"
                :class="{ 'is-expanded': activeSubmenu === item.id }"
              >
                <ArrowDown v-if="activeSubmenu === item.id" />
                <ArrowRight v-else />
              </el-icon>
            </div>
          </el-menu-item>

          <!-- 二级菜单，垂直展开显示 -->
          <transition name="submenu-slide">
            <div
              v-if="
                item.children &&
                activeSubmenu === item.id &&
                !isSidebarCollapsed
              "
              class="submenu-vertical"
            >
              <el-menu-item
                v-for="(subItem, subIndex) in item.children"
                :key="subIndex"
                :index="subItem.path"
                @click="handleSubItemClick(subItem.path, subItem)"
                class="nav-item submenu-item"
              >
                <div class="nav-item-content submenu-content">
                  <el-icon>
                    <component :is="subItem.icon"></component>
                  </el-icon>
                  <span class="nav-text">{{ subItem.name }}</span>
                </div>
              </el-menu-item>
            </div>
          </transition>
        </div>
      </div>

      <!-- 主题切换按钮 -->
      <div class="theme-toggle-container">
        <el-tooltip
          :content="isLightMode ? '切换到夜间模式' : '切换到日间模式'"
          placement="right"
          effect="light"
        >
          <el-button circle class="theme-toggle-btn" @click="toggleThemeMode">
            <el-icon v-if="isLightMode"><Moon /></el-icon>
            <el-icon v-else><Sunny /></el-icon>
          </el-button>
        </el-tooltip>
        <span v-if="!isSidebarCollapsed" class="theme-text">
          {{ isLightMode ? "切换到夜间模式" : "切换到日间模式" }}
        </span>
      </div>
    </el-menu>

    <!-- 添加吸附在侧边栏边缘的展开/收起按钮 -->
    <div class="sidebar-toggle-container">
      <button class="toggle-button-fixed" @click="toggleSidebar">
        <el-icon>
          <ArrowLeft v-if="!isSidebarCollapsed" />
          <ArrowRight v-else />
        </el-icon>
      </button>
    </div>

    <!-- 主内容区域 -->
    <div class="main-container">
      <!-- 顶部导航栏 -->
      <div class="header">
        <div class="header-left">
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/main' }"
              >首页</el-breadcrumb-item
            >
            <el-breadcrumb-item>{{ currentPageName }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>

        <div class="header-right">
          <div class="header-tools">
            <el-tooltip content="通知" placement="bottom" effect="light">
              <el-badge :value="3" class="tool-item">
                <el-button circle class="tool-button">
                  <el-icon><Bell /></el-icon>
                </el-button>
              </el-badge>
            </el-tooltip>
            <el-tooltip content="帮助" placement="bottom" effect="light">
              <el-button circle class="tool-button">
                <el-icon><QuestionFilled /></el-icon>
              </el-button>
            </el-tooltip>
          </div>

          <div class="user-info">
            <el-dropdown trigger="click">
              <div class="user-avatar-container">
                <el-avatar :size="32" src="../../assets/img/avatar.png" />
                <span class="username">教师用户</span>
                <el-icon class="el-icon--right"><ArrowDown /></el-icon>
              </div>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item>
                    <el-icon><User /></el-icon>个人中心
                  </el-dropdown-item>
                  <el-dropdown-item>
                    <el-icon><Setting /></el-icon>系统设置
                  </el-dropdown-item>
                  <el-dropdown-item divided @click="handleLogout">
                    <el-icon><SwitchButton /></el-icon>退出登录
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>
      </div>

      <!-- 主内容 -->
      <div class="content-wrapper">
        <el-card class="content-card" :body-style="{ padding: '0' }">
          <transition name="fade-transform" mode="out-in">
            <RouterView />
          </transition>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, defineComponent, nextTick, provide } from "vue";
import { useRoute, useRouter } from "vue-router";
import { logoutUser, getCurrentUser } from "@/api/auth";
import { ElMessage, ElMessageBox } from "element-plus";
import axios from 'axios'; // 添加axios导入
import {
  Notebook,
  Picture,
  Document,
  VideoPlay,
  Collection,
  Search,
  User,
  Setting,
  SwitchButton,
  ArrowDown,
  ArrowLeft,
  ArrowRight,
  Bell,
  QuestionFilled,
  Moon,
  Sunny,
  Home,
  Reading,
  Files,
  Connection,
  VideoCameraFilled, // 添加这个图标导入
  Avatar, // 添加数字人图标
} from "@element-plus/icons-vue";

export default defineComponent({
  components: {
    Notebook,
    Picture,
    Document,
    VideoPlay,
    Collection,
    Search,
    User,
    Setting,
    SwitchButton,
    ArrowDown,
    ArrowLeft,
    ArrowRight,
    Bell,
    QuestionFilled,
    Moon,
    Sunny,
    Home,
    Reading,
    Files,
    Connection,
    VideoCameraFilled, // 添加到组件列表中
    Avatar, // 添加到组件列表
  },
  setup() {
    const isSidebarCollapsed = ref(false);
    const searchQuery = ref("");
    const route = useRoute();
    const router = useRouter();
    const isLightMode = ref(false);
    const currentUser = ref(getCurrentUser());
    const activeSubmenu = ref(null);

    // 需要全屏显示的路由列表
    const fullscreenRoutes = [
      "/main/exercise",
      "/main/prepare",
      "/main/image",
      "/main/resource",
      "/main/PPT",
      "/main/home",
      "/main/pptvideo",
    ];

    // 添加DOM引用
    const sidebarRef = ref(null);

    // 修改导航菜单结构，支持子菜单
    const navItems = computed(() => {
      // 基础菜单项 - 所有角色都能看到
      const baseItems = [
        { 
          id: "resources",
          name: "学习资源",
          icon: "Reading",
          children: [
          { 
              name: "资源推荐", 
              icon: "Reading", 
              path: "/main/resource-recommend",
              handler: () => {
                // 直接跳转到外部URL
                window.location.href = '/api/recommend/login';
              }
            },
            { name: "课后习题", icon: "Files", path: "/main/homework" },
          ]
        }
      ];

      // 如果是教师角色，添加教师特有的菜单项
      if (currentUser.value && currentUser.value.role === "teacher") {
        return [
          { name: "首页", icon: "House", path: "/main/home" },
          { name: "智慧助教", icon: "Avatar", path: "/main/digital-assistant", handler: runDigitalAssistant },
          { 
            id: "ai-teaching",
            name: "AI备课助手",
            icon: "Connection",
            children: [
              { name: "教案生成", icon: "Notebook", path: "/main/prepare" },
              { name: "图片生成", icon: "Picture", path: "/main/image" },
              { name: "视频生成", icon: "VideoPlay", path: "/main/resource" },
              { name: "PPT生成", icon: "Collection", path: "/main/PPT" },
              {name: "PPT讲解", icon: "VideoCameraFilled", path: "/main/pptvideo"},
              { name: "试题生成", icon: "Document", path: "/main/exercise" },
            ],
          },
          ...baseItems,
        ];
      }

      // 其他角色（如学生）只看到基本菜单
      return baseItems;
    });

    const filteredNavItems = computed(() => {
      if (!searchQuery.value) return navItems.value;

      // 搜索匹配主菜单和子菜单
      return navItems.value
        .map((item) => {
          // 创建一个新对象，避免修改原对象
          const newItem = { ...item };
          if (item.children) {
            newItem.children = item.children.filter((subItem) =>
              subItem.name
                .toLowerCase()
                .includes(searchQuery.value.toLowerCase())
            );
            // 只有子菜单有匹配项或主菜单名称匹配时才返回
            return newItem.children.length > 0 ||
              item.name.toLowerCase().includes(searchQuery.value.toLowerCase())
              ? newItem
              : null;
          }
          // 对于没有子菜单的项，直接检查名称
          return item.name
            .toLowerCase()
            .includes(searchQuery.value.toLowerCase())
            ? newItem
            : null;
        })
        .filter(Boolean); // 移除空值
    });

    const activeMenu = computed(() => route.path);

    // 判断父菜单是否处于激活状态
    const isActiveParent = (item) => {
      if (!item.children) return activeMenu.value === item.path;
      return item.children.some((child) => activeMenu.value === child.path);
    };

    // 获取子菜单的第一个路径作为默认路径
    const getDefaultSubItemPath = (item) => {
      return item.children && item.children.length > 0
        ? item.children[0].path
        : item.path || "";
    };

    const currentPageName = computed(() => {
      const currentPath = route.path;

      // 搜索所有子菜单项
      for (const item of navItems.value) {
        if (item.children) {
          for (const subItem of item.children) {
            if (subItem.path === currentPath) {
              return subItem.name;
            }
          }
        } else if (item.path === currentPath) {
          return item.name;
        }
      }

      return "页面";
    });

    const toggleSidebar = async () => {
      // 直接切换状态
      isSidebarCollapsed.value = !isSidebarCollapsed.value;

      // 使用 nextTick 等待 DOM 更新完成，但不再强制重排
      await nextTick();
    };

    // 添加一个标志来控制路由切换行为
    const isNavigating = ref(false);

    // 修改navigateTo函数
    const navigateTo = async (path, item) => {
      if (isNavigating.value) return;

      isNavigating.value = true;

      // 检查是否有正在进行的对话
      const hasActiveConversation =
        localStorage.getItem("has_active_conversation") === "true";

      if (hasActiveConversation && path !== route.path) {
        // 使用Element Plus的确认对话框
        ElMessageBox.confirm("切换功能将中断当前对话，是否继续？", "提示", {
          confirmButtonText: "继续",
          cancelButtonText: "取消",
          type: "warning",
        })
          .then(() => {
            // 用户确认切换
            router.push(path);
            activeMenu.value = path;
          })
          .catch(() => {
            // 用户取消切换，不执行任何操作
          })
          .finally(() => {
            isNavigating.value = false;
          });
      } else {
        // 没有活跃对话，直接切换
        router.push(path);
        activeMenu.value = path;
        isNavigating.value = false;
      }
    };

    // 添加专门处理子菜单点击的方法
    const handleSubItemClick = (path, item) => {
      // 如果菜单项有自定义处理程序，优先调用
      if (item.handler && typeof item.handler === 'function') {
        item.handler();
        return;
      }
      
      // 没有处理程序则继续使用导航方法
      navigateTo(path, item);
    };

    // 提供一个方法让子组件设置活跃对话状态
    const setActiveConversation = (active) => {
      localStorage.setItem(
        "has_active_conversation",
        active ? "true" : "false"
      );
    };

    // 使用provide提供给子组件
    provide("setActiveConversation", setActiveConversation);

    // 从localStorage读取主题设置
    onMounted(() => {
      const savedTheme = localStorage.getItem("theme-mode");
      if (savedTheme === "light") {
        isLightMode.value = true;
      }

      // 设置当前活动菜单
      activeMenu.value = route.path;
      
      // 添加: 根据当前路由自动打开对应的子菜单
      for (const item of navItems.value) {
        if (item.children) {
          for (const subItem of item.children) {
            if (subItem.path === route.path) {
              // 找到对应的子菜单项，设置其父菜单为展开状态
              activeSubmenu.value = item.id;
              break;
            }
          }
        }
      }
    });

    // 切换主题模式
    const toggleThemeMode = () => {
      isLightMode.value = !isLightMode.value;
      localStorage.setItem("theme-mode", isLightMode.value ? "light" : "dark");

      // 触发自定义事件，通知所有子组件主题已更改
      window.dispatchEvent(new Event("themeChange"));
    };

    // 修改为展开/收起子菜单的函数
    const toggleSubMenu = (id) => {
      if (isSidebarCollapsed.value) {
        // 如果侧边栏已折叠，先展开侧边栏
        isSidebarCollapsed.value = false;
        // 使用nextTick确保DOM更新后再展开子菜单
        nextTick(() => {
          activeSubmenu.value = id === activeSubmenu.value ? null : id;
        });
      } else {
        // 直接切换子菜单的展开状态
        activeSubmenu.value = id === activeSubmenu.value ? null : id;
      }
    };

    const handleLogout = () => {
      // 清除用户信息并跳转到登录页
      logoutUser();
      ElMessage.success("退出登录成功");
      router.push("/");
    };

    // 添加数字人助手运行函数
    const runDigitalAssistant = () => {
      ElMessage.info('正在启动数字人助手...');
      
      axios.post('/api/run-exe', {
        path: 'D:/Desktop/csrace/计设/design/server/assistant/AI.exe'
      })
      .then(response => {
        if (response.data.success) {
          ElMessage.success('数字人助手已启动');
        } else {
          ElMessage.error('启动失败: ' + response.data.error);
        }
      })
      .catch(error => {
        console.error('API调用失败:', error);
        ElMessage.error('无法启动数字人助手: ' + (error.response?.data?.error || error.message));
      });
    };

    return {
      isSidebarCollapsed,
      searchQuery,
      navItems,
      filteredNavItems,
      activeMenu,
      currentPageName,
      toggleSidebar,
      navigateTo,
      route,
      fullscreenRoutes,
      isLightMode,
      toggleThemeMode,
      handleLogout,
      currentUser,
      activeSubmenu,
      isActiveParent,
      getDefaultSubItemPath,
      toggleSubMenu,
      handleSubItemClick,
      runDigitalAssistant, // 添加到返回值中
    };
  },
});
</script>

<style>
@import url("https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700&display=swap");

/* 基础样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: "Nunito", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
  color: #2c3e50;
  background-color: #f8fafc;
}

/* 应用容器 */
.app-container {
  display: flex;
  width: 100%;
  height: 100vh;
  overflow: hidden;
  position: relative;
  /* 夜间模式（默认） */
  background-color: #2d2339;
  color: #e6ecf5;
  transition: background-color 0.3s, color 0.3s;
}

/* 日间模式 */
.app-container.light-mode {
  background-color: #fff9f0;
  color: #593618;
}

/* 侧边栏样式 */
.sidebar {
  width: auto;
  height: 100%;
  background: linear-gradient(135deg, #352941, #5e3a6e);
  background-size: 200% 200%;
  animation: gradientBackground 15s ease infinite;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
  border-right: 0;
  will-change: width;
  transition: width 0.5s ease-out;
  overflow: hidden;
  z-index: 1000;
  display: flex;
  flex-direction: column;
}

/* 日间模式下的侧边栏 */
.light-mode .sidebar {
  background: linear-gradient(135deg, #f4a259, #f7cb87);
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.05);
}

@keyframes gradientBackground {
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

.el-menu {
  border-right: none;
  transition: width 0.5s ease-out !important;
}

.el-menu--collapse {
  width: 64px;
}

.sidebar:not(.el-menu--collapse) {
  width: 240px;
}

/* 侧边栏顶部 */
.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: center; /* 修改为居中 */
  padding: 20px 16px;
  margin-bottom: 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo-container {
  display: flex;
  align-items: center;
}

.logo {
  width: 36px;
  height: 36px;
  object-fit: contain;
  filter: drop-shadow(0 2px 8px rgba(255, 255, 255, 0.6));
  transition: transform 0.5s ease;
}

.logo:hover {
  transform: scale(1.1) rotate(5deg);
}

/* 系统名称样式 */
.system-name {
  margin-left: 12px;
  font-size: 18px;
  font-weight: 700;
  color: #fff;
  letter-spacing: 0.5px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  overflow: hidden;
  white-space: nowrap;
  transition: opacity 0.15s ease;
}

.light-mode .system-name {
  color: #b35c00;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.toggle-button {
  color: #fff;
  background-color: rgba(255, 255, 255, 0.2);
  border: none;
  transition: all 0.5s;
}

.toggle-button:hover {
  background-color: rgba(255, 255, 255, 0.3);
  transform: scale(1.1);
}

/* 搜索框 */
.search-container {
  padding: 0 16px 16px 16px;
  margin-bottom: 10px;
}

.search-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  background-color: rgba(255, 255, 255, 0.15);
  border-radius: 20px;
  padding: 0 12px;
}

.search-icon-input {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.7);
  margin-right: 8px;
  background-color: rgba(255, 255, 255, 0.15);
}

.light-mode .search-icon-input {
  color: rgba(179, 92, 0, 0.6);
}

.search-input {
  width: 100%;
  padding: 10px 0;
  border: none;
  background: transparent;
  font-size: 14px;
  color: #ffffff;
  outline: none;
}

.light-mode .search-input {
  background-color: transparent;
  color: #b35c00;
}

.search-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.light-mode .search-input::placeholder {
  color: rgba(179, 92, 0, 0.6);
}

.search-icon-container {
  display: flex;
  justify-content: center;
  padding: 10px 0;
  margin-bottom: 10px;
  width: 100%;
}

.search-icon-btn {
  background-color: rgba(255, 255, 255, 0.2);
  color: #fff;
  border: none;
}

.light-mode .search-icon-btn {
  background-color: rgba(179, 92, 0, 0.15);
  color: #b35c00;
  border: none;
}

.search-icon-btn:hover {
  background-color: rgba(255, 255, 255, 0.3);
}

/* 导航菜单项 */
.nav-item {
  height: 56px;
  margin: 4px 12px;
  padding: 0 16px !important;
  border-radius: 8px;
  overflow: hidden;
}

.el-menu-item.is-active {
  background: rgba(255, 255, 255, 0.2) !important;
  color: #ff9e5e !important;  /* 夜间模式活动项 */
}

.light-mode .el-menu-item.is-active {
  background: rgba(255, 255, 255, 0.5) !important;
  color: #d86500 !important;  /* 日间模式活动项 */
}

.el-menu-item:hover {
  background-color: rgba(255, 255, 255, 0.1) !important;
}

.nav-item-content {
  display: flex;
  align-items: center;
  width: 100%;
}

.el-menu--collapse .nav-item {
  padding: 0 !important;
  display: flex;
  justify-content: center;
}

.el-menu--collapse .menu-item-content {
  justify-content: center;
}

.el-menu--collapse .nav-icon {
  margin-right: 0;
  margin-left: 0;
}

.nav-icon {
  font-size: 18px;
  margin-right: 10px;
  transition: transform 0.5s;
}

.el-menu-item:hover .nav-icon {
  transform: scale(1.2);
}

.nav-text {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  transition: opacity 0.15s ease;
}

/* 边缘展开/收起按钮容器 */
.sidebar-toggle-container {
  position: absolute;
  top: 45%; /* 从50%改为40%, 向上移动10% */
  transform: translateY(-50%);
  z-index: 1001;
}

/* 边缘固定的展开/收起按钮 - 水滴拼接效果 */
.toggle-button-fixed {
  position: relative;
  left: 0;
  height: 80px; /* 调整高度 */
  width: 20px; /* 调整宽度 */
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(255, 158, 94, 0.6); /* 夜间模式 - 橙色按钮 */
  color: #fff;
  border: none;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
  /* 特殊的border-radius创建水滴拼接形状 */
  border-radius: 0 80% 80% 0 / 50% 50% 50% 50%;
  cursor: pointer;
  transition: all 0.25s;
}

.light-mode .toggle-button-fixed {
  background-color: rgba(216, 101, 0, 0.6); /* 日间模式 - 深橙色按钮 */
}

/* 当侧边栏展开时按钮的位置 */
.sidebar:not(.el-menu--collapse) ~ .sidebar-toggle-container {
  left: 240px; /* 与侧边栏展开宽度相同 */
}

/* 当侧边栏收起时按钮的位置 */
.el-menu--collapse ~ .sidebar-toggle-container {
  left: 64px; /* 与侧边栏收起宽度相同 */
}

.toggle-button-fixed:hover {
  background-color: rgba(216, 101, 0, 0.8); /* 悬停时加深，但保持同色系 */
  width: 24px; /* 悬停时稍微变宽 */
}

.toggle-button-fixed .el-icon {
  font-size: 12px; /* 调整图标大小 */
  transition: transform 0.25s;
}

.toggle-button-fixed:hover .el-icon {
  transform: scale(1.2); /* 悬停时图标放大 */
}

.toggle-button-fixed:focus {
  outline: none;
}

/* 主内容区域 */
.main-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: margin-left 0.15s ease-out;
  background-color: #2d2339; /* 夜间模式 - 深紫色背景 */
  position: relative; /* 添加相对定位使内容不被按钮覆盖 */
  z-index: 100;
  width: calc(100% - 64px); /* 减去折叠侧边栏宽度 */
}

/* 日间模式下的主容器 */
.light-mode .main-container {
  background-color: #fff9f0; /* 日间模式 - 米色背景 */
}

/* 顶部导航栏 - 适配深色主题 */
.header {
  height: 60px;
  background-color: #3d2d4e; /* 夜间模式 - 深紫色背景 */
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  z-index: 100;
  color: #e6ecf5;
}

.light-mode .header {
  background-color: #ffffff; /* 日间模式 - 纯白色背景 */
  box-shadow: 0 2px 8px rgba(244, 162, 89, 0.1);
  color: #593618; /* 日间模式 - 深棕色文字 */
}

.header-left {
  display: flex;
  align-items: center;
}

.header-right {
  display: flex;
  align-items: center;
}

.header-tools {
  display: flex;
  margin-right: 16px;
}

.tool-item {
  margin: 0 6px;
}

.tool-button {
  background: transparent;
  color: #c2a5dd; /* 夜间模式 - 浅紫色图标 */
  border: none;
  font-size: 18px;
  transition: transform 0.5s;
  padding: 8px;
}

.light-mode .tool-button {
  background: transparent;
  color: #593618; /* 日间模式 - 深棕色图标 */
  border: none;
  font-size: 18px;
  transition: transform 0.5s;
  padding: 8px;
}

.tool-button:hover {
  transform: scale(1.1);
  color: #ff9e5e; /* 夜间模式悬停 - 橙色 */
  background-color: rgba(255, 158, 94, 0.1);
}

.light-mode .tool-button:hover {
  color: #f4a259; /* 日间模式悬停 - 金黄色 */
  background-color: rgba(244, 162, 89, 0.1);
}

.user-info {
  display: flex;
  align-items: center;
}

.user-avatar-container {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 5px 8px;
  border-radius: 20px;
  transition: all 0.5s;
  background-color: rgba(255, 255, 255, 0.1); /* 半透明背景 */
}

.light-mode .user-avatar-container {
  background-color: rgba(179, 92, 0, 0.08); /* 日间模式 - 半透明橙色背景 */
}

.user-avatar-container:hover {
  background-color: rgba(255, 158, 94, 0.15); /* 夜间模式悬停 - 半透明橙色 */
}

.light-mode .user-avatar-container:hover {
  background-color: rgba(244, 162, 89, 0.15); /* 日间模式悬停 - 半透明金黄色 */
}

.username {
  margin: 0 8px;
  font-size: 14px;
  color: #e6ecf5;
  font-weight: 500;
}

.light-mode .username {
  color: #593618; /* 日间模式 - 深棕色文字 */
}

/* 面包屑导航样式 */
.el-breadcrumb__inner {
  color: #c2a5dd !important; /* 夜间模式 - 浅紫色文字 */
  font-weight: normal !important;
}

.light-mode .el-breadcrumb__inner {
  color: #f4a259 !important; /* 日间模式 - 金黄色文字 */
}

.el-breadcrumb__inner.is-link:hover {
  color: #ff9e5e !important; /* 夜间模式悬停 - 橙色 */
}

.light-mode .el-breadcrumb__inner.is-link:hover {
  color: #d86500 !important; /* 日间模式悬停 - 深橙色 */
}

.el-breadcrumb__separator {
  color: #7d6391 !important; /* 夜间模式 - 浅紫色分隔符 */
}

.light-mode .el-breadcrumb__separator {
  color: #f7cb87 !important; /* 日间模式 - 浅金色分隔符 */
}

/* 内容区域 */
.content-wrapper {
  flex: 1;
  padding: 10px;
  overflow: hidden; /* 改为hidden防止滚动冲突 */
  display: flex;
  width: 100%; /* 确保宽度占满 */
}

.content-card {
  height: calc(100% - 20px); /* 确保高度正确 */
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  border-radius: 12px;
  border:1px solid #150d3a;
  background-color: #3d2d4e; /* 夜间模式 - 深紫色背景 */
  color: #e6ecf5;
  display: flex;
  flex-direction: column;
  overflow: hidden; /* 防止内容溢出 */
  width: 100%; /* 确保宽度占满 */
  flex: 1; /* 让卡片占满可用空间 */
}

/* 日间模式下的内容卡片 */
.light-mode .content-card {
  background-color: #ffffff; /* 日间模式 - 纯白色背景 */
  color: #593618; /* 日间模式 - 深棕色文字 */
  box-shadow: 0 4px 20px rgba(244, 162, 89, 0.08); /* 日间模式 - 金黄色阴影 */
  border:1px solid #f7cb87;
}

/* 确保子路由视图占满卡片内容区域 */
.content-card .el-card__body {
  flex: 1;
  height: 100%;
  width: 100%; /* 确保宽度占满 */
  overflow: hidden;
  padding: 0 !important; /* 移除内边距 */
}

/* 全屏内容容器 */
.fullscreen-content {
  height: 100%;
  width: 100%;
  overflow: hidden;
  flex: 1; /* 确保占满可用空间 */
}

.content-wrapper .fullscreen-content {
  margin: -20px;
  flex: 1;
  width: calc(100% + 40px); /* 补偿margin的影响 */
}

/* 过渡动画 */
.fade-transform-enter-active,
.fade-transform-leave-active {
  transition: all 0.5s;
}

.fade-transform-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.fade-transform-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

/* 响应式设计 */
@media (max-width: 992px) {
  .sidebar {
    position: absolute;
    height: 100%;
    z-index: 2000;
    transform: translateX(0);
    transition: transform 0.15s ease-out;
  }

  .sidebar.collapsed {
    transform: translateX(-100%);
  }

  .el-menu--collapse {
    width: 64px;
  }
}

@media (max-width: 768px) {
  .header {
    padding: 0 15px;
  }

  .username {
    display: none;
  }

  .content-wrapper {
    padding: 15px;
  }

  .header-tools {
    margin-right: 8px;
  }

  .tool-item {
    margin: 0 3px;
  }
}

/* 滚动条美化 */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: rgba(144, 147, 153, 0.3);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(144, 147, 153, 0.5);
}

/* 当侧边栏展开时调整主容器宽度 */
.sidebar:not(.el-menu--collapse) ~ .main-container {
  width: calc(100% - 240px); /* 减去展开侧边栏宽度 */
}

/* 主题切换按钮 */
.theme-toggle-container {
  margin-top: auto;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.theme-toggle-btn {
  background: rgba(255, 158, 94, 0.15) !important; /* 夜间模式 - 半透明橙色背景 */
  border: none !important;
  color: rgba(255, 255, 255, 0.8) !important;
}

.light-mode .theme-toggle-btn {
  background: rgba(244, 162, 89, 0.1) !important; /* 日间模式 - 半透明金黄色背景 */
  color: #593618 !important; /* 日间模式 - 深棕色图标 */
}

.theme-text {
  font-size: 14px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.8);
}

.light-mode .theme-text {
  color: #593618; /* 日间模式 - 深棕色文字 */
}

/* 二级菜单样式 */
.parent-nav-item {
  position: relative;
}

.parent-nav-item.is-active > .nav-item {
  background: rgba(255, 158, 94, 0.2) !important; /* 夜间模式 - 半透明橙色背景 */
}

.light-mode .parent-nav-item.is-active > .nav-item {
  background: rgba(244, 162, 89, 0.15) !important; /* 日间模式 - 半透明金黄色背景 */
}

/* 垂直展开的子菜单样式 */
.submenu-vertical {
  overflow: hidden;
  background: rgba(45, 35, 57, 0.5); /* 夜间模式 - 半透明深紫色背景 */
  border-radius: 0 0 8px 8px;
  margin: 0 12px;
  margin-top: -4px;
}

.light-mode .submenu-vertical {
  background: rgba(244, 162, 89, 0.08); /* 日间模式 - 半透明金黄色背景 */
}

/* 子菜单项样式 */
.submenu-item {
  height: 44px !important;
  margin: 4px 8px !important;
  border-radius: 6px !important;
  padding-left: 24px !important;
}

.submenu-content {
  padding-left: 8px;
}

/* 展开/收起动画 */
.submenu-slide-enter-active,
.submenu-slide-leave-active {
  transition: all 0.3s ease;
  max-height: 300px;
}

.submenu-slide-enter-from,
.submenu-slide-leave-to {
  max-height: 0;
  opacity: 0;
}

/* 菜单容器样式 */
.menu-item-wrapper {
  margin: 4px 0;
}
</style>
