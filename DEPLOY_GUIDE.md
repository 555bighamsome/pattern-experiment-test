# 🚀 部署到测试仓库 - 快速指南

已为你准备了完整的部署方案！以下是三种推荐的方法：

---

## 🎯 方法 1: 自动化脚本部署（最简单）

### 步骤：

1. **运行快速部署脚本**
```bash
cd /Users/mac/pattern_experiment-2
./quick_deploy.sh
```

这个脚本会：
- ✅ 创建一个独立的项目副本（不包含 git 历史）
- ✅ 自动初始化新的 git 仓库
- ✅ 创建初始提交
- ✅ 设置好 README.md
- ✅ 准备好推送到 GitHub

2. **在 GitHub 创建新仓库**
   - 访问：https://github.com/new
   - 仓库名：`pattern-experiment-test`（或你喜欢的名字）
   - ⚠️ **不要**勾选"Add a README file"
   - 点击 "Create repository"

3. **推送到 GitHub**
```bash
cd /Users/mac/pattern-experiment-test
git remote add origin https://github.com/YOUR_USERNAME/pattern-experiment-test.git
git push -u origin main
```

---

## 🔄 方法 2: 保留历史记录部署

如果你想保留所有 git 提交历史：

```bash
cd /Users/mac/pattern_experiment-2

# 添加新的远程仓库
git remote add test https://github.com/YOUR_USERNAME/pattern-experiment-test.git

# 推送当前分支
git push test main
```

---

## 📦 方法 3: 使用脚本一键部署

```bash
cd /Users/mac/pattern_experiment-2
./deploy_to_new_repo.sh
```

按照提示输入新仓库的 URL，脚本会自动完成推送。

---

## 🌐 启用 GitHub Pages

推送成功后，启用 GitHub Pages 让实验在线可访问：

1. 进入你的新仓库页面
2. 点击 **Settings** 标签
3. 在左侧菜单找到 **Pages**
4. 在 "Source" 下：
   - 选择 **Deploy from a branch**
   - Branch: **main**
   - Folder: **/ (root)**
5. 点击 **Save**

几分钟后，你的网站将在以下地址可用：
```
https://YOUR_USERNAME.github.io/pattern-experiment-test/
```

---

## 📂 你将得到的文件

新仓库将包含以下关键文件：

### 核心文件
- `index.html` - 实验入口
- `demo_guide.html` - 演示指南（推荐用于展示）
- `test_conditions.html` - 测试面板
- `README.md` - 完整的项目文档

### 脚本文件
- `deploy_to_new_repo.sh` - 部署脚本
- `quick_deploy.sh` - 快速部署脚本
- `DEPLOYMENT.md` - 详细部署文档

### 实验文件
- `routes/` - 所有实验页面
- `js/` - JavaScript 代码
- `css/` - 样式文件

---

## ✅ 验证部署

部署完成后，测试以下页面：

1. **演示指南**
   ```
   https://YOUR_USERNAME.github.io/pattern-experiment-test/demo_guide.html
   ```
   查看两种条件的对比和快速启动按钮

2. **测试面板**
   ```
   https://YOUR_USERNAME.github.io/pattern-experiment-test/test_conditions.html
   ```
   手动测试条件切换

3. **实验入口**
   ```
   https://YOUR_USERNAME.github.io/pattern-experiment-test/
   ```
   体验完整实验流程

---

## 🔧 常见问题

### Q: 推送时要求用户名和密码
**A**: 使用 Personal Access Token（PAT）代替密码：
1. 访问 GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. 生成新 token，勾选 `repo` 权限
3. 复制 token
4. 推送时，用户名填你的 GitHub 用户名，密码填 token

### Q: 推送失败，提示 rejected
**A**: 确保新仓库是空的，没有初始化 README 或其他文件

### Q: GitHub Pages 404 错误
**A**: 
- 等待几分钟，GitHub Pages 需要时间构建
- 确保 index.html 在根目录
- 检查 Settings → Pages 是否正确配置

### Q: 想要更新测试仓库的内容
**A**: 如果使用方法 1，重新运行脚本会创建新副本。如果使用方法 2：
```bash
cd /Users/mac/pattern_experiment-2
git push test main
```

---

## 📧 分享给他人

部署完成后，你可以分享以下链接：

**给参与者（开始实验）：**
```
https://YOUR_USERNAME.github.io/pattern-experiment-test/
```

**给合作者（查看演示）：**
```
https://YOUR_USERNAME.github.io/pattern-experiment-test/demo_guide.html
```

**给开发者（测试功能）：**
```
https://YOUR_USERNAME.github.io/pattern-experiment-test/test_conditions.html
```

---

## 🎉 完成！

选择一个方法开始部署吧！推荐使用**方法 1**（quick_deploy.sh），最简单直接。

如有问题，查看 `DEPLOYMENT.md` 获取详细文档。
