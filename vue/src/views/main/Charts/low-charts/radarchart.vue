<template>
   <div demo-bg>
            <dv-border-box12 style="width: 100%;height: 380px;padding: 0 20px;">
                    <dv-charts :option="option1" style="width:100%;height:350px;"/>
            </dv-border-box12>
        </div>
</template>

<script setup>
import {ref,reactive} from "vue";

const option1 = {
    title: {
        text: '畅销饮料占比雷达图',
        style: {
        fill: '#fff',
        fontSize:14,
        
    }
    },
  radar: {
    indicator: [
      { name: '西峡', max: 300 },
      { name: '周口', max: 300 },
      { name: '南阳', max: 300 },
      { name: '驻马店', max: 300 },
      { name: '郑州', max: 300 },
      { name: '洛阳', max: 300 }
    ],
    polygon: true,
    splitLine: {
      style: {
        stroke: 'rgba(159, 230, 184, 1)'
      }
    },
    axisLine: {
      style: {
        stroke: 'rgba(159, 230, 184, 1)'
      }
    },
    axisLabel: {
        style: {
            fill: '#fff',
        }
    },
    splitArea: {
      show: true,
      color: ['rgba(159, 230, 184, .2)', 'rgba(251, 114, 147, .2)']
    }
  },
  series: [
    {
      type: 'radar',
      data: [111, 256, 178, 152, 266, 132],
      animationCurve: 'easeInOutBack'
    }
  ]
}
</script>