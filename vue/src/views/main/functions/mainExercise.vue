<template>
  <div class="app-container" :class="{ 'light-mode': isLightMode }">
    <div v-if="toast.show" class="toast" :class="toast.type">
      {{ toast.message }}
    </div>
    <!-- 主内容区域 -->
    <div class="main-content">
      <!-- 侧边栏移到主内容区域内 -->
      <div
        class="sidebar"
        :class="{ collapsed: isCollapsed, hidden: isHidden }"
      >
        <div class="sidebar-header">
          <h2>历史对话</h2>
          <button @click="createNewConversation" class="new-chat-btn">
            <span class="btn-icon">+</span>
            <span class="btn-text" v-if="!isCollapsed">新建对话</span>
          </button>
        </div>
        <div class="conversation-list" v-show="!isCollapsed">
          <div
            v-for="conv in conversations"
            :key="conv.id"
            class="conversation-item"
            :class="{ active: activeConversationId === conv.id }"
            @click="switchConversation(conv.id)"
          >
            <div class="conv-info">
              <div class="conv-title">{{ conv.title }}</div>
              <div class="conv-time">{{ formatDate(conv.timestamp) }}</div>
            </div>
            <button
              class="delete-btn"
              @click.stop="deleteConversation(conv.id)"
            >
              <span class="delete-icon">×</span>
            </button>
          </div>
        </div>
      </div>

      <!-- 修改chat-container的class绑定 -->
      <div
        class="chat-container"
        :class="{ 'editing-mode': isEditing, 'sidebar-expanded': !isHidden }"
      >
        <div class="conversation-pane">
          <header class="chat-header">
            <!-- 将折叠按钮移到这里 -->
            <button @click="toggleSidebar" class="toggle-sidebar-btn">
              <span v-if="isHidden">☰</span>
              <span v-else>✕</span>
            </button>
            <div class="header-decoration"></div>
            <h1>智能试题生成</h1>
            <div class="branding">
              <span class="ai-logo">AI</span>
              <span class="powered-by">Powered by DeepSeek</span>
            </div>
          </header>

          <div class="chat-window" ref="chatWindow">
            <div
              v-for="(msg, index) in messages"
              :key="index"
              :class="['message', msg.role]"
            >
              <div class="message-content">
                <div class="avatar" :class="msg.role">
                  <img src="../../../assets/img/logo.png" alt="Avatar" />
                </div>
                <div class="bubble">
                  <div class="text">
                    <template v-if="msg.role === 'assistant'">
                      <!-- 思考过程部分 -->
                      <div
                        class="thinking-process"
                        v-if="msg.reasoning && msg.reasoning.trim()"
                      >
                        <div
                          class="thinking-header"
                          @click="toggleReasoning(index)"
                        >
                          <span class="thinking-icon">💡</span> 思考过程
                          <span class="toggle-icon">{{
                            msg.showReasoning ? "▼" : "▶"
                          }}</span>
                        </div>
                        <!-- 将思考过程内容放在思考过程盒子内 -->
                        <div
                          class="reasoning-content"
                          v-if="msg.showReasoning"
                          v-html="compiledMarkdown(msg.reasoning)"
                        ></div>
                      </div>

                      <!-- 正式回答部分 - 使用白色背景 -->
                      <div
                        class="correct-answer"
                        v-if="msg.content && msg.content.trim()"
                      >
                        <div class="correct-answer-label">
                          <span class="correct-answer-icon">📝</span> 正式回答
                        </div>
                        <div
                          class="correct-answer-content"
                          v-html="compiledMarkdown(msg.content)"
                        ></div>
                      </div>

                      <!-- 正在回答的提示 -->
                      <div
                        class="answering-indicator"
                        v-if="msg.isAnswering && !msg.content"
                      >
                        <div class="dot-flashing-small"></div>
                        <span
                          >AI 正在思考{{ ".".repeat(msg.thinkingDots) }}</span
                        >
                      </div>
                    </template>

                    <div
                      v-if="msg.role === 'user' && msg.content"
                      class="markdown-body"
                    >
                      <div v-html="compiledMarkdown(msg.content)"></div>
                    </div>
                  </div>

                  <div class="message-actions">
                    <button
                      class="edit-button"
                      v-if="msg.role === 'assistant'"
                      @click="startEditing(index)"
                    >
                      <span class="button-icon">✏️</span>
                      编辑
                    </button>
                    <button
                      class="break-button"
                      v-if="msg.role === 'assistant'"
                      @click="breaktalk(index)"
                    >
                      <span class="button-icon">⏹️</span>
                      打断
                    </button>
                    <div class="timestamp">{{ formatTime(msg.timestamp) }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="input-area">
            <div class="file-upload">
              <input
                type="file"
                ref="fileInput"
                @change="handleFileUpload"
                :disabled="loading"
                multiple
                style="display: none"
              />
              <button
                type="button"
                class="upload-button"
                @click="triggerFileUpload"
              >
                <span class="upload-icon">📎</span>
                <span class="upload-text">上传文件</span>
              </button>
              <span class="upload-tip">支持PDF/Word/PPT/TXT/MD</span>
            </div>

            <div class="text-inputer">
              <input
                v-model="inputMsg"
                type="text"
                placeholder="请输入您的问题..."
                :disabled="loading"
                @keyup.enter="sendMessage"
              />
            </div>

            <div class="send-button">
              <button @click="sendMessage" :disabled="!inputMsg || loading">
                <span v-if="!loading" class="send-icon">▶</span>
                <span class="send-text">{{
                  loading ? "思考中..." : "发送"
                }}</span>
              </button>
            </div>
          </div>
          <div v-if="loading" class="loading-indicator">
            <div class="dot-flashing"></div>
          </div>
        </div>
        <div v-if="isEditing" class="editor-pane">
          <div class="editor-header">
            <h1>在线编辑</h1>
            <div class="editor-actions">
              <button class="save-button" @click="saveEditing">保存</button>
              <button class="cancel-button" @click="cancelEditing">取消</button>
              <button class="export-button" @click="saveToWord(editingContent)">
                导出Word
              </button>
            </div>
          </div>
          <div id="vditor-container" ref="vditorContainer"></div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { MathpixMarkdownModel as MM } from "mathpix-markdown-it";
import "highlight.js/styles/a11y-dark.css";
import { marked } from "marked";

// 配置MathpixMarkdownModel使用KaTeX
MM.setOptions({
  mathJax: false, // 禁用MathJax
  katex: true, // 启用KaTeX
});

// 优化Markdown渲染函数
const compiledMarkdownCache = new Map();

const compiledMarkdown = (val) => {
  if (!val) return "";

  // 使用缓存避免重复渲染相同内容
  if (compiledMarkdownCache.has(val)) {
    return compiledMarkdownCache.get(val);
  }

  const result = MM.markdownToHTML(val, {
    htmlTags: true,
    codeHighlight: {
      auto: true,
      code: true,
    },
  });

  // 缓存结果
  compiledMarkdownCache.set(val, result);
  return result;
};
</script>

<script setup>
import { ref, nextTick, watch, onMounted, onBeforeUnmount } from "vue";

import { saveAs } from "file-saver";
import hljs from "highlight.js";
import "highlight.js/styles/github.css";
import Vditor from "vditor";
import "vditor/dist/index.css";

const saveToWord = async (content) => {
  try {
    // 显示加载提示并阻止自动清除
    showToast("正在生成Word文档...", "info", false);

    // 调用后端API
    const response = await fetch("/api/exercise/export-word", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ content }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || "导出失败");
    }

    // 获取文件blob
    const blob = await response.blob();

    // 使用file-saver保存文件
    saveAs(blob, "习题.docx");

    // 导出成功后显示成功提示（自动清除）
    showToast("Word文档导出成功", "success", true);
  } catch (error) {
    console.error("导出Word文档失败:", error);
    // 出错时显示错误提示（自动清除）
    showToast(`导出失败: ${error.message}`, "error", true);
  }
};

const conversations = ref([]);
const activeConversationId = ref(null);
const inputMsg = ref("");
const messages = ref([]);
const userId = ref(localStorage.getItem("userId") || Date.now().toString());
if (!localStorage.getItem("userId")) {
  localStorage.setItem("userId", userId.value);
}
const abortController = ref(null);

const loading = ref(false);
const chatWindow = ref(null);
const isEditing = ref(false);
const editingIndex = ref(-1);
const editingContent = ref("");
const have_file = ref(false);
const isCollapsed = ref(true);
const isHidden = ref(true);
const vditorContainer = ref(null);
let vditorInstance = null;

// 在 setup 函数中添加 uploadStatus 变量
const uploadStatus = ref(""); // 添加上传状态变量

function convertMathpixToLatex(mathpixMarkdown) {
  if (!mathpixMarkdown) return "";

  // 先检查内容中是否已经包含 $$ 格式的公式，避免重复转换导致嵌套
  if (mathpixMarkdown.includes("$$")) {
    return mathpixMarkdown;
  }

  // 处理块级公式 \[ ... \] 转换为 $$ ... $$
  let converted = mathpixMarkdown.replace(
    /\\\[([\s\S]*?)\\\]/g,
    function (match, p1) {
      return `\n$$${p1.trim()}$$\n`; // 确保前后有换行
    }
  );

  // 处理行内公式 \( ... \) 转换为 $ ... $
  converted = converted.replace(/\\\(([\s\S]*?)\\\)/g, function (match, p1) {
    return `$${p1.trim()}$`;
  });

  return converted;
}

