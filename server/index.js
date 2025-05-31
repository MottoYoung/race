const express = require('express');
const { exec } = require('child_process');
const cors = require('cors');
const app = express();

// 配置CORS，允许所有来源的请求
app.use(cors({
  origin: '*',
  methods: ['GET', 'POST'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));
app.use(express.json());

app.post('/api/run-exe', (req, res) => {
  const { path } = req.body;
  
  exec(path, (error, stdout, stderr) => {
    if (error) {
      console.error(`执行错误: ${error}`);
      return res.status(500).json({ error: error.message });
    }
    res.json({ 
      success: true, 
      output: stdout,
      error: stderr 
    });
  });
});

const PORT = 2200;
app.listen(PORT, () => {
  console.log(`服务器运行在 http://localhost:${PORT}`);
});