<template>
  <div class="chart-container">
    <div class="api-stats-wrapper">
      <div class="api-summary">
        <div class="summary-card" v-for="(item, index) in apiData" :key="index" :style="{'--card-color': item.color}">
          <div class="card-icon">
            <i class="el-icon-data-analysis"></i>
          </div>
          <div class="card-info">
            <div class="card-title">{{ item.name }}</div>
            <div class="card-value">{{ item.count.toLocaleString() }}</div>
          </div>
          <div class="card-trend" :class="{ 'up': item.trend > 0, 'down': item.trend < 0 }">
            <i :class="item.trend > 0 ? 'el-icon-top' : 'el-icon-bottom'"></i>
            {{ Math.abs(item.trend) }}%
          </div>
        </div>
      </div>
      
      <div class="chart-area-wrapper">
        <div class="chart-background"></div>
        <div class="chart-area" ref="chartContainer"></div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, onUnmounted, nextTick } from 'vue';
import * as echarts from 'echarts';

export default {
  name: 'ApiCallsChart',
  setup() {
    const chartContainer = ref(null);
    let chart = null;
    let timer = null; // 全局定时器变量

    // API 调用数据
    const apiData = reactive([
      {
        name: 'DeepSeek',
        count: 45628,
        trend: 12.3,
        percentage: 85,
        color: '#36d1dc'
      },
      {
        name: '讯飞星火',
        count: 38715,
        trend: 8.7,
        percentage: 72,
        color: '#5b86e5'
      },
      {
        name: '智谱AI',
        count: 32164,
        trend: -3.2,
        percentage: 60,
        color: '#8884ff'
      },
      {
        name: '百度云',
        count: 27839,
        trend: 5.4,
        percentage: 52,
        color: '#d88cd0'
      }
    ]);

    const initChart = async () => {
      await nextTick();
      if (!chartContainer.value) return;
      
      // 确保容器可见并且有尺寸
      if (chartContainer.value.offsetHeight === 0) {
        console.error('Chart container has no height');
        setTimeout(initChart, 100); // 延迟重试
        return;
      }
      
      try {
        if (chart) {
          chart.dispose();
        }
        
        chart = echarts.init(chartContainer.value);
        
        // 生成过去24小时的数据
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

        // 生成随机数据
        const generateApiData = (baseValue, variance) => {
          const data = [];
          for (let i = 0; i < 24; i++) {
            // 模拟工作时间的数据波动
            let hourFactor = 1;
            const hour = (new Date().getHours() - 23 + i + 24) % 24;
            
            // 工作时间 (9-18点) 活跃度更高
            if (hour >= 9 && hour <= 18) {
              hourFactor = 1.5;
            } 
            // 夜间 (0-6点) 活跃度更低
            else if (hour >= 0 && hour <= 6) {
              hourFactor = 0.5;
            }
            
            const value = Math.round(baseValue * hourFactor * (0.8 + Math.random() * variance));
            data.push(value);
          }
          return data;
        };

        const hourLabels = generateHourLabels();
        const deepseekData = generateApiData(800, 0.5);
        const xunfeiData = generateApiData(650, 0.4);
        const zhipuData = generateApiData(550, 0.6);
        const baiduData = generateApiData(450, 0.7);

        const option = {
          backgroundColor: 'transparent',
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'shadow'
            }
          },
          legend: {
            data: ['DeepSeek', '讯飞星火', '智谱AI', '百度云'],
            top: 0,
            textStyle: {
              color: '#fff'
            }
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            top: '40px',
            containLabel: true
          },
          xAxis: {
            type: 'category',
            data: hourLabels,
            axisLine: {
              lineStyle: {
                color: 'rgba(255, 255, 255, 0.3)'
              }
            },
            axisLabel: {
              color: 'rgba(255, 255, 255, 0.7)',
              fontSize: 10,
              interval: 3
            },
            axisTick: {
              show: false
            }
          },
          yAxis: {
            type: 'value',
            name: '调用次数',
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
              name: 'DeepSeek',
              type: 'bar',
              barWidth: '12',
              itemStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  { offset: 0, color: '#36d1dc' },
                  { offset: 1, color: 'rgba(54, 209, 220, 0.5)' }
                ]),
                borderRadius: [3, 3, 0, 0]
              },
              data: deepseekData
            },
            {
              name: '讯飞星火',
              type: 'bar',
              barWidth: '12',
              itemStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  { offset: 0, color: '#5b86e5' },
                  { offset: 1, color: 'rgba(91, 134, 229, 0.5)' }
                ]),
                borderRadius: [3, 3, 0, 0]
              },
              data: xunfeiData
            },
            {
              name: '智谱AI',
              type: 'bar',
              barWidth: '12',
              itemStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  { offset: 0, color: '#8884ff' },
                  { offset: 1, color: 'rgba(136, 132, 255, 0.5)' }
                ]),
                borderRadius: [3, 3, 0, 0]
              },
              data: zhipuData
            },
            {
              name: '百度云',
              type: 'bar',
              barWidth: '12',
              itemStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  { offset: 0, color: '#d88cd0' },
                  { offset: 1, color: 'rgba(216, 140, 208, 0.5)' }
                ]),
                borderRadius: [3, 3, 0, 0]
              },
              data: baiduData
            }
          ]
        };

        chart.setOption(option);
        
        // 确保图表渲染完成
        chart.on('rendered', () => {
          console.log('Chart rendered successfully');
        });
      } catch (error) {
        console.error('Error initializing chart:', error);
      }
      
      // 添加定时器，每隔10秒更新一次数据
      const updateData = () => {
        if (!chart) return;
        
        // 更新API卡片数据
        apiData.forEach(api => {
          api.count += Math.floor(Math.random() * 1000) - 200;
          api.trend = +(Math.random() * 20 - 5).toFixed(1);
          api.percentage = Math.min(100, Math.floor(Math.random() * 40) + 40);
        });

        try {
          // 获取当前配置
          const currentOption = chart.getOption();
          
          // 更新图表数据
          const hourLabels = currentOption.xAxis[0].data;
          hourLabels.shift();
          const now = new Date();
          const currentHour = now.getHours();
          hourLabels.push(`${currentHour}:00`);

          // 更新每个系列的数据
          const updateSeriesData = (data, baseValue, variance) => {
            data.shift();
            
            // 模拟工作时间的数据波动
            let hourFactor = 1;
            
            // 工作时间 (9-18点) 活跃度更高
            if (currentHour >= 9 && currentHour <= 18) {
              hourFactor = 1.5;
            } 
            // 夜间 (0-6点) 活跃度更低
            else if (currentHour >= 0 && currentHour <= 6) {
              hourFactor = 0.5;
            }
            
            const value = Math.round(baseValue * hourFactor * (0.8 + Math.random() * variance));
            data.push(value);
            return data;
          };

          chart.setOption({
            xAxis: {
              data: hourLabels
            },
            series: [
              { data: updateSeriesData(currentOption.series[0].data, 800, 0.5) },
              { data: updateSeriesData(currentOption.series[1].data, 650, 0.4) },
              { data: updateSeriesData(currentOption.series[2].data, 550, 0.6) },
              { data: updateSeriesData(currentOption.series[3].data, 450, 0.7) }
            ]
          });
        } catch (error) {
          console.error('Error updating chart:', error);
        }
      };
      
      // 清除之前的定时器
      if (timer) {
        clearInterval(timer);
      }
      
      // 设置新的定时器
      timer = setInterval(updateData, 10000);
    };

    const handleResize = () => {
      if (chart) {
        try {
          chart.resize();
        } catch (error) {
          console.error('Error resizing chart:', error);
        }
      }
    };

    // 在组件挂载时初始化图表
    onMounted(() => {
      // 初始化图表
      initChart();
      
      // 监听窗口大小变化
      window.addEventListener('resize', handleResize);
      
      // 额外添加一次延迟初始化，确保DOM完全渲染
      setTimeout(() => {
        if (!chart && chartContainer.value) {
          initChart();
        }
      }, 500);
    });

    // 在组件卸载时清理资源
    onUnmounted(() => {
      // 移除窗口大小变化监听
      window.removeEventListener('resize', handleResize);
      
      // 清除定时器
      if (timer) {
        clearInterval(timer);
        timer = null;
      }
      
      // 销毁图表实例
      if (chart) {
        chart.dispose();
        chart = null;
      }
    });

    return {
      chartContainer,
      apiData
    };
  }
};
</script>