const initVditor = () => {
  if (vditorContainer.value) {
    vditorInstance = new Vditor(vditorContainer.value, {
      cache: {
        id: "vditor-cache",
        enable: true,
      },
      height: "100%",
      mode: "wysiwyg", // 实时预览模式
      toolbar: [
        "headings",
        "bold",
        "italic",
        "strike",
        "|",
        "line",
        "quote",
        "list",
        "ordered-list",
        "check",
        "code",
        "inline-code",
        "|",
        "link",
        "image",
        "table",
        "|",
        "formula", // 数学公式按钮
        "fullscreen",
      ],
      preview: {
        math: {
          engine: "KaTeX", // 使用KaTeX
          inlineDigit: true,
        },
        markdown: {
          autoSpace: true,
          fixTermLink: true,
        },
        hljs: {
          enable: true,
          lineNumber: true,
        },
      },
      input: (value) => {
        // 实时更新编辑内容
        editingContent.value = value;
      },
      after: () => {
        nextTick(() => {
          // 先转换Mathpix格式为标准LaTeX格式
          const convertedContent = convertMathpixToLatex(editingContent.value);
          if (vditorInstance) {
            vditorInstance.setValue(convertedContent);
          }
        });
      },
    });
  }
};

// 监听编辑状态
watch(isEditing, (val) => {
  if (val) {
    nextTick(() => {
      initVditor();
    });
  } else {
    vditorInstance?.destroy();
  }
});

const toast = ref({
  show: false,
  message: "",
  type: "info", // info/success/error
  timeoutId: null, // 添加这个属性来跟踪超时ID
});

const showToast = (message, type = "info", autoClear = true) => {
  // 如果已经有一个显示中的相同消息和类型的提示，不要重新创建
  if (
    toast.value.show &&
    toast.value.message === message &&
    toast.value.type === type
  ) {
    return;
  }

  // 清除任何现有的超时
  if (toast.value.timeoutId) {
    clearTimeout(toast.value.timeoutId);
  }

  // 设置新的提示
  toast.value = {
    show: true,
    message,
    type,
    timeoutId: null,
  };

  // 如果需要自动清除，设置超时
  if (autoClear) {
    toast.value.timeoutId = setTimeout(() => {
      toast.value.show = false;
    }, 3000);
  }
};
// 配置 Markdown 解析器
marked.setOptions({
  highlight: (code, lang) => {
    const language = hljs.getLanguage(lang) ? lang : "plaintext";
    return hljs.highlight(code, { language }).value;
  },
  breaks: true,
  gfm: true,
});
// 添加一个变量来控制是否自动滚动
const autoScroll = ref(true);
const userHasScrolled = ref(false);

// 修复滚动方法，添加保护性检查
const scrollToBottom = () => {
  // 添加null检查
  if (chatWindow.value) {
    nextTick(() => {
      if (chatWindow.value) {  // 二次检查以确保DOM元素存在
        chatWindow.value.scrollTo({
          top: chatWindow.value.scrollHeight,
          behavior: "smooth",
        });
      }
    });
  }
};

// 添加滚动事件监听
onMounted(() => {
  // 修改本地存储键名，添加功能前缀
  const saved = localStorage.getItem("math_conversations");
  if (saved) {
    const rawData = JSON.parse(saved);
    conversations.value = rawData.map((conv) => ({
      ...conv,
      timestamp: new Date(conv.timestamp), // 恢复会话时间
      messages: conv.messages.map((msg) => ({
        ...msg,
        timestamp: new Date(msg.timestamp), // 恢复消息时间
      })),
    }));

    if (conversations.value.length > 0) {
      activeConversationId.value = conversations.value[0].id;
    }

    // 确保在DOM更新后滚动到底部
    nextTick(() => {
      scrollToBottom();
      // 添加一个延迟再次滚动，确保所有内容都已完全渲染
      setTimeout(scrollToBottom, 300);
    });
  }

  // 添加滚动事件监听
  if (chatWindow.value) {
    chatWindow.value.addEventListener("scroll", handleScroll);
  }

  // 添加动态标题效果
  const title = document.querySelector(".chat-header h1");
  if (title) {
    const text = title.textContent;
    title.innerHTML = "";

    for (let i = 0; i < text.length; i++) {
      const span = document.createElement("span");
      span.textContent = text[i];
      span.style.animationDelay = `${i * 0.1}s`;
      span.classList.add("char-animation");
      title.appendChild(span);
    }
  }

  // 添加主题监听
  checkThemeMode();
  window.addEventListener("storage", checkThemeMode);
  window.addEventListener("themeChange", checkThemeMode);

  // 设置交叉观察器来优化长消息的渲染
  messageObserver.value = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        // 为进入视口的消息添加可见类
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
        }
      });
    },
    { root: chatWindow.value, threshold: 0.1 }
  );

  // 观察现有消息
  nextTick(() => {
    document.querySelectorAll(".message").forEach((msg) => {
      messageObserver.value.observe(msg);
    });
  });
});

onBeforeUnmount(() => {
  // 移除事件监听
  if (chatWindow.value) {
    chatWindow.value.removeEventListener("scroll", handleScroll);
  }
  window.removeEventListener("storage", checkThemeMode);
  window.removeEventListener("themeChange", checkThemeMode);

  // 断开交叉观察器
  if (messageObserver.value) {
    messageObserver.value.disconnect();
  }
});
const isLightMode = ref(localStorage.getItem("theme-mode") === "light");
// 添加检查主题的方法
const checkThemeMode = () => {
  isLightMode.value = localStorage.getItem("theme-mode") === "light";
};

// 处理滚动事件
const handleScroll = () => {
  if (!chatWindow.value || !loading.value) return;

  const container = chatWindow.value;
  const isAtBottom =
    container.scrollHeight - container.scrollTop - container.clientHeight < 50;

  // 如果用户向上滚动，暂停自动滚动
  if (!isAtBottom && !userHasScrolled.value) {
    userHasScrolled.value = true;
    autoScroll.value = false;
  }

  // 如果用户滚动到底部，恢复自动滚动
  if (isAtBottom && userHasScrolled.value) {
    userHasScrolled.value = false;
    autoScroll.value = true;
  }
};

// 创建新对话
const createNewConversation = () => {
  const newId = Date.now().toString() + Math.random().toString(36).substr(2, 9);
  const newConv = {
    id: newId,
    title: `对话 ${conversations.value.length + 1}`,
    timestamp: new Date(),
    messages: [],
  };
  conversations.value.unshift(newConv);
  activeConversationId.value = newId;
  messages.value = [];

  // 重置文件上传状态
  have_file.value = false;

  // 保存到本地存储
  saveToLocalStorage();

  // 如果正在编辑，退出编辑模式
  if (isEditing.value) {
    isEditing.value = false;
  }

  // 确保在DOM更新后滚动到底部
  nextTick(() => {
    scrollToBottom();
  });

  return newId;
};

const switchConversation = (id) => {
  if (loading.value) {
    showToast("请等待当前对话完成", "info");
    return;
  }

  activeConversationId.value = id;
  const conv = conversations.value.find((c) => c.id === id);
  if (conv) {
    messages.value = conv.messages;

    // 检查该对话是否有上传的文件
    have_file.value = false;
    if (userId.value && id) {
      // 异步检查文件状态
      fetch(`/api/exercise/check-files`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: userId.value,
          conversation_id: id,
        }),
      })
        .then((res) => res.json())
        .then((data) => {
          have_file.value = data.has_files;
        })
        .catch((err) => {
          console.error("检查文件状态失败:", err);
        });
    }
  }

  // 如果正在编辑，退出编辑模式
  if (isEditing.value) {
    isEditing.value = false;
  }

  // 确保在DOM更新后滚动到底部
  nextTick(() => {
    scrollToBottom();
    // 添加一个延迟再次滚动，确保所有内容都已完全渲染
    setTimeout(scrollToBottom, 300);
  });
};

// 删除对话
const deleteConversation = (convId) => {
  conversations.value = conversations.value.filter((c) => c.id !== convId);
  if (activeConversationId.value === convId) {
    activeConversationId.value = conversations.value[0]?.id || null;
  }
  saveToLocalStorage();
};
// 自动生成标题
const generateTitle = (message) => {
  const firstMessage = message.substring(0, 30);
  return firstMessage.length < message.length
    ? firstMessage + "..."
    : firstMessage;
};

// 发送消息时更新对话
watch(
  messages,
  (newMsgs) => {
    const conv = conversations.value.find(
      (c) => c.id === activeConversationId.value
    );
    if (conv) {
      // 直接保存Date对象，不进行转换
      conv.messages = [...newMsgs];

      // 自动更新标题
      const firstUserMsg = newMsgs.find((m) => m.role === "user");
      if (firstUserMsg) {
        conv.title = generateTitle(firstUserMsg.content);
      }
      conv.timestamp = new Date(); // 保持为Date对象
      saveToLocalStorage(); // 调用统一保存方法
    }
  },
  { deep: true }
);
// 本地存储 - 修改键名
const saveToLocalStorage = () => {
  const dataToSave = conversations.value.map((conv) => ({
    ...conv,
    // 添加安全转换
    timestamp:
      conv.timestamp instanceof Date
        ? conv.timestamp.getTime()
        : new Date(conv.timestamp).getTime(),
    messages: conv.messages.map((msg) => ({
      ...msg,
      timestamp:
        msg.timestamp instanceof Date
          ? msg.timestamp.getTime()
          : new Date(msg.timestamp).getTime(),
    })),
  }));

  // 使用带前缀的键名
  localStorage.setItem("math_conversations", JSON.stringify(dataToSave));
};

