<template>
  <div class="chart-container">
    <div class="user-activity-wrapper">
      <div class="activity-header">
        <div class="stats-cards">
          <div class="stats-card" v-for="(item, index) in statsItems" :key="index">
            <div class="stats-icon" :style="{ backgroundColor: item.color }">
              <i :class="item.icon"></i>
            </div>
            <div class="stats-content">
              <div class="stats-label">{{ item.label }}</div>
              <div class="stats-value">{{ item.value }}</div>
            </div>
          </div>
        </div>
        
        <div class="filter-buttons">
          <div 
            v-for="(filter, index) in timeFilters" 
            :key="index"
            :class="['filter-btn', { active: currentFilter === filter.value }]"
            @click="setTimeFilter(filter.value)"
          >
            {{ filter.label }}
          </div>
        </div>
      </div>
      
      <div class="chart-area" ref="chartContainer"></div>
      
      <div class="user-distribution">
        <div class="distribution-item" v-for="(item, index) in userDistribution" :key="index">
          <div class="user-type">
            <div class="user-icon" :style="{ backgroundColor: item.color }">
              <i :class="item.icon"></i>
            </div>
            <div class="user-info">
              <div class="user-name">{{ item.name }}</div>
              <div class="user-count">{{ item.count }}</div>
            </div>
          </div>
          <div class="distribution-bar">
            <div class="progress-track">
              <div class="progress-fill" :style="{ width: `${item.percentage}%`, background: item.color }"></div>
              <div class="percentage-text">{{ item.percentage }}%</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, onUnmounted, computed } from 'vue';
import * as echarts from 'echarts';

