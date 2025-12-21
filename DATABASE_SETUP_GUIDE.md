# 数据库集成完整指南

## 📋 目录
1. [配置 cPanel 数据库](#步骤1-配置-cpanel-数据库)
2. [上传 PHP 文件](#步骤2-上传-php-文件)
3. [集成前端代码](#步骤3-集成前端代码)
4. [测试系统](#步骤4-测试系统)
5. [查看和导出数据](#步骤5-查看和导出数据)

---

## 步骤1: 配置 cPanel 数据库

### 1.1 创建数据库
1. 登录 cPanel
2. 找到 **"MySQL Databases"**
3. 创建数据库，名称例如：`experiment_db`
4. **记录完整名称**（可能是 `username_experiment_db`）

### 1.2 创建数据库用户
1. 在同一页面创建用户，例如：`exp_user`
2. 使用 Password Generator 生成密码
3. **重要：保存这个密码！**

### 1.3 关联用户和数据库
1. 在 "Add User To Database" 部分选择用户和数据库
2. 授予 **ALL PRIVILEGES**

### 1.4 创建数据表
1. 打开 **phpMyAdmin**
2. 选择你的数据库
3. 点击 **SQL** 标签
4. 执行以下 SQL：

```sql
CREATE TABLE experiment_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    participant_id VARCHAR(100) NOT NULL,
    condition VARCHAR(50) NOT NULL,
    submission_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    task_data JSON,
    freeplay_data JSON,
    user_agent TEXT,
    screen_resolution VARCHAR(50),
    INDEX idx_participant (participant_id),
    INDEX idx_condition (condition),
    INDEX idx_time (submission_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

## 步骤2: 上传 PHP 文件

### 2.1 修改 save_data.php
打开 `save_data.php`，修改这些行：

```php
// 第 7 行：你的前端域名
header('Access-Control-Allow-Origin: https://555bighamsome.github.io');

// 第 21-24 行：数据库配置
$db_host = 'localhost';
$db_name = 'username_experiment_db';  // 你的完整数据库名
$db_user = 'username_exp_user';       // 你的完整用户名
$db_pass = 'your_password_here';      // 步骤1.2的密码
```

### 2.2 上传到服务器
1. 在 cPanel 打开 **File Manager**
2. 进入 `public_html` 文件夹
3. 创建文件夹 `api`（可选）
4. 上传 `save_data.php`
5. **记录 URL**，例如：`https://yourdomain.com/api/save_data.php`

### 2.3 测试 PHP 文件
在浏览器访问：`https://yourdomain.com/api/save_data.php`

应该看到错误消息（因为没有 POST 数据），这是正常的 ✅

---

## 步骤3: 集成前端代码

### 3.1 修改 dataSubmission.js
打开 `js/dataSubmission.js`，修改第 4 行：

```javascript
const API_ENDPOINT = 'https://yourdomain.com/api/save_data.php';  // 你的 PHP URL
```

### 3.2 在 HTML 中引入脚本

**修改 `routes/task.html`**，在 `</body>` 前添加：
```html
<script src="../js/dataSubmission.js"></script>
```

**修改 `routes/freeplay.html`**，在 `</body>` 前添加：
```html
<script src="../js/dataSubmission.js"></script>
```

### 3.3 修改下载函数为自动提交

**选项 A：完全替换（推荐）**
- 用户完成实验后，数据自动提交到服务器
- 不再需要手动下载

**选项 B：双保险（最安全）**
- 先尝试提交到服务器
- 如果失败，自动下载到本地作为备份

我建议使用**选项 B（双保险）**，继续下一步...

---

## 步骤4: 修改 task.js 和 freeplay.js

### 4.1 修改 task.js 的下载函数

找到 `downloadTaskDataOnly()` 函数，替换为：

```javascript
async function downloadTaskDataOnly() {
    let condition = localStorage.getItem('experimentCondition') || 'puzzleFirst';
    condition = normalizeCondition(condition);
    
    // 先尝试提交到服务器
    try {
        showToast('Saving data to server...', 'info');
        
        const result = await submitCombinedData();
        
        if (result && result.success) {
            showToast('Data saved successfully! ✓', 'success', 3000);
            // 数据已保存，显示感谢信息
            setTimeout(() => {
                alert('Thank you! Your data has been saved successfully.');
            }, 500);
            return;
        }
    } catch (error) {
        console.error('Server submission failed:', error);
    }
    
    // 如果服务器提交失败，使用原来的下载方式作为备份
    showToast('Downloading data as backup...', 'warning');
    
    // 原来的下载代码...
    const sanitizedTrials = allTrialsData.map(sanitizeTrialRecord).filter(Boolean);
    const experimentData = {
        metadata: {
            experimentName: 'Pattern DSL Experiment (Task Only)',
            experimentCondition: condition,
            completionTime: new Date().toISOString(),
            browserInfo: { language: navigator.language },
            includesFreePlay: false
        },
        taskData: {
            trials: sanitizedTrials,
            summary: {
                totalTrials: sanitizedTrials.length,
                successfulTrials: sanitizedTrials.filter(t => t && t.success === true).length
            }
        }
    };

    const jsonString = JSON.stringify(experimentData, null, 2);
    const blob = new Blob([jsonString], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
    link.download = `pattern_experiment_task_only_${timestamp}.json`;
    link.href = url;
    link.click();
    URL.revokeObjectURL(url);
    
    showToast('Please email this file to the researcher', 'warning', 5000);
}
```

### 4.2 类似修改 freeplay.js 的下载函数

（代码类似，我可以帮你完成）

---

## 步骤5: 测试系统

### 5.1 本地测试
1. 提交所有代码到 GitHub
2. 访问你的 GitHub Pages 网站
3. 完成一个简短的测试实验
4. 检查 console 是否有错误

### 5.2 检查数据库
1. 打开 cPanel 的 phpMyAdmin
2. 选择你的数据库
3. 点击 `experiment_data` 表
4. 点击 "Browse" 查看数据
5. 应该能看到刚才提交的测试数据 ✅

---

## 步骤6: 导出数据

### 方法 1：phpMyAdmin 导出
1. 在 phpMyAdmin 选择表
2. 点击 "Export"
3. 选择格式（CSV 或 JSON）
4. 下载

### 方法 2：创建管理面板（可选）
我可以帮你创建一个简单的 PHP 管理页面来查看和导出数据

---

## 🎯 下一步做什么？

请告诉我你现在到了哪一步，我会帮你继续：

1. ✅ 我已经创建了数据库（告诉我数据库名和URL）
2. ✅ 我已经上传了 PHP 文件（告诉我 PHP 的 URL）
3. ❓ 我需要帮助修改前端代码
4. ❓ 我需要测试系统
5. ❓ 我需要管理面板

---

## ⚠️ 重要提示

### 安全性
- ✅ PHP 文件已经包含基本的安全措施
- ✅ CORS 限制只允许你的域名访问
- ✅ 使用 PDO 预处理语句防止 SQL 注入

### 备份
- 定期备份数据库
- 保留本地下载功能作为备份

### 测试
- 先在测试环境运行
- 至少测试两个完整的实验流程（puzzleFirst 和 freeplayFirst）
