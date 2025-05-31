<template>
  <div class="homework-container" :class="{ 'light-mode': isLightMode }">
    <div class="page-header">
      <h1>课后习题</h1>
      <p>{{ isTeacher ? '发布和管理课后习题' : '查看和完成课后习题' }}</p>
    </div>

    <!-- 教师端视图 -->
    <div v-if="isTeacher" class="teacher-view">
      <div class="action-bar">
        <el-button type="primary" @click="showUploadDialog">
          <el-icon><Upload /></el-icon>
          上传新习题
        </el-button>
        <el-button type="success" @click="showCreateDialog">
          <el-icon><Plus /></el-icon>
          创建试题
        </el-button>
      </div>

      <!-- 教师端试题列表 -->
      <el-tabs v-model="teacherActiveTab" class="homework-tabs">
        <el-tab-pane label="已发布" name="published">
          <el-table :data="publishedHomeworks" style="width: 100%">
            <el-table-column prop="title" label="试题标题" min-width="180"></el-table-column>
            <el-table-column prop="subject" label="学科" width="100"></el-table-column>
            <el-table-column prop="grade" label="年级" width="100"></el-table-column>
            <el-table-column prop="publishDate" label="发布日期" width="120"></el-table-column>
            <el-table-column prop="dueDate" label="截止日期" width="120"></el-table-column>
            <el-table-column prop="submissions" label="已提交/总人数" width="120">
              <template #default="scope">
                {{ scope.row.submissionCount }}/{{ scope.row.totalStudents }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="220">
              <template #default="scope">
                <el-button size="small" @click="previewHomework(scope.row)">
                  预览
                </el-button>
                <el-button size="small" type="success" @click="checkSubmissions(scope.row)">
                  查看提交
                </el-button>
                <el-button size="small" type="danger" @click="unpublishHomework(scope.row)">
                  撤回
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
        
        <el-tab-pane label="草稿" name="drafts">
          <el-table :data="draftHomeworks" style="width: 100%">
            <el-table-column prop="title" label="试题标题" min-width="180"></el-table-column>
            <el-table-column prop="subject" label="学科" width="100"></el-table-column>
            <el-table-column prop="grade" label="年级" width="100"></el-table-column>
            <el-table-column prop="createdDate" label="创建日期" width="120"></el-table-column>
            <el-table-column label="操作" width="240">
              <template #default="scope">
                <el-button size="small" @click="previewHomework(scope.row)">
                  预览
                </el-button>
                <el-button size="small" type="primary" @click="editHomework(scope.row)">
                  编辑
                </el-button>
                <el-button size="small" type="success" @click="publishHomework(scope.row)">
                  发布
                </el-button>
                <el-button size="small" type="danger" @click="deleteHomework(scope.row)">
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </div>

    <!-- 学生端视图 -->
    <div v-else class="student-view">
      <el-tabs v-model="studentActiveTab" class="homework-tabs">
        <el-tab-pane label="待完成" name="pending">
          <el-empty v-if="!pendingHomeworks.length" description="没有待完成的作业"></el-empty>
          
          <div v-else class="homework-cards">
            <el-card v-for="homework in pendingHomeworks" :key="homework.id" class="homework-card">
              <template #header>
                <div class="homework-header">
                  <span class="homework-title">{{ homework.title }}</span>
                  <el-tag 
                    :type="isUrgent(homework.dueDate) ? 'danger' : 'warning'" 
                    size="small"
                  >
                    {{ isUrgent(homework.dueDate) ? '紧急' : '待完成' }}
                  </el-tag>
                </div>
              </template>
              
              <div class="homework-details">
                <p><strong>学科：</strong>{{ homework.subject }}</p>
                <p><strong>年级：</strong>{{ homework.grade }}</p>
                <p><strong>发布日期：</strong>{{ homework.publishDate }}</p>
                <p><strong>截止日期：</strong>{{ homework.dueDate }}</p>
                <p><strong>发布老师：</strong>{{ homework.teacherName }}</p>
              </div>
              
              <div class="homework-actions">
                <el-button type="primary" @click="startHomework(homework)">开始做题</el-button>
              </div>
            </el-card>
          </div>
        </el-tab-pane>
        
        <el-tab-pane label="已完成" name="completed">
          <el-empty v-if="!completedHomeworks.length" description="没有已完成的作业"></el-empty>
          
          <div v-else class="homework-cards">
            <el-card v-for="homework in completedHomeworks" :key="homework.id" class="homework-card">
              <template #header>
                <div class="homework-header">
                  <span class="homework-title">{{ homework.title }}</span>
                  <el-tag type="success" size="small">已完成</el-tag>
                </div>
              </template>
              
              <div class="homework-details">
                <p><strong>学科：</strong>{{ homework.subject }}</p>
                <p><strong>年级：</strong>{{ homework.grade }}</p>
                <p><strong>发布日期：</strong>{{ homework.publishDate }}</p>
                <p><strong>提交日期：</strong>{{ homework.submissionDate }}</p>
                <p><strong>得分：</strong>{{ homework.score ? `${homework.score}分` : '待批阅' }}</p>
              </div>
              
              <div class="homework-actions">
                <el-button type="primary" @click="viewSubmission(homework)">查看提交</el-button>
              </div>
            </el-card>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>

    <!-- 上传习题对话框 -->
    <el-dialog
      v-model="uploadDialogVisible"
      title="上传新习题"
      width="500px"
    >
      <el-form :model="uploadForm" label-width="80px">
        <el-form-item label="标题">
          <el-input v-model="uploadForm.title" placeholder="请输入试题标题"></el-input>
        </el-form-item>
        <el-form-item label="学科">
          <el-select v-model="uploadForm.subject" placeholder="请选择学科" style="width: 100%;">
            <el-option v-for="item in subjects" :key="item" :label="item" :value="item"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="年级">
          <el-select v-model="uploadForm.grade" placeholder="请选择年级" style="width: 100%;">
            <el-option v-for="item in grades" :key="item" :label="item" :value="item"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="文件">
          <el-upload
            action="#"
            :auto-upload="false"
            :limit="1"
            accept=".pdf,.doc,.docx"
          >
            <el-button type="primary">选择文件</el-button>
            <template #tip>
              <div class="el-upload__tip">
                只能上传PDF、Word文档，且不超过10MB
              </div>
            </template>
          </el-upload>
        </el-form-item>
        <el-form-item label="截止日期">
          <el-date-picker
            v-model="uploadForm.dueDate"
            type="date"
            placeholder="选择截止日期"
            style="width: 100%;"
          ></el-date-picker>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="uploadDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="uploadHomework(false)">保存为草稿</el-button>
          <el-button type="success" @click="uploadHomework(true)">直接发布</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 试题预览对话框 -->
    <el-dialog
      v-model="previewDialogVisible"
      title="试题预览"
      width="70%"
    >
      <div v-if="currentHomework" class="homework-preview">
        <h2>{{ currentHomework.title }}</h2>
        <div class="preview-meta">
          <p><strong>学科：</strong>{{ currentHomework.subject }}</p>
          <p><strong>年级：</strong>{{ currentHomework.grade }}</p>
          <p v-if="currentHomework.publishDate"><strong>发布日期：</strong>{{ currentHomework.publishDate }}</p>
          <p v-if="currentHomework.dueDate"><strong>截止日期：</strong>{{ currentHomework.dueDate }}</p>
        </div>
        
        <div class="preview-content">
          <!-- 这里应该展示文档内容，可以是iframe嵌入PDF或其他格式 -->
          <div class="document-placeholder">
            <p>文档预览区域</p>
            <p>（实际应用中应该显示PDF或文档内容）</p>
          </div>
        </div>
      </div>
    </el-dialog>

    <!-- 做题对话框 -->
    <el-dialog
      v-model="doHomeworkDialogVisible"
      title="做题"
      width="80%"
    >
      <div v-if="currentHomework" class="do-homework">
        <h2>{{ currentHomework.title }}</h2>
        <div class="homework-meta">
          <p><strong>截止日期：</strong>{{ currentHomework.dueDate }}</p>
          <p><strong>剩余时间：</strong>{{ getRemainingTime(currentHomework.dueDate) }}</p>
        </div>
        
        <div class="homework-content">
          <!-- 这里应该展示做题界面，包含问题和答题区域 -->
          <div class="question-area">
            <div class="document-placeholder">
              <p>试题内容区域</p>
              <p>（实际应用中应该显示试题内容）</p>
            </div>
          </div>
          
          <div class="answer-area">
            <h3>答题区</h3>
            <el-input
              v-model="answerContent"
              type="textarea"
              :rows="8"
              placeholder="请在此输入你的答案..."
            ></el-input>
            
            <div class="file-upload">
              <p>或上传答案文件：</p>
              <el-upload
                action="#"
                :auto-upload="false"
                :limit="1"
                accept=".pdf,.doc,.docx,.jpg,.png"
              >
                <el-button type="primary">选择文件</el-button>
              </el-upload>
            </div>
          </div>
        </div>
        
        <div class="submit-area">
          <el-button @click="doHomeworkDialogVisible = false">稍后再做</el-button>
          <el-button type="primary" @click="submitHomework">提交答案</el-button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted, onBeforeUnmount } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { getCurrentUser } from '@/api/auth';
