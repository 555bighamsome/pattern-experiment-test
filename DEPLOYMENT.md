# 部署到新仓库的步骤

## 方法 1: 使用 Git 命令（推荐）

### 步骤 1: 创建新的 GitHub 仓库

1. 访问 GitHub: https://github.com/new
2. 创建一个新仓库，例如 `pattern-experiment-test`
3. **不要**初始化 README、.gitignore 或 license（保持空仓库）
4. 复制新仓库的 URL，例如：`https://github.com/YOUR_USERNAME/pattern-experiment-test.git`

### 步骤 2: 在终端中执行以下命令

```bash
# 进入项目目录
cd /Users/mac/pattern_experiment-2

# 检查当前的远程仓库
git remote -v

# 添加新的远程仓库（命名为 test）
git remote add test https://github.com/YOUR_USERNAME/pattern-experiment-test.git

# 推送当前分支到新仓库
git push test main

# 或者如果你想推送所有分支和标签
git push test --all
git push test --tags
```

### 步骤 3: 验证

访问你的新仓库 URL，确认文件已经上传。

---

## 方法 2: 创建一个新的独立副本

如果你想创建一个完全独立的仓库副本：

```bash
# 创建一个新的目录
cd /Users/mac
mkdir pattern-experiment-test
cd pattern-experiment-test

# 从原项目复制所有文件（排除 .git 目录）
rsync -av --exclude='.git' /Users/mac/pattern_experiment-2/ .

# 初始化新的 git 仓库
git init
git add .
git commit -m "Initial commit: Pattern DSL Experiment"

# 连接到新的 GitHub 仓库
git remote add origin https://github.com/YOUR_USERNAME/pattern-experiment-test.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

---

## 方法 3: 使用 GitHub 的 Fork 或 Import 功能

### 使用 GitHub Import:

1. 访问：https://github.com/new/import
2. 输入原仓库 URL：`https://github.com/555bighamsome/pattern_experiment`
3. 为新仓库命名，例如：`pattern-experiment-test`
4. 选择公开或私有
5. 点击 "Begin import"

---

## 方法 4: 使用提供的部署脚本

运行项目中的部署脚本：

```bash
cd /Users/mac/pattern_experiment-2
chmod +x deploy_to_new_repo.sh
./deploy_to_new_repo.sh
```

按照提示输入新仓库的 URL。

---

## 配置 GitHub Pages（可选）

如果你想将这个测试页面部署为在线可访问的网站：

1. 进入新仓库的 Settings
2. 找到 "Pages" 部分
3. Source 选择 "Deploy from a branch"
4. Branch 选择 "main" 和 "/ (root)"
5. 点击 Save

几分钟后，你的网站将可以通过以下地址访问：
```
https://YOUR_USERNAME.github.io/pattern-experiment-test/
```

### GitHub Pages 访问路径：
- 首页：`https://YOUR_USERNAME.github.io/pattern-experiment-test/`
- 演示指南：`https://YOUR_USERNAME.github.io/pattern-experiment-test/demo_guide.html`
- 测试面板：`https://YOUR_USERNAME.github.io/pattern-experiment-test/test_conditions.html`

---

## 常见问题

### Q: 推送时要求身份验证
A: 你可能需要配置 GitHub Personal Access Token：
1. 访问 GitHub Settings → Developer settings → Personal access tokens
2. 创建一个新的 token，勾选 `repo` 权限
3. 使用 token 作为密码进行推送

### Q: 想要保留原仓库的提交历史
A: 使用方法 1，它会保留所有的 git 历史记录

### Q: 想要一个全新的开始
A: 使用方法 2，它会创建一个新的 git 历史

### Q: 推送失败
A: 确保新仓库是空的，没有初始化任何文件

---

## 推荐配置

部署后，建议在新仓库中：

1. 创建一个 README.md 文件说明这是测试版本
2. 在 GitHub Pages 中启用网站
3. 更新项目中的邮箱地址（如果需要）
4. 添加 .gitignore 文件（如果还没有）

---

## 测试部署

部署完成后，访问以下页面测试：

1. `demo_guide.html` - 查看实验流程演示
2. `test_conditions.html` - 测试条件切换
3. `index.html` - 开始实验

确保所有功能正常工作！
