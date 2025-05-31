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
            <h1>智能教案生成</h1>
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
                        <span>AI 正在思考中...</span>
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
              <span class="upload-tip">支持PDF/Word/TXT/MD</span>
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

const compiledMarkdown = (val) => {
  return MM.markdownToHTML(val, {
    htmlTags: true,
    codeHighlight: {
      auto: true,
      code: true,
    },
  });
};
</script>

<script setup>
import { ref, nextTick, watch, onMounted, onBeforeUnmount } from "vue";

import { saveAs } from "file-saver";
import hljs from "highlight.js";
import "highlight.js/styles/github.css";
import Vditor from "vditor";
import "vditor/dist/index.css";
import htmlDocx from "html-docx-js/dist/html-docx";
const compiledMarkdown1 = (val) => {
  const isLoad = MM.loadMathJax();
  if (isLoad) {
    return MM.markdownToHTML(val, {
      htmlTags: true,
      codeHighlight: {
        auto: true,
        code: true,
      },
    });
  }
};
const saveToWord = (content) => {
  const tempDiv = document.createElement("div");
  tempDiv.innerHTML = compiledMarkdown1(content);

  // 增强 SVG 转换兼容性
  tempDiv.querySelectorAll(".MathJax").forEach((mathJaxElem) => {
    const svg = mathJaxElem.querySelector("svg");
    if (svg) {
      if (!svg.getAttribute("xmlns")) {
        svg.setAttribute("xmlns", "http://www.w3.org/2000/svg");
      }
      const svgString = new XMLSerializer().serializeToString(svg);
      const decoded = unescape(encodeURIComponent(svgString));
      const base64 = btoa(decoded);

      const img = document.createElement("img");
      img.src = `data:image/svg+xml;base64,${base64}`;
      img.style.verticalAlign = "middle";
      const fontSize = window.getComputedStyle(mathJaxElem).fontSize;
      img.style.height = fontSize;
      img.style.width = "auto";

      mathJaxElem.replaceWith(img);
    }
  });

  // 增强 Word 兼容样式
  const styledHtml = `
    <html xmlns:w="urn:schemas-microsoft-com:office:word">
      <head>
        <meta charset="UTF-8">
        <style>
          body {
            font-family: "Arial", sans-serif;
            line-height: 1.6;
            margin: 20px;
          }
          h1, h2, h3, h4, h5, h6 {
            text-align: center; /* 标题居中 */
          }
          hr {
            border: 1px solid #ddd;
            margin: 20px 0;
          }
          ol {
            padding-left: 40px;
          }
          img {
            height: 1.2em;
            vertical-align: middle;
          }
          strong {
            color: #2c3e50;
          }
        </style>
      </head>
      <body>${tempDiv.innerHTML}</body>
    </html>
  `;

  const blob = htmlDocx.asBlob(styledHtml);
  saveAs(blob, "教学计划.docx");
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
// 修改初始状态：确保侧边栏默认完全隐藏
const isCollapsed = ref(true);
const isHidden = ref(true);
const vditorContainer = ref(null);
let vditorInstance = null;

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
const fileInput = ref(null);
const triggerFileUpload = () => {
  fileInput.value.click();
};
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
        // 延迟设置内容，确保编辑器完全初始化
        nextTick(() => {
          // 如果内容不为空，则进行格式转换和设置
          if (editingContent.value) {
            const convertedContent = convertMathpixToLatex(
              editingContent.value
            );
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
});

const showToast = (message, type = "info") => {
  toast.value = { show: true, message, type };
  setTimeout(() => {
    toast.value.show = false;
  }, 3000);
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
// 初始化加载
onMounted(() => {
  // 修改本地存储键名，添加功能前缀
  const saved = localStorage.getItem("jiaoan_conversations");
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
    scrollToBottom();
  }
  // 添加滚动事件监听
  if (chatWindow.value) {
    chatWindow.value.addEventListener("scroll", handleScroll);
  }

  // 确保侧边栏初始隐藏
  isHidden.value = true;
  isCollapsed.value = true;
});
// 创建新对话
const createNewConversation = () => {
  // 确保生成Date对象
  const now = new Date();

  const newConv = {
    id: Date.now().toString(),
    title: "新对话",
    timestamp: now, // 直接使用Date对象
    messages: [],
  };

  conversations.value.unshift(newConv);
  activeConversationId.value = newConv.id;
  saveToLocalStorage();
};
const autoScroll = ref(true);
const userHasScrolled = ref(false);
const handleScroll = () => {
  if (!chatWindow.value) return;

  const container = chatWindow.value;
  const isAtBottom =
    container.scrollHeight - container.scrollTop - container.clientHeight < 50;

  // 如果用户向上滚动，标记用户已滚动，暂停自动滚动
  if (!isAtBottom) {
    userHasScrolled.value = true;
    autoScroll.value = false;
  }

  // 如果用户滚动到底部，恢复自动滚动
  if (isAtBottom && userHasScrolled.value) {
    userHasScrolled.value = false;
    autoScroll.value = true;
  }
};
// 切换对话
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
      fetch("api/jiaoan/check-files", {
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

  scrollToBottom();
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
  localStorage.setItem("jiaoan_conversations", JSON.stringify(dataToSave));
};

// 时间格式化
const formatDate = (date) => {
  const actualDate = date instanceof Date ? date : new Date(Number(date));
  return actualDate.toLocaleTimeString("zh-CN", {
    hour: "2-digit",
    minute: "2-digit",
  });
};

// 添加文件大小格式化函数
const formatFileSize = (bytes) => {
  if (bytes < 1024) return bytes + " B";
  else if (bytes < 1048576) return (bytes / 1024).toFixed(1) + " KB";
  else return (bytes / 1048576).toFixed(1) + " MB";
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
      // 检查文件类型
      if (
        !allowedTypes.includes(file.type) &&
        !file.name.endsWith(".md") &&
        !file.name.endsWith(".txt") &&
        !file.name.endsWith(".doc") &&
        !file.name.endsWith(".ppt")
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
    formData.append("function_type", "jiaoan");

    console.log("开始上传文件...");
    console.log("用户ID:", userId.value);
    console.log("对话ID:", activeConversationId.value);
    console.log("有效文件数:", validFiles);

    const response = await fetch("/api/jiaoan/upload", {  // 这里移除了可能存在的/main前缀
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

      // 在对话中显示文件上传消息
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
  }
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

// 保留原来的折叠函数，重命名为toggleCollapse
const toggleCollapse = () => {
  isCollapsed.value = !isCollapsed.value;
};

const startEditing = (index) => {
  isEditing.value = true;
  editingIndex.value = index;
  editingContent.value = messages.value[index].content;
};
const saveEditing = () => {
  if (editingIndex.value >= 0) {
    messages.value[editingIndex.value].content = editingContent.value;
  }
  cancelEditing();
};
const cancelEditing = () => {
  isEditing.value = false;
  editingIndex.value = -1;
  editingContent.value = "";
};
const breaktalk = async () => {
  if (abortController.value) {
    abortController.value.abort();
  }
  showToast("对话已打断", "info");
  // 通知后端终止 - 修复请求路径，移除/main前缀
  try {
    await fetch("/api/jiaoan/abort", {  // 这里移除了/main前缀
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: userId.value,
        conversation_id: activeConversationId.value,
        function_type: "jiaoan", // 添加功能标识
      }),
    });
  } catch (e) {
    console.error("终止请求失败:", e);
  }

  loading.value = false;
};
const sendMessage = async () => {
  if (!inputMsg.value.trim() || loading.value) return;
  if (!activeConversationId.value || !conversations.value.length) {
    createNewConversation();
    await nextTick(); // 等待新建对话完成
  }

  // 仅当用户在底部或未滚动时自动滚动到底部
  if (!userHasScrolled.value) {
    scrollToBottom();
  }

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
    // 创建新的AI消息占位 - 修改这部分
    const aiMessage = {
      role: "assistant",
      content: "",
      reasoning: "",
      timestamp: new Date(),
      isAnswering: true, // 标记为正在回答
      showReasoning: true,
    };
    messages.value.push(aiMessage);

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
          "请扮演一个特别擅长编写教学设计的资深教师" +
          "你编写的教学设计必须包括教学内容,教学活动安排,时间分配,预期成果" +
          "其他内容你可以自行斟酌但是一定要保证至少3个互动环节" +
          "互动环节必须有趣，不能只是简单的回答问题或者复习" +
          "你必须严格遵守以上要求,否则会造成及其严重的后果",
      });
    }

    const response = await fetch("/api/jiaoan/chat", {  // 这里移除了可能存在的/main前缀
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
            const currentMsg = messages.value[messages.value.length - 1];

            if (data.error) {
              throw new Error(data.error);
            }

            if (data.reasoning_content) {
              currentMsg.reasoning += data.reasoning_content;
              currentMsg.isAnswering = false;
            }

            if (data.content) {
              currentMsg.content += data.content;
              if (currentMsg.isAnswering) {
                currentMsg.isAnswering = false; // 收到内容后，不再显示"正在回答"
              }
            }

            // 只有在用户未手动滚动时才滚动到底部
            if (autoScroll.value) {
              await scrollToBottom();
            }
          } catch (e) {
            console.error("解析错误:", e);
          }
        }
      }
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
    // 最终完成后，仅在用户未手动滚动时滚动到底部
    if (autoScroll.value) {
      await scrollToBottom();
    }
  }
};
watch(activeConversationId, (newVal) => {
  const conv = conversations.value.find((c) => c.id === newVal);
  messages.value = conv?.messages || [];
});

