<template>
  <div class="dashboard-container">
    <!-- DataV背景装饰 -->
    <dv-loading v-if="loading">Loading...</dv-loading>
    <dv-decoration-9 class="bg-decoration-left" />
    <dv-decoration-9 class="bg-decoration-right" />
    
    <!-- 标题区域 -->
    <div class="dashboard-header">
      <dv-decoration-3 style="width:160px;height:20px;" />
      <div class="time-display">
        <dv-decoration-10 style="width:100px;height:20px;" />
        <span>{{ currentTime }}</span>
      </div>
    </div>
    
    <!-- 内容区域 -->
    <div class="dashboard-content">
      <!-- 左侧区域 -->
      <div class="left-panel">
        <!-- 班级学习情况 -->
        <div class="panel-item learning-situation">
          <dv-border-box-12 class="panel-border">
            <div class="panel-header">
              <span class="panel-title">
                <dv-decoration-4 style="width:16px;height:16px;position:relative;top:3px;margin-right:4px;" />
                班级近期学习情况
              </span>
              <div class="panel-controls">
                <select v-model="learningSubject" class="tech-select">
                  <option value="" disabled selected>选择学科</option>
                  <option v-for="item in subjects" :key="item.value" :value="item.value">{{ item.label }}</option>
                </select>
              </div>
            </div>
            <div class="panel-body">
              <div class="chart-group">
                <div ref="scoreDistributionChart" class="chart-item"></div>
                <div ref="scoreChangeChart" class="chart-item"></div>
              </div>
            </div>
          </dv-border-box-12>
        </div>
        
        <!-- 学科知识图谱 -->
        <div class="panel-item knowledge-graph">
          <dv-border-box-12 class="panel-border">
            <div class="panel-header">
              <span class="panel-title">
                <dv-decoration-4 style="width:16px;height:16px;position:relative;top:3px;margin-right:4px;" />
                学科知识图谱
              </span>
              <div class="panel-controls">
                <select v-model="selectedSubject" class="tech-select">
                  <option value="" disabled selected>选择学科</option>
                  <option v-for="item in subjects" :key="item.value" :value="item.value">{{ item.label }}</option>
                </select>
                <select v-model="selectedGrade" class="tech-select">
                  <option value="" disabled selected>选择年级</option>
                  <option v-for="item in grades" :key="item.value" :value="item.value">{{ item.label }}</option>
                </select>
              </div>
            </div>
            <div class="panel-body">
              <div ref="knowledgeGraphChart" class="chart-container"></div>
            </div>
          </dv-border-box-12>
        </div>
      </div>
      
      <!-- 中间区域 -->
      <div class="middle-panel">
        <!-- 学生信息轮播表 -->
        <div class="panel-item student-carousel">
          <dv-border-box-8 class="panel-border" :reverse="true">
            <div class="panel-header">
              <span class="panel-title">
                <dv-decoration-4 style="width:16px;height:16px;position:relative;top:3px;margin-right:4px;" />
                学生信息动态
              </span>
              <dv-decoration-5 style="width:80px;height:25px;" />
            </div>
            <div class="panel-body">
              <el-carousel height="220px" indicator-position="none" :interval="5000" arrow="always">
                <el-carousel-item v-for="(group, index) in studentGroups" :key="index">
                  <div class="tech-table-container">
                    <div class="tech-table-header">
                      <div class="tech-th" style="width: 80px">学生姓名</div>
                      <div class="tech-th">薄弱知识点</div>
                      <div class="tech-th" style="width: 150px">学习建议</div>
                    </div>
                    <div class="tech-table-body">
                      <div v-for="(student, i) in group" :key="i" class="tech-table-row">
                        <div class="tech-td" style="width: 80px">{{ student.name }}</div>
                        <div class="tech-td">{{ student.weakPoints }}</div>
                        <div class="tech-td" style="width: 150px">{{ student.suggestion }}</div>
                      </div>
                    </div>
                  </div>
                </el-carousel-item>
              </el-carousel>
            </div>
          </dv-border-box-8>
        </div>
        
        <!-- 热门资源推荐 -->
        <div class="panel-item resource-recommendation">
          <dv-border-box-8 class="panel-border">
            <div class="panel-header">
              <span class="panel-title">
                <dv-decoration-4 style="width:16px;height:16px;position:relative;top:3px;margin-right:4px;" />
                热门资源推荐
              </span>
              <dv-decoration-5 style="width:80px;height:25px;" />
            </div>
            <div class="panel-body">
              <div class="resource-tabs">
                <el-tabs v-model="activeResourceTab">
                  <el-tab-pane label="热门习题" name="exercises">
                    <div class="resource-list">
                      <div v-for="(item, index) in recommendedExercises" :key="index" class="resource-item" :class="{'featured': item.featured}">
                        <div class="resource-title">{{ item.title }}</div>
                        <div class="resource-desc">{{ item.description }}</div>
                        <div class="resource-meta">使用次数：{{ item.usageCount }}</div>
                      </div>
                    </div>
                  </el-tab-pane>
                  <el-tab-pane label="热门视频" name="videos">
                    <div class="resource-list">
                      <div v-for="(item, index) in recommendedVideos" :key="index" class="resource-item">
                        <div class="resource-title">{{ item.title }}</div>
                        <div class="resource-desc">{{ item.description }}</div>
                        <div class="resource-meta">观看次数：{{ item.viewCount }}</div>
                      </div>
                    </div>
                  </el-tab-pane>
                  <el-tab-pane label="推荐书籍" name="books">
                    <div class="resource-list">
                      <div v-for="(item, index) in recommendedBooks" :key="index" class="resource-item">
                        <div class="resource-title">{{ item.title }}</div>
                        <div class="resource-desc">{{ item.author }}</div>
                        <div class="resource-meta">推荐指数：{{ item.rating }}/5</div>
                      </div>
                    </div>
                  </el-tab-pane>
                </el-tabs>
              </div>
            </div>
          </dv-border-box-8>
        </div>
      </div>
      
      <!-- 右侧区域 -->
      <div class="right-panel">
        <!-- 班级预备知识雷达图 -->
        <div class="panel-item radar-chart">
          <dv-border-box-13 class="panel-border">
            <div class="panel-header">
              <span class="panel-title">
                <dv-decoration-4 style="width:16px;height:16px;position:relative;top:3px;margin-right:4px;" />
                班级预备知识掌握度
              </span>
              <div class="panel-controls">
                <select v-model="selectedKnowledgePoint" class="tech-select">
                  <option value="" disabled selected>选择知识点</option>
                  <option v-for="item in knowledgePoints" :key="item.value" :value="item.value">{{ item.label }}</option>
                </select>
              </div>
            </div>
            <div class="panel-body">
              <div ref="radarChart" class="chart-container"></div>
            </div>
          </dv-border-box-13>
        </div>
        
        <!-- 数据卡片 -->
        <div class="panel-item data-cards">
          <dv-border-box-13 class="panel-border">
            <div class="panel-header">
              <span class="panel-title">
                <dv-decoration-4 style="width:16px;height:16px;position:relative;top:3px;margin-right:4px;" />
                班级成绩统计
              </span>
              <div class="panel-controls">
                <select v-model="selectedStatsSubject" class="tech-select">
                  <option value="" disabled selected>选择学科</option>
                  <option v-for="item in subjects" :key="item.value" :value="item.value">{{ item.label }}</option>
                </select>
              </div>
            </div>
            <div class="card-grid">
              <div class="data-card">
                <dv-decoration-12 style="width:40px;height:40px;" />
                <div class="card-title">班级总人数</div>
                <dv-digital-flop :config="{ number: [classStats.totalStudents], toFixed: 0, textStyle: { fill: '#ffffff', fontSize: 28, fontWeight: 'bold' } }" style="width:120px;height:45px;" />
              </div>
              <div class="data-card">
                <dv-decoration-12 style="width:40px;height:40px;transform:rotate(90deg);" />
                <div class="card-title">班级平均分</div>
                <dv-digital-flop :config="{ number: [currentSubjectStats.averageScore], toFixed: 1, textStyle: { fill: '#ffffff', fontSize: 28, fontWeight: 'bold' } }" style="width:120px;height:45px;" />
              </div>
              <div class="data-card">
                <dv-decoration-12 style="width:40px;height:40px;transform:rotate(180deg);" />
                <div class="card-title">优秀率</div>
                <dv-digital-flop :config="{ number: [currentSubjectStats.excellentRate], toFixed: 1, suffix: '%', textStyle: { fill: '#ffffff', fontSize: 28, fontWeight: 'bold' } }" style="width:120px;height:45px;" />
              </div>
              <div class="data-card">
                <dv-decoration-12 style="width:40px;height:40px;transform:rotate(270deg);" />
                <div class="card-title">及格率</div>
                <dv-digital-flop :config="{ number: [currentSubjectStats.passRate], toFixed: 1, suffix: '%', textStyle: { fill: '#ffffff', fontSize: 28, fontWeight: 'bold' } }" style="width:120px;height:45px;" />
              </div>
            </div>
          </dv-border-box-13>
        </div>
      </div>
    </div>
    
    <!-- 底部装饰 -->
    <div class="dashboard-footer">
      <dv-decoration-11 style="width:100%;height:25px;" />
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import { ref, onMounted, watch, reactive, computed } from 'vue'