export default {
  name: 'UserActivityChart',
  setup() {
    const chartContainer = ref(null);
    let chart = null;
    
    const totalUsers = ref('3,256');
    const activeUsers = ref('1,485');
    const totalLogins = ref('4,879');
    
    const statsItems = computed(() => [
      {
        label: '总用户数',
        value: totalUsers.value,
        color: '#36d1dc',
        icon: 'el-icon-user'
      },
      {
        label: '今日活跃用户',
        value: activeUsers.value,
        color: '#5b86e5',
        icon: 'el-icon-data-board'
      },
      {
        label: '今日登录次数',
        value: totalLogins.value,
        color: '#8884ff',
        icon: 'el-icon-monitor'
      }
    ]);
    
    const timeFilters = [
      { label: '今日', value: 'today' },
      { label: '本周', value: 'week' },
      { label: '本月', value: 'month' }
    ];
    
    const currentFilter = ref('today');
    
    const userDistribution = reactive([
      {
        name: '教师用户',
        count: '756',
        percentage: 35,
        color: '#36d1dc',
        icon: 'el-icon-user'
      },
      {
        name: '学生用户',
        count: '2,350',
        percentage: 65,
        color: '#5b86e5',
        icon: 'el-icon-user'
      }
    ]);
    
    const setTimeFilter = (filter) => {
      currentFilter.value = filter;
      updateChartData(filter);
    };
    
    const updateChartData = (filter) => {
      if (!chart) return;
      
      // 根据过滤器更新数据范围
      let timeLabels;
      let teacherData;
      let studentData;
      
      switch (filter) {
        case 'today':
          timeLabels = generateHourLabels();
          teacherData = generateUserActivityData(30, 0.5);
          studentData = generateUserActivityData(60, 0.6);
          break;
        case 'week':
          timeLabels = generateWeekLabels();
          teacherData = generateUserActivityData(200, 0.4);
          studentData = generateUserActivityData(350, 0.5);
          break;
        case 'month':
          timeLabels = generateMonthLabels();
          teacherData = generateUserActivityData(150, 0.6);
          studentData = generateUserActivityData(320, 0.5);
          break;
      }
      
      chart.setOption({
        xAxis: {
          data: timeLabels
        },
        series: [
          {
            name: '教师活跃度',
            data: teacherData
          },
          {
            name: '学生活跃度',
            data: studentData
          }
        ]
      });
    };
    
    // 生成过去24小时的标签
    const generateHourLabels = () => {
      const labels = [];
      const now = new Date();
      const hour = now.getHours();
      
      for (let i = 0; i < 24; i++) {
        const h = (hour - 23 + i + 24) % 24;
        labels.push(`${h}:00`);
      }
      
      return labels;
    };
    
    // 生成过去7天的标签
    const generateWeekLabels = () => {
      const labels = [];
      const days = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
      const now = new Date();
      const day = now.getDay();
      
      for (let i = 6; i >= 0; i--) {
        const index = (day - i + 7) % 7;
        labels.push(days[index]);
      }
      
      return labels;
    };
    
    // 生成过去30天的标签
    const generateMonthLabels = () => {
      const labels = [];
      const now = new Date();
      const today = now.getDate();
      
      for (let i = 29; i >= 0; i--) {
        const date = new Date();
        date.setDate(today - i);
        labels.push(`${date.getMonth() + 1}/${date.getDate()}`);
      }
      
      return labels;
    };
    
    // 生成用户活跃度数据
    const generateUserActivityData = (baseValue, variance) => {
      const data = [];
      
      // 根据当前过滤器生成不同数量的数据点
      const count = currentFilter.value === 'today' ? 24 : 
                    currentFilter.value === 'week' ? 7 : 30;
      
      for (let i = 0; i < count; i++) {
        // 模拟工作/学习时间的数据波动
        let timeFactor = 1;
        
        if (currentFilter.value === 'today') {
          const hour = (new Date().getHours() - 23 + i + 24) % 24;
          // 工作/学习时间 (8-21点) 活跃度更高
          if (hour >= 8 && hour <= 21) {
            timeFactor = 1.5;
            // 高峰时段：上午9-11点，下午14-16点，晚上19-21点
            if ((hour >= 9 && hour <= 11) || (hour >= 14 && hour <= 16) || (hour >= 19 && hour <= 21)) {
              timeFactor = 2.5;
            }
          } else {
            timeFactor = 0.3; // 深夜活跃度低
          }
        } else if (currentFilter.value === 'week') {
          // 工作日活跃度更高
          const index = (new Date().getDay() - 6 + i + 7) % 7;
          if (index >= 1 && index <= 5) {
            timeFactor = 1.5;
          } else {
            timeFactor = 0.8; // 周末活跃度低
          }
        }
        
        const randomFactor = 0.7 + Math.random() * variance;
        const value = Math.round(baseValue * timeFactor * randomFactor);
        data.push(value);
      }
      
      return data;
    };

    const initChart = () => {
      if (!chartContainer.value) return;
      
      chart = echarts.init(chartContainer.value);
      
      const timeLabels = generateHourLabels();
      const teacherData = generateUserActivityData(30, 0.5);
      const studentData = generateUserActivityData(60,.6);
      
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'line',
            lineStyle: {
              color: 'rgba(91, 134, 229, 0.3)',
              width: 1,
              type: 'solid'
            }
          }
        },
        legend: {
          data: ['教师活跃度', '学生活跃度'],
          right: 0,
          top: 0,
          textStyle: {
            color: '#fff'
          },
          itemWidth: 10,
          itemHeight: 10,
          icon: 'circle'
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          top: '50px',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: timeLabels,
          axisLine: {
            lineStyle: {
              color: 'rgba(255, 255, 255, 0.3)'
            }
          },
          axisLabel: {
            color: 'rgba(255, 255, 255, 0.7)',
            fontSize: 10
          },
          axisTick: {
            show: false
          }
        },
        yAxis: {
          type: 'value',
          name: '活跃人数',
          nameTextStyle: {
            color: 'rgba(255, 255, 255, 0.7)',
            padding: [0, 30, 0, 0]
          },
          axisLine: {
            show: false
          },
          axisLabel: {
            color: 'rgba(255, 255, 255, 0.7)'
          },
          splitLine: {
            lineStyle: {
              color: 'rgba(255, 255, 255, 0.1)'
            }
          }
        },
        series: [
          {
            name: '教师活跃度',
            type: 'line',
            stack: 'Total',
            smooth: true,
            symbol: 'circle',
            symbolSize: 6,
            showSymbol: false,
            lineStyle: {
              width: 3,
              color: '#36d1dc'
            },
            areaStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: 'rgba(54, 209, 220, 0.3)' },
                { offset: 1, color: 'rgba(54, 209, 220, 0.05)' }
              ])
            },
            itemStyle: {
              color: '#36d1dc',
              borderColor: '#fff',
              borderWidth: 1
            },
            emphasis: {
              focus: 'series',
              itemStyle: {
                borderWidth: 2
              }
            },
            data: teacherData
          },
          {
            name: '学生活跃度',
            type: 'line',
            stack: 'Total',
            smooth: true,
            symbol: 'circle',
            symbolSize: 6,
            showSymbol: false,
            lineStyle: {
              width: 3,
              color: '#5b86e5'
            },
            areaStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: 'rgba(91, 134, 229, 0.3)' },
                { offset: 1, color: 'rgba(91, 134, 229, 0.05)' }
              ])
            },
            itemStyle: {
              color: '#5b86e5',
              borderColor: '#fff',
              borderWidth: 1
            },
            emphasis: {
              focus: 'series',
              itemStyle: {
                borderWidth: 2
              }
            },
            data: studentData
          }
        ]
      };
      
      chart.setOption(option);
      
      // 添加定时器，每隔10秒更新一次数据
      const updateData = () => {
        // 更新统计数据
        totalUsers.value = (parseInt(totalUsers.value.replace(/,/g, '')) + Math.floor(Math.random() * 10)).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
        activeUsers.value = (parseInt(activeUsers.value.replace(/,/g, '')) + Math.floor(Math.random() * 30) - 15).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
        totalLogins.value = (parseInt(totalLogins.value.replace(/,/g, '')) + Math.floor(Math.random() * 50)).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
        
        // 更新用户分布数据
        userDistribution.forEach(item => {
          item.count = (parseInt(item.count.replace(/,/g, '')) + Math.floor(Math.random() * 10) - 5).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
        });
        
        // 计算新百分比
        const teacher = parseInt(userDistribution[0].count.replace(/,/g, ''));
        const student = parseInt(userDistribution[1].count.replace(/,/g, ''));
        const total = teacher + student;
        
        userDistribution[0].percentage = Math.round(teacher / total * 100);
        userDistribution[1].percentage = 100 - userDistribution[0].percentage;
        
        // 更新图表数据
        updateChartData(currentFilter.value);
      };
      
      const timer = setInterval(updateData, 10000);
      
      return () => {
        clearInterval(timer);
      };
    };

    const handleResize = () => {
      chart && chart.resize();
    };

    onMounted(() => {
      const cleanup = initChart();
      window.addEventListener('resize', handleResize);
      
      onUnmounted(() => {
        cleanup && cleanup();
        window.removeEventListener('resize', handleResize);
        chart && chart.dispose();
        chart = null;
      });
    });

    return {
      chartContainer,
      totalUsers,
      activeUsers,
      totalLogins,
      statsItems,
      timeFilters,
      currentFilter,
      userDistribution,
      setTimeFilter
    };
  }
};
</script>

