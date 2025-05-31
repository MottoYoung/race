<template>
<div class="d-flex" style="height: 180px;padding-top: 10px;">
                <dv-charts :option="option1" />
                <dv-charts :option="option2" />
              </div>
</template>

<script setup>
import {ref,reactive} from "vue";

const option1 = {
  series: [
    {
      type: 'gauge',
      startAngle: -Math.PI / 2,
      endAngle: Math.PI * 1.5,
      arcLineWidth: 20,
      data: [
        { name: 'itemA', value: 65, gradient: ['#ff9f7f', '#1ed3e5', '#2fded6'] }
      ],
      axisLabel: {
        show: false
      },
      axisTick: {
        show: false
      },
      pointer: {
        show: false
      },
      dataItemStyle: {
        lineCap: 'round'
      },
      details: {
        show: true,
        formatter: '{value}%',
        style: {
            fill: '#ff9f7f',
            fontSize: 25
        }
      }
    }
  ]
}
const option2 = {
  series: [
    {
      type: 'gauge',
      startAngle: -Math.PI / 2,
      endAngle: Math.PI * 1.5,
      arcLineWidth: 25,
      data: [
        { name: 'itemA', value: 89, gradient: ['#03c2fd', '#1ed3e5', '#2fded6'] }
      ],
      axisLabel: {
        show: false
      },
      axisTick: {
        show: false
      },
      pointer: {
        show: false
      },
      dataItemStyle: {
        lineCap: 'round'
      },
      details: {
        show: true,
        formatter: '{value}%',
        style: {
            fill: '#1ed3e5',
            fontSize: 35
        }
      }
    }
  ]
}
</script>