export default {
  name: 'TeacherDashboard',
  
  setup() {
    // 加载状态
    const loading = ref(true)
    setTimeout(() => {
      loading.value = false
    }, 1000)
    
    // 当前时间显示
    const currentTime = ref(formatDateTime(new Date()))
    setInterval(() => {
      currentTime.value = formatDateTime(new Date())
    }, 1000)
    
    // 学科与年级选择
    const selectedSubject = ref('math')
    const selectedGrade = ref('grade7')
    const learningSubject = ref('math')
    const selectedKnowledgePoint = ref('function')
    const selectedStatsSubject = ref('math')
    
    // 科目列表
    const subjects = [
      { label: '数学', value: 'math' },
      { label: '语文', value: 'chinese' },
      { label: '英语', value: 'english' },
      { label: '物理', value: 'physics' },
      { label: '化学', value: 'chemistry' }
    ]
    
    // 年级列表
    const grades = [
      { label: '七年级', value: 'grade7' },
      { label: '八年级', value: 'grade8' },
      { label: '九年级', value: 'grade9' }
    ]
    
    // 知识点列表
    const knowledgePoints = [
      { label: '函数', value: 'function' },
      { label: '几何', value: 'geometry' },
      { label: '代数', value: 'algebra' },
      { label: '概率统计', value: 'statistics' }
    ]
    
    // 图表引用
    const knowledgeGraphChart = ref(null)
    const radarChart = ref(null)
    const scoreDistributionChart = ref(null)
    const scoreChangeChart = ref(null)
    
    // 资源推荐相关
    const activeResourceTab = ref('exercises')
    const recommendedExercises = [
      { title: '二次函数图像分析', description: '通过图像理解二次函数性质', usageCount: 245, featured: true },
      { title: '解析几何综合练习', description: '圆与直线的位置关系', usageCount: 198 },
      { title: '概率计算专项训练', description: '古典概型与几何概型结合', usageCount: 167 }
    ]
    const recommendedVideos = [
      { title: '三角函数教学视频', description: '详解三角函数的基本性质', viewCount: 3120 },
      { title: '空间几何体体积计算', description: '空间几何体的体积与表面积', viewCount: 2834 },
      { title: '方程组解法大全', description: '线性方程组的多种解法', viewCount: 2541 }
    ]
    const recommendedBooks = [
      { title: '中学数学思维训练', author: '张三', rating: 4.8 },
      { title: '几何证明方法精讲', author: '李四', rating: 4.6 },
      { title: '数学竞赛题解分析', author: '王五', rating: 4.5 }
    ]
    
    // 班级统计数据
    const classStats = reactive({
      totalStudents: 45,
      subjectStats: {
        math: {
          averageScore: 82.5,
          excellentRate: 35.6,
          passRate: 89.2
        },
        chinese: {
          averageScore: 85.3,
          excellentRate: 42.2,
          passRate: 92.5
        },
        english: {
          averageScore: 78.9,
          excellentRate: 28.9,
          passRate: 85.3
        },
        physics: {
          averageScore: 76.5,
          excellentRate: 25.3,
          passRate: 82.7
        },
        chemistry: {
          averageScore: 79.8,
          excellentRate: 31.1,
          passRate: 86.4
        }
      }
    })
    
    // 计算当前选中学科的统计数据
    const currentSubjectStats = computed(() => {
      return classStats.subjectStats[selectedStatsSubject.value] || {
        averageScore: 0,
        excellentRate: 0,
        passRate: 0
      }
    })
    
    // 学生信息
    const studentList = [
      { name: '张三', weakPoints: '三角函数、空间向量', suggestion: '加强函数概念理解' },
      { name: '李四', weakPoints: '立体几何、解析几何', suggestion: '多做空间想象练习' },
      { name: '王五', weakPoints: '概率统计、导数应用', suggestion: '注重公式理解' },
      { name: '赵六', weakPoints: '数列、立体几何', suggestion: '强化空间想象能力' },
      { name: '钱七', weakPoints: '函数、方程', suggestion: '多做函数图像练习' },
      { name: '孙八', weakPoints: '概率、统计', suggestion: '理解概率基本概念' },
      { name: '周九', weakPoints: '三角函数、数列', suggestion: '加强公式记忆与理解' },
      { name: '吴十', weakPoints: '解析几何、立体几何', suggestion: '提高空间思维能力' },
      { name: '郑十一', weakPoints: '概率统计、导数', suggestion: '加强应用题训练' },
      { name: '王十二', weakPoints: '不等式、三角函数', suggestion: '注重基础知识巩固' }
    ]
    
    // 分组学生信息用于轮播
    const studentGroups = computed(() => {
      const groups = []
      const size = 4
      for (let i = 0; i < studentList.length; i += size) {
        groups.push(studentList.slice(i, i + size))
      }
      return groups
    })
    
    // 初始化雷达图
    const initRadarChart = () => {
      if (!radarChart.value) return
      
      const chartInstance = echarts.init(radarChart.value, null, {
        renderer: 'canvas',
        useDirtyRect: true,
        devicePixelRatio: window.devicePixelRatio
      })
      
      const option = {
        backgroundColor: 'transparent',
        title: {
          text: '函数知识点掌握雷达图',
          left: 'center',
          textStyle: {
            color: '#7feaff',
            fontSize: 13,
            fontWeight: 'normal',
            textShadow: '0 0 5px rgba(126, 234, 255, 0.5)'
          }
        },
        tooltip: {
          trigger: 'item',
          backgroundColor: 'rgba(11, 27, 103, 0.8)',
          borderColor: 'rgba(126, 234, 255, 0.3)',
          textStyle: {
            color: '#fff'
          },
          extraCssText: 'box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);'
        },
        legend: {
          data: ['当前掌握度', '上周掌握度'],
          bottom: '3%',
          textStyle: {
            color: '#a3aed0',
            fontSize: 11
          },
          itemWidth: 12,
          itemHeight: 12,
          itemStyle: {
            borderWidth: 0
          },
          textGap: 8
        },
        radar: {
          indicator: [
            { name: '函数定义', max: 100 },
            { name: '函数图像', max: 100 },
            { name: '函数性质', max: 100 },
            { name: '函数应用', max: 100 },
            { name: '函数变换', max: 100 }
          ],
          radius: '55%',
          center: ['50%', '45%'],
          axisName: {
            color: '#7feaff',
            fontSize: 11,
            fontWeight: 'normal',
            backgroundColor: 'rgba(11, 27, 103, 0.5)',
            padding: [3, 6],
            borderRadius: 3,
            textShadow: '0 0 3px rgba(126, 234, 255, 0.3)'
          },
          axisLine: {
            lineStyle: {
              color: 'rgba(126, 234, 255, 0.3)'
            }
          },
          splitArea: {
            areaStyle: {
              color: ['rgba(46, 78, 229, 0.05)', 'rgba(46, 78, 229, 0.1)', 'rgba(46, 78, 229, 0.15)', 'rgba(46, 78, 229, 0.2)']
            }
          },
          splitLine: {
            lineStyle: {
              color: 'rgba(126, 234, 255, 0.2)',
              width: 1
            }
          }
        },
        series: [
          {
            name: '掌握度对比',
            type: 'radar',
            data: [
              {
                value: [85, 78, 80, 72, 68],
                name: '当前掌握度',
                areaStyle: {
                  color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    { offset: 0, color: 'rgba(0, 242, 254, 0.8)' },
                    { offset: 1, color: 'rgba(0, 112, 192, 0.2)' }
                  ]),
                  shadowColor: 'rgba(0, 242, 254, 0.5)',
                  shadowBlur: 10
                },
                lineStyle: {
                  width: 2.5,
                  color: '#00f2fe',
                  shadowColor: 'rgba(0, 242, 254, 0.7)',
                  shadowBlur: 5
                },
                itemStyle: {
                  color: '#00f2fe',
                  borderColor: '#ffffff',
                  borderWidth: 2,
                  shadowColor: 'rgba(0, 242, 254, 0.7)',
                  shadowBlur: 5
                },
                symbol: 'circle',
                symbolSize: 6
              },
              {
                value: [75, 65, 70, 60, 55],
                name: '上周掌握度',
                areaStyle: {
                  color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    { offset: 0, color: 'rgba(255, 177, 0, 0.8)' },
                    { offset: 1, color: 'rgba(255, 153, 0, 0.2)' }
                  ]),
                  shadowColor: 'rgba(255, 177, 0, 0.5)',
                  shadowBlur: 10
                },
                lineStyle: {
                  width: 2.5,
                  color: '#ffb100',
                  shadowColor: 'rgba(255, 177, 0, 0.7)',
                  shadowBlur: 5
                },
                itemStyle: {
                  color: '#ffb100',
                  borderColor: '#ffffff',
                  borderWidth: 2,
                  shadowColor: 'rgba(255, 177, 0, 0.7)',
                  shadowBlur: 5
                },
                symbol: 'circle',
                symbolSize: 6
              }
            ]
          }
        ],
        animation: true,
        animationDuration: 1500,
        animationEasing: 'cubicOut'
      }
      
      chartInstance.setOption(option)
      
      const resizeObserver = new ResizeObserver(() => {
        chartInstance.resize();
      });
      resizeObserver.observe(radarChart.value);
      
      window.addEventListener('resize', () => {
        chartInstance.resize()
      })
    }
    
    // 初始化知识图谱
    const initKnowledgeGraph = () => {
      if (!knowledgeGraphChart.value) return
      
      const chartInstance = echarts.init(knowledgeGraphChart.value, null, {
        renderer: 'canvas',
        useDirtyRect: true,
        devicePixelRatio: window.devicePixelRatio
      })
      
      // 根据学科和年级获取对应的知识图谱数据
      const graphData = getKnowledgeGraphData(selectedSubject.value, selectedGrade.value)
      
      const option = {
        backgroundColor: 'transparent',
        title: {
          text: `${getSubjectName(selectedSubject.value)}知识图谱`,
          subtext: getGradeName(selectedGrade.value),
          left: 'center',
          textStyle: {
            color: '#7feaff',
            fontSize: 12
          },
          subtextStyle: {
            color: '#a3aed0',
            fontSize: 10
          }
        },
        tooltip: {
          formatter: '{b}'
        },
        animationDurationUpdate: 1500,
        animationEasingUpdate: 'quinticInOut',
        series: [
          {
            type: 'graph',
            layout: 'force',
            force: {
              repulsion: 100,
              edgeLength: 50,
              layoutAnimation: true,
              gravity: 0.1
            },
            roam: true,
            draggable: true,
            label: {
              show: true,
              color: '#fff',
              fontSize: 12
            },
            data: graphData.nodes.map(node => ({
              ...node,
              itemStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 1, 1, [
                  { offset: 0, color: node.category === 0 ? '#7feaff' : node.category === 1 ? '#4facfe' : node.category === 2 ? '#0a4dd3' : '#2b68ec' },
                  { offset: 1, color: node.category === 0 ? '#2e4ee5' : node.category === 1 ? '#00f2fe' : node.category === 2 ? '#3458de' : '#1e40af' }
                ])
              }
            })),
            links: graphData.links.map(link => ({
              ...link,
              lineStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                  { offset: 0, color: 'rgba(127, 234, 255, 0.7)' },
                  { offset: 1, color: 'rgba(46, 78, 229, 0.7)' }
                ]),
                width: 1.5,
                curveness: 0.3
              }
            })),
            categories: [
              { name: '学科' },
              { name: '一级知识点' },
              { name: '二级知识点' },
              { name: '三级知识点' }
            ],
            emphasis: {
              focus: 'adjacency',
              lineStyle: {
                width: 5,
                color: '#7feaff'
              },
              itemStyle: {
                borderColor: '#fff',
                borderWidth: 2,
                shadowBlur: 10,
                shadowColor: 'rgba(127, 234, 255, 0.5)'
              }
            }
          }
        ]
      }
      
      chartInstance.setOption(option)
      
      const resizeObserver = new ResizeObserver(() => {
        chartInstance.resize();
      });
      resizeObserver.observe(knowledgeGraphChart.value);
      
      window.addEventListener('resize', () => {
        chartInstance.resize()
      })
    }
    
    // 获取学科名称
    const getSubjectName = (value) => {
      const subject = subjects.find(item => item.value === value)
      return subject ? subject.label : '数学'
    }
    
    // 获取年级名称
    const getGradeName = (value) => {
      const grade = grades.find(item => item.value === value)
      return grade ? grade.label : '七年级'
    }
    
    // 获取知识图谱数据
    const getKnowledgeGraphData = (subject, grade) => {
      // 默认返回数学的知识图谱
      if (subject === 'math') {
        return {
          nodes: [
            { name: '数学', symbolSize: 60, category: 0 },
            { name: '代数', symbolSize: 50, category: 1 },
            { name: '几何', symbolSize: 50, category: 1 },
            { name: '统计', symbolSize: 40, category: 1 },
            { name: '方程', symbolSize: 35, category: 2 },
            { name: '函数', symbolSize: 35, category: 2 },
            { name: '不等式', symbolSize: 30, category: 2 },
            { name: '平面图形', symbolSize: 30, category: 2 },
            { name: '立体图形', symbolSize: 25, category: 2 },
            { name: '坐标系', symbolSize: 25, category: 2 },
            { name: '概率', symbolSize: 25, category: 2 },
            { name: '数据分析', symbolSize: 25, category: 2 },
            { name: '一元一次方程', symbolSize: 20, category: 3 },
            { name: '二元一次方程组', symbolSize: 20, category: 3 },
            { name: '一次函数', symbolSize: 20, category: 3 },
            { name: '三角形', symbolSize: 20, category: 3 },
            { name: '四边形', symbolSize: 20, category: 3 },
            { name: '圆', symbolSize: 20, category: 3 }
          ],
          links: [
            { source: '数学', target: '代数' },
            { source: '数学', target: '几何' },
            { source: '数学', target: '统计' },
            { source: '代数', target: '方程' },
            { source: '代数', target: '函数' },
            { source: '代数', target: '不等式' },
            { source: '几何', target: '平面图形' },
            { source: '几何', target: '立体图形' },
            { source: '几何', target: '坐标系' },
            { source: '统计', target: '概率' },
            { source: '统计', target: '数据分析' },
            { source: '方程', target: '一元一次方程' },
            { source: '方程', target: '二元一次方程组' },
            { source: '函数', target: '一次函数' },
            { source: '平面图形', target: '三角形' },
            { source: '平面图形', target: '四边形' },
            { source: '平面图形', target: '圆' }
          ]
        }
      } else if (subject === 'chinese') {
        return {
          nodes: [
            { name: '语文', symbolSize: 60, category: 0 },
            { name: '文学常识', symbolSize: 50, category: 1 },
            { name: '阅读理解', symbolSize: 50, category: 1 },
            { name: '写作', symbolSize: 50, category: 1 },
            { name: '古代文学', symbolSize: 35, category: 2 },
            { name: '现代文学', symbolSize: 35, category: 2 },
            { name: '文言文', symbolSize: 35, category: 2 },
            { name: '散文阅读', symbolSize: 30, category: 2 },
            { name: '小说阅读', symbolSize: 30, category: 2 },
            { name: '议论文写作', symbolSize: 30, category: 2 },
            { name: '记叙文写作', symbolSize: 30, category: 2 },
            { name: '唐诗', symbolSize: 20, category: 3 },
            { name: '宋词', symbolSize: 20, category: 3 },
            { name: '元曲', symbolSize: 20, category: 3 },
            { name: '文言实词', symbolSize: 20, category: 3 },
            { name: '文言虚词', symbolSize: 20, category: 3 },
            { name: '现代散文', symbolSize: 20, category: 3 },
            { name: '现代小说', symbolSize: 20, category: 3 }
          ],
          links: [
            { source: '语文', target: '文学常识' },
            { source: '语文', target: '阅读理解' },
            { source: '语文', target: '写作' },
            { source: '文学常识', target: '古代文学' },
            { source: '文学常识', target: '现代文学' },
            { source: '阅读理解', target: '文言文' },
            { source: '阅读理解', target: '散文阅读' },
            { source: '阅读理解', target: '小说阅读' },
            { source: '写作', target: '议论文写作' },
            { source: '写作', target: '记叙文写作' },
            { source: '古代文学', target: '唐诗' },
            { source: '古代文学', target: '宋词' },
            { source: '古代文学', target: '元曲' },
            { source: '文言文', target: '文言实词' },
            { source: '文言文', target: '文言虚词' },
            { source: '现代文学', target: '现代散文' },
            { source: '现代文学', target: '现代小说' }
          ]
        }
      } else if (subject === 'english') {
        return {
          nodes: [
            { name: '英语', symbolSize: 60, category: 0 },
            { name: '语法', symbolSize: 50, category: 1 },
            { name: '词汇', symbolSize: 50, category: 1 },
            { name: '阅读', symbolSize: 50, category: 1 },
            { name: '写作', symbolSize: 50, category: 1 },
            { name: '时态', symbolSize: 35, category: 2 },
            { name: '句型', symbolSize: 35, category: 2 },
            { name: '词性', symbolSize: 35, category: 2 },
            { name: '常用词汇', symbolSize: 30, category: 2 },
            { name: '短语动词', symbolSize: 30, category: 2 },
            { name: '书面表达', symbolSize: 30, category: 2 },
            { name: '阅读理解', symbolSize: 30, category: 2 },
            { name: '现在时', symbolSize: 20, category: 3 },
            { name: '过去时', symbolSize: 20, category: 3 },
            { name: '将来时', symbolSize: 20, category: 3 },
            { name: '名词', symbolSize: 20, category: 3 },
            { name: '动词', symbolSize: 20, category: 3 },
            { name: '形容词', symbolSize: 20, category: 3 }
          ],
          links: [
            { source: '英语', target: '语法' },
            { source: '英语', target: '词汇' },
            { source: '英语', target: '阅读' },
            { source: '英语', target: '写作' },
            { source: '语法', target: '时态' },
            { source: '语法', target: '句型' },
            { source: '语法', target: '词性' },
            { source: '词汇', target: '常用词汇' },
            { source: '词汇', target: '短语动词' },
            { source: '写作', target: '书面表达' },
            { source: '阅读', target: '阅读理解' },
            { source: '时态', target: '现在时' },
            { source: '时态', target: '过去时' },
            { source: '时态', target: '将来时' },
            { source: '词性', target: '名词' },
            { source: '词性', target: '动词' },
            { source: '词性', target: '形容词' }
          ]
        }
      } else if (subject === 'physics') {
        return {
          nodes: [
            { name: '物理', symbolSize: 60, category: 0 },
            { name: '力学', symbolSize: 50, category: 1 },
            { name: '电学', symbolSize: 50, category: 1 },
            { name: '热学', symbolSize: 50, category: 1 },
            { name: '力和运动', symbolSize: 35, category: 2 },
            { name: '牛顿定律', symbolSize: 35, category: 2 },
            { name: '电路', symbolSize: 35, category: 2 },
            { name: '磁场', symbolSize: 30, category: 2 },
            { name: '热量', symbolSize: 30, category: 2 },
            { name: '压强', symbolSize: 30, category: 2 },
            { name: '功和能', symbolSize: 30, category: 2 },
            { name: '匀速运动', symbolSize: 20, category: 3 },
            { name: '变速运动', symbolSize: 20, category: 3 },
            { name: '自由落体', symbolSize: 20, category: 3 },
            { name: '欧姆定律', symbolSize: 20, category: 3 },
            { name: '焦耳定律', symbolSize: 20, category: 3 },
            { name: '比热容', symbolSize: 20, category: 3 },
            { name: '热传递', symbolSize: 20, category: 3 }
          ],
          links: [
            { source: '物理', target: '力学' },
            { source: '物理', target: '电学' },
            { source: '物理', target: '热学' },
            { source: '力学', target: '力和运动' },
            { source: '力学', target: '牛顿定律' },
            { source: '力学', target: '功和能' },
            { source: '力学', target: '压强' },
            { source: '电学', target: '电路' },
            { source: '电学', target: '磁场' },
            { source: '热学', target: '热量' },
            { source: '力和运动', target: '匀速运动' },
            { source: '力和运动', target: '变速运动' },
            { source: '力和运动', target: '自由落体' },
            { source: '电路', target: '欧姆定律' },
            { source: '电路', target: '焦耳定律' },
            { source: '热量', target: '比热容' },
            { source: '热量', target: '热传递' }
          ]
        }
      } else {
        // 默认返回化学的知识图谱
        return {
          nodes: [
            { name: '化学', symbolSize: 60, category: 0 },
            { name: '物质结构', symbolSize: 50, category: 1 },
            { name: '化学反应', symbolSize: 50, category: 1 },
            { name: '元素化合物', symbolSize: 50, category: 1 },
            { name: '原子结构', symbolSize: 35, category: 2 },
            { name: '分子结构', symbolSize: 35, category: 2 },
            { name: '氧化还原', symbolSize: 35, category: 2 },
            { name: '酸碱反应', symbolSize: 30, category: 2 },
            { name: '金属元素', symbolSize: 30, category: 2 },
            { name: '非金属元素', symbolSize: 30, category: 2 },
            { name: '有机化学', symbolSize: 30, category: 2 },
            { name: '电子排布', symbolSize: 20, category: 3 },
            { name: '化学键', symbolSize: 20, category: 3 },
            { name: '氧化数', symbolSize: 20, category: 3 },
            { name: '电解质', symbolSize: 20, category: 3 },
            { name: '碱金属', symbolSize: 20, category: 3 },
            { name: '卤族元素', symbolSize: 20, category: 3 },
            { name: '烃类', symbolSize: 20, category: 3 }
          ],
          links: [
            { source: '化学', target: '物质结构' },
            { source: '化学', target: '化学反应' },
            { source: '化学', target: '元素化合物' },
            { source: '物质结构', target: '原子结构' },
            { source: '物质结构', target: '分子结构' },
            { source: '化学反应', target: '氧化还原' },
            { source: '化学反应', target: '酸碱反应' },
            { source: '元素化合物', target: '金属元素' },
            { source: '元素化合物', target: '非金属元素' },
            { source: '元素化合物', target: '有机化学' },
            { source: '原子结构', target: '电子排布' },
            { source: '分子结构', target: '化学键' },
            { source: '氧化还原', target: '氧化数' },
            { source: '酸碱反应', target: '电解质' },
            { source: '金属元素', target: '碱金属' },
            { source: '非金属元素', target: '卤族元素' },
            { source: '有机化学', target: '烃类' }
          ]
        }
      }
    }
    
    // 初始化分数分布图
    const initScoreDistributionChart = () => {
      if (!scoreDistributionChart.value) return
      
      const chartInstance = echarts.init(scoreDistributionChart.value, null, {
        renderer: 'canvas',
        useDirtyRect: true,
        devicePixelRatio: window.devicePixelRatio
      })
      
      const option = {
        backgroundColor: 'transparent',
        title: {
          text: '班级分数段分布',
          left: 'center',
          textStyle: {
            color: '#7feaff',
            fontSize: 13,
            fontWeight: 'normal',
            textShadow: '0 0 5px rgba(126, 234, 255, 0.5)'
          }
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow',
            shadowStyle: {
              color: 'rgba(126, 234, 255, 0.1)'
            }
          },
          backgroundColor: 'rgba(11, 27, 103, 0.8)',
          borderColor: 'rgba(126, 234, 255, 0.3)',
          textStyle: {
            color: '#fff'
          },
          extraCssText: 'box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);'
        },
        grid: {
          left: '10%',
          right: '10%',
          bottom: '20%',
          top: '28%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: ['0-59', '60-69', '70-79', '80-89', '90-100'],
          axisLine: {
            lineStyle: {
              color: 'rgba(126, 234, 255, 0.3)',
              width: 2
            }
          },
          axisTick: {
            show: false
          },
          axisLabel: {
            color: '#a3aed0',
            fontSize: 11,
            interval: 0,
            rotate: 0,
            margin: 10
          }
        },
        yAxis: {
          type: 'value',
          name: '学生数',
          nameTextStyle: {
            color: '#a3aed0',
            fontSize: 11,
            padding: [0, 0, 0, 10]
          },
          axisLine: {
            show: true,
            lineStyle: {
              color: 'rgba(126, 234, 255, 0.3)',
              width: 2
            }
          },
          splitLine: {
            lineStyle: {
              color: 'rgba(126, 234, 255, 0.1)'
            }
          },
          axisLabel: {
            color: '#a3aed0',
            fontSize: 11,
            margin: 10
          }
        },
        series: [
          {
            name: '学生人数',
            type: 'bar',
            data: [5, 8, 12, 15, 5],
            itemStyle: {
              color: function(params) {
                const colorList = [
                  new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    { offset: 0, color: '#ff4b6b' },
                    { offset: 1, color: '#a52a33' }
                  ]),
                  new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    { offset: 0, color: '#ff8142' },
                    { offset: 1, color: '#c25e2f' }
                  ]),
                  new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    { offset: 0, color: '#5698fe' },
                    { offset: 1, color: '#4469db' }
                  ]),
                  new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    { offset: 0, color: '#4bf0ff' },
                    { offset: 1, color: '#00d8ff' }
                  ]),
                  new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    { offset: 0, color: '#4fc1ff' },
                    { offset: 1, color: '#0080ff' }
                  ])
                ];
                return colorList[params.dataIndex];
              },
              barBorderRadius: [6, 6, 0, 0],
              borderColor: 'rgba(255, 255, 255, 0.2)',
              borderWidth: 1,
              shadowColor: 'rgba(126, 234, 255, 0.3)',
              shadowBlur: 10
            },
            barWidth: '45%',
            emphasis: {
              itemStyle: {
                shadowBlur: 15,
                shadowColor: 'rgba(126, 234, 255, 0.7)'
              }
            },
            label: {
              show: true,
              position: 'top',
              color: '#ffffff',
              fontSize: 12,
              fontWeight: 'bold',
              formatter: '{c}人',
              textShadow: '0 0 3px rgba(0, 0, 0, 0.5)'
            },
            animation: true,
            animationDuration: 1500,
            animationEasing: 'elasticOut'
          }
        ]
      }
      
      chartInstance.setOption(option)
      
      const resizeObserver = new ResizeObserver(() => {
        chartInstance.resize();
      });
      resizeObserver.observe(scoreDistributionChart.value);
      
      window.addEventListener('resize', () => {
        chartInstance.resize()
      })
    }
    
    // 初始化成绩变化趋势图
    const initScoreChangeChart = () => {
      if (!scoreChangeChart.value) return
      
      const chartInstance = echarts.init(scoreChangeChart.value, null, {
        renderer: 'canvas',
        useDirtyRect: true,
        devicePixelRatio: window.devicePixelRatio
      })
      
      const option = {
        backgroundColor: 'transparent',
        title: {
          text: '班级整体成绩趋势',
          left: 'center',
          textStyle: {
            color: '#7feaff',
            fontSize: 13,
            fontWeight: 'normal',
            textShadow: '0 0 5px rgba(126, 234, 255, 0.5)'
          }
        },
        tooltip: {
          trigger: 'axis',
          backgroundColor: 'rgba(11, 27, 103, 0.8)',
          borderColor: 'rgba(126, 234, 255, 0.3)',
          textStyle: {
            color: '#fff'
          },
          extraCssText: 'box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);'
        },
        grid: {
          left: '10%',
          right: '10%',
          bottom: '20%',
          top: '28%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: ['第一周', '第二周', '第三周', '第四周', '第五周', '第六周'],
          axisLine: {
            lineStyle: {
              color: 'rgba(126, 234, 255, 0.3)',
              width: 2
            }
          },
          axisTick: {
            show: false
          },
          axisLabel: {
            color: '#a3aed0',
            fontSize: 11,
            interval: 0,
            rotate: 30,
            margin: 15
          }
        },
        yAxis: {
          type: 'value',
          name: '平均分',
          min: 60,
          max: 100,
          nameTextStyle: {
            color: '#a3aed0',
            fontSize: 11,
            padding: [0, 0, 0, 10]
          },
          axisLine: {
            show: true,
            lineStyle: {
              color: 'rgba(126, 234, 255, 0.3)',
              width: 2
            }
          },
          splitLine: {
            lineStyle: {
              color: 'rgba(126, 234, 255, 0.1)',
              type: 'dashed'
            }
          },
          axisLabel: {
            color: '#a3aed0',
            fontSize: 11,
            margin: 10
          }
        },
        series: [
          {
            name: '平均分',
            type: 'line',
            data: [75.2, 78.5, 77.8, 82.3, 83.5, 85.2],
            markPoint: {
              data: [
                { type: 'max', name: '最高', symbolSize: 55 },
                { type: 'min', name: '最低', symbolSize: 55 }
              ],
              symbol: 'pin',
              symbolSize: 40,
              itemStyle: {
                color: function(params) {
                  return params.data.type === 'max' ? '#00f2fe' : '#ff4b6b';
                },
                borderColor: '#ffffff',
                borderWidth: 2,
                shadowColor: 'rgba(0, 0, 0, 0.3)',
                shadowBlur: 10
              },
              label: {
                fontSize: 12
              }
            },
            markLine: {
              data: [{ type: 'average', name: '平均值' }],
              lineStyle: {
                color: '#ffb100',
                width: 2,
                type: 'dashed',
                opacity: 0.8
              },
              label: {
                position: 'middle',
                formatter: '平均: {c}'
              }
            },
            lineStyle: {
              width: 5,
              color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                { offset: 0, color: '#3e75ff' },
                { offset: 1, color: '#42d3fd' }
              ]),
              shadowColor: 'rgba(66, 211, 253, 0.5)',
              shadowBlur: 10,
              cap: 'round'
            },
            itemStyle: {
              color: '#42d3fd',
              borderWidth: 3,
              borderColor: '#fff',
              shadowColor: 'rgba(66, 211, 253, 0.7)',
              shadowBlur: 10
            },
            symbol: 'circle',
            symbolSize: 10,
            areaStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: 'rgba(66, 211, 253, 0.7)' },
                { offset: 0.5, color: 'rgba(66, 211, 253, 0.3)' },
                { offset: 1, color: 'rgba(66, 211, 253, 0.1)' }
              ]),
              shadowColor: 'rgba(66, 211, 253, 0.2)',
              shadowBlur: 15
            },
            smooth: true,
            animation: true,
            animationDuration: 1500,
            animationEasing: 'cubicOut'
          }
        ]
      }
      
      chartInstance.setOption(option)
      
      const resizeObserver = new ResizeObserver(() => {
        chartInstance.resize();
      });
      resizeObserver.observe(scoreChangeChart.value);
      
      window.addEventListener('resize', () => {
        chartInstance.resize()
      })
    }
    
    // 监听知识点变化，更新雷达图
    watch(selectedKnowledgePoint, () => {
      setTimeout(initRadarChart, 300)
    })
    
    // 监听学科和年级变化，更新知识图谱
    watch([selectedSubject, selectedGrade], () => {
      setTimeout(initKnowledgeGraph, 300)
    })
    
    // 监听学习科目变化，更新学习情况图表
    watch(learningSubject, () => {
      setTimeout(() => {
        initScoreDistributionChart()
        initScoreChangeChart()
      }, 300)
    })
    
    // 格式化日期时间
    function formatDateTime(date) {
      const year = date.getFullYear()
      const month = (date.getMonth() + 1).toString().padStart(2, '0')
      const day = date.getDate().toString().padStart(2, '0')
      const hours = date.getHours().toString().padStart(2, '0')
      const minutes = date.getMinutes().toString().padStart(2, '0')
      const seconds = date.getSeconds().toString().padStart(2, '0')
      
      return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
    }
    
    // 挂载后初始化图表
    onMounted(() => {
      setTimeout(() => {
        initKnowledgeGraph()
        initRadarChart()
        initScoreDistributionChart()
        initScoreChangeChart()
        loading.value = false
        
        // 添加窗口大小变化的处理
        window.addEventListener('resize', () => {
          setTimeout(() => {
            const charts = [
              knowledgeGraphChart.value && echarts.getInstanceByDom(knowledgeGraphChart.value),
              radarChart.value && echarts.getInstanceByDom(radarChart.value),
              scoreDistributionChart.value && echarts.getInstanceByDom(scoreDistributionChart.value),
              scoreChangeChart.value && echarts.getInstanceByDom(scoreChangeChart.value)
            ].filter(Boolean);
            
            charts.forEach(chart => chart.resize());
          }, 100);
        });
      }, 1000)
    })
    
    return {
      loading,
      currentTime,
      selectedSubject,
      selectedGrade,
      learningSubject,
      selectedKnowledgePoint,
      selectedStatsSubject,
      subjects,
      grades,
      knowledgePoints,
      knowledgeGraphChart,
      radarChart,
      scoreDistributionChart,
      scoreChangeChart,
      activeResourceTab,
      recommendedExercises,
      recommendedVideos,
      recommendedBooks,
      classStats,
      currentSubjectStats,
      studentGroups
    }
  }
}
</script>

