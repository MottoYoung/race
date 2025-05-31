<template>
    <div class="map-container-wrapper">
      <div id="map-container"></div>
      <div class="map-overlay"></div>
      <div class="tech-grid"></div>
      <div class="map-info">
        <div class="info-item">
          <div class="info-icon">
            <el-icon color="#40e0d0"><LocationInformation /></el-icon>
          </div>
          <div class="info-content"></div>
        </div>
      </div>
    </div>
  </template>


<script setup>
import { onMounted, onUnmounted, ref } from "vue";
import { LocationInformation } from '@element-plus/icons-vue';
import AMapLoader from "@amap/amap-jsapi-loader";

let map = null;

onMounted(() => {
  window._AMapSecurityConfig = {
    securityJsCode: "abd0caf620f3b3cafa43a34f587e75cb",
  };
  AMapLoader.load({
    key: "151645771f8808a6a210c1040276a79f", // 申请好的Web端开发者Key，首次调用 load 时必填
    version: "2.0", // 指定要加载的 JSAPI 的版本，缺省时默认为 1.4.15
    plugins: ["AMap.Scale","AMap.ToolBar","AMap.Geolocation"], //需要使用的的插件列表，如比例尺'AMap.Scale'，支持添加多个如：['...','...']
  })
    .then((AMap) => {
      // 中国石油大学（华东）唐岛湾校区坐标
      const upcCoordinates = [120.176394, 35.945718];
      
      map = new AMap.Map("map-container", {
        // 设置地图容器id
        viewMode: "3D", // 是否为3D地图模式
        zoom: 16, // 初始化地图级别
        center: upcCoordinates, 
        mapStyle: 'amap://styles/purple', // 使用紫色主题，更符合网站风格
        features: ['bg', 'building', 'road'],
        pitch: 35, // 倾斜角度
      });

      // 添加工具栏
      let toolbar = new AMap.ToolBar({
        position: 'RB',
        offset: new AMap.Pixel(20, 20),
        theme: "dark"
      });
      map.addControl(toolbar);

      // 添加比例尺
      let scale = new AMap.Scale({
        position: 'LB',
        theme: "dark"
      });
      map.addControl(scale);

      // 添加定位控件 - 移至左上角避免重叠
      let geo_location = new AMap.Geolocation({
        position: 'LT',
        offset: new AMap.Pixel(20, 20),
        zoomToAccuracy: true,
        showButton: true,
        theme: "dark"
      });
      map.addControl(geo_location);

      // 添加学校位置标记
      const marker = new AMap.Marker({
        position: upcCoordinates,
        title: 'AI教师备课智能辅助系统',
        icon: 'https://webapi.amap.com/theme/v1.3/markers/n/mark_r.png', // 紫红色标记
        animation: 'AMAP_ANIMATION_DROP',
        anchor: 'bottom-center',
        clickable: true
      });
      map.add(marker);

      // 添加信息窗体
      const infoWindow = new AMap.InfoWindow({
        content: `<div style="padding:10px;background:#6557ec;color:#ffffff;border-radius:5px;border:1px solid #ffffff;">
                    <h3 style="margin:0;color:#ffffff;font-size:14px;">AI教师备课智能辅助系统</h3>
                    <p style="margin:5px 0;font-size:12px;">XXXX大学XXXX校区</p>
                    <p style="margin:5px 0;font-size:12px;">电话: 010-12345678</p>
                  </div>`,
        offset: new AMap.Pixel(0, -30)
      });

      // 鼠标点击标记时打开信息窗体
      marker.on('click', () => {
        infoWindow.open(map, marker.getPosition());
      });
      
      // 自动打开信息窗口
      infoWindow.open(map, marker.getPosition());
    })
    .catch((e) => {
      console.log(e);
    });
});

onUnmounted(() => {
  map?.destroy();
});
</script>

<style scoped>
.map-container-wrapper {
  position: relative;
  width: 100%;
  height: 500px;
  overflow: hidden;
}

#map-container {
  padding: 0;
  margin: 0;
  width: 100%;
  height: 100%;
  transition: all 0.3s ease;
}

.map-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to bottom, rgba(78, 67, 206, 0.2), transparent);
  pointer-events: none;
  z-index: 10;
}

.tech-grid {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    linear-gradient(rgba(255, 255, 255, 0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.05) 1px, transparent 1px);
  background-size: 30px 30px;
  z-index: 5;
  pointer-events: none;
  animation: gridMove 20s linear infinite;
}

.map-info {
  position: absolute;
  bottom: 20px;
  left: 20px;
  z-index: 15;
  background: rgba(78, 67, 206, 0.8);
  border-radius: 8px;
  padding: 10px 15px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(5px);
}

.info-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.info-icon {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.info-content {
  color: #ffffff;
  font-size: 14px;
}

@keyframes gridMove {
  0% {
    transform: translateY(0);
  }
  100% {
    transform: translateY(30px);
  }
}

:deep(.amap-logo) {
  opacity: 0.5 !important;
}

:deep(.amap-copyright) {
  opacity: 0.5 !important;
}
</style>