#!/bin/bash

# 快速部署脚本 - 创建独立的测试仓库副本
# Usage: ./quick_deploy.sh

echo "================================================"
echo "  创建独立的测试仓库副本"
echo "================================================"
echo ""

# 设置变量
SOURCE_DIR="/Users/mac/pattern_experiment-2"
TARGET_DIR="/Users/mac/pattern-experiment-test"
REPO_NAME="pattern-experiment-test"

echo "📋 配置："
echo "   源目录: $SOURCE_DIR"
echo "   目标目录: $TARGET_DIR"
echo "   仓库名: $REPO_NAME"
echo ""

# 检查目标目录是否已存在
if [ -d "$TARGET_DIR" ]; then
    echo "⚠️  警告：目标目录已存在"
    echo "是否删除并重新创建？(y/n)"
    read CONFIRM
    
    if [ "$CONFIRM" == "y" ] || [ "$CONFIRM" == "Y" ]; then
        echo "🗑️  删除旧目录..."
        rm -rf "$TARGET_DIR"
    else
        echo "❌ 操作已取消"
        exit 0
    fi
fi

# 创建目标目录
echo "📁 创建目标目录..."
mkdir -p "$TARGET_DIR"

# 复制文件（排除 .git 目录）
echo "📋 复制文件..."
rsync -av --exclude='.git' --exclude='node_modules' --exclude='.DS_Store' "$SOURCE_DIR/" "$TARGET_DIR/"

if [ $? -ne 0 ]; then
    echo "❌ 错误：文件复制失败"
    exit 1
fi

# 进入目标目录
cd "$TARGET_DIR"

# 将 README_TEST.md 重命名为 README.md
if [ -f "README_TEST.md" ]; then
    echo "📝 设置 README..."
    mv README_TEST.md README.md
fi

# 初始化 git 仓库
echo "🔧 初始化 Git 仓库..."
git init

# 添加所有文件
echo "➕ 添加文件到 Git..."
git add .

# 创建初始提交
echo "💾 创建初始提交..."
git commit -m "Initial commit: Pattern DSL Experiment (Test Version)

- Counterbalanced design (puzzleFirst / freeplayFirst)
- Random condition assignment
- Simplified tutorial (12 steps + 5 practice exercises)
- Complete data collection for both phases
- Helper/favorite system with proper isolation
- Dynamic UI based on condition
- Comprehensive testing tools included"

if [ $? -ne 0 ]; then
    echo "❌ 错误：提交失败"
    exit 1
fi

# 设置主分支为 main
git branch -M main

echo ""
echo "✅ 本地仓库创建成功！"
echo ""
echo "================================================"
echo "📝 接下来的步骤："
echo "================================================"
echo ""
echo "1️⃣  在 GitHub 创建新仓库："
echo "   访问: https://github.com/new"
echo "   仓库名建议: $REPO_NAME"
echo "   ⚠️  不要初始化 README、.gitignore 或 license"
echo ""
echo "2️⃣  连接到远程仓库并推送："
echo "   cd $TARGET_DIR"
echo "   git remote add origin https://github.com/YOUR_USERNAME/$REPO_NAME.git"
echo "   git push -u origin main"
echo ""
echo "3️⃣  启用 GitHub Pages（可选）："
echo "   - 进入仓库 Settings → Pages"
echo "   - Source: Deploy from a branch"
echo "   - Branch: main / (root)"
echo "   - Save"
echo ""
echo "4️⃣  访问你的网站："
echo "   https://YOUR_USERNAME.github.io/$REPO_NAME/"
echo ""
echo "================================================"
echo ""

# 显示仓库位置
echo "📍 新仓库位置: $TARGET_DIR"
echo ""

# 询问是否立即打开目录
echo "是否在 Finder 中打开新仓库目录？(y/n)"
read OPEN_FINDER

if [ "$OPEN_FINDER" == "y" ] || [ "$OPEN_FINDER" == "Y" ]; then
    open "$TARGET_DIR"
fi

echo ""
echo "🎉 完成！"
