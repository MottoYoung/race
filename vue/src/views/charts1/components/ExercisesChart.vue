<template>
  <div class="chart-container" ref="chartContainer"></div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue';
import * as echarts from 'echarts';

export default {
  name: 'ExercisesChart',
  setup() {
    const chartContainer = ref(null);
    let chart = null;

    const initChart = () => {
      if (!chartContainer.value) return;
      
      chart = echarts.init(chartContainer.value);
      
      // 模拟数据
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        legend: {
          data: ['选择题', '填空题', '简答题'],
          textStyle: {
            color: '#fff'
          },
          top: 10
        },
        grid: {
          left: '3%',
          right: '5%',
          bottom: '3%',
          top: '20%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: ['语文', '数学', '英语', '物理', '化学', '生物'],
          axisLine: {
            lineStyle: {
              color: 'rgba(255, 255, 255, 0.3)'
            }
          },
          axisLabel: {
            color: 'rgba(255, 255, 255, 0.7)'
          }
        },
        yAxis: {
          type: 'value',
          name: '数量',
          nameTextStyle: {
            color: 'rgba(255, 255, 255, 0.7)'
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
            name: '选择题',
            type: 'bar',
            stack: 'total',
            emphasis: {
              focus: 'series'
            },
            itemStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: '#36d1dc' },
                { offset: 1, color: '#5b86e5' }
              ])
            },
            data: [120, 132, 101, 134, 90, 70]
          },
          {
            name: '填空题',
            type: 'bar',
            stack: 'total',
            emphasis: {
              focus: 'series'
            },
            itemStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: '#6a7bff' },
                { offset: 1, color: '#8884ff' }
              ])
            },
            data: [220, 182, 191, 234, 290, 150]
          },
          {
            name: '简答题',
            type: 'bar',
            stack: 'total',
            emphasis: {
              focus: 'series'
            },
            itemStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: '#b48def' },
                { offset: 1, color: '#d88cd0' }
              ])
            },
            data: [150, 232, 201, 154, 190, 80]
          }
        ]
      };

      chart.setOption(option);
      
      // 添加定时器，每隔10秒更新一次数据
      const updateData = () => {
        const newData1 = option.series[0].data.map(() => Math.floor(Math.random() * 100) + 50);
        const newData2 = option.series[1].data.map(() => Math.floor(Math.random() * 150) + 100);
        const newData3 = option.series[2].data.map(() => Math.floor(Math.random() * 100) + 100);
        
        chart.setOption({
          series: [
            { data: newData1 },
            { data: newData2 },
            { data: newData3 }
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
}
</style> 