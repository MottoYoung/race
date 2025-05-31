<template>
  <div class="chart-container">
    <div class="datav-wrapper">
      <div class="resources-overview">
        <div class="total-section">
          <div class="total-counter">
            <div class="counter-title">教学资源总量</div>
            <div class="counter-value">{{ totalResources }}</div>
          </div>
          <div class="growth-indicator">
            <div class="growth-title">日环比增长</div>
            <div class="growth-value" :class="{ 'positive': growthRate >= 0, 'negative': growthRate < 0 }">
              {{ growthRate >= 0 ? '+' : '' }}{{ growthRate }}%
            </div>
          </div>
        </div>
        
        <div class="content-container">
          <!-- 左侧资源卡片列 -->
          <div class="resource-column">
            <div class="category-card">
              <div class="category-icon" :style="{ backgroundColor: categoryData[0].color }">
                <i :class="categoryData[0].icon"></i>
              </div>
              <div class="category-info">
                <div class="category-name">{{ categoryData[0].name }}</div>
                <div class="category-count">{{ categoryData[0].count }}</div>
              </div>
              <div class="category-progress">
                <div class="progress-bar" :style="{ width: categoryData[0].percentage + '%', backgroundColor: categoryData[0].color }"></div>
              </div>
            </div>
            
            <div class="category-card">
              <div class="category-icon" :style="{ backgroundColor: categoryData[1].color }">
                <i :class="categoryData[1].icon"></i>
              </div>
              <div class="category-info">
                <div class="category-name">{{ categoryData[1].name }}</div>
                <div class="category-count">{{ categoryData[1].count }}</div>
              </div>
              <div class="category-progress">
                <div class="progress-bar" :style="{ width: categoryData[1].percentage + '%', backgroundColor: categoryData[1].color }"></div>
              </div>
            </div>
          </div>
          
          <!-- 右侧柱状图 -->
          <div class="chart-column">
            <div class="chart-title">资源分布对比</div>
            <div class="bar-chart" ref="barChartContainer"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, onUnmounted } from 'vue';
import * as echarts from 'echarts';

export default {
  name: 'ResourcesTotalChart',
  setup() {
    // 仅保留习题资源和视频资源数据
    const categoryData = reactive([
      { 
        name: '习题资源', 
        count: '12,458', 
        percentage: 45, 
        color: '#36d1dc',
        icon: 'el-icon-tickets'
      },
      { 
        name: '视频资源', 
        count: '8,239', 
        percentage: 30, 
        color: '#5b86e5',
        icon: 'el-icon-video-camera'
      }
    ]);

    const totalResources = ref('20,697'); // 更新为仅包含两种资源的总和
    const growthRate = ref(12.8);
    
    // 柱状图容器引用
    const barChartContainer = ref(null);
    let barChart = null;
    
    // 初始化柱状图
    const initBarChart = () => {
      if (!barChartContainer.value) return;
      
      barChart = echarts.init(barChartContainer.value);
      
      const option = {
        grid: {
          top: '10%',
          left: '3%',
          right: '3%',
          bottom: '5%',
          containLabel: true
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          },
          formatter: '{b}: {c}'
        },
        xAxis: {
          type: 'category',
          data: categoryData.map(item => item.name),
          axisLine: {
            lineStyle: {
              color: 'rgba(255, 255, 255, 0.3)'
            }
          },
          axisLabel: {
            color: 'rgba(255, 255, 255, 0.7)',
            interval: 0
          },
          axisTick: {
            show: false
          }
        },
        yAxis: {
          type: 'value',
          splitLine: {
            lineStyle: {
              color: 'rgba(255, 255, 255, 0.1)',
              type: 'dashed'
            }
          },
          axisLine: {
            show: false
          },
          axisTick: {
            show: false
          },
          axisLabel: {
            color: 'rgba(255, 255, 255, 0.7)'
          }
        },
        series: [
          {
            type: 'bar',
            barWidth: '40%',
            data: categoryData.map((item, index) => {
              return {
                value: parseInt(item.count.replace(/,/g, '')),
                itemStyle: {
                  color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    { offset: 0, color: item.color },
                    { offset: 1, color: index === 0 ? 'rgba(54, 209, 220, 0.5)' : 'rgba(91, 134, 229, 0.5)' }
                  ])
                }
              };
            }),
            label: {
              show: true,
              position: 'top',
              color: '#fff',
              formatter: (params) => {
                return params.value.toLocaleString();
              }
            },
            itemStyle: {
              borderRadius: [4, 4, 0, 0]
            }
          }
        ]
      };
      
      barChart.setOption(option);
    };
    
    // 更新柱状图数据
    const updateBarChart = () => {
      if (!barChart) return;
      
      barChart.setOption({
        series: [
          {
            data: categoryData.map((item, index) => {
              return {
                value: parseInt(item.count.replace(/,/g, '')),
                itemStyle: {
                  color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    { offset: 0, color: item.color },
                    { offset: 1, color: index === 0 ? 'rgba(54, 209, 220, 0.5)' : 'rgba(91, 134, 229, 0.5)' }
                  ])
                }
              };
            })
          }
        ]
      });
    };
    
    // 处理窗口大小变化
    const handleResize = () => {
      if (barChart) {
        barChart.resize();
      }
    };

    // 定时更新数据
    onMounted(() => {
      // 初始化柱状图
      initBarChart();
      window.addEventListener('resize', handleResize);
      
      const timer = setInterval(() => {
        // 更新分类数据
        categoryData.forEach(category => {
          // 生成新的随机数值
          const newCount = parseInt(category.count.replace(/,/g, '')) + Math.floor(Math.random() * 50) - 20;
          category.count = newCount.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
          
          // 更新百分比
          category.percentage = Math.floor(Math.random() * 40) + 10;
        });
        
        // 更新总量为两种资源的总和
        const exerciseCount = parseInt(categoryData[0].count.replace(/,/g, ''));
        const videoCount = parseInt(categoryData[1].count.replace(/,/g, ''));
        totalResources.value = (exerciseCount + videoCount).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
        
        // 更新增长率
        growthRate.value = (Math.random() * 20 - 5).toFixed(1);
        
        // 更新柱状图
        updateBarChart();
      }, 10000);
      
      onUnmounted(() => {
        clearInterval(timer);
        window.removeEventListener('resize', handleResize);
        if (barChart) {
          barChart.dispose();
          barChart = null;
        }
      });
    });

    return {
      categoryData,
      totalResources,
      growthRate,
      barChartContainer
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
  overflow: visible;
}