// 时间格式化
const formatDate = (date) => {
  const actualDate = date instanceof Date ? date : new Date(Number(date));
  return actualDate.toLocaleTimeString("zh-CN", {
    hour: "2-digit",
    minute: "2-digit",
  });
};

// 添加文件输入引用
const fileInput = ref(null);

// 添加触发文件选择对话框的方法
const triggerFileUpload = () => {
  fileInput.value.click();
};

// 修改文件上传处理函数
const handleFileUpload = async (event) => {
  const files = event.target.files;
  if (!files || files.length === 0) return;

  if (!activeConversationId.value) {
    createNewConversation();
    await nextTick();
  }

  try {
    showToast("正在上传文件...", "info");

    const formData = new FormData();

    // 检查文件类型 - 更新允许的文件类型列表
    const allowedTypes = [
      "application/pdf",
      "application/msword",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
      "application/vnd.ms-powerpoint",
      "application/vnd.openxmlformats-officedocument.presentationml.presentation",
      "text/plain",
      "text/markdown",
    ];

    // 添加所有选择的文件
    let validFiles = 0;
    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      // 检查文件类型 - 添加对PPT文件的支持
      if (
        !allowedTypes.includes(file.type) &&
        !file.name.endsWith(".md") &&
        !file.name.endsWith(".txt") &&
        !file.name.endsWith(".doc") &&
        !file.name.endsWith(".ppt") &&
        !file.name.endsWith(".pptx")
      ) {
        showToast(`不支持的文件类型: ${file.name}`, "error");
        continue;
      }
      formData.append("files", file);
      validFiles++;
    }

    if (validFiles === 0) {
      showToast("没有有效的文件可上传", "error");
      return;
    }

    formData.append("user_id", userId.value);
    formData.append("conversation_id", activeConversationId.value);
    // 添加功能标识
    formData.append("function_type", "math");

    console.log("开始上传文件...");
    console.log("用户ID:", userId.value);
    console.log("对话ID:", activeConversationId.value);
    console.log("有效文件数:", validFiles);

    // 确保使用数学题API的端口
    const response = await fetch("/api/exercise/upload", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || "上传失败");
    }

    const result = await response.json();
    console.log("上传结果:", result);

    if (result.status === "success") {
      showToast(`${result.message}`, "success");
      have_file.value = true;
      messages.value.push({
        role: "assistant",
        content: `<div class="file-upload-message">
          <p>📁 已上传 ${validFiles} 个文件</p>
          <ul>
            ${Array.from(files)
              .filter(
                (file) =>
                  allowedTypes.includes(file.type) ||
                  file.name.endsWith(".md") ||
                  file.name.endsWith(".txt")
              )
              .map(
                (file) => `<li>${file.name} (${formatFileSize(file.size)})</li>`
              )
              .join("")}
          </ul>
        </div>`,
        timestamp: new Date(),
      });
      // 保存对话历史
      const conv = conversations.value.find(
        (c) => c.id === activeConversationId.value
      );
      if (conv) {
        conv.messages = [...messages.value];
        saveToLocalStorage();
      }

      scrollToBottom();
    } else {
      throw new Error(result.message || "上传失败");
    }
  } catch (error) {
    console.error("文件上传失败:", error);
    showToast(`上传失败: ${error.message}`, "error");
  } finally {
    // 清空文件输入，允许重新选择相同文件
    event.target.value = "";
    uploadStatus.value = "上传成功";
    setTimeout(() => {
      uploadStatus.value = ""; // 3秒后清除状态
    }, 3000);
  }
};

// 添加文件大小格式化函数
const formatFileSize = (bytes) => {
  if (bytes < 1024) return bytes + " B";
  else if (bytes < 1048576) return (bytes / 1024).toFixed(1) + " KB";
  else return (bytes / 1048576).toFixed(1) + " MB";
};

const startEditing = (index) => {
  isEditing.value = true;
  editingIndex.value = index;
  editingContent.value = messages.value[index].content;
};

const saveEditing = () => {
  if (editingIndex.value >= 0) {
    // 获取编辑器的内容
    const editorContent = vditorInstance
      ? vditorInstance.getValue()
      : editingContent.value;
    // 保存到消息中
    messages.value[editingIndex.value].content = editorContent;
  }
  cancelEditing();
};
const toggleReasoning = (index) => {
  messages.value[index].showReasoning = !messages.value[index].showReasoning;
};
// 修改折叠函数为侧边栏的显示/隐藏切换
const toggleSidebar = () => {
  isHidden.value = !isHidden.value;
  // 当显示侧边栏时自动展开，隐藏时自动折叠
  isCollapsed.value = isHidden.value;
};
const toggleCollapse = () => {
  isCollapsed.value = !isCollapsed.value;
};
const cancelEditing = () => {
  isEditing.value = false;
  editingIndex.value = -1;
  editingContent.value = "";
};
const breaktalk = async () => {
  if (abortController.value) {
    abortController.value.abort();
    abortController.value = null; // 重置控制器
  }

  // 立即停止加载状态，使按钮可以响应
  loading.value = false;
  messages.value[messages.value.length - 1].isAnswering = false;
  showToast("对话已打断", "info");

  // 通知后端终止
  try {
    await fetch("/api/exercise/abort", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: userId.value,
        conversation_id: activeConversationId.value,
        function_type: "math", // 添加功能标识
      }),
    });
  } catch (e) {
    console.error("终止请求失败:", e);
  }
};
const sendMessage = async () => {
  userHasScrolled.value = false;
  autoScroll.value = true;
  if (!inputMsg.value.trim() || loading.value) return;
  if (!activeConversationId.value || !conversations.value.length) {
    createNewConversation();
    await nextTick(); // 等待新建对话完成
  }
  scrollToBottom();
  messages.value.push({
    role: "user",
    content: inputMsg.value,
    timestamp: new Date(),
  });
  if (abortController.value) {
    abortController.value.abort(); // 终止之前的请求
  }
  abortController.value = new AbortController();
  try {
    loading.value = true;
    const currentConvId = activeConversationId.value;
    // 创建新的AI消息占位 - 修改这部分，添加新的typing相关字段
    const aiMessage = {
      role: "assistant",
      content: "",
      reasoning: "",
      timestamp: new Date(),
      isAnswering: true, // 标记为正在回答
      showReasoning: true,
      typingContent: "", // 正式回答的打字内容字段
      typingBuffer: "", // 正式回答的打字缓冲区
      typingReasoning: "", // 添加思考过程的打字内容字段
      reasoningTypingBuffer: "", // 添加思考过程的打字缓冲区
      isTypingContent: false, // 标记是否正在为content打字
      isTypingReasoning: false, // 标记是否正在为reasoning打字
      thinkingDots: 0, // 添加思考点计数
      thinkingInterval: null, // 添加思考动画间隔
    };
    messages.value.push(aiMessage);

    // 在aiMessage创建后，添加思考动画
    aiMessage.thinkingInterval = setInterval(() => {
      if (aiMessage.isAnswering) {
        aiMessage.thinkingDots = (aiMessage.thinkingDots + 1) % 4;
      } else {
        clearInterval(aiMessage.thinkingInterval);
      }
    }, 500);

    // 确保包含完整历史记录
    const currentConv = conversations.value.find(
      (c) => c.id === activeConversationId.value
    );
    const history = currentConv
      ? currentConv.messages.map((msg) => ({
          role: msg.role,
          content: msg.content,
        }))
      : [];

    // 如果没有系统消息，添加一个
    if (!history.some((msg) => msg.role === "system")) {
      history.unshift({
        role: "system",
        content:
          "请扮演一个ai出题助手,你必须按照用户要求的格式出题,或者严格按照用户上传的文件" +
          "的格式出相应数量和格式的题目,你必须不能省略任何回答内容,尤其是不能省略题目的数量" +
          "否则就会有人因为你省略题目数量和不遵照格式的行为造成过度劳累而去世" +
          "再次强调，你绝对不能省略任何回答内容,尤其是不能省略题目的数量，在题目生成完之后给出答案",
      });
    }

    const response = await fetch("/api/exercise/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        conversation_id: activeConversationId.value,
        message: inputMsg.value,
        user_id: userId.value,
        function_type: "jiaoan",
        history: history, // 添加完整历史
        signal: abortController.value.signal,
      }),
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let a = true;
    let buffer = "";
    let contentBuffer = "";
    let reasoningBuffer = "";
    let updateTimer = null;

    // 修改updateMessage函数，实现逐字生成效果
    const updateMessage = () => {
      const currentMsg = messages.value[messages.value.length - 1];

      if (reasoningBuffer) {
        // 对于思考过程，使用逐字显示效果
        if (!currentMsg.typingReasoning) {
          currentMsg.typingReasoning = "";
        }

        // 将新内容添加到思考过程的打字缓冲区
        currentMsg.reasoningTypingBuffer =
          (currentMsg.reasoningTypingBuffer || "") + reasoningBuffer;
        reasoningBuffer = "";

        // 如果没有正在进行的思考过程打字动画，启动一个
        if (!currentMsg.isTypingReasoning) {
          typeReasoningChar(currentMsg);
        }
      }

      if (contentBuffer) {
        // 对于正式回答，使用逐字显示效果
        if (!currentMsg.typingContent) {
          currentMsg.typingContent = "";
        }

        // 将新内容添加到正式回答打字缓冲区
        currentMsg.typingBuffer =
          (currentMsg.typingBuffer || "") + contentBuffer;
        contentBuffer = "";

        if (currentMsg.isAnswering) {
          currentMsg.isAnswering = false;
        }

        // 如果没有正在进行的正式回答打字动画，启动一个
        if (!currentMsg.isTypingContent) {
          typeContentChar(currentMsg);
        }
      }

      // 使用防抖处理滚动
      scrollToBottom();
    };

    while (a) {
      const { done, value } = await reader.read();
      if (done) break;
      // 关键检查：如果会话已切换则中止处理
      if (activeConversationId.value !== currentConvId) {
        console.log("检测到对话切换，中止处理");
        reader.cancel();
        break;
      }

      buffer += decoder.decode(value, { stream: true });

      let eventEndIndex;
      while ((eventEndIndex = buffer.indexOf("\n\n")) >= 0) {
        const eventData = buffer.slice(0, eventEndIndex);
        buffer = buffer.slice(eventEndIndex + 2);

        const lines = eventData.split("\n");
        let dataStr = "";
        for (const line of lines) {
          if (line.startsWith("data: ")) {
            dataStr += line.slice(6);
          }
        }

        if (dataStr) {
          try {
            const data = JSON.parse(dataStr);

            if (data.error) {
              throw new Error(data.error);
            }

            if (data.reasoning_content) {
              reasoningBuffer += data.reasoning_content;
            }

            if (data.content) {
              contentBuffer += data.content;
            }

            // 使用防抖更新UI，减少渲染次数
            clearTimeout(updateTimer);
            updateTimer = setTimeout(updateMessage, 100);
          } catch (e) {
            console.error("解析错误:", e);
          }
        }
      }
    }

    // 确保最后的内容被更新
    if (reasoningBuffer || contentBuffer) {
      updateMessage();
    }
  } catch (error) {
    if (error.name === "AbortError") {
      showToast("对话已终止", "info");
    }
    console.error("请求失败:", error);
    messages.value[messages.value.length - 1].content =
      "请求失败: " + error.message;
  } finally {
    loading.value = false;
    inputMsg.value = "";

    // 清除所有消息的思考动画
    messages.value.forEach((msg) => {
      if (msg.thinkingInterval) {
        clearInterval(msg.thinkingInterval);
        msg.thinkingInterval = null;
      }
    });

    await scrollToBottom();
  }
};
watch(activeConversationId, (newVal) => {
  const conv = conversations.value.find((c) => c.id === newVal);
  messages.value = conv?.messages || [];
});

