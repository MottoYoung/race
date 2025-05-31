<template>
  <div class="chart-container" ref="chartContainer"></div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue';
import * as echarts from 'echarts';

export default {
  name: 'LessonsChart',
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
          formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        legend: {
          orient: 'vertical',
          right: 10,
          top: 'center',
          textStyle: {
            color: '#fff'
          },
          itemWidth: 10,
          itemHeight: 10
        },
        series: [
          {
            name: '教案类型',
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            itemStyle: {
              borderRadius: 10,
              borderColor: '#031339',
              borderWidth: 2
            },
            label: {
              show: false,
              position: 'center'
            },
            emphasis: {
              label: {
                show: true,
                fontSize: '18',
                fontWeight: 'bold',
                color: '#fff'
              }
            },
            labelLine: {
              show: false
            },
            data: [
              { value: 148, name: '语文' },
              { value: 112, name: '数学' },
              { value: 95, name: '英语' },
              { value: 78, name: '物理' },
              { value: 65, name: '化学' },
              { value: 55, name: '生物' },
              { value: 40, name: '历史' },
              { value: 38, name: '地理' }
            ],
            color: ['#36d1dc', '#5b86e5', '#5654de', '#6a7bff', '#8884ff', '#b48def', '#d88cd0', '#ff8ab4']
          }
        ]
      };

      chart.setOption(option);
      
      // 添加定时器，每隔10秒更新一次数据
      const updateData = () => {
        const newData = option.series[0].data.map(item => {
          return {
            name: item.name,
            value: Math.floor(item.value * (0.9 + Math.random() * 0.2))
          };
        });
        
        chart.setOption({
          series: [{
            data: newData
          }]
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
}
</style> 