import { Plus, Upload } from '@element-plus/icons-vue';

export default {
  name: 'Homework',
  components: { Plus, Upload },
  setup() {
    // 添加夜间模式状态
    const isLightMode = ref(localStorage.getItem("theme-mode") === "light");

    // 获取当前用户信息
    const currentUser = ref(getCurrentUser());
    const isTeacher = computed(() => currentUser.value?.role === 'teacher');
    
    // 教师端状态
    const teacherActiveTab = ref('published');
    const publishedHomeworks = ref([]);
    const draftHomeworks = ref([]);
    
    // 学生端状态
    const studentActiveTab = ref('pending');
    const pendingHomeworks = ref([]);
    const completedHomeworks = ref([]);
    
    // 对话框状态
    const uploadDialogVisible = ref(false);
    const previewDialogVisible = ref(false);
    const doHomeworkDialogVisible = ref(false);
    const currentHomework = ref(null);
    const answerContent = ref('');
    
    // 上传表单
    const uploadForm = reactive({
      title: '',
      subject: '',
      grade: '',
      dueDate: ''
    });
    
    // 选项数据
    const subjects = ['语文', '数学', '英语', '物理', '化学', '生物', '历史', '地理', '政治'];
    const grades = ['一年级', '二年级', '三年级', '四年级', '五年级', '六年级', '初一', '初二', '初三', '高一', '高二', '高三'];
    
    // 加载试题数据
    const loadHomeworkData = async () => {
      try {
        // 实际应用中应调用API获取数据
        // 这里使用模拟数据
        
        if (isTeacher.value) {
          // 加载教师端数据
          publishedHomeworks.value = [
            {
              id: 1,
              title: '高中物理力学综合测试',
              subject: '物理',
              grade: '高一',
              publishDate: '2023-09-15',
              dueDate: '2023-09-22',
              submissionCount: 25,
              totalStudents: 40
            },
            {
              id: 2,
              title: '英语定语从句练习',
              subject: '英语',
              grade: '初三',
              publishDate: '2023-09-10',
              dueDate: '2023-09-20',
              submissionCount: 32,
              totalStudents: 45
            }
          ];
          
          draftHomeworks.value = [
            {
              id: 3,
              title: '数学函数与导数练习',
              subject: '数学',
              grade: '高二',
              createdDate: '2023-09-14'
            }
          ];
        } else {
          // 加载学生端数据
          pendingHomeworks.value = [
            {
              id: 1,
              title: '高中物理力学综合测试',
              subject: '物理',
              grade: '高一',
              teacherName: '王老师',
              publishDate: '2023-09-15',
              dueDate: '2023-09-22'
            }
          ];
          
          completedHomeworks.value = [
            {
              id: 2,
              title: '英语定语从句练习',
              subject: '英语',
              grade: '初三',
              teacherName: '李老师',
              publishDate: '2023-09-10',
              submissionDate: '2023-09-18',
              score: 92
            }
          ];
        }
      } catch (error) {
        console.error('加载作业数据失败:', error);
        ElMessage.error('加载作业数据失败，请稍后重试');
      }
    };
    
    // 显示上传对话框
    const showUploadDialog = () => {
      // 重置表单
      Object.keys(uploadForm).forEach(key => {
        uploadForm[key] = '';
      });
      uploadDialogVisible.value = true;
    };
    
    // 显示创建对话框（此处简化为与上传相同）
    const showCreateDialog = () => {
      showUploadDialog();
    };
    
    // 上传作业
    const uploadHomework = (isPublish) => {
      // 表单验证
      if (!uploadForm.title || !uploadForm.subject || !uploadForm.grade) {
        ElMessage.warning('请填写完整信息');
        return;
      }
      
      // 如果是立即发布，必须有截止日期
      if (isPublish && !uploadForm.dueDate) {
        ElMessage.warning('发布作业必须设置截止日期');
        return;
      }
      
      // 在实际应用中，这里应调用API保存数据
      ElMessage.success(isPublish ? '作业已发布' : '作业已保存为草稿');
      uploadDialogVisible.value = false;
      
      // 重新加载数据
      loadHomeworkData();
    };
    
    // 预览作业
    const previewHomework = (homework) => {
      currentHomework.value = homework;
      previewDialogVisible.value = true;
    };
    
    // 编辑作业
    const editHomework = (homework) => {
      ElMessage.info('编辑作业功能待实现');
    };
    
    // 发布作业
    const publishHomework = (homework) => {
      ElMessageBox.confirm(`确定发布"${homework.title}"吗？`, '发布确认', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        ElMessage.success('作业已成功发布');
        loadHomeworkData();
      }).catch(() => {});
    };
    
    // 删除作业
    const deleteHomework = (homework) => {
      ElMessageBox.confirm(`确定删除"${homework.title}"吗？此操作不可恢复`, '删除确认', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'danger'
      }).then(() => {
        ElMessage.success('作业已成功删除');
        loadHomeworkData();
      }).catch(() => {});
    };
    
    // 撤回已发布的作业
    const unpublishHomework = (homework) => {
      ElMessageBox.confirm(`确定撤回"${homework.title}"吗？已提交的学生答案将保留`, '撤回确认', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        ElMessage.success('作业已成功撤回');
        loadHomeworkData();
      }).catch(() => {});
    };
    
    // 查看提交
    const checkSubmissions = (homework) => {
      ElMessage.info('查看提交功能待实现');
    };
    
    // 学生端开始做题
    const startHomework = (homework) => {
      currentHomework.value = homework;
      answerContent.value = '';
      doHomeworkDialogVisible.value = true;
    };
    
    // 学生端提交作业
    const submitHomework = () => {
      if (!answerContent.value.trim()) {
        ElMessage.warning('请输入答案或上传答案文件');
        return;
      }
      
      ElMessageBox.confirm('确定提交此答案吗？提交后不可修改', '提交确认', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        ElMessage.success('答案已成功提交');
        doHomeworkDialogVisible.value = false;
        loadHomeworkData();
      }).catch(() => {});
    };
    
    // 查看已提交的作业
    const viewSubmission = (homework) => {
      ElMessage.info('查看提交功能待实现');
    };
    
    // 判断作业是否紧急（距离截止日期不到2天）
    const isUrgent = (dueDate) => {
      const now = new Date();
      const due = new Date(dueDate);
      const diffTime = due - now;
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
      return diffDays <= 2 && diffDays >= 0;
    };
    
    // 获取剩余时间
    const getRemainingTime = (dueDate) => {
      const now = new Date();
      const due = new Date(dueDate);
      const diffTime = due - now;
      
      if (diffTime <= 0) {
        return '已过期';
      }
      
      const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
      const diffHours = Math.floor((diffTime % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      
      return `${diffDays}天${diffHours}小时`;
    };
    
    // 添加主题监听
    const checkThemeMode = () => {
      isLightMode.value = localStorage.getItem("theme-mode") === "light";
    };
    
    onMounted(() => {
      loadHomeworkData();
      
      // 添加主题监听
      checkThemeMode();
      window.addEventListener("storage", checkThemeMode);
      window.addEventListener("themeChange", checkThemeMode);
    });
    
    onBeforeUnmount(() => {
      // 移除主题监听
      window.removeEventListener("storage", checkThemeMode);
      window.removeEventListener("themeChange", checkThemeMode);
    });
    
    return {
      isLightMode,
      isTeacher,
      teacherActiveTab,
      publishedHomeworks,
      draftHomeworks,
      studentActiveTab,
      pendingHomeworks,
      completedHomeworks,
      uploadDialogVisible,
      previewDialogVisible,
      doHomeworkDialogVisible,
      currentHomework,
      answerContent,
      uploadForm,
      subjects,
      grades,
      showUploadDialog,
      showCreateDialog,
      uploadHomework,
      previewHomework,
      editHomework,
      publishHomework,
      deleteHomework,
      unpublishHomework,
      checkSubmissions,
      startHomework,
      submitHomework,
      viewSubmission,
      isUrgent,
      getRemainingTime
    };
  }
}
</script>