<style scoped>
.dashboard-container {
  width: 100%;
  height: 100vh;
  background: transparent;
  color: #fff;
  overflow: hidden;
  position: relative;
  padding: 8px;
  box-sizing: border-box;
  font-family: "Microsoft YaHei", sans-serif;
  display: flex;
  flex-direction: column;
}

/* 背景装饰 */
.bg-decoration-left {
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 150px;
  height: 400px;
  opacity: 0.2;
  pointer-events: none;
  z-index: 0;
}

.bg-decoration-right {
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%) rotateY(180deg);
  width: 150px;
  height: 400px;
  opacity: 0.2;
  pointer-events: none;
  z-index: 0;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 45px;
  margin-bottom: 8px;
  z-index: 10;
}

.time-display {
  font-size: 14px;
  color: #a3aed0;
  display: flex;
  align-items: center;
  gap: 10px;
}

.time-display span {
  position: absolute;
  right: 30px;
  text-shadow: 0 0 5px rgba(126, 234, 255, 0.5);
}

.dashboard-content {
  display: flex;
  height: calc(100% - 85px);
  gap: 8px;
  flex: 1;
  z-index: 10;
  overflow: hidden;
}

.dashboard-footer {
  height: 25px;
  width: 100%;
  z-index: 10;
  margin-top: 8px;
}