const formatTime = (date) => {
  // 处理可能的null/undefined
  if (!date) return "--:--";

  // 统一转换为Date对象
  const safeDate = date instanceof Date ? date : new Date(date);

  // 有效性验证
  if (isNaN(safeDate.getTime())) {
    console.error("无效的时间值:", date);
    return "时间错误";
  }

  return safeDate.toLocaleTimeString("zh-CN", {
    hour: "2-digit",
    minute: "2-digit",
  });
};

// 添加恢复自动滚动的方法
const resumeAutoScroll = () => {
  autoScroll.value = true;
  userHasScrolled.value = false;
  scrollToBottom();
};

// 添加虚拟滚动优化
const visibleMessages = ref([]);
const messageObserver = ref(null);

// 监听消息变化，为新消息添加观察
watch(
  messages,
  () => {
    nextTick(() => {
      // 为新添加的消息元素添加观察
      const messageElements = document.querySelectorAll(
        ".message:not(.observed)"
      );
      messageElements.forEach((el) => {
        el.classList.add("observed");
        if (messageObserver.value) {
          messageObserver.value.observe(el);
        }
      });
    });
  },
  { deep: true }
);

// 添加思考过程的逐字打字效果函数
const typeReasoningChar = (message) => {
  if (
    !message.reasoningTypingBuffer ||
    message.reasoningTypingBuffer.length === 0
  ) {
    message.isTypingReasoning = false;
    return;
  }

  message.isTypingReasoning = true;

  // 从缓冲区取出第一个字符
  const nextChar = message.reasoningTypingBuffer.charAt(0);
  message.typingReasoning += nextChar;
  message.reasoning = message.typingReasoning;
  message.reasoningTypingBuffer = message.reasoningTypingBuffer.substring(1);

  // 根据字符类型调整延迟时间
  let delay = 8; // 基础延迟时间，可以比content稍快一些

  // 标点符号后面稍微停顿长一点
  if ([".", "!", "?", "。", "！", "？", "\n"].includes(nextChar)) {
    delay = 40;
  }

  // 递归调用，实现连续打字效果
  setTimeout(() => typeReasoningChar(message), delay);

  // 每添加一个字符就滚动到底部
  scrollToBottom();
};

// 修改为专门处理正式回答的打字效果函数
const typeContentChar = (message) => {
  if (!message.typingBuffer || message.typingBuffer.length === 0) {
    message.isTypingContent = false;
    return;
  }

  message.isTypingContent = true;

  // 从缓冲区取出第一个字符
  const nextChar = message.typingBuffer.charAt(0);
  message.typingContent += nextChar;
  message.content = message.typingContent;
  message.typingBuffer = message.typingBuffer.substring(1);

  // 根据字符类型调整延迟时间
  let delay = 10; // 基础延迟时间

  // 标点符号后面稍微停顿长一点
  if ([".", "!", "?", "。", "！", "？", "\n"].includes(nextChar)) {
    delay = 50;
  }

  // 递归调用，实现连续打字效果
  setTimeout(() => typeContentChar(message), delay);

  // 每添加一个字符就滚动到底部
  scrollToBottom();
};

// 替换原来的typeNextChar函数
// const typeNextChar = (message) => {
//   // ... 原有代码 ...
// };
</script>

<style scoped>
/* 基础风格 - 夜间模式 */
.app-container {
  display: flex;
  height: 100%;
  background: #2d2339; /* 更改为深紫色背景 */
  color: #e6ecf5;
  font-family: "SF Pro Display", -apple-system, BlinkMacSystemFont, "Segoe UI",
    Roboto, sans-serif;
  position: relative;
  overflow: hidden;
  transition: background-color 0.3s, color 0.3s;
}

/* 日间模式 */
.app-container.light-mode {
  background: #fff9f0; /* 更改为温暖米色背景 */
  color: #593618; /* 深棕色文字 */
}

/* 确保顶层容器占满父元素空间 */
:deep(.el-card__body) {
  height: 100%;
  padding: 0 !important;
  background: #2d2339; /* 更改为深紫色背景 */
  transition: background-color 0.3s;
  border: 1px solid #53416e; /* 添加紫色边框 */
}

.light-mode :deep(.el-card__body) {
  background: #fff9f0; /* 更改为温暖米色背景 */
  border: 1px solid #f4a259; /* 更改为橙金色边框 */
}

/* 提示信息样式 */
.toast {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  padding: 12px 24px;
  border-radius: 12px;
  z-index: 9999;
  font-size: 14px;
  font-weight: 500;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
  animation: toastSlideDown 0.5s cubic-bezier(0.22, 1, 0.36, 1) forwards;
  max-width: 90%;
  text-align: center;
  backdrop-filter: blur(8px);
}

.toast.info {
  background: rgba(56, 189, 248, 0.15);
  color: #38bdf8;
  border: 1px solid rgba(56, 189, 248, 0.3);
}

.toast.success {
  background: rgba(34, 197, 94, 0.15);
  color: #22c55e;
  border: 1px solid rgba(34, 197, 94, 0.3);
}

.toast.error {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

/* 侧边栏样式 - 夜间模式 */
.sidebar {
  width: 280px;
  background: #352941; /* 更改为更深的紫色 */
  border-right: 1px solid #53416e;
  display: flex;
  flex-direction: column;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  z-index: 10;
  height: 100%; /* 确保侧边栏充满高度 */
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.2);
}

/* 加强侧边栏隐藏状态 */
.sidebar.hidden {
  width: 0 !important;
  min-width: 0 !important;
  overflow: hidden !important;
  border-right: none !important;
  margin-left: -1px !important; /* 解决边框可能出现的问题 */
  opacity: 0;
  visibility: hidden;
  transform: translateX(-20px);
}

/* 侧边栏样式 - 日间模式 */
.light-mode .sidebar {
  background:  rgba(255, 255, 255, 0.9); /* 更改为更深的橙色，而不是原来的金黄色 */
  border-right: 1px solid rgba(216, 101, 0, 0.3);
}

.sidebar-header {
  height: 70px; /* 与聊天头部高度一致 */
  padding: 0 16px; /* 调整内边距 */
  display: flex;
  align-items: center; /* 确保垂直居中 */
  justify-content: space-between;
  position: relative; /* 为装饰条添加定位上下文 */
  background: #3d2d4e; /* 更改为深紫色 */
  border-bottom: 1px solid #53416e;
}

.light-mode .sidebar-header {
  background: linear-gradient(135deg, #f4a259, #f7cb87); /* 橙金色渐变 */
  border-bottom: 1px solid rgba(216, 101, 0, 0.2);
}

.sidebar-header h2 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: #ff9e5e; /* 更改为橙色 */
  text-shadow: 0 0 5px rgba(255, 158, 94, 0.3);
}

.light-mode .sidebar-header h2 {
  color: #b35c00; /* 更改为深橙色 */
  text-shadow: none;
}