<style scoped>
/* 夜间模式(默认) */
.homework-container {
  padding: 20px;
  height: 100%;
  overflow-y: auto;
  background-color: #2d2339; /* 更改为深紫色背景 */
  color: #e6ecf5;
  transition: background-color 0.3s, color 0.3s;
}

/* 日间模式 */
.homework-container.light-mode {
  background-color: #fff9f0; /* 更改为温暖米色背景 */
  color: #593618; /* 深棕色文字 */
}

.page-header {
  margin-bottom: 24px;
}

.page-header h1 {
  font-size: 24px;
  margin-bottom: 8px;
  color: #ff9e5e; /* 更改为橙色主色 */
  transition: color 0.3s;
}

.light-mode .page-header h1 {
  color: #d86500; /* 更改为深橙色主色 */
}

.page-header p {
  color: #a0b0d0; /* 夜间模式次要文本色 */
  font-size: 14px;
  transition: color 0.3s;
}

.light-mode .page-header p {
  color: #593618; /* 更改为深棕色文字 */
}

.action-bar {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
}

.homework-tabs {
  margin-top: 10px;
  border-radius: 8px;
  overflow: hidden;
}

/* 表格样式 */
:deep(.el-table) {
  background-color: #3d2d4e !important; /* 更改为深紫色表格背景 */
  color: #e6ecf5 !important;
  transition: background-color 0.3s, color 0.3s;
}

