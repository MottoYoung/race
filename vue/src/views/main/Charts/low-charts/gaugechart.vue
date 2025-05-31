<template>
<div style="flex: 2">
                  <div>
                    <i style="margin-right: 8px;">😘</i>
                    渠道分析
                  </div>
                  <div>
                    <dv-capsule-chart :config="config" style="width: 100%;height: 200px;"/>
                  </div>
                </div>
    </template>
    
    <script setup>
    import {ref,reactive} from "vue";
    
    const config = reactive({
  data: [
    {
      name: '南阳',
      value: 167
    },
    {
      name: '周口',
      value: 123
    },
    {
      name: '漯河',
      value: 98
    },
    {
      name: '郑州',
      value: 75
    },
    {
      name: '西峡',
      value: 66
    },
  ],
  colors: ['#e062ae', '#fb7293', '#e690d1', '#32c5e9', '#96bfff'],
  labelNum: 8,
})
    </script>