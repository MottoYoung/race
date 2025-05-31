<template>
  <div class="chart-container" ref="chartContainer">
    <div class="chart-title">多媒体资源生成量</div>
    <div class="media-type-indicators">
      <div class="indicator img-indicator">
        <div class="icon"><i class="icon-image"></i></div>
        <div class="label">图片素材</div>
      </div>
      <div class="indicator video-indicator">
        <div class="icon"><i class="icon-video"></i></div>
        <div class="label">视频资源</div>
      </div>
      <div class="indicator ppt-indicator">
        <div class="icon"><i class="icon-ppt"></i></div>
        <div class="label">PPT模板</div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue';
import * as echarts from 'echarts';

export default {
  name: 'MediaChart',
  setup() {
    const chartContainer = ref(null);
    let chart = null;

    const initChart = () => {
      if (!chartContainer.value) return;
      
      chart = echarts.init(chartContainer.value);
      
      // 模拟数据
      const option = {
        tooltip: {
          trigger: 'item',
          formatter: '<div style="font-size:12px;font-weight:bold">{b}</div><div style="display:flex;justify-content:space-between;align-items:center;margin:8px 0"><span style="display:inline-block;width:10px;height:10px;border-radius:50%;background-color:{color}"></span><span style="font-size:14px;font-weight:bold">{c}个</span></div><div style="font-size:10px;color:#8f9bb3">占比 {d}%</div>',
          backgroundColor: 'rgba(3, 19, 57, 0.9)',
          borderColor: 'rgba(59, 141, 255, 0.3)',
          textStyle: {
            color: '#fff',
            fontSize: 12
          },
          borderWidth: 1,
          padding: 10,
          extraCssText: 'box-shadow: 0 0 10px rgba(59, 141, 255, 0.2); border-radius: 4px;'
        },
        legend: {
          show: true,
          bottom: '5%',
          textStyle: {
            color: '#36d1dc',
            fontSize: 10
          },
          icon: 'circle',
          itemWidth: 8,
          itemHeight: 8,
          itemGap: 15
        },
        series: [
          {
            name: '多媒体资源',
            type: 'pie',
            radius: ['42%', '70%'],
            center: ['50%', '45%'],
            avoidLabelOverlap: true,
            itemStyle: {
              borderColor: '#031339',
              borderWidth: 2
            },
            label: {
              show: false,
              position: 'center',
              formatter: '{total|{c}}\n{name|{b}}',
              rich: {
                total: {
                  fontSize: 22,
                  fontWeight: 'bold',
                  color: '#36d1dc',
                  padding: [0, 0, 5, 0]
                },
                name: {
                  fontSize: 12,
                  color: '#5b86e5'
                }
              }
            },
            emphasis: {
              label: {
                show: true
              },
              itemStyle: {
                shadowBlur: 15,
                shadowOffsetX: 0,
                shadowColor: 'rgba(59, 141, 255, 0.5)'
              }
            },
            labelLine: {
              show: false
            },
            animationType: 'scale',
            animationEasing: 'elasticOut',
            animationDelay: function (idx) {
              return Math.random() * 200;
            },
            data: [
              {
                value: 113,
                name: '图片素材',
                itemStyle: {
                  color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    { offset: 0, color: '#36d1dc' },
                    { offset: 1, color: '#5b86e5' }
                  ])
                }
              },
              {
                value: 75,
                name: '视频资源',
                itemStyle: {
                  color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    { offset: 0, color: '#8884ff' },
                    { offset: 1, color: '#d88cd0' }
                  ])
                }
              },
              {
                value: 42,
                name: 'PPT模板',
                itemStyle: {
                  color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    { offset: 0, color: '#45cafc' },
                    { offset: 1, color: '#45ecbd' }
                  ])
                }
              }
            ]
          },
          {
            name: '总计',
            type: 'pie',
            radius: ['0%', '35%'],
            center: ['50%', '45%'],
            label: {
              position: 'center',
              formatter: '{total|{c}个}\n{name|总资源量}',
              rich: {
                total: {
                  fontSize: 20,
                  fontWeight: 'bold',
                  color: '#36d1dc',
                  padding: [0, 0, 5, 0],
                  textShadow: '0 0 5px rgba(54, 209, 220, 0.5)'
                },
                name: {
                  fontSize: 12,
                  color: '#5b86e5'
                }
              }
            },
            tooltip: {
              show: false
            },
            itemStyle: {
              color: 'rgba(23, 39, 87, 0.6)',
              borderColor: 'rgba(59, 141, 255, 0.3)',
              borderWidth: 1,
              shadowBlur: 10,
              shadowColor: 'rgba(54, 209, 220, 0.3)'
            },
            emphasis: {
              scale: false
            },
            data: [
              {
                value: 230,
                name: '总计'
              }
            ]
          }
        ]
      };

      chart.setOption(option);
      
      // 添加定时器，每隔10秒更新一次数据
      const updateData = () => {
        const imageCount = Math.floor(Math.random() * 50) + 90; // 90-140
        const videoCount = Math.floor(Math.random() * 30) + 60; // 60-90
        const pptCount = Math.floor(Math.random() * 20) + 30; // 30-50
        const totalCount = imageCount + videoCount + pptCount;
        
        // 更新中心文本显示总数
        chart.setOption({
          series: [
            {
              data: [
                { value: imageCount, name: '图片素材' },
                { value: videoCount, name: '视频资源' },
                { value: pptCount, name: 'PPT模板' }
              ]
            },
            {
              data: [{ value: totalCount, name: '总计' }]
            }
          ]
        });
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
      chartContainer
    };
  }
};
</script>