.left-panel, .middle-panel, .right-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
  overflow: hidden;
  min-width: 0;
}

.panel-item {
  position: relative;
  height: calc(50% - 4px);
  overflow: hidden;
  min-height: 0;
  transition: all 0.3s ease;
  animation: fadeIn 0.6s ease-out forwards;
}

.panel-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.panel-border {
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 5px 15px;
  height: 38px;
  background: linear-gradient(90deg, rgba(11, 27, 103, 0.4) 0%, rgba(46, 78, 229, 0.2) 100%);
  border-bottom: 1px solid rgba(126, 234, 255, 0.2);
}

.panel-title {
  font-size: 14px;
  font-weight: 600;
  color: #7feaff;
  display: flex;
  align-items: center;
  white-space: nowrap;
  gap: 8px;
  text-shadow: 0 0 5px rgba(126, 234, 255, 0.3);
}

.panel-controls {
  display: flex;
  gap: 10px;
  align-items: center;
}

.panel-body {
  padding: 8px 12px;
  height: calc(100% - 50px);
  overflow: hidden;
}

.chart-container {
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.chart-group {
  display: flex;
  height: 100%;
  gap: 8px;
  overflow: hidden;
}

.chart-item {
  flex: 1;
  height: 100%;
  overflow: hidden;
  border-radius: 4px;
  background: rgba(11, 27, 103, 0.2);
}

/* 技术感数据表格 */
.tech-table-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border-radius: 6px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

.tech-table-header {
  display: flex;
  background: linear-gradient(90deg, rgba(11, 27, 103, 0.9) 0%, rgba(46, 78, 229, 0.9) 100%);
  border-bottom: 2px solid #3e75ff;
  height: 38px;
  flex-shrink: 0;
}

.tech-th {
  padding: 8px;
  font-weight: bold;
  color: #7feaff;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  position: relative;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  text-shadow: 0 0 5px rgba(126, 234, 255, 0.5);
}

.tech-th::after {
  content: '';
  position: absolute;
  right: 0;
  top: 20%;
  height: 60%;
  width: 1px;
  background: rgba(126, 234, 255, 0.3);
}

.tech-th:last-child::after {
  display: none;
}

.tech-table-body {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  scrollbar-width: thin;
  scrollbar-color: #3e75ff rgba(11, 27, 103, 0.5);
}

.tech-table-body::-webkit-scrollbar {
  width: 5px;
}

.tech-table-body::-webkit-scrollbar-track {
  background: rgba(11, 27, 103, 0.5);
}

.tech-table-body::-webkit-scrollbar-thumb {
  background-color: #3e75ff;
  border-radius: 6px;
}

.tech-table-row {
  display: flex;
  border-bottom: 1px solid rgba(126, 234, 255, 0.1);
  background: rgba(11, 27, 103, 0.4);
  transition: all 0.3s;
}

.tech-table-row:nth-child(odd) {
  background: rgba(21, 44, 138, 0.4);
}

.tech-table-row:hover {
  background: rgba(46, 78, 229, 0.6);
  transform: translateX(3px);
}

.tech-td {
  padding: 10px 6px;
  flex: 1;
  text-align: center;
  color: #fff;
  position: relative;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.tech-td::after {
  content: '';
  position: absolute;
  right: 0;
  top: 20%;
  height: 60%;
  width: 1px;
  background: rgba(126, 234, 255, 0.1);
}

.tech-td:last-child::after {
  display: none;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: repeat(2, 1fr);
  gap: 15px;
  height: 360px;
  padding: 15px;
  overflow: hidden;
}

.data-card {
  background: linear-gradient(135deg, rgba(11, 27, 103, 0.7) 0%, rgba(46, 78, 229, 0.4) 100%);
  border-radius: 10px;
  padding: 18px 12px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 12px;
  border: 1px solid rgba(126, 234, 255, 0.3);
  position: relative;
  overflow: hidden;
  transition: all 0.4s ease;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  animation: glow 4s infinite;
}

.data-card:hover {
  border-color: rgba(126, 234, 255, 0.8);
  box-shadow: 0 8px 20px rgba(126, 234, 255, 0.4);
  transform: translateY(-5px);
}

.data-card::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(126, 234, 255, 0.1) 0%, transparent 70%);
  opacity: 0;
  transition: opacity 0.4s ease;
}