<style lang="scss" scoped>
.chart-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.api-stats-wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.api-summary {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  padding: 0 5px 10px;
  flex-wrap: wrap;
  
  .summary-card {
    flex: 1;
    min-width: 150px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 8px;
    padding: 8px 10px;
    display: flex;
    align-items: center;
    position: relative;
    overflow: hidden;
    
    &::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      width: 4px;
      height: 100%;
      background: var(--card-color);
    }
    
    .card-icon {
      width: 36px;
      height: 36px;
      border-radius: 8px;
      background-color: var(--card-color);
      display: flex;
      align-items: center;
      justify-content: center;
      margin-right: 12px;
      
      i {
        color: white;
        font-size: 18px;
      }
    }
    
    .card-info {
      flex: 1;
      display: flex;
      flex-direction: column;
      
      .card-title {
        font-size: 14px;
        color: rgba(255, 255, 255, 0.8);
        margin-bottom: 5px;
      }
      
      .card-value {
        font-size: 18px;
        font-weight: bold;
        color: white;
      }
    }
    
    .card-trend {
      padding: 4px 8px;
      border-radius: 4px;
      font-size: 13px;
      font-weight: 500;
      display: flex;
      align-items: center;
      
      i {
        margin-right: 3px;
      }
      
      &.up {
        color: #36d1dc;
        background: rgba(54, 209, 220, 0.1);
      }
      
      &.down {
        color: #ff6e76;
        background: rgba(255, 110, 118, 0.1);
      }
    }
  }
}

.chart-area-wrapper {
  flex: 1;
  position: relative;
  min-height: 250px;
  
  .chart-background {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(5, 15, 45, 0.3);
    border-radius: 6px;
    z-index: 0;
  }
  
  .chart-area {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 1;
  }
}
</style> 