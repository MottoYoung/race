-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS smartprep DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE smartprep;

-- 创建用户表
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('student', 'teacher', 'admin') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建管理员账户（默认账户名和密码都是admin）
-- 注意：在实际生产环境中，应该使用更安全的密码存储方式
INSERT INTO users (email, password, role) VALUES ('admin', 'admin', 'admin')
ON DUPLICATE KEY UPDATE password = 'admin12345';

-- 添加索引
CREATE INDEX idx_email_role ON users(email, role); 