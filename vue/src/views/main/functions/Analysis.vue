<template>
  <div>
    <el-card>
      <el-input style="width: 240px;margin-right: 10px" v-model="data.name" placeholder="请输入名称查询" prefix-icon="Search"></el-input>
      <el-button type="primary">查询</el-button>
      <el-button type="warning">重置</el-button>
    </el-card>
    <el-card>
      <el-button type="primary">新增</el-button>
      <el-button type="warning">批量删除</el-button>
      <el-button type="info">导入</el-button>
      <el-button type="success">导出</el-button>
      <el-button type="primary" @click="runExe">运行程序</el-button>
    </el-card>
    <div class="card" style="margin-bottom: 5px">
      <el-table :data="data.tableData" stripe>
        <el-table-column label="日期" prop="date" />
        <el-table-column label="名称" prop="name" />
        <el-table-column label="地址" prop="address" />
      </el-table>
    </div>
    <div style="margin-top: 15px">
      <el-pagination
          v-model="data.pageNum"
          @update:current-page="data.pageNum = $event"
          @update:page-size="data.pageSize = $event"
          :page-size="data.pageSize"
          :page-sizes="[5, 10, 15, 20]"
          background
          layout="total, sizes, prev, pager, next, jumper"
          :total="data.total"
      />
    </div>
  </div>
</template>

<script setup>
import { reactive } from "vue";
import axios from 'axios';
import { ElMessage } from 'element-plus';

const data = reactive({
  name: null,
  tableData: [
    { date: '2024-10-11', name: '亲哥哥哥哥', address: '安徽合肥' },
    { date: '2024-10-11', name: '亲哥哥哥哥', address: '安徽合肥' },
    { date: '2024-10-11', name: '亲哥哥哥哥', address: '安徽合肥' }],
  pageNum:1,
  pageSize:10,
  total:47,
})

const runExe = async () => {
  try {
    ElMessage.info('正在执行程序，请稍后...');
    
    // 使用变量定义API基础URL，便于修改
    const apiBaseUrl = 'http://localhost:3000';
    
    const response = await axios.post(`${apiBaseUrl}/api/run-exe`, {
      path: 'F:/test/AI.exe'  // 使用正斜杠替代反斜杠
    });
    
    console.log('程序执行成功:', response.data);
    
    if (response.data.success) {
      ElMessage.success('程序执行成功');
    } else {
      ElMessage.warning('程序执行完成，但可能有警告');
    }
  } catch (error) {
    console.error('执行失败:', error);
    ElMessage.error('程序执行失败: ' + (error.response?.data?.error || error.message));
  }
}
</script>