.data-card:hover::before {
  opacity: 1;
}

.card-title {
  font-size: 15px;
  color: #7feaff;
  text-shadow: 0 0 8px rgba(126, 234, 255, 0.7);
  white-space: nowrap;
  font-weight: 600;
  letter-spacing: 1px;
}

.resource-tabs {
  height: 100%;
  overflow: hidden;
}

:deep(.el-tabs) {
  height: 100%;
  overflow: hidden;
}

:deep(.el-tabs__header) {
  margin-bottom: 10px;
  border-bottom-color: rgba(126, 234, 255, 0.2);
}

:deep(.el-tabs__nav) {
  border-color: transparent;
}

:deep(.el-tabs__item) {
  color: #a3aed0;
  transition: all 0.3s;
  padding: 0 15px;
  height: 35px;
  line-height: 35px;
}

:deep(.el-tabs__item.is-active) {
  color: #7feaff;
  font-weight: bold;
  text-shadow: 0 0 5px rgba(126, 234, 255, 0.5);
}

:deep(.el-tabs__item:hover) {
  color: #fff;
}

:deep(.el-tabs__active-bar) {
  background-color: #7feaff;
  box-shadow: 0 0 10px rgba(126, 234, 255, 0.7);
  height: 3px;
}

:deep(.el-tabs__content) {
  height: calc(100% - 45px);
  overflow: auto;
  scrollbar-width: thin;
  scrollbar-color: #3e75ff rgba(11, 27, 103, 0.5);
}