<style lang="scss" scoped>
.chart-container {
  width: 100%;
  height: 100%;
}

.user-activity-wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.activity-header {
  padding: 0 0 15px;
  
  .stats-cards {
    display: flex;
    gap: 15px;
    margin-bottom: 15px;
    
    .stats-card {
      flex: 1;
      background: rgba(255, 255, 255, 0.05);
      border-radius: 8px;
      padding: 12px;
      display: flex;
      align-items: center;
      
      .stats-icon {
        width: 40px;
        height: 40px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 12px;
        
        i {
          color: white;
          font-size: 20px;
        }
      }
      
      .stats-content {
        flex: 1;
        
        .stats-label {
          font-size: 13px;
          color: rgba(255, 255, 255, 0.7);
          margin-bottom: 5px;
        }
        
        .stats-value {
          font-size: 22px;
          font-weight: bold;
          color: white;
        }
      }
    }
  }
  
  .filter-buttons {
    display: flex;
    justify-content: center;
    gap: 10px;
    
    .filter-btn {
      padding: 6px 16px;
      border-radius: 4px;
      font-size: 13px;
      cursor: pointer;
      background: rgba(255, 255, 255, 0.05);
      color: rgba(255, 255, 255, 0.7);
      transition: all 0.3s;
      
      &:hover {
        background: rgba(255, 255, 255, 0.1);
      }
      
      &.active {
        background: rgba(91, 134, 229, 0.2);
        color: #5b86e5;
        position: relative;
        
        &::after {
          content: '';
          position: absolute;
          bottom: 0;
          left: 50%;
          transform: translateX(-50%);
          width: 20px;
          height: 2px;
          background: linear-gradient(90deg, #36d1dc, #5b86e5);
          border-radius: 1px;
        }
      }
    }
  }
}

.chart-area {
  flex: 1;
  width: 100%;
  min-height: 0;
}

.user-distribution {
  display: flex;
  gap: 20px;
  padding: 15px 0 0;
  
  .distribution-item {
    flex: 1;
    
    .user-type {
      display: flex;
      align-items: center;
      margin-bottom: 10px;
      
      .user-icon {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 12px;
        
        i {
          color: white;
          font-size: 18px;
        }
      }
      
      .user-info {
        flex: 1;
        
        .user-name {
          font-size: 14px;
          color: rgba(255, 255, 255, 0.7);
          margin-bottom: 5px;
        }
        
        .user-count {
          font-size: 18px;
          font-weight: bold;
          color: white;
        }
      }
    }
    
    .distribution-bar {
      .progress-track {
        height: 8px;
        width: 100%;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 4px;
        overflow: hidden;
        position: relative;
        
        .progress-fill {
          height: 100%;
          border-radius: 4px;
          transition: width 0.5s;
        }
        
        .percentage-text {
          position: absolute;
          right: 5px;
          top: -20px;
          font-size: 14px;
          font-weight: 500;
          color: white;
        }
      }
    }
  }
}
</style>