.datav-wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.resources-overview {
  display: flex;
  flex-direction: column;
  padding: 10px 15px;
  height: auto;
}

.total-section {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
  
  .total-counter {
    display: flex;
    flex-direction: column;
    
    .counter-title {
      font-size: 13px;
      color: rgba(255, 255, 255, 0.8);
      letter-spacing: 0.5px;
      margin-bottom: 5px;
    }
    
    .counter-value {
      font-size: 28px;
      font-weight: bold;
      background: linear-gradient(90deg, #36d1dc, #5b86e5);
      -webkit-background-clip: text;
      color: transparent;
      text-shadow: 0 0 10px rgba(54, 209, 220, 0.4);
      letter-spacing: 1px;
    }
  }
  
  .growth-indicator {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    
    .growth-title {
      font-size: 13px;
      color: rgba(255, 255, 255, 0.8);
      letter-spacing: 0.5px;
      margin-bottom: 5px;
    }
    
    .growth-value {
      font-size: 22px;
      font-weight: bold;
      
      &.positive {
        color: #36d1dc;
        text-shadow: 0 0 10px rgba(54, 209, 220, 0.4);
      }
      
      &.negative {
        color: #ff6e76;
        text-shadow: 0 0 10px rgba(255, 110, 118, 0.4);
      }
    }
  }
}

.content-container {
  display: flex;
  gap: 15px;
  margin-bottom: 10px;
  
  @media (max-width: 768px) {
    flex-direction: column;
  }
}

.resource-column {
  width: 40%;
  display: flex;
  flex-direction: column;
  gap: 15px;
  
  @media (max-width: 768px) {
    width: 100%;
  }
}

.chart-column {
  width: 60%;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(59, 141, 255, 0.1);
  padding: 8px;
  display: flex;
  flex-direction: column;
  height: 170px;
  max-height: 170px;
  
  @media (max-width: 768px) {
    width: 100%;
    min-height: 170px;
    max-height: 170px;
  }
  
  .chart-title {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.8);
    margin-bottom: 5px;
    font-weight: 600;
    letter-spacing: 0.5px;
  }
  
  .bar-chart {
    flex: 1;
    width: 100%;
    height: calc(100% - 20px);
    min-height: 140px;
  }
}

.category-card {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
  padding: 6px 8px;
  height: 75px;
  max-height: 75px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  border: 1px solid rgba(59, 141, 255, 0.1);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(59, 141, 255, 0.15);
    border-color: rgba(59, 141, 255, 0.3);
  }
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, 
      rgba(255, 255, 255, 0.05) 0%, 
      rgba(255, 255, 255, 0.02) 40%, 
      rgba(255, 255, 255, 0) 100%);
    z-index: 1;
    pointer-events: none;
  }
  
  .category-icon {
    width: 28px;
    height: 28px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 5px;
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.05));
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    
    i {
      color: white;
      font-size: 12px;
    }
  }
  
  .category-info {
    display: flex;
    flex-direction: column;
    margin-bottom: 5px;
    z-index: 2;
    
    .category-name {
      font-size: 11px;
      color: rgba(255, 255, 255, 0.8);
      margin-bottom: 2px;
      letter-spacing: 0.5px;
    }
    
    .category-count {
      font-size: 16px;
      font-weight: bold;
      color: white;
      letter-spacing: 0.5px;
    }
  }
  
  .category-progress {
    height: 4px;
    width: 100%;
    background-color: rgba(255, 255, 255, 0.1);
    border-radius: 2px;
    overflow: hidden;
    z-index: 2;
    position: relative;
    
    .progress-bar {
      height: 100%;
      border-radius: 3px;
      transition: width 0.5s ease;
      position: relative;
      overflow: hidden;
      
      &::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, 
          rgba(255, 255, 255, 0.1), 
          rgba(255, 255, 255, 0.2), 
          rgba(255, 255, 255, 0.1));
        animation: shimmer 2s infinite;
        transform: translateX(-100%);
      }
    }
  }
}

@keyframes shimmer {
  100% {
    transform: translateX(100%);
  }
}
</style> 