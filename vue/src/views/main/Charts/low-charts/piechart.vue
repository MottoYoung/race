<template>
        <div demo-bg>
            <dv-border-box12 style="width: 100%;height: 380px;padding: 0 20px;">
                    <dv-charts :option="option" style="width:100%;height:350px;"/>
            </dv-border-box12>
        </div>
  </template>
  
  <script setup>
  import {ref,reactive} from "vue";

  const option = {
  title: {
    text: '畅销饮料占比饼状图',
    style: {
        fill: '#fff',
        fontSize:14,
        
    }
  },
  color: [
        '#ffdb5c','#ff9f7f','#fb7293','#e062ae','#e7bcf3'
      ],
  series: [
    {
      type: 'pie',
      
      data: [
        { name: '可口可乐', value: 93 },
        { name: '百事可乐', value: 32 },
        { name: '哇哈哈', value: 65 },
        { name: '康师傅', value: 44 },
        { name: '统一', value: 52 },
      ],
      insideLabel: {
        show: true
      },

      roseType: true,
      outsideLabel: {
        labelLineEndLength:10
      }
    }
  ]
}
  </script>