.light-mode :deep(.el-table) {
  background-color: #ffffff !important; /* 日间模式表格背景 */
  color: #593618 !important; /* 更改为深棕色文字 */
}

:deep(.el-table th.el-table__cell) {
  background-color: #5e3a6e !important; /* 更改为紫色表头背景 */
  color: #ff9e5e !important; /* 更改为橙色 */
  transition: background-color 0.3s, color 0.3s;
}

.light-mode :deep(.el-table th.el-table__cell) {
  background-color: #f5f7fa !important; /* 日间模式表头背景 */
  color: #d86500 !important; /* 更改为深橙色 */
}

:deep(.el-table--striped .el-table__body tr.el-table__row--striped td.el-table__cell) {
  background-color: rgba(61, 45, 78, 0.4) !important; /* 更改为半透明紫色条纹背景 */
  transition: background-color 0.3s;
}

.light-mode :deep(.el-table--striped .el-table__body tr.el-table__row--striped td.el-table__cell) {
  background-color: rgba(244, 162, 89, 0.05) !important; /* 更改为半透明金黄色背景 */
}

:deep(.el-table td.el-table__cell) {
  border-bottom-color: rgba(255, 255, 255, 0.05) !important; /* 夜间模式边框色 */
  transition: border-color 0.3s;
}