const scrollToBottom = () => {
  // 仅在用户未手动滚动或明确请求滚动时执行
  if (!userHasScrolled.value || autoScroll.value) {
    nextTick(() => {
      if (chatWindow.value) {
        const container = chatWindow.value;
        container.scrollTo({
          top: container.scrollHeight,
          behavior: "smooth",
        });
      }
    });
  }
};

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

const isLightMode = ref(localStorage.getItem("theme-mode") === "light");

const checkThemeMode = () => {
  isLightMode.value = localStorage.getItem("theme-mode") === "light";
};

onMounted(() => {
  checkThemeMode();
  window.addEventListener("storage", checkThemeMode);
  window.addEventListener("themeChange", checkThemeMode);
});

onBeforeUnmount(() => {
  if (chatWindow.value) {
    chatWindow.value.removeEventListener("scroll", handleScroll);
  }
  window.removeEventListener("storage", checkThemeMode);
  window.removeEventListener("themeChange", checkThemeMode);
});
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
  border: 1px solid #53416e; /* 添加边框 */
}

.light-mode :deep(.el-card__body) {
  background: #fff9f0; /* 更改为温暖米色背景 */
  border: 1px solid #f4a259; /* 更改为更明显的橙金色边框 */
}

/* 提示信息样式 */
.toast {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  padding: 12px 24px;
  border-radius: 8px;
  z-index: 9999;
  font-size: 14px;
  font-weight: 500;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
  animation: slideDown 0.3s forwards;
  max-width: 90%;
  text-align: center;
}