.sidebar.collapsed {
  width: 60px;
}

.sidebar.collapsed .sidebar-header h2 {
  display: none;
}

/* 新对话按钮 */
.new-chat-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 40px;
  padding: 0 12px;
  background: linear-gradient(135deg, #7dd3fc, #0ea5e9);
  color: #0f172a;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.22, 1, 0.36, 1);
  font-weight: 600;
  box-shadow: 0 0 15px rgba(125, 211, 252, 0.4);
  overflow: hidden;
}

.light-mode .new-chat-btn {
  background: #f4a259;
  color: #ffffff;
  border: none;
  box-shadow: 0 4px 12px rgba(14, 165, 233, 0.3);
}

.sidebar.collapsed .new-chat-btn {
  width: 40px;
  height: 40px;
  padding: 0;
  border-radius: 50%;
}

.light-mode .sidebar.collapsed .new-chat-btn {
  background: linear-gradient(135deg, #0ea5e9, #0284c7);
  color: #ffffff;
}

.new-chat-btn:hover {
  transform: translateY(-2px) scale(1.05);
  box-shadow: 0 0 20px rgba(125, 211, 252, 0.6);
}

.light-mode .new-chat-btn:hover {
  box-shadow: 0 6px 16px rgba(14, 165, 233, 0.4);
}

.btn-icon {
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.new-chat-btn:hover .btn-icon {
  transform: rotate(90deg);
}

/* 折叠按钮 */
.collapse-btn {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  width: 80%;
  height: 36px;
  background: rgba(125, 211, 252, 0.1);
  color: #7dd3fc;
  border: 1px solid rgba(125, 211, 252, 0.3);
  border-radius: 18px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s cubic-bezier(0.22, 1, 0.36, 1);
  font-size: 14px;
}

.light-mode .collapse-btn {
  background: rgba(14, 165, 233, 0.1);
  color: #0ea5e9;
  border: 1px solid rgba(14, 165, 233, 0.3);
}

.sidebar.collapsed .collapse-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.light-mode .sidebar.collapsed .collapse-btn {
  background: rgba(14, 165, 233, 0.1);
  color: #0ea5e9;
}

.collapse-btn:hover {
  background: rgba(125, 211, 252, 0.2);
  transform: translateX(-50%) scale(1.05);
}

.light-mode .collapse-btn:hover {
  background: rgba(14, 165, 233, 0.2);
}

/* 对话列表 */
.conversation-list {
  flex: 1;
  overflow-y: auto;
  padding: 10px 0;
}

.conversation-item {
  display: flex;
  align-items: center;
  padding: 14px 16px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.22, 1, 0.36, 1);
  border-radius: 10px;
  margin: 6px 8px;
  border-left: 3px solid transparent;
  position: relative;
  overflow: hidden;
}

.conversation-item::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(125, 211, 252, 0.05),
    transparent
  );
  transform: translateX(-100%);
  transition: transform 0.6s ease;
}

.conversation-item:hover::before {
  transform: translateX(100%);
}

.light-mode .conversation-item {
  background:#e78d2b; /* 提高透明度，使背景更亮 */
  border: 1px solid rgba(244, 162, 89, 0.15); /* 降低边框透明度 */
}

.light-mode .conversation-item::before {
  background: linear-gradient(
    90deg,
    transparent,
    rgba(14, 165, 233, 0.05),
    transparent
  );
}

.conversation-item:hover {
  background: rgba(125, 211, 252, 0.08);
  transform: translateX(4px);
}

.light-mode .conversation-item:hover {
  background: rgba(255, 255, 255, 0.95);
  transform: translateX(4px);
  border-color: rgba(244, 162, 89, 0.3);
}

.conversation-item.active {
  background: rgba(125, 211, 252, 0.12);
  border-left: 3px solid #7dd3fc;
}

.light-mode .conversation-item.active {
  background: rgba(255, 255, 255, 1); /* 完全不透明白色 */
  border-left: 3px solid #d86500; /* 深橙色边框 */
  box-shadow: 0 2px 8px rgba(244, 162, 89, 0.2); /* 添加轻微阴影 */
}

.conv-info {
  flex: 1;
  overflow: hidden;
}

.conv-title {
  font-weight: 500;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: #e2e8f0;
  transition: color 0.3s;
}

.light-mode .conv-title {
  color: #1e293b;
}

.conv-time {
  font-size: 0.8em;
  color: #94a3b8;
  transition: color 0.3s;
}

.light-mode .conv-time {
  color: #64748b;
}