<style lang="scss" scoped>
.chart-container {
  width: 100%;
  height: 100%;
  position: relative;
  
  &::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background: radial-gradient(circle at center, rgba(54, 209, 220, 0.05) 0%, transparent 70%);
    pointer-events: none;
    animation: pulseGlow 6s ease-in-out infinite;
  }
  
  &::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: 
      linear-gradient(90deg, rgba(54, 209, 220, 0) 0%, rgba(54, 209, 220, 0.03) 50%, rgba(54, 209, 220, 0) 100%);
    background-size: 200% 100%;
    animation: scanEffect 8s linear infinite;
    pointer-events: none;
  }
}

.chart-title {
  position: absolute;
  top: 10px;
  left: 50%;
  transform: translateX(-50%);
  color: #36d1dc;
  font-size: 14px;
  font-weight: bold;
  text-shadow: 0 0 8px rgba(54, 209, 220, 0.5);
  z-index: 10;
}

.media-type-indicators {
  position: absolute;
  top: 10px;
  right: 10px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  z-index: 10;
  
  .indicator {
    display: flex;
    align-items: center;
    background: rgba(3, 19, 57, 0.6);
    border: 1px solid rgba(59, 141, 255, 0.2);
    border-radius: 4px;
    padding: 4px 8px;
    font-size: 10px;
    color: #fff;
    
    .icon {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 16px;
      height: 16px;
      margin-right: 6px;
      
      i {
        display: block;
        width: 14px;
        height: 14px;
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
      }
    }
    
    &.img-indicator .icon i {
      background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%2336d1dc'%3E%3Cpath d='M19,4H5C3.9,4,3,4.9,3,6v12c0,1.1,0.9,2,2,2h14c1.1,0,2-0.9,2-2V6C21,4.9,20.1,4,19,4z M19,18H5V6h14V18z M13.5,10c0,0.83-0.67,1.5-1.5,1.5s-1.5-0.67-1.5-1.5s0.67-1.5,1.5-1.5S13.5,9.17,13.5,10z M5,17h14l-4.5-6l-3,4l-1.5-2L5,17z'/%3E%3C/svg%3E");
    }
    
    &.video-indicator .icon i {
      background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%238884ff'%3E%3Cpath d='M21,3H3C1.9,3,1,3.9,1,5v14c0,1.1,0.9,2,2,2h18c1.1,0,2-0.9,2-2V5C23,3.9,22.1,3,21,3z M21,17H3V5h18V17z M10,8.5v7c0,0.28,0.34,0.42,0.53,0.23l4.5-3.5c0.29-0.23,0.29-0.69,0-0.92l-4.5-3.5C10.34,8.08,10,8.22,10,8.5z'/%3E%3C/svg%3E");
    }
    
    &.ppt-indicator .icon i {
      background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%2345cafc'%3E%3Cpath d='M19,3H5C3.9,3,3,3.9,3,5v14c0,1.1,0.9,2,2,2h14c1.1,0,2-0.9,2-2V5C21,3.9,20.1,3,19,3z M6,17h2v-2h2v2h2v-2h2v2h2v-2h2v2h1v-3H5v3H6z M5,10h14V5H5V10z M13,9H6V6h7V9z'/%3E%3C/svg%3E");
    }
  }
}

@keyframes pulseGlow {
  0%, 100% {
    opacity: 0.5;
  }
  50% {
    opacity: 0.8;
  }
}

@keyframes scanEffect {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}
</style> 