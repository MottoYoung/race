<template>
    <!-- 第一行 -->
    <div class="module-box">
      <div style="flex: 0 1 20%">
        <piechart />
      </div>
      <div style="flex: 0 1 20%">
        <radarchart />

      </div>
      <div style="flex: 0 1 40%">
        <div demo-bg>
          <dv-border-box8 :dur="5" style="width: 100%;height: 380px;">
              <capsulechart />
              <div class="d-flex" style="height: 200px;padding: 0 20px;">
                <gaugechart />
                <waterchart />
              </div>
          </dv-border-box8>
        </div>

      </div>
      <div style="flex: 0 1 20%">
            <scrollboard/>
      </div>




    </div>
</template>
<script setup>
import { colorPickerContextKey } from 'element-plus';
import {ref,reactive} from 'vue'
import piechart from './low-charts/piechart.vue'
import radarchart from './low-charts/radarchart.vue'
import scrollboard from './low-charts/scrollboard.vue'
import capsulechart from './low-charts/capsulechart.vue'
import gaugechart from './low-charts/gaugechart.vue'
import waterchart from './low-charts/water.vue'


</script>