.delete-btn {
  background: none;
  border: none;
  color: #94a3b8;
  font-size: 1.2em;
  padding: 0;
  opacity: 0;
  transition: all 0.3s cubic-bezier(0.22, 1, 0.36, 1);
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.light-mode .delete-btn {
  color: #64748b;
}

.conversation-item:hover .delete-btn {
  opacity: 1;
}

.delete-btn:hover {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
  transform: rotate(90deg);
}

.light-mode .delete-btn:hover {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
}

.delete-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

/* 主内容区域 */
.main-content {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: row; /* 修改为水平布局 */
  height: 100%; /* 确保主内容区域占满高度 */
  padding: 0;
  position: relative; /* 添加相对定位 */
}

/* 聊天容器区域 */
.chat-container {
  display: flex;
  flex: 1;
  height: 100%;
  background: #2d2339; /* 更改为深紫色背景 */
  transition: all 0.3s;
  position: relative;
}

/* 侧边栏展开时聊天容器样式 */
.chat-container.sidebar-expanded {
  flex: 1;
  /* 添加侧边栏展开时的过渡效果 */
  transition: all 0.4s cubic-bezier(0.22, 1, 0.36, 1);
}

/* 对话面板 */
.conversation-pane {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #3d2d4e; /* 更改为深紫色 */
  position: relative;
  border-radius: 16px;
  overflow: hidden;
  max-height: 100%; /* 确保不超出容器 */
  transition: all 0.4s cubic-bezier(0.22, 1, 0.36, 1); /* 添加过渡效果 */
  box-shadow: 0 0 30px rgba(0, 0, 0, 0.2);
}

/* 修改聊天容器在日间模式下的样式 */
.light-mode .conversation-pane {
  background-color: #ffffff;
  color: #593618; /* 深棕色文字 */
}

/* 修改聊天窗口在日间模式下的样式 */
.light-mode .chat-window {
  background-color: #fff9f0; /* 更改为温暖米色背景 */
}

/* 修改聊天头部在日间模式下的样式 */
.light-mode .chat-header {
  background: linear-gradient(135deg, #ffffff, #f7cb87); /* 更改为与侧边栏匹配的渐变 */
  border-bottom: 1px solid rgba(216, 101, 0, 0.1);
}

/* 编辑模式 */
.chat-container.editing-mode {
  flex-direction: row;
}

.chat-container.editing-mode .conversation-pane {
  flex: 1.1;
  margin-right: 0;
  border-radius: 16px 0 0 16px;
  transform: translateX(-10px);
  transition: transform 0.5s cubic-bezier(0.22, 1, 0.36, 1);
}

.chat-container.editing-mode .editor-pane {
  flex: 0.9;
  background: #1e293b;
  border-radius: 0 16px 16px 0;
  box-shadow: 0 0 30px rgba(0, 0, 0, 0.3);
  border-left: 1px solid #334155;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transform: translateX(10px);
  animation: slideInEditor 0.5s cubic-bezier(0.22, 1, 0.36, 1) forwards;
}

/* 日间模式下的编辑面板 */
.light-mode .chat-container.editing-mode .editor-pane {
  background: #ffffff;
  border-left: 2px solid rgba(244, 162, 89, 0.3); /* 增加边框宽度并调整颜色 */
}

@keyframes slideInEditor {
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* 聊天头部 */
.chat-header {
  height: 70px;
  padding: 0 24px 0 70px;
  background: #3d2d4e; /* 更改为深紫色 */
  color: #e6ecf5;
  display: flex;
  position: relative;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #53416e;
  overflow: hidden;
}

.header-decoration {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: linear-gradient(90deg, #7dd3fc, #0ea5e9, #0284c7);
  opacity: 0.8;
  animation: gradientShift 8s linear infinite;
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

/* 添加侧边栏折叠/展开按钮样式 */
.toggle-sidebar-btn {
  position: absolute;
  left: 20px;
  top: 50%;
  transform: translateY(-50%);
  width: 36px;
  height: 36px;
  background: rgba(255, 158, 94, 0.1); /* 更改为半透明橙色 */
  color: #ff9e5e; /* 更改为橙色 */
  border: 1px solid rgba(255, 158, 94, 0.3);
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  font-size: 18px;
  z-index: 5;
}

.light-mode .toggle-sidebar-btn {
  background: rgba(216, 101, 0, 0.1); /* 半透明深橙色 */
  color: #b35c00;
  border: 1px solid rgba(216, 101, 0, 0.2);
}

.chat-header h1 {
  font-size: 1.8rem;
  font-weight: 800;
  margin: 0;
  background: linear-gradient(90deg, #ff9e5e, #f4a259); /* 更改为橙金色渐变 */
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  position: relative;
  animation: titlePulse 3s ease-in-out infinite;
}

@keyframes titlePulse {
  0%,
  100% {
    opacity: 1;
    filter: brightness(1);
  }
  50% {
    opacity: 0.9;
    filter: brightness(1.2);
  }
}

.chat-header h1::after {
  content: "";
  position: absolute;
  bottom: -3px;
  left: 0;
  width: 100%;
  height: 1px;
  background: linear-gradient(90deg, transparent, #7dd3fc, transparent);
}
.chat-header {
  border-radius: 0;
}
/* 字符动画 */
.char-animation {
  display: inline-block;
  opacity: 0;
  transform: translateY(10px);
  animation: charFadeIn 0.5s forwards;
}

@keyframes charFadeIn {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 品牌信息 */
.branding {
  position: absolute;
  right: 24px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.ai-logo {
  background: linear-gradient(135deg, #ff9e5e, #f4a259); /* 更改为橙金色渐变 */
  color: #2d2339; /* 紫色文字 */
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  box-shadow: 0 0 15px rgba(255, 158, 94, 0.4); /* 橙色阴影 */
  animation: pulseLogo 3s infinite alternate;
}

@keyframes pulseLogo {
  0% {
    transform: scale(1);
    box-shadow: 0 0 15px rgba(125, 211, 252, 0.4);
  }
  100% {
    transform: scale(1.1);
    box-shadow: 0 0 20px rgba(125, 211, 252, 0.6);
  }
}

.powered-by {
  font-size: 0.8rem;
  color: #94a3b8;
}

/* 聊天窗口 */
.chat-window {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  background: #2d2339; /* 更改为深紫色背景 */
  scroll-behavior: smooth;
  background-image: radial-gradient(
      circle at 10% 20%,
      rgba(125, 211, 252, 0.03) 0%,
      transparent 20%
    ),
    radial-gradient(
      circle at 90% 80%,
      rgba(125, 211, 252, 0.03) 0%,
      transparent 20%
    ),
    radial-gradient(
      circle at 50% 50%,
      rgba(125, 211, 252, 0.02) 0%,
      transparent 50%
    );
  min-height: 0; /* 允许flex收缩 */
}

/* 消息样式 */
.message {
  margin-bottom: 30px;
  animation: messageFadeIn 0.5s cubic-bezier(0.22, 1, 0.36, 1);
}

@keyframes messageFadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message-content {
  display: flex;
  gap: 16px;
  max-width: 90%;
}

.message.assistant .message-content {
  flex-direction: row;
}

.message.user .message-content {
  flex-direction: row-reverse;
  margin-left: auto;
}

/* 头像 */
.avatar {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  overflow: hidden;
  flex-shrink: 0;
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.message:hover .avatar {
  transform: scale(1.05);
}

.avatar.assistant {
  border: 1px solid rgba(255, 158, 94, 0.4); /* 更改为半透明橙色 */
  box-shadow: 0 0 10px rgba(255, 158, 94, 0.2); /* 橙色阴影 */
}

.avatar.user {
  border: 1px solid rgba(244, 162, 89, 0.4); /* 更改为半透明金黄色 */
  box-shadow: 0 0 10px rgba(244, 162, 89, 0.2); /* 金黄色阴影 */
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 消息气泡 */
.bubble {
  border-radius: 16px;
  padding: 16px;
  position: relative;
  max-width: 100%;
  transition: all 0.3s cubic-bezier(0.22, 1, 0.36, 1);
  backdrop-filter: blur(10px);
}

.assistant .bubble {
  background: rgba(15, 23, 42, 0.8);
  border: 1px solid rgba(125, 211, 252, 0.2);
  min-width: 50%;
}

.user .bubble {
  background: rgba(79, 70, 229, 0.15);
  color: #e2e8f0;
  border: 1px solid rgba(168, 85, 247, 0.3);
}

/* 修改消息气泡在日间模式下的样式 */
.light-mode .message .bubble {
  background-color: #fff5e6; /* 更新为淡橙色背景 */
  border: 2px solid rgba(216, 101, 0, 0.2); /* 增加边框宽度并调整颜色 */
  color: #593618; /* 深棕色文字 */
  box-shadow: 0 2px 8px rgba(244, 162, 89, 0.1); /* 添加阴影增强立体感 */
}

.light-mode .message.assistant .bubble {
  background-color: rgba(244, 162, 89, 0.15); /* 更新为半透明金黄色背景 */
  border: 2px solid rgba(244, 162, 89, 0.4); /* 增加边框宽度并调整颜色 */
}

.light-mode .message.user .bubble {
  background-color: #fff9f0; /* 更新为温暖米色背景 */
  border: 2px solid rgba(216, 101, 0, 0.3); /* 增加边框宽度并调整颜色 */
}

/* 思考过程容器样式 */
.thinking-process {
  margin-bottom: 15px;
  border-radius: 12px;
  overflow: hidden;
  background-color: #0f172a;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s cubic-bezier(0.22, 1, 0.36, 1);
}

/* 思考过程标题样式 */
.thinking-header {
  padding: 12px 16px;
  background: rgba(125, 211, 252, 0.08);
  color: rgba(255, 255, 255, 0.9);
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  transition: background 0.3s;
}

.thinking-header:hover {
  background: rgba(125, 211, 252, 0.12);
}

.thinking-icon {
  margin-right: 8px;
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.thinking-header:hover .thinking-icon {
  transform: rotate(20deg);
}

.toggle-icon {
  margin-left: auto;
  transition: transform 0.3s cubic-bezier(0.22, 1, 0.36, 1);
}

/* 思考过程内容样式 */
.reasoning-content {
  padding: 16px;
  color: rgba(255, 255, 255, 0.8);
  background-color: #0f172a;
  font-size: 14px;
  line-height: 1.6;
  animation: contentExpand 0.4s cubic-bezier(0.22, 1, 0.36, 1);
}

@keyframes contentExpand {
  from {
    opacity: 0;
    max-height: 0;
  }
  to {
    opacity: 1;
    max-height: 1000px;
  }
}

/* 正式回答容器样式 */
.correct-answer {
  background-color: #0f172a;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.1);
  margin-top: 10px; /* 增加与思考过程的间距 */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); /* 增加阴影效果 */
  transition: all 0.3s cubic-bezier(0.22, 1, 0.36, 1);
  animation: answerFadeIn 0.6s cubic-bezier(0.22, 1, 0.36, 1);
}

@keyframes answerFadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.correct-answer:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

/* 正式回答标题样式 */
.correct-answer-label {
  padding: 12px 16px;
  background: linear-gradient(135deg, #0f172a, #0284c7);
  color: white;
  font-weight: 500;
  display: flex;
  align-items: center;
  position: relative;
  overflow: hidden;
}

.answering-indicator {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  background: rgba(30, 41, 59, 0.5);
  border-radius: 8px;
  margin-top: 8px;
  font-style: italic;
  color: #94a3b8;
  transition: all 0.3s ease;
}

.light-mode .answering-indicator {
  background: rgba(241, 245, 249, 0.7);
  color: #64748b;
}

.dot-flashing-small {
  position: relative;
  width: 6px;
  height: 6px;
  border-radius: 3px;
  background-color: #7dd3fc;
  animation: dotFlashing 1s infinite linear alternate;
  animation-delay: 0.5s;
}

.dot-flashing-small::before,
.dot-flashing-small::after {
  content: "";
  display: inline-block;
  position: absolute;
  top: 0;
}

.dot-flashing-small::before {
  left: -10px;
  width: 6px;
  height: 6px;
  border-radius: 3px;
  background-color: #7dd3fc;
  animation: dotFlashing 1s infinite alternate;
  animation-delay: 0s;
}

.dot-flashing-small::after {
  left: 10px;
  width: 6px;
  height: 6px;
  border-radius: 3px;
  background-color: #7dd3fc;
  animation: dotFlashing 1s infinite alternate;
  animation-delay: 1s;
}
.correct-answer-label::after {
  content: "";
  position: absolute;
  top: 0;
  right: 0;
  width: 30%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(125, 211, 252, 0.2));
  animation: shimmer 2s infinite;
}

@keyframes shimmer {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(200%);
  }
}

.correct-answer-icon {
  margin-right: 8px;
  animation: iconFloat 3s ease-in-out infinite;
}

@keyframes iconFloat {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-3px);
  }
}

/* 正式回答内容样式 */
.correct-answer-content {
  padding: 16px;
  color: rgba(255, 255, 255, 0.9);
  font-size: 14px;
  line-height: 1.6;
}

/* 修复无序列表和有序列表的样式 */
.correct-answer-content ul,
.correct-answer-content ol {
  padding-left: 2em !important;
  margin-left: 0 !important;
  list-style-position: outside !important;
}

/* 修复列表项的样式 */
.correct-answer-content li {
  display: list-item !important;
  margin-bottom: 0.5em !important;
  padding-left: 0.5em !important;
}

/* 确保无序列表的圆点正确显示 */
.correct-answer-content ul {
  list-style-type: disc !important;
}

.correct-answer-content ul ul {
  list-style-type: circle !important;
}

.correct-answer-content ul ul ul {
  list-style-type: square !important;
}

/* 确保有序列表的数字正确显示 */
.correct-answer-content ol {
  list-style-type: decimal !important;
}

.correct-answer-content ol ol {
  list-style-type: lower-alpha !important;
}

.correct-answer-content ol ol ol {
  list-style-type: lower-roman !important;
}

/* 修复嵌套列表的缩进 */
.correct-answer-content ul ul,
.correct-answer-content ol ol,
.correct-answer-content ul ol,
.correct-answer-content ol ul {
  margin-top: 0.5em !important;
  margin-bottom: 0 !important;
}

/* 日间模式样式 */
.light-mode .thinking-process {
  background-color: #fff5e6; /* 更改为淡橙色背景 */
  border: 2px solid rgba(216, 101, 0, 0.15); /* 增加边框宽度并调整颜色 */
  box-shadow: 0 2px 6px rgba(14, 165, 233, 0.08); /* 轻微阴影效果 */
}

.light-mode .thinking-header {
  background: rgba(14, 165, 233, 0.08);
  color: #0f172a;
  border-bottom: 1px solid #e2e8f0;
}

.light-mode .reasoning-content {
  background-color: #fff5e6;
  color: #1e293b;
}

.light-mode .correct-answer {
  background-color: #ffffff;
  border: 2px solid rgba(244, 162, 89, 0.3); /* 增加边框宽度并调整颜色 */
  box-shadow: 0 4px 12px rgba(244, 162, 89, 0.12); /* 增强阴影效果 */
}

/* 清新的渐变色彩 */
.light-mode .correct-answer-label {
  background: linear-gradient(135deg, #f4a259, #f7cb87); /* 更改为橙金色渐变 */
  color: white;
}

.light-mode .correct-answer-content {
  color: #1e293b;
}

/* 消息操作 */
.message-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 12px;
}

.edit-button,
.break-button {
  background: rgba(61, 45, 78, 0.8); /* 更改为深紫色半透明 */
  color: #a0b0d0;
  border: 1px solid rgba(255, 158, 94, 0.15); /* 更改为半透明橙色边框 */
  border-radius: 10px;
  padding: 8px 14px;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.22, 1, 0.36, 1);
  display: flex;
  align-items: center;
  gap: 6px;
}

.light-mode .edit-button,
.light-mode .break-button {
  background: rgba(255, 255, 255, 0.8);
  color: #64748b;
  border: 1px solid rgba(14, 165, 233, 0.2);
}

.edit-button:hover {
  background: rgba(125, 211, 252, 0.15);
  color: #7dd3fc;
  border-color: rgba(125, 211, 252, 0.3);
  transform: translateY(-2px);
}

.break-button:hover {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
  border-color: rgba(239, 68, 68, 0.3);
  transform: translateY(-2px);
}

.button-icon {
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.edit-button:hover .button-icon {
  transform: rotate(15deg);
}

.break-button:hover .button-icon {
  transform: scale(1.2);
}

.timestamp {
  font-size: 0.8rem;
  color: #94a3b8;
}

/* 输入区域 */
.input-area {
  padding: 16px 24px;
  background: #3d2d4e; /* 更改为深紫色 */
  border-top: 1px solid #53416e;
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 16px;
  align-items: center;
  min-height: 80px; /* 确保最小高度 */
  position: relative; /* 确保定位正确 */
  z-index: 5;
}

.light-mode .input-area {
  background-color: #fff5e6; /* 温暖米色背景 */
  border-top: 1px solid #f7cb87; /* 金黄色边框 */
}

.file-upload {
  position: relative;
}

.upload-button {
  background: rgba(255, 158, 94, 0.1); /* 更改为半透明橙色 */
  color: #ff9e5e; /* 更改为橙色 */
  border: 1px solid rgba(255, 158, 94, 0.2); /* 更改为半透明橙色边框 */
  padding: 10px 16px;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.22, 1, 0.36, 1);
  display: flex;
  align-items: center;
  gap: 8px;
}

.upload-icon {
  font-size: 1.2em;
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.upload-button:hover .upload-icon {
  transform: translateY(-2px);
}

.upload-button:hover {
  background: rgba(255, 158, 94, 0.2); /* 更改为半透明橙色 */
  border-color: rgba(255, 158, 94, 0.4); /* 更改为半透明橙色边框 */
  transform: translateY(-2px);
}

.upload-tip {
  font-size: 0.75em;
  color: #94a3b8;
  position: absolute;
  bottom: -18px;
  left: 12px;
  white-space: nowrap;
  transition: opacity 0.3s;
}

.file-upload:hover .upload-tip {
  opacity: 0.8;
}

.text-inputer input {
  width: 100%;
  padding: 14px 16px;
  border: 1px solid #334155;
  border-radius: 10px;
  outline: none;
  background: rgba(15, 23, 42, 0.6);
  color: #e2e8f0;
  font-size: 1rem;
  transition: all 0.3s cubic-bezier(0.22, 1, 0.36, 1);
}

.text-inputer input:focus {
  border-color: rgba(125, 211, 252, 0.4);
  box-shadow: 0 0 0 3px rgba(125, 211, 252, 0.1);
  transform: translateY(-1px);
}

.text-inputer input::placeholder {
  color: #94a3b8;
}
/* 修复日间模式下的思考中按钮 */
.light-mode .send-button button:disabled {
  background: linear-gradient(135deg, #f4a259, #f7cb87); /* 更新为橙金色渐变 */
  opacity: 0.6; /* 降低不可用状态的透明度 */
  color: #ffffff !important;
}

/* 修改输入框在日间模式下的样式 */
.light-mode .text-inputer input {
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(244, 162, 89, 0.3); /* 更新为金黄色边框 */
  color: #593618; /* 深棕色文字 */
}

.light-mode .text-inputer input:focus {
  border-color: rgba(244, 162, 89, 0.5); /* 更新为半透明金黄色边框 */
  box-shadow: 0 0 0 2px rgba(244, 162, 89, 0.2); /* 更新为半透明金黄色阴影 */
}
.send-button button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: linear-gradient(135deg, #5e3a6e, #ff9e5e); /* 从紫色到橙色的渐变 */
  color: #ffffff;
  border: none;
  padding: 12px 24px;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.22, 1, 0.36, 1);
  font-weight: 600;
  min-width: 100px;
  position: relative;
  overflow: hidden;
}

.send-button button::after {
  content: "";
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(
    circle,
    rgba(255, 255, 255, 0.3) 0%,
    transparent 70%
  );
  opacity: 0;
  transition: opacity 0.3s;
}

.send-button button:hover::after {
  opacity: 1;
}

.send-button button:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 6px 16px rgba(14, 165, 233, 0.4);
}

.send-icon {
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.send-button button:hover .send-icon {
  transform: translateX(3px);
}

/* 加载指示器 */
.loading-indicator {
  display: flex;
  justify-content: center;
  padding: 20px 0;
}

.dot-flashing {
  position: relative;
  width: 10px;
  height: 10px;
  border-radius: 5px;
  background-color: #ff9e5e; /* 更改为橙色 */
  color: #ff9e5e; /* 更改为橙色 */
  animation: dotFlashing 1s infinite linear alternate;
  animation-delay: 0.5s;
}

.dot-flashing::before,
.dot-flashing::after {
  content: "";
  display: inline-block;
  position: absolute;
  top: 0;
  width: 10px;
  height: 10px;
  border-radius: 5px;
  background-color: #ff9e5e; /* 更改为橙色 */
  color: #ff9e5e; /* 更改为橙色 */
}

@keyframes dotFlashing {
  0% {
    background-color: #ff9e5e; /* 更改为橙色 */
  }
  50%,
  100% {
    background-color: rgba(255, 158, 94, 0.2); /* 更改为半透明橙色 */
  }
}

/* 编辑器面板 */
.editor-header {
  padding: 16px 24px;
  background: #3d2d4e; /* 更改为深紫色 */
  border-bottom: 1px solid #53416e;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 70px;
}

.editor-header h1 {
  font-size: 1.2rem;
  font-weight: 600;
  margin: 0;
  background: linear-gradient(90deg, #ff9e5e, #f4a259); /* 更改为橙金色渐变 */
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.editor-actions {
  display: flex;
  gap: 10px;
}

.editor-actions button {
  padding: 8px 16px;
  font-size: 0.9rem;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.22, 1, 0.36, 1);
  font-weight: 500;
}

.save-button {
  background: rgba(125, 211, 252, 0.1);
  color: #7dd3fc;
  border: 1px solid rgba(125, 211, 252, 0.2);
}

.save-button:hover {
  background: rgba(125, 211, 252, 0.2);
  border-color: rgba(125, 211, 252, 0.4);
  transform: translateY(-2px);
}

.cancel-button {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.cancel-button:hover {
  background: rgba(239, 68, 68, 0.2);
  border-color: rgba(239, 68, 68, 0.4);
  transform: translateY(-2px);
}

.export-button {
  background: rgba(34, 197, 94, 0.1);
  color: #22c55e;
  border: 1px solid rgba(34, 197, 94, 0.2);
}

.export-button:hover {
  background: rgba(34, 197, 94, 0.2);
  border-color: rgba(34, 197, 94, 0.4);
  transform: translateY(-2px);
}

/* 优化编辑器样式 */
:deep(.vditor) {
  border: none !important;
  height: calc(100% - 70px) !important;
  background: #2d2339 !important; /* 更改为深紫色背景 */
  transition: background 0.3s !important;
}

:deep(.vditor-toolbar) {
  background: #3d2d4e !important; /* 更改为深紫色 */
  border-bottom: 1px solid #53416e !important;
  transition: background 0.3s, border 0.3s !important;
}

:deep(.vditor-toolbar svg) {
  fill: #a0b0d0 !important;
  transition: fill 0.3s !important;
}

:deep(.vditor-toolbar button:hover svg) {
  fill: #ff9e5e !important; /* 更改为橙色 */
}

:deep(.vditor-reset) {
  color: #e6ecf5 !important;
  background: #2d2339 !important; /* 更改为深紫色背景 */
  transition: color 0.3s, background 0.3s !important;
}

:deep(.vditor-reset pre) {
  background: rgba(61, 45, 78, 0.8) !important; /* 更改为深紫色半透明 */
  border: 1px solid rgba(255, 158, 94, 0.2) !important; /* 更改为半透明橙色边框 */
  border-radius: 10px !important;
}

:deep(.vditor-reset code) {
  color: #ff9e5e !important; /* 更改为橙色 */
  background: rgba(61, 45, 78, 0.6) !important; /* 更改为深紫色半透明 */
  padding: 2px 6px !important;
  border-radius: 4px !important;
  transition: color 0.3s, background 0.3s !important;
}

/* 修复日间模式下的编辑器内容区域 */
.light-mode :deep(.vditor) {
  border: none !important;
  height: calc(100% - 70px) !important;
  background: #fff9f0 !important; /* 更改为温暖米色背景 */
  box-shadow: 0 2px 8px rgba(244, 162, 89, 0.08); /* 添加轻微金黄色阴影 */
}

/* 修复日间模式下的编辑器工具栏 */
.light-mode :deep(.vditor-toolbar) {
  background: #fff5e6 !important; /* 更改为淡橙色背景 */
  border-bottom: 1px solid rgba(244, 162, 89, 0.2) !important; /* 更改为半透明金黄色边框 */
}

.light-mode :deep(.vditor-toolbar svg) {
  fill: #593618 !important; /* 更改为深棕色 */
}

.light-mode :deep(.vditor-toolbar button:hover svg) {
  fill: #d86500 !important; /* 更改为深橙色 */
}

/* 修复日间模式下的编辑器内容区域 */
.light-mode :deep(.vditor-reset) {
  color: #593618 !important; /* 更改为深棕色文字 */
  background: #fff9f0 !important; /* 更改为温暖米色背景 */
}

/* 修复日间模式下的代码块 */
.light-mode :deep(.vditor-reset pre) {
  background: rgba(244, 162, 89, 0.1) !important; /* 更改为半透明金黄色背景 */
  border: 1px solid rgba(216, 101, 0, 0.2) !important; /* 更改为半透明深橙色边框 */
}

/* 修复日间模式下的行内代码 */
.light-mode :deep(.vditor-reset code) {
  color: #d86500 !important; /* 更改为深橙色 */
  background: rgba(244, 162, 89, 0.15) !important; /* 更改为半透明金黄色背景 */
}

/* 对动画生命周期的定义 */
@keyframes toastSlideDown {
  from {
    opacity: 0;
    transform: translate(-50%, -30px);
  }
  to {
    opacity: 1;
    transform: translate(-50%, 0);
  }
}

/* 自定义滚动条 */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: rgba(148, 163, 184, 0.3);
  border-radius: 3px;
  transition: background 0.3s;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(148, 163, 184, 0.5);
}

.control-panel {
  background-color: #1e293b; /* 稍微深一点的蓝色 */
  padding: 30px;
  border-radius: 16px;
  box-shadow: 0 0 30px rgba(0, 0, 0, 0.3);
  transition: background-color 0.3s, box-shadow 0.3s;
}

/* 日间模式 */
.light-mode .control-panel {
  background-color: #ffffff;
  box-shadow: 0 0 30px rgba(0, 0, 0, 0.1);
}

/* 修复日间模式下的整体聊天容器背景 */
.light-mode .chat-container {
  background: #f8fafc;
}

/* 修复日间模式下的聊天窗口背景图案 */
.light-mode .chat-window {
  background-image: radial-gradient(
      circle at 10% 20%,
      rgba(14, 165, 233, 0.03) 0%,
      transparent 20%
    ),
    radial-gradient(
      circle at 90% 80%,
      rgba(14, 165, 233, 0.03) 0%,
      transparent 20%
    ),
    radial-gradient(
      circle at 50% 50%,
      rgba(14, 165, 233, 0.02) 0%,
      transparent 50%
    );
}

/* 修复日间模式下的编辑器面板 */
.light-mode .editor-pane {
  background: #ffffff;
  border-left: 1px solid #e2e8f0;
}

.light-mode .editor-header {
  background: #f1f5f9;
  border-bottom: 1px solid #e2e8f0;
}

/* 修复日间模式下的加载指示器 */
.light-mode .loading-indicator {
  color: #0ea5e9;
}

.light-mode .dot-flashing {
  background-color: #0ea5e9;
}

.light-mode .dot-flashing::before,
.light-mode .dot-flashing::after {
  background-color: #0ea5e9;
}

@keyframes dotFlashingLight {
  0% {
    background-color: #0ea5e9;
  }
  50%,
  100% {
    background-color: rgba(14, 165, 233, 0.2);
  }
}

.light-mode .dot-flashing,
.light-mode .dot-flashing::before,
.light-mode .dot-flashing::after {
  animation-name: dotFlashingLight;
}

/* 修复日间模式下的编辑器内容区域 */
.light-mode :deep(.vditor) {
  border: none !important;
  height: calc(100% - 70px) !important;
  background: #ffffff !important;
  box-shadow: 0 2px 8px rgba(14, 165, 233, 0.08); /* 添加轻微阴影 */
}

/* 修复日间模式下的编辑器按钮 */
.light-mode .editor-actions button {
  background: rgba(14, 165, 233, 0.05);
  color: #0ea5e9;
  border: 1px solid rgba(14, 165, 233, 0.1);
}

.light-mode .editor-actions button:hover {
  background: rgba(14, 165, 233, 0.1);
}

.light-mode .save-button {
  background: rgba(14, 165, 233, 0.1) !important;
  color: #0ea5e9 !important;
  border: 1px solid rgba(14, 165, 233, 0.3) !important;
}

.light-mode .save-button:hover {
  background: rgba(14, 165, 233, 0.2) !important;
}

.light-mode .cancel-button {
  background: rgba(239, 68, 68, 0.1) !important;
  color: #ef4444 !important;
}

.light-mode .export-button {
  background: rgba(34, 197, 94, 0.1) !important;
  color: #22c55e !important;
}

/* 全局覆盖 Mathpix 列表样式 */
:deep(.mp-md-block-list) {
  padding-left: 2em !important;
  margin-left: 0 !important;
}

:deep(.mp-md-block-list-item) {
  display: list-item !important;
  padding-left: 0.5em !important;
}

:deep(ul),
:deep(ol) {
  padding-left: 2em !important;
  margin-left: 0 !important;
}

:deep(li) {
  display: list-item !important;
}

/* 修改对话面板在侧边栏展开时的圆角 */
.chat-container.sidebar-expanded .conversation-pane {
  border-radius: 0 16px 16px 0;
  border-left: none; /* 移除左侧边框 */
}

/* 确保聊天头部在侧边栏展开时左上角没有圆角 */
.chat-container.sidebar-expanded .chat-header {
  border-top-left-radius: 0;
  border-bottom-left-radius: 0;
}

/* 调整侧边栏背景与对话面板头部背景一致 */
.sidebar-header {
  background: #0f172a; /* 与聊天头部背景一致 */
  border-bottom: 1px solid #334155;
}

/* 日间模式下的一致性调整 */
.light-mode .sidebar-header {
  background: linear-gradient(135deg, #ffffff, #f1f5f9);
  border-bottom: 1px solid #e2e8f0;
}

/* 为侧边栏头部添加顶部装饰条，与聊天头部一致 */
.sidebar-header::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: linear-gradient(90deg, #0284c7, #0ea5e9, #7dd3fc);
  opacity: 0.8;
  animation: gradientShift 8s linear infinite;
}

.answering-indicator {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  background: rgba(30, 41, 59, 0.5);
  border-radius: 8px;
  margin-top: 8px;
  font-style: italic;
  color: #94a3b8;
  transition: all 0.3s ease;
}

.light-mode .answering-indicator {
  background: rgba(241, 245, 249, 0.7);
  color: #64748b;
}

/* 添加性能优化相关的CSS */
.message {
  will-change: transform, opacity;
  contain: content;
  transform: translateZ(0);
}

/* 优化长文本渲染 */
.bubble {
  contain: content;
  overflow-wrap: break-word;
  word-break: break-word;
}

/* 优化Markdown内容渲染 */
.markdown-body,
.correct-answer-content,
.reasoning-content {
  contain: content;
}

/* 优化滚动性能 */
.chat-window {
  -webkit-overflow-scrolling: touch;
  overscroll-behavior: contain;
  scroll-behavior: auto; /* 改为auto以提高性能 */
}

/* 添加渐进式加载效果 */
.message:not(.visible) {
  opacity: 0.6;
  transform: translateY(10px);
}

.message.visible {
  opacity: 1;
  transform: translateY(0);
  transition: opacity 0.3s, transform 0.3s;
}

/* 添加打字动画相关样式 */
.typing-cursor {
  display: inline-block;
  width: 2px;
  height: 1em;
  background-color: #7dd3fc;
  margin-left: 2px;
  vertical-align: middle;
  animation: cursor-blink 1s infinite;
}

@keyframes cursor-blink {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0;
  }
}

/* 优化思考中动画 */
.answering-indicator {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  background: rgba(30, 41, 59, 0.5);
  border-radius: 8px;
  margin-top: 8px;
  font-style: italic;
  color: #94a3b8;
  transition: all 0.3s ease;
}

.light-mode .answering-indicator {
  background: rgba(241, 245, 249, 0.7);
  color: #64748b;
}
</style>
