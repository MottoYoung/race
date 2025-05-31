<template>
    <!-- 第二行 -->
    <div class="module-box">
        <div style="flex:0 1 50%">
            <barchart />
        </div>
        <div style="flex:0 1 50%">
            <div demo-bg>
                <dv-border-box13 style="width: 100%;height: 350px;">
                <div dv-bg>
                    dv-border-box-13
                </div>
                </dv-border-box13>
            </div>
        </div>
    </div>
</template>
<script setup>
import {ref,reactive} from 'vue'
import barchart from './low-charts/barchart.vue'
</script>