:deep(.el-tabs__content::-webkit-scrollbar) {
  width: 5px;
}

:deep(.el-tabs__content::-webkit-scrollbar-track) {
  background: rgba(11, 27, 103, 0.5);
}

:deep(.el-tabs__content::-webkit-scrollbar-thumb) {
  background-color: #3e75ff;
  border-radius: 6px;
}

:deep(.el-tab-pane) {
  height: 100%;
  overflow: auto;
}

.resource-list {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
  height: 100%;
  overflow-y: auto;
  padding: 5px 8px 10px 5px;
}

.resource-item {
  background: linear-gradient(135deg, rgba(11, 27, 103, 0.6) 0%, rgba(46, 78, 229, 0.3) 100%);
  border-radius: 8px;
  padding: 15px 12px;
  display: flex;
  flex-direction: column;
  border: 1px solid rgba(126, 234, 255, 0.3);
  transition: all 0.4s;
  min-width: 0;
  height: 120px;
  box-shadow: 0 5px 12px rgba(0, 0, 0, 0.15);
  position: relative;
  overflow: hidden;
}

.resource-item.featured {
  background: linear-gradient(135deg, rgba(46, 78, 229, 0.7) 0%, rgba(11, 27, 103, 0.5) 100%);
  border: 1px solid rgba(126, 234, 255, 0.7);
  box-shadow: 0 5px 15px rgba(126, 234, 255, 0.3);
  transform: scale(1.03);
  z-index: 1;
}

