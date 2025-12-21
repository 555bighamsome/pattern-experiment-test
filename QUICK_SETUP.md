# 快速集成步骤（简化版）

## 🚀 只需 6 个步骤！

### 步骤 1：在 cPanel 创建数据库（5分钟）

1. 登录 cPanel → 点击 "MySQL Databases"
2. 创建数据库：`experiment_db`
3. 创建用户：`exp_user`（用 Password Generator 生成密码并保存）
4. 关联用户和数据库（ALL PRIVILEGES）

---

### 步骤 2：创建数据表（2分钟）

1. 打开 phpMyAdmin → 选择你的数据库 → 点击 SQL
2. 粘贴并执行：

```sql
CREATE TABLE experiment_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    participant_id VARCHAR(100),
    condition VARCHAR(50),
    submission_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    task_data JSON,
    freeplay_data JSON,
    user_agent TEXT,
    screen_resolution VARCHAR(50)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

### 步骤 3：配置并上传 PHP 文件（5分钟）

1. 打开 `save_data.php`
2. 修改这 4 行：
   ```php
   header('Access-Control-Allow-Origin: https://555bighamsome.github.io');
   $db_name = 'yourusername_experiment_db';  // 你的数据库名
   $db_user = 'yourusername_exp_user';        // 你的用户名
   $db_pass = '你的密码';                      // 步骤1的密码
   ```
3. 上传到 cPanel File Manager 的 `public_html/api/` 文件夹
4. 记录 URL：`https://yourdomain.com/api/save_data.php`

---

### 步骤 4：配置前端（2分钟）

1. 打开 `js/dataSubmission.js`
2. 修改第 4 行：
   ```javascript
   const API_ENDPOINT = 'https://yourdomain.com/api/save_data.php';
   ```

---

### 步骤 5：引入脚本（1分钟）

在 `routes/task.html` 和 `routes/freeplay.html` 的 `</body>` 前添加：

```html
<script src="../js/dataSubmission.js"></script>
```

---

### 步骤 6：测试（5分钟）

1. 提交代码到 GitHub
2. 访问你的网站完成一个测试
3. 在 phpMyAdmin 检查 `experiment_data` 表
4. 看到数据 = 成功！✅

---

## 📊 查看数据

随时在 phpMyAdmin 中查看：
1. 选择数据库 → 点击 `experiment_data` → Browse
2. Export → CSV/JSON 下载所有数据

---

## ❓ 需要帮助？

告诉我你卡在哪一步！