.toast.info {
  background: #ecf5ff;
  color: #409eff;
  border: 1px solid #d9ecff;
}

.toast.success {
  background: #f0f9eb;
  color: #67c23a;
  border: 1px solid #e1f3d8;
}

.toast.error {
  background: #fef0f0;
  color: #f56c6c;
  border: 1px solid #fde2e2;
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
}

/* 侧边栏样式 - 日间模式 */
.light-mode .sidebar {
  background: rgba(255, 255, 255, 0.9); /* 更改为更深的橙色 */
  border-right: 1px solid rgba(216, 101, 0, 0.3);
}

/* 修改侧边栏头部与聊天头部高度一致 */
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
  padding: 0 5px;
  background: linear-gradient(135deg, #64ffda, #1ec6ff);
  color: #0f1629;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 600;
  box-shadow: 0 0 15px rgba(100, 255, 218, 0.4);
  overflow: hidden;
}

.light-mode .new-chat-btn {
  background:#f4a259;
  color: #1a2980;
  border: 1px solid rgba(30, 50, 100, 0.2);
}

.sidebar.collapsed .new-chat-btn {
  width: 40px;
  height: 40px;
  padding: 0;
  border-radius: 50%;
}

.light-mode .sidebar.collapsed .new-chat-btn {
  background: rgba(30, 50, 100, 0.1);
  color: #1a2980;
}

.new-chat-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 0 20px rgba(100, 255, 218, 0.6);
}

.light-mode .new-chat-btn:hover {
  background: rgba(30, 50, 100, 0.2);
}

/* 折叠按钮 */
.collapse-btn {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  width: 80%;
  height: 36px;
  background: rgba(100, 255, 218, 0.1);
  color: #64ffda;
  border: 1px solid rgba(100, 255, 218, 0.3);
  border-radius: 18px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  font-size: 14px;
}

.light-mode .collapse-btn {
  background: rgba(30, 50, 100, 0.1);
  color: #1a2980;
}

.sidebar.collapsed .collapse-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.light-mode .sidebar.collapsed .collapse-btn {
  background: rgba(30, 50, 100, 0.1);
  color: #1a2980;
}

.collapse-btn:hover {
  background: rgba(100, 255, 218, 0.2);
}

.light-mode .collapse-btn:hover {
  background: rgba(30, 50, 100, 0.2);
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
  transition: all 0.2s;
  border-radius: 8px;
  margin: 4px 8px;
  border-left: 3px solid transparent;
}

/* 修改日间模式下的对话项样式 */
.light-mode .conversation-item {
  background:#e78d2b; /* 提高透明度，使背景更亮 */
  border: 1px solid rgba(244, 162, 89, 0.15);
}

/* 修改日间模式下对话项的悬停状态 */
.light-mode .conversation-item:hover {
  background: rgba(255, 255, 255, 0.95);
  border-color: rgba(244, 162, 89, 0.3);
}

/* 修改日间模式下活动对话项的样式 */
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
  color: #e6ecf5;
}

.light-mode .conv-title {
  color: #1a2980;
}

.conv-time {
  font-size: 0.8em;
  color: #8a94b8;
}

.light-mode .conv-time {
  color: rgba(30, 50, 100, 0.6);
}

.delete-btn {
  background: none;
  border: none;
  color: #8a94b8;
  font-size: 1.2em;
  padding: 0;
  opacity: 0;
  transition: all 0.2s;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.light-mode .delete-btn {
  background: rgba(255, 76, 76, 0.1);
}

.conversation-item:hover .delete-btn {
  opacity: 1;
}

.light-mode .conversation-item:hover .delete-btn {
  background: rgba(255, 76, 76, 0.1);
}

.delete-btn:hover {
  background: rgba(255, 76, 76, 0.1);
}

.light-mode .delete-btn:hover {
  background: rgba(255, 76, 76, 0.1);
}

.delete-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
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
  flex: 1; /* 让聊天容器充满剩余空间 */
  height: 100%; /* 修改为100%替代100vh */
  background: #2d2339; /* 更改为深紫色背景 */
  transition: all 0.3s;
  position: relative;
}

/* 侧边栏展开时聊天容器样式 */
.chat-container.sidebar-expanded {
  flex: 1;
  /* 添加侧边栏展开时的过渡效果 */
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* 对话面板 */
.conversation-pane {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #3d2d4e; /* 更改为深紫色 */
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  max-height: 100%; /* 确保不超出容器 */
  transition: all 0.3s; /* 添加过渡效果 */
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
  border-radius: 12px 0 0 12px;
}

.chat-container.editing-mode .editor-pane {
  flex: 0.9;
  background: #131b30;
  border-radius: 0 12px 12px 0;
  box-shadow: 0 0 30px rgba(0, 0, 0, 0.3);
  border-left: 1px solid #2a3356;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* 聊天头部 */
.chat-header {
  height: 70px;
  padding: 0 24px 0 70px; /* 增加左侧padding以容纳折叠按钮 */
  background: #3d2d4e; /* 更改为深紫色 */
  color: #e6ecf5;
  display: flex;
  position: relative;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #53416e;
  overflow: hidden;
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

/* 修改按钮hover效果增强用户体验 */
.toggle-sidebar-btn:hover {
  background: rgba(255, 158, 94, 0.2); /* 更改为半透明橙色 */
  transform: translateY(-50%) scale(1.05);
  box-shadow: 0 0 10px rgba(255, 158, 94, 0.3); /* 橙色阴影 */
}

.light-mode .toggle-sidebar-btn {
  background: rgba(216, 101, 0, 0.1); /* 半透明深橙色 */
  color: #b35c00;
  border: 1px solid rgba(216, 101, 0, 0.2);
}

.light-mode .toggle-sidebar-btn:hover {
  background: rgba(216, 101, 0, 0.2); /* 半透明深橙色 */
  transform: translateY(-50%) scale(1.05);
  box-shadow: 0 0 10px rgba(216, 101, 0, 0.3);
}

.chat-header h1 {
  font-size: 1.8rem;
  font-weight: 800;
  margin: 0;
  background: linear-gradient(90deg, #ff9e5e, #f4a259); /* 更改为橙金色渐变 */
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  position: relative;
}

.chat-header h1::after {
  content: "";
  position: absolute;
  bottom: -3px;
  left: 0;
  width: 100%;
  height: 1px;
  background: linear-gradient(90deg, transparent, #ff9e5e, transparent); /* 更改为橙色 */
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
}

.powered-by {
  font-size: 0.8rem;
  color: #8a94b8;
}

/* 聊天窗口 */
.chat-window {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  background: #2d2339; /* 更改为深紫色背景 */
  scroll-behavior: smooth;
  background-image: radial-gradient(
      circle at 50% 50%,
      rgba(255, 158, 94, 0.03) 0%, /* 更改为半透明橙色 */
      transparent 20%
    ),
    radial-gradient(
      circle at 80% 20%,
      rgba(255, 158, 94, 0.03) 0%, /* 更改为半透明橙色 */
      transparent 20%
    );
  min-height: 0; /* 允许flex收缩 */
}

/* 消息样式 */
.message {
  margin-bottom: 30px;
  animation: fadeIn 0.4s cubic-bezier(0.4, 0, 0.2, 1);
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
  border-radius: 12px;
  padding: 16px;
  position: relative;
  max-width: 100%;
  transition: all 0.2s;
  backdrop-filter: blur(10px);
}

.assistant .bubble {
  background: rgba(61, 45, 78, 0.8); /* 更改为深紫色半透明 */
  border: 1px solid rgba(255, 158, 94, 0.2); /* 更改为半透明橙色边框 */
  min-width: 50%;
}

.user .bubble {
  background: rgba(94, 58, 110, 0.4); /* 更改为紫色半透明 */
  color: #e6ecf5;
  border: 1px solid rgba(255, 158, 94, 0.3); /* 更改为半透明橙色边框 */
}

.bubble:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.assistant .bubble:hover {
  border-color: rgba(255, 158, 94, 0.4); /* 更改为半透明橙色 */
}

.user .bubble:hover {
  border-color: rgba(244, 162, 89, 0.5); /* 更改为半透明金黄色 */
}

/* 思考过程容器样式 */
.thinking-process {
  margin-bottom: 15px;
  border-radius: 8px;
  overflow: hidden;
  background-color: #251c46; /* 更改为暗紫色 */
  border: 1px solid rgba(255, 255, 255, 0.1);
}

/* 思考过程标题样式 */
.thinking-header {
  padding: 10px 15px;
  background: rgba(255, 255, 255, 0.05);
  color: rgba(255, 255, 255, 0.9);
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.thinking-icon {
  margin-right: 8px;
}

.toggle-icon {
  margin-left: auto;
}

/* 思考过程内容样式 */
.reasoning-content {
  padding: 15px;
  color: rgba(255, 255, 255, 0.8);
  background-color: #251c46; /* 更改为暗紫色 */
  font-size: 14px;
  line-height: 1.6;
}

/* 正式回答容器样式 */
.correct-answer {
  background-color: #251c46; /* 更改为暗紫色 */
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.1);
  margin-top: 10px; /* 增加与思考过程的间距 */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); /* 增加阴影效果 */
}

/* 正式回答标题样式 */
.correct-answer-label {
  padding: 10px 15px;
  background: linear-gradient(135deg, #352941, #ff9e5e); /* 从深紫到橙色的渐变 */
  color: white;
  font-weight: 500;
  display: flex;
  align-items: center;
}

.correct-answer-icon {
  margin-right: 8px;
}

/* 正式回答内容样式 */
.correct-answer-content {
  padding: 15px;
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

/* 覆盖可能的 Mathpix 默认样式 */
.correct-answer-content .katex-html ul,
.correct-answer-content .katex-html ol {
  padding-left: 2em !important;
}

/* 针对 Mathpix 特定的列表渲染 */
.correct-answer-content .mp-md-block-list {
  padding-left: 2em !important;
  margin-left: 0 !important;
}

.correct-answer-content .mp-md-block-list-item {
  display: list-item !important;
  padding-left: 0.5em !important;
}

/* 日间模式样式 */
.light-mode .thinking-process {
  background-color: #fff5e6; /* 更改为淡橙色背景 */
  border: 1px solid rgba(216, 101, 0, 0.1);
}

.light-mode .thinking-header {
  background: rgba(244, 162, 89, 0.05); /* 更改为半透明金黄色 */
  color: #593618; /* 深棕色文字 */
  border-bottom: 1px solid rgba(216, 101, 0, 0.1);
}

.light-mode .reasoning-content {
  background-color: #fff5e6; /* 更改为淡橙色背景 */
  color: #593618; /* 深棕色文字 */
}

.light-mode .correct-answer {
  background-color: #ffffff;
  border: 1px solid rgba(216, 101, 0, 0.1);
  box-shadow: 0 4px 12px rgba(244, 162, 89, 0.08); /* 更改为金黄色阴影 */
}

/* 清新的渐变色彩 */
.light-mode .correct-answer-label {
  background: linear-gradient(135deg, #f4a259, #f7cb87); /* 更改为橙金色渐变 */
  color: white;
}

.light-mode .correct-answer-content {
  color: #593618; /* 深棕色文字 */
}

/* 完善日间模式下正式回答中的markdown内容格式 */
.light-mode .correct-answer-content h1,
.light-mode .correct-answer-content h2,
.light-mode .correct-answer-content h3,
.light-mode .correct-answer-content h4,
.light-mode .correct-answer-content h5,
.light-mode .correct-answer-content h6 {
  color: #593618; /* 深棕色文字 */
  margin-top: 1.2em;
  margin-bottom: 0.8em;
  font-weight: 600;
}

.light-mode .correct-answer-content h1 {
  font-size: 1.8em;
  border-bottom: 1px solid #e0e6f5;
  padding-bottom: 0.3em;
}

.light-mode .correct-answer-content h2 {
  font-size: 1.5em;
  border-bottom: 1px solid #e0e6f5;
  padding-bottom: 0.3em;
}

.light-mode .correct-answer-content h3 {
  font-size: 1.3em;
}

.light-mode .correct-answer-content h4 {
  font-size: 1.1em;
}

.light-mode .correct-answer-content p {
  margin: 0.8em 0;
  line-height: 1.6;
}

.light-mode .correct-answer-content a {
  color: #5b86e5;
  text-decoration: none;
}

.light-mode .correct-answer-content a:hover {
  text-decoration: underline;
}

.light-mode .correct-answer-content pre {
  background-color: #f5f8ff !important;
  border-radius: 6px;
  padding: 12px;
  overflow: auto;
  margin: 1em 0;
  border: 1px solid #e0e6f5 !important;
}

.light-mode .correct-answer-content code {
  background-color: #f0f5ff;
  padding: 2px 5px;
  border-radius: 3px;
  font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
  font-size: 0.9em;
  color: #36d1dc;
}

.light-mode .correct-answer-content pre code {
  background-color: white;
  padding: 0;
  border-radius: 0;
  color: #1a2980;
}

.light-mode .correct-answer-content blockquote {
  border-left: 4px solid #5b86e5;
  padding: 0.5em 1em;
  margin: 1em 0;
  background-color: #f5f8ff;
  color: #1a2980;
}

.light-mode .correct-answer-content img {
  max-width: 100%;
  margin: 1em 0;
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(26, 41, 128, 0.1);
}

.light-mode .correct-answer-content table {
  border-collapse: collapse;
  width: 100%;
  margin: 1em 0;
  overflow: auto;
  display: block;
}

.light-mode .correct-answer-content table th {
  background-color: #f0f5ff !important;
  font-weight: 600;
  text-align: left;
}

.light-mode .correct-answer-content table th,
.light-mode .correct-answer-content table td {
  padding: 8px 12px;
  border: 1px solid #e0e6f5 !important;
}

.light-mode .correct-answer-content table tr:nth-child(even) {
  background-color: #f9faff;
}

.light-mode .correct-answer-content hr {
  height: 1px;
  background-color: #e0e6f5;
  border: none;
  margin: 1.5em 0;
}

/* KaTeX公式在日间模式下的样式 */
.light-mode .correct-answer-content .katex {
  font-size: 1.1em;
}

.light-mode .correct-answer-content .katex-display {
  margin: 1em 0;
  overflow-x: auto;
  overflow-y: hidden;
}

/* 确保列表样式正确 */
.light-mode .correct-answer-content ul,
.light-mode .correct-answer-content ol {
  padding-left: 2em !important;
  margin: 0.8em 0 !important;
}

.light-mode .correct-answer-content li {
  margin-bottom: 0.5em !important;
}

/* 夜间模式下对应的正式回答markdown内容格式优化 */
.correct-answer-content h1,
.correct-answer-content h2,
.correct-answer-content h3,
.correct-answer-content h4,
.correct-answer-content h5,
.correct-answer-content h6 {
  color: rgba(255, 255, 255, 0.95);
  margin-top: 1.2em;
  margin-bottom: 0.8em;
  font-weight: 600;
}

.correct-answer-content h1 {
  font-size: 1.8em;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 0.3em;
}

.correct-answer-content h2 {
  font-size: 1.5em;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 0.3em;
}

.correct-answer-content a {
  color: #64ffda;
  text-decoration: none;
}

.correct-answer-content a:hover {
  text-decoration: underline;
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
  border-radius: 8px;
  padding: 6px 12px;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 6px;
}

.light-mode .edit-button,
.light-mode.break-button {
  background: rgba(255, 255, 255, 0.8);
  color: #593618; /* 深棕色文字 */
  border: 1px solid rgba(216, 101, 0, 0.2);
}
.edit-button:hover {
  background: rgba(255, 158, 94, 0.1); /* 更改为半透明橙色 */
  color: #ff9e5e; /* 更改为橙色 */
  border-color: rgba(255, 158, 94, 0.3); /* 更改为半透明橙色 */
}

.break-button:hover {
  background: rgba(255, 76, 76, 0.1);
  color: #ff4c4c;
  border-color: rgba(255, 76, 76, 0.3);
}

.timestamp {
  font-size: 0.8rem;
  color: #8a94b8;
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

/* 修复选择器，之前使用了错误的.light-mode.input-area */
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
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.upload-icon {
  font-size: 1.2em;
}

.upload-button:hover {
  background: rgba(255, 158, 94, 0.2); /* 更改为半透明橙色 */
  border-color: rgba(255, 158, 94, 0.4); /* 更改为半透明橙色边框 */
}

.upload-tip {
  font-size: 0.75em;
  color: #8a94b8;
  position: absolute;
  bottom: -18px;
  left: 12px;
  white-space: nowrap;
}

.text-inputer input {
  width: 100%;
  padding: 14px 16px;
  border: 1px solid #53416e;
  border-radius: 8px;
  outline: none;
  background: rgba(61, 45, 78, 0.6); /* 更改为深紫色半透明 */
  color: #e6ecf5;
  font-size: 1rem;
  transition: all 0.3s;
}

.text-inputer input:focus {
  border-color: rgba(255, 158, 94, 0.4); /* 更改为半透明橙色边框 */
  box-shadow: 0 0 0 2px rgba(255, 158, 94, 0.1); /* 更改为半透明橙色阴影 */
}

.text-inputer input::placeholder {
  color: #8a94b8;
}

.send-button button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: linear-gradient(135deg, #5e3a6e, #ff9e5e); /* 从紫色到橙色的渐变 */
  color: #0f1629;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 600;
  min-width: 100px;
}

.send-button button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 0 15px rgba(255, 158, 94, 0.4); /* 橙色阴影 */
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

.dot-flashing::before {
  left: -15px;
  animation: dotFlashing 1s infinite alternate;
  animation-delay: 0s;
}

.dot-flashing::after {
  left: 15px;
  animation: dotFlashing 1s infinite alternate;
  animation-delay: 1s;
}
.answering-indicator {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px;
  background: rgba(241, 245, 249, 0.7);
  border-radius: 8px;
  margin-top: 8px;
  font-style: italic;
  color: #94a3b8;
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
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: 500;
  background: rgba(255, 158, 94, 0.1); /* 更改为半透明橙色 */
  color: #ff9e5e; /* 更改为橙色 */
  border: 1px solid rgba(255, 158, 94, 0.2); /* 更改为半透明橙色边框 */
}

.editor-actions button:hover {
  background: rgba(255, 158, 94, 0.2); /* 更改为半透明橙色 */
  border-color: rgba(255, 158, 94, 0.4); /* 更改为半透明橙色边框 */
}

/* 优化编辑器样式 */
:deep(.vditor) {
  border: none !important;
  height: calc(100% - 70px) !important;
  background: #2d2339 !important; /* 更改为深紫色背景 */
}

:deep(.vditor-toolbar) {
  background: #3d2d4e !important; /* 更改为深紫色 */
  border-bottom: 1px solid #53416e !important;
}

:deep(.vditor-toolbar svg) {
  fill: #a0b0d0 !important;
}

:deep(.vditor-toolbar button:hover svg) {
  fill: #64ffda !important;
}

:deep(.vditor-reset) {
  color: #e6ecf5 !important;
  background: #131b30 !important;
}

:deep(.vditor-reset pre) {
  background: rgba(23, 31, 56, 0.8) !important;
  border: 1px solid rgba(100, 255, 218, 0.2) !important;
  border-radius: 8px !important;
}

:deep(.vditor-reset code) {
  color: #64ffda !important;
  background: rgba(23, 31, 56, 0.6) !important;
  padding: 2px 6px !important;
  border-radius: 4px !important;
}

/* 对动画生命周期的定义 */
@keyframes slideDown {
  from {
    opacity: 0;
    transform: translate(-50%, -20px);
  }
  to {
    opacity: 1;
    transform: translate(-50%, 0);
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

/* 自定义滚动条 */
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

.control-panel {
  background-color: #1e3286; /* 稍微深一点的蓝色 */
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 0 30px rgba(0, 0, 0, 0.3);
}

/* 日间模式 */
.light-mode .control-panel {
  background-color: #ffffff;
  box-shadow: 0 0 30px rgba(0, 0, 0, 0.1);
}

/* 修复日间模式下的整体聊天容器背景 */
.light-mode .chat-container {
  background: #f0f5ff;
}

/* 修复日间模式下的聊天窗口背景图案 */
.light-mode .chat-window {
  background-image: radial-gradient(
    circle at 50% 50%,
    rgba(26, 41, 128, 0.03) 0%,
    rgba(26, 41, 128, 0.01) 100%
  );
}

/* 修复日间模式下的思考过程区域 */
.light-mode .thinking-header {
  background: rgba(14, 165, 233, 0.08);
  color: #0f172a;
  border-bottom: 1px solid #e2e8f0;
}

.light-mode .reasoning-content {
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid rgba(26, 41, 128, 0.1);
  color: #1a2980;
}

/* 修复日间模式下的编辑器面板 */
.light-mode .chat-container.editing-mode .editor-pane {
  background: #ffffff;
  border-left: 1px solid #e0e6f5;
}

.light-mode .editor-header {
  background: #f0f5ff;
  border-bottom: 1px solid #e0e6f5;
}

/* 修复日间模式下的加载指示器 */
.light-mode .loading-indicator {
  color: #1a2980;
}

.light-mode .dot-flashing {
  background-color: #1a2980;
}

.light-mode .dot-flashing::before,
.light-mode .dot-flashing::after {
  background-color: #1a2980;
}

@keyframes dotFlashingLight {
  0% {
    background-color: #1a2980;
  }
  50%,
  100% {
    background-color: rgba(26, 41, 128, 0.2);
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
}

.light-mode :deep(.vditor-toolbar) {
  background: #f0f5ff !important;
  border-bottom: 1px solid #e0e6f5 !important;
}

.light-mode :deep(.vditor-toolbar svg) {
  fill: #1a2980 !important;
}

.light-mode :deep(.vditor-toolbar button:hover svg) {
  fill: #1ec6ff !important;
}

/* 修正CSS选择器拼写错误 */
.light-mode :deep(.vditor-reset) {
  color: #1a2980 !important;
  background: #ffffff !important;
}

.light-mode :deep(.vditor-reset pre) {
  background: rgba(240, 245, 255, 0.8) !important;
  border: 1px solid rgba(26, 41, 128, 0.1) !important;
}

.light-mode :deep(.vditor-reset code) {
  color: #1a2980 !important;
  background: rgba(240, 245, 255, 0.6) !important;
}

/* 修复日间模式下的编辑器按钮 */
.light-mode .editor-actions button {
  background: rgba(26, 41, 128, 0.05);
  color: #1a2980;
  border: 1px solid rgba(26, 41, 128, 0.1);
}

.light-mode .editor-actions button:hover {
  background: rgba(26, 41, 128, 0.1);
}

.light-mode .save-button {
  background: rgba(30, 198, 255, 0.1) !important;
  color: #1a2980 !important;
}

/* 修正CSS选择器拼写错误 */
.light-mode .save-button:hover {
  background: rgba(30, 198, 255, 0.2) !important;
}

.light-mode .cancel-button {
  background: rgba(255, 76, 76, 0.1) !important;
  color: #ff4c4c !important;
}

.light-mode .export-button {
  background: rgba(26, 41, 128, 0.1) !important;
  color: #1a2980 !important;
}

/* 修复日间模式下的消息操作按钮 */
.light-mode .message-actions button {
  background: rgba(26, 41, 128, 0.05);
  color: #1a2980;
  border: 1px solid rgba(26, 41, 128, 0.1);
}

.light-mode .message-actions button:hover {
  background: rgba(26, 41, 128, 0.1);
}

/* 修复日间模式下的时间戳 */
.light-mode .timestamp {
  color: #8a94b8;
}

/* 修复日间模式下的思考中按钮 */
.light-mode .send-button button:disabled {
  background: linear-gradient(135deg, #64ffda, #1ec6ff);
  color: #000000 !important;
}

/* 修复正式回答区域 */
.light-mode .message .final-answer {
  background-color: #ffffff !important;
  color: #1a2980 !important;
  border: 1px solid #e0e6f5 !important;
  box-shadow: 0 2px 12px rgba(26, 41, 128, 0.1) !important;
}

/* 修复正式回答标签 */
.light-mode .message .final-answer-label {
  background: linear-gradient(135deg, #1a2980, #26d0ce);
  color: white;
}

/* 修复正式回答内容 */
.light-mode .message .final-answer-content {
  color: #1a2980 !important;
}

/* 修复正式回答中的markdown内容 */
.light-mode .message .markdown-body {
  color: #1a2980 !important;
  background-color: transparent !important;
}

.importantght-moimportantghtessage .markdown-body pre {
  background-color: #f5f7fa !important;
  border: 1px solid #e0e6f5 !important;
}

.light-mode .message .markdown-body code {
  color: #1a2980 !important;
  background-color: rgba(240, 245, 255, 0.6) !important;
}

/* 修复正式回答中的表格 */
.light-mode .message .markdown-body table {
  border-color: #e0e6f5 !important;
}

.light-mode .message .markdown-body th {
  background-color: #f0f5ff !important;
  color: #1a2980 !important;
  border-color: #e0e6f5 !important;
}

.importantght-mode .message .markdown-body td {
  border-color: #e0e6f5 !important;
  color: #1a2980 !important;
}

/* 修复正式回答中的引用块 */
.light-mode .message .markdown-body blockquote {
  border-left-color: #1a2980 !important;
  background-color: #f5f7fa !important;
  color: #1a2980 !important;
}

/* 修改侧边栏头部与聊天头部高度一致 */
.sidebar-header {
  height: 70px; /* 与聊天头部高度一致 */
  padding: 0 16px; /* 调整内边距 */
  display: flex;
  align-items: center; /* 确保垂直居中 */
  justify-content: space-between;
  position: relative; /* 为装饰条添加定位上下文 */
  background: #171f38; /* 与聊天头部背景一致 */
  border-bottom: 1px solid #2a3356;
}

/* 确保侧边栏与对话面板在展开状态下视觉上连贯 */
.chat-container.sidebar-expanded .conversation-pane {
  border-radius: 0 16px 16px 0;
  border-left: none; /* 移除左侧边框 */
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

/* 确保聊天头部在侧边栏展开时左上角没有圆角 */
.chat-container.sidebar-expanded .chat-header {
  border-top-left-radius: 0;
  border-bottom-left-radius: 0;
}

/* 日间模式下的一致性调整 */
.light-mode .sidebar-header {
  background: linear-gradient(135deg, #ffffff, #f0f5ff);
  border-bottom: 1px solid #e0e7ff;
}

/* 添加渐变动画 */
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

/* 修改发送按钮在日间模式下的样式 */
.light-mode .send-button button {
  background: linear-gradient(135deg, #f4a259, #f7cb87); /* 更新为橙金色渐变 */
  color: #ffffff;
}

.light-mode .send-button button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 0 15px rgba(244, 162, 89, 0.5); /* 更新为金黄色阴影 */
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

/* 修改上传按钮在日间模式下的样式 */
.light-mode .upload-button {
  background: rgba(244, 162, 89, 0.1); /* 更新为半透明金黄色背景 */
  color: #d86500; /* 更新为深橙色文字 */
  border: 1px solid rgba(244, 162, 89, 0.3); /* 更新为半透明金黄色边框 */
}

.light-mode .upload-button:hover {
  background: rgba(244, 162, 89, 0.2); /* 更新为半透明金黄色背景 */
  border-color: rgba(244, 162, 89, 0.5); /* 更新为半透明金黄色边框 */
}

.light-mode .upload-tip {
  color: rgba(89, 54, 24, 0.6); /* 更新为半透明深棕色 */
}
</style>