.resource-item.featured::before {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 30px;
  height: 30px;
  background: linear-gradient(45deg, transparent 50%, #7feaff 50%);
  border-radius: 0 8px 0 8px;
}

.resource-item.featured::after {
  content: '热门';
  position: absolute;
  top: 5px;
  right: 6px;
  transform: rotate(45deg);
  font-size: 9px;
  font-weight: bold;
  color: #003366;
}

.resource-item.featured .resource-title {
  color: #ffffff;
  text-shadow: 0 0 8px rgba(255, 255, 255, 0.5);
}

.resource-item.featured:hover {
  transform: translateY(-5px) scale(1.03);
  box-shadow: 0 8px 25px rgba(126, 234, 255, 0.5);
}

.resource-item::after {
  content: '';
  position: absolute;
  right: -50px;
  bottom: -50px;
  width: 100px;
  height: 100px;
  background: radial-gradient(circle, rgba(126, 234, 255, 0.3) 0%, transparent 70%);
  opacity: 0;
  transition: opacity 0.4s ease;
}

.resource-item:hover::after {
  opacity: 1;
}

.resource-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
  border-color: rgba(126, 234, 255, 0.8);
}

.resource-title {
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 8px;
  color: #fff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  text-shadow: 0 0 5px rgba(126, 234, 255, 0.3);
}

