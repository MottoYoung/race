<template>
    <div style="flex: 1;margin-left: 20px;">
                      <dv-water-level-pond :config="config" style="width:200px;height:160px" />
                    </div>
      </template>
      
      <script setup>
      import {ref,reactive} from "vue";
    
      const config = reactive({
      data: [66, 45],
      shape: 'roundRect',
    })
      </script>