.light-mode :deep(.el-table td.el-table__cell) {
  border-bottom-color: rgba(0, 0, 0, 0.05) !important; /* 日间模式边框色 */
}

/* 表格单元格样式修复 */
:deep(.el-table__cell),
:deep(td.el-table_3_column_13.el-table__cell),
:deep(td.el-table__cell.el-table-column) {
  background-color: #3d2d4e !important; /* 更改为深紫色 */
  color: #e6ecf5 !important;
  transition: all 0.3s;
}

.light-mode :deep(.el-table__cell),
.light-mode :deep(td.el-table_3_column_13.el-table__cell),
.light-mode :deep(td.el-table__cell.el-table-column) {
  background-color: #ffffff !important;
  color: #593618 !important; /* 更改为深棕色 */
}

:deep(.el-table tr:hover td.el-table__cell) {
  background-color: rgba(255, 158, 94, 0.05) !important; /* 更改为半透明橙色 */
}

.light-mode :deep(.el-table tr:hover td.el-table__cell) {
  background-color: rgba(244, 162, 89, 0.05) !important; /* 更改为半透明金黄色 */
}

/* 卡片样式 */
.homework-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.homework-card {
  transition: all 0.3s;
  background-color: #3d2d4e; /* 更改为深紫色 */
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.light-mode .homework-card {
  background-color: #ffffff;
  border: 1px solid rgba(244, 162, 89, 0.1); /* 更改为半透明金黄色边框 */
}

.homework-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
}

.light-mode .homework-card:hover {
  box-shadow: 0 10px 20px rgba(244, 162, 89, 0.15); /* 更改为金黄色阴影 */
}

.homework-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  transition: border-color 0.3s;
}