.resource-desc {
  font-size: 12px;
  color: #a3aed0;
  margin-bottom: 8px;
  flex-grow: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.resource-meta {
  font-size: 11px;
  color: #7feaff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  padding-top: 5px;
  border-top: 1px dashed rgba(126, 234, 255, 0.2);
}

.tech-select {
  width: 120px;
  height: 30px;
  background-color: rgba(11, 27, 103, 0.6);
  border: 1px solid rgba(126, 234, 255, 0.4);
  border-radius: 5px;
  color: #fff;
  font-size: 12px;
  padding: 0 28px 0 10px;
  cursor: pointer;
  outline: none;
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  position: relative;
  transition: all 0.3s ease;
}

.tech-select:hover {
  border-color: rgba(126, 234, 255, 0.8);
  box-shadow: 0 0 10px rgba(126, 234, 255, 0.3);
  background-color: rgba(46, 78, 229, 0.4);
}

.tech-select:focus {
  border-color: #7feaff;
  box-shadow: 0 0 15px rgba(126, 234, 255, 0.5);
}

.tech-select option {
  background-color: rgba(11, 27, 103, 0.9);
  color: #a3aed0;
  padding: 10px;
}

.tech-select option:hover,
.tech-select option:focus,
.tech-select option:checked {
  background-color: rgba(126, 234, 255, 0.2);
  color: #7feaff;
}

/* 调整下拉箭头位置 */
.tech-select {
  background-image: linear-gradient(45deg, transparent 50%, #7feaff 50%),
                    linear-gradient(135deg, #7feaff 50%, transparent 50%);
  background-position: calc(100% - 15px) calc(50% + 2px),
                       calc(100% - 10px) calc(50% + 2px);
  background-size: 5px 5px,
                  5px 5px;
  background-repeat: no-repeat;
}

/* Animation glowing effects */
@keyframes glow {
  0% {
    box-shadow: 0 0 5px rgba(126, 234, 255, 0.2);
  }
  50% {
    box-shadow: 0 0 15px rgba(126, 234, 255, 0.5);
  }
  100% {
    box-shadow: 0 0 5px rgba(126, 234, 255, 0.2);
  }
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.02);
  }
  100% {
    transform: scale(1);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.data-card {
  animation: glow 4s infinite;
}

.data-card:nth-child(1) {
  animation-delay: 0s;
}

.data-card:nth-child(2) {
  animation-delay: 1s;
}

.data-card:nth-child(3) {
  animation-delay: 2s;
}

.data-card:nth-child(4) {
  animation-delay: 3s;
}

:deep(.dv-digital-flop) {
  width: 120px !important;
  height: 45px !important;
}

/* Loading 样式 */
:deep(.dv-loading) {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(11, 27, 103, 0.9);
  z-index: 1000;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #7feaff;
  font-size: 18px;
  letter-spacing: 2px;
  text-shadow: 0 0 10px rgba(126, 234, 255, 0.7);
}

/* 标题装饰 */
:deep(.dv-decoration-3) {
  filter: drop-shadow(0 0 3px rgba(126, 234, 255, 0.5));
}

:deep(.dv-decoration-10) {
  filter: drop-shadow(0 0 3px rgba(126, 234, 255, 0.5));
}

:deep(.dv-decoration-11) {
  filter: drop-shadow(0 0 2px rgba(126, 234, 255, 0.3));
}

:deep(.dv-decoration-4) {
  filter: drop-shadow(0 0 3px rgba(126, 234, 255, 0.5));
}

:deep(.dv-decoration-5) {
  filter: drop-shadow(0 0 3px rgba(126, 234, 255, 0.5));
}

:deep(.dv-decoration-12) {
  filter: drop-shadow(0 0 5px rgba(126, 234, 255, 0.7));
}

/* 响应式设计 */
@media (max-width: 1400px) {
  .resource-list {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .card-title {
    font-size: 12px;
  }
  
  .tech-td, .tech-th {
    font-size: 12px;
    padding: 6px 4px;
  }
}

@media (max-width: 1200px) {
  .dashboard-content {
    flex-direction: column;
    height: auto;
    overflow-y: auto;
  }
  
  .left-panel, .middle-panel, .right-panel {
    min-height: 500px;
  }
  
  .panel-item {
    min-height: 240px;
  }
}
</style> 