.light-mode .homework-header {
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.homework-title {
  font-weight: bold;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 200px;
  color: #e6ecf5;
  transition: color 0.3s;
}

.light-mode .homework-title {
  color: #593618;
}

.homework-details {
  margin: 10px 0;
}

.homework-details p {
  margin: 5px 0;
  font-size: 14px;
  color: #a0b0d0; /* 夜间模式文本色 */
  transition: color 0.3s;
}

.light-mode .homework-details p {
  color: #4b6cb7; /* 日间模式文本色 */
}

.homework-actions {
  margin-top: 15px;
  display: flex;
  justify-content: flex-end;
}

/* 预览和做题对话框 */
.homework-preview {
  padding: 20px;
}

.homework-preview h2 {
  text-align: center;
  margin-bottom: 20px;
  color: #ff9e5e; /* 更改为橙色 */
  transition: color 0.3s;
}

.light-mode .homework-preview h2 {
  color: #d86500; /* 更改为深橙色 */
}

.preview-meta {
  margin-bottom: 20px;
  padding: 10px;
  background-color: rgba(61, 45, 78, 0.4); /* 更改为半透明深紫色 */
  border-radius: 4px;
  transition: background-color 0.3s;
}

.light-mode .preview-meta {
  background-color: rgba(244, 162, 89, 0.05); /* 更改为半透明金黄色背景 */
}

.preview-meta p {
  margin: 5px 0;
  color: #a0b0d0; /* 夜间模式文本色 */
  transition: color 0.3s;
}

.light-mode .preview-meta p {
  color: #4b6cb7; /* 日间模式文本色 */
}

.preview-content {
  min-height: 400px;
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 4px;
  transition: border-color 0.3s;
}

.light-mode .preview-content {
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.document-placeholder {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 400px;
  background-color: rgba(61, 45, 78, 0.3); /* 更改为半透明紫色 */
  font-size: 18px;
  color: #a0b0d0;
  transition: background-color 0.3s, color 0.3s;
}

.light-mode .document-placeholder {
  background-color: #f5f7fa;
  color: #593618; /* 更改为深棕色 */
}

/* 做题界面 */
.do-homework {
  padding: 10px;
}

.do-homework h2 {
  text-align: center;
  margin-bottom: 15px;
  color: #ff9e5e; /* 更改为橙色 */
  transition: color 0.3s;
}

.light-mode .do-homework h2 {
  color: #d86500; /* 更改为深橙色 */
}

.homework-meta {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
  padding: 10px;
  background-color: rgba(61, 45, 78, 0.4); /* 更改为半透明紫色 */
  border-radius: 4px;
  transition: background-color 0.3s;
}

.light-mode .homework-meta {
  background-color: rgba(244, 162, 89, 0.05); /* 更改为半透明金黄色 */
}

.homework-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 20px;
}

.question-area {
  flex: 1;
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 4px;
  padding: 10px;
  transition: border-color 0.3s;
}

.light-mode .question-area {
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.answer-area {
  flex: 1;
  padding: 10px;
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 4px;
  transition: border-color 0.3s;
}

.light-mode .answer-area {
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.answer-area h3 {
  margin-bottom: 15px;
  font-size: 16px;
  color: #ff9e5e; /* 更改为橙色 */
  transition: color 0.3s;
}

.light-mode .answer-area h3 {
  color: #d86500; /* 更改为深橙色 */
}

.file-upload {
  margin-top: 15px;
}

.submit-area {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

/* 滚动条美化 */
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
  transition: background 0.3s;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 158, 94, 0.3); /* 更改为半透明橙色 */
}

.light-mode ::-webkit-scrollbar-track {
  background: rgba(255, 249, 240, 0.5); /* 更改为半透明米色 */
}

.light-mode ::-webkit-scrollbar-thumb {
  background: rgba(244, 162, 89, 0.2); /* 更改为半透明金黄色 */
}

.light-mode ::-webkit-scrollbar-thumb:hover {
  background: rgba(244, 162, 89, 0.3); /* 更改为半透明金黄色 */
}

/* 响应式布局 */
@media (min-width: 768px) {
  .homework-content {
    flex-direction: row;
  }
}

/* Element Plus表单组件夜间模式 */
:deep(.el-form-item__label) {
  color: #a0b0d0 !important;
}

.light-mode :deep(.el-form-item__label) {
  color: #593618 !important; /* 更改为深棕色 */
}

:deep(.el-input__wrapper) {
  background-color: rgba(61, 45, 78, 0.4) !important; /* 更改为半透明紫色 */
  border: 1px solid rgba(255, 158, 94, 0.2) !important; /* 更改为半透明橙色边框 */
  box-shadow: none !important;
}

.light-mode :deep(.el-input__wrapper) {
  background-color: rgba(255, 249, 240, 0.5) !important; /* 更改为半透明米色 */
  border: 1px solid rgba(244, 162, 89, 0.2) !important; /* 更改为半透明金黄色边框 */
}

:deep(.el-input__inner), :deep(.el-textarea__inner) {
  color: #e6ecf5 !important;
}

.light-mode :deep(.el-input__inner), .light-mode :deep(.el-textarea__inner) {
  color: #1a2980 !important;
}

:deep(.el-date-editor .el-input__wrapper) {
  background-color: rgba(61, 45, 78, 0.4) !important; /* 更改为半透明紫色 */
  border: 1px solid rgba(255, 158, 94, 0.2) !important; /* 更改为半透明橙色边框 */
}

.light-mode :deep(.el-date-editor .el-input__wrapper) {
  background-color: rgba(255, 249, 240, 0.5) !important; /* 更改为半透明米色 */
  border: 1px solid rgba(244, 162, 89, 0.2) !important; /* 更改为半透明金黄色边框 */
}

:deep(.el-date-picker) {
  background-color: #3d2d4e !important; /* 更改为深紫色 */
  border: 1px solid rgba(255, 158, 94, 0.2) !important; /* 更改为半透明橙色边框 */
  color: #e6ecf5 !important;
}

.light-mode :deep(.el-date-picker) {
  background-color: #ffffff !important;
  border: 1px solid rgba(244, 162, 89, 0.2) !important; /* 更改为半透明金黄色边框 */
  color: #593618 !important; /* 更改为深棕色 */
}

/* 上传组件样式 */
:deep(.el-upload-dragger) {
  background-color: rgba(61, 45, 78, 0.4) !important; /* 更改为半透明紫色 */
  border: 1px dashed rgba(255, 158, 94, 0.3) !important; /* 更改为半透明橙色边框 */
}

.light-mode :deep(.el-upload-dragger) {
  background-color: rgba(255, 249, 240, 0.5) !important; /* 更改为半透明米色 */
  border: 1px dashed rgba(244, 162, 89, 0.3) !important; /* 更改为半透明金黄色边框 */
}

:deep(.el-upload-dragger:hover) {
  border-color: #ff9e5e !important; /* 更改为橙色 */
}

.light-mode :deep(.el-upload-dragger:hover) {
  border-color: #f4a259 !important; /* 更改为金黄色 */
}

:deep(.el-upload__tip) {
  color: #8a94b8 !important;
}

.light-mode :deep(.el-upload__tip) {
  color: #6c7eb9 !important;
}

/* 选择框和下拉菜单 */
:deep(.el-select__popper.el-popper) {
  background-color: #3d2d4e !important; /* 更改为深紫色 */
  border: 1px solid rgba(255, 158, 94, 0.2) !important; /* 更改为半透明橙色边框 */
}

.light-mode :deep(.el-select__popper.el-popper) {
  background-color: #ffffff !important;
  border: 1px solid rgba(244, 162, 89, 0.2) !important; /* 更改为半透明金黄色边框 */
}

:deep(.el-select-dropdown__item) {
  color: #e6ecf5 !important;
}

:deep(.el-select-dropdown__item:hover) {
  background-color: rgba(255, 158, 94, 0.1) !important; /* 更改为半透明橙色 */
}

.light-mode :deep(.el-select-dropdown__item) {
  color: #593618 !important; /* 更改为深棕色 */
}

.light-mode :deep(.el-select-dropdown__item:hover) {
  background-color: rgba(244, 162, 89, 0.1) !important; /* 更改为半透明金黄色 */
}

:deep(.el-select-dropdown__item.selected) {
  color: #ff9e5e !important; /* 更改为橙色 */
  background-color: rgba(255, 158, 94, 0.1) !important; /* 更改为半透明橙色 */
}

.light-mode :deep(.el-select-dropdown__item.selected) {
  color: #d86500 !important; /* 更改为深橙色 */
  background-color: rgba(244, 162, 89, 0.1) !important; /* 更改为半透明金黄色 */
}

/* 对话框样式 */
:deep(.el-dialog) {
  background-color: #3d2d4e !important; /* 更改为深紫色 */
  border: 1px solid rgba(255, 158, 94, 0.1) !important; /* 更改为半透明橙色边框 */
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3) !important;
}

.light-mode :deep(.el-dialog) {
  background-color: #ffffff !important;
  border: 1px solid rgba(244, 162, 89, 0.1) !important; /* 更改为半透明金黄色边框 */
  box-shadow: 0 10px 30px rgba(244, 162, 89, 0.08) !important; /* 更改为金黄色阴影 */
}

:deep(.el-dialog__header) {
  border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
}

.light-mode :deep(.el-dialog__header) {
  border-bottom: 1px solid rgba(0, 0, 0, 0.05) !important;
}

:deep(.el-dialog__title) {
  color: #ff9e5e !important; /* 更改为橙色 */
}

.light-mode :deep(.el-dialog__title) {
  color: #d86500 !important; /* 更改为深橙色 */
}

:deep(.el-dialog__close) {
  color: #e6ecf5 !important;
}

.light-mode :deep(.el-dialog__close) {
  color: #1a2980 !important;
}

/* 按钮样式覆盖 */
:deep(.el-button--primary) {
  background: linear-gradient(135deg, #ff9e5e, #f4a259) !important; /* 更改为橙金色渐变 */
  color: #ffffff !important; /* 白色文字更可读 */
  border: none !important;
}

:deep(.el-button--success) {
  background: rgba(52, 211, 153, 0.15) !important;
  border: 1px solid rgba(52, 211, 153, 0.3) !important;
  color: #34d399 !important;
}

:deep(.el-button--danger) {
  background: rgba(244, 67, 54, 0.15) !important;
  border: 1px solid rgba(244, 67, 54, 0.3) !important;
  color: #f44336 !important;
}

/* 标签样式 */
:deep(.el-tag) {
  background-color: rgba(61, 45, 78, 0.4) !important; /* 更改为半透明紫色 */
  border-color: rgba(255, 158, 94, 0.2) !important; /* 更改为半透明橙色边框 */
}

.light-mode :deep(.el-tag) {
  background-color: rgba(255, 249, 240, 0.5) !important; /* 更改为半透明米色 */
  border-color: rgba(244, 162, 89, 0.2) !important; /* 更改为半透明金黄色边框 */
}

:deep(.el-tag--danger) {
  background-color: rgba(244, 67, 54, 0.15) !important;
  border-color: rgba(244, 67, 54, 0.3) !important;
  color: #ff8080 !important;
}

.light-mode :deep(.el-tag--danger) {
  color: #f44336 !important;
}

:deep(.el-tag--warning) {
  background-color: rgba(255, 152, 0, 0.15) !important;
  border-color: rgba(255, 152, 0, 0.3) !important;
  color: #ffb74d !important;
}

.light-mode :deep(.el-tag--warning) {
  color: #ff9800 !important;
}

:deep(.el-tag--success) {
  background-color: rgba(52, 211, 153, 0.15) !important;
  border-color: rgba(52, 211, 153, 0.3) !important;
  color: #34d399 !important;
}

/* 空状态样式 */
:deep(.el-empty__description) {
  color: #8a94b8 !important;
}

.light-mode :deep(.el-empty__description) {
  color: #4b6cb7 !important;
}

:deep(.el-empty__image) {
  opacity: 0.5;
}

/* 全局覆盖所有Element Plus组件背景色 */
:deep(.el-select__wrapper),
:deep(.el-select__wrapper.el-tooltip__trigger),
:deep(.el-input__wrapper),
:deep(.el-textarea__wrapper),
:deep(.el-date-editor .el-input__wrapper) {
  background-color: rgba(61, 45, 78, 0.4) !important; /* 更改为半透明紫色 */
  border: 1px solid rgba(255, 158, 94, 0.2) !important; /* 更改为半透明橙色边框 */
  box-shadow: none !important;
  color: #e6ecf5 !important;
  transition: all 0.3s;
}

.light-mode :deep(.el-select__wrapper),
.light-mode :deep(.el-select__wrapper.el-tooltip__trigger),
.light-mode :deep(.el-input__wrapper),
.light-mode :deep(.el-textarea__wrapper),
.light-mode :deep(.el-date-editor .el-input__wrapper) {
  background-color: rgba(255, 249, 240, 0.5) !important; /* 更改为半透明米色 */
  border: 1px solid rgba(244, 162, 89, 0.2) !important; /* 更改为半透明金黄色边框 */
  color: #593618 !important; /* 深棕色文字 */
}

/* 强制覆盖所有Element Plus文本颜色 */
:deep(.el-input__inner),
:deep(.el-textarea__inner),
:deep(.el-select-dropdown__item) {
  color: #e6ecf5 !important;
}

.light-mode :deep(.el-input__inner),
.light-mode :deep(.el-textarea__inner),
.light-mode :deep(.el-select-dropdown__item) {
  color: #1a2980 !important;
}
</style>