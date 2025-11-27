#!/bin/bash

# 部署脚本：将项目推送到新的 Git 仓库
# Usage: ./deploy_to_new_repo.sh

echo "================================================"
echo "  Pattern Experiment - 部署到新仓库"
echo "================================================"
echo ""

# 检查是否在 git 仓库中
if [ ! -d .git ]; then
    echo "❌ 错误：当前目录不是一个 git 仓库"
    echo "请在项目根目录运行此脚本"
    exit 1
fi

# 获取新仓库 URL
echo "请输入新仓库的 URL（例如：https://github.com/username/repo-name.git）："
read NEW_REPO_URL

if [ -z "$NEW_REPO_URL" ]; then
    echo "❌ 错误：仓库 URL 不能为空"
    exit 1
fi

echo ""
echo "📋 配置信息："
echo "   新仓库 URL: $NEW_REPO_URL"
echo ""

# 确认
echo "是否继续部署？(y/n)"
read CONFIRM

if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
    echo "❌ 部署已取消"
    exit 0
fi

echo ""
echo "🔄 开始部署..."
echo ""

# 检查是否已存在 test 远程仓库
if git remote | grep -q "^test$"; then
    echo "⚠️  警告：'test' 远程仓库已存在"
    echo "是否要删除并重新添加？(y/n)"
    read REMOVE_CONFIRM
    
    if [ "$REMOVE_CONFIRM" == "y" ] || [ "$REMOVE_CONFIRM" == "Y" ]; then
        echo "🗑️  移除旧的 'test' 远程仓库..."
        git remote remove test
    else
        echo "❌ 部署已取消"
        exit 0
    fi
fi

# 添加新的远程仓库
echo "➕ 添加新的远程仓库..."
git remote add test "$NEW_REPO_URL"

if [ $? -ne 0 ]; then
    echo "❌ 错误：添加远程仓库失败"
    exit 1
fi

# 显示当前分支
CURRENT_BRANCH=$(git branch --show-current)
echo "📌 当前分支: $CURRENT_BRANCH"
echo ""

# 确认要推送的内容
echo "即将推送的文件："
git status --short
echo ""

echo "是否推送到新仓库？(y/n)"
read PUSH_CONFIRM

if [ "$PUSH_CONFIRM" != "y" ] && [ "$PUSH_CONFIRM" != "Y" ]; then
    echo "❌ 推送已取消"
    git remote remove test
    exit 0
fi

# 推送到新仓库
echo ""
echo "🚀 推送到新仓库..."
git push test "$CURRENT_BRANCH"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 部署成功！"
    echo ""
    echo "📝 接下来的步骤："
    echo "   1. 访问你的新仓库确认文件已上传"
    echo "   2. （可选）在仓库 Settings → Pages 中启用 GitHub Pages"
    echo "   3. （可选）添加 README.md 说明这是测试版本"
    echo ""
    echo "🌐 如果启用了 GitHub Pages，你的网站将在几分钟后可用"
    echo ""
    
    # 显示远程仓库列表
    echo "📍 当前配置的远程仓库："
    git remote -v
    echo ""
else
    echo ""
    echo "❌ 推送失败"
    echo ""
    echo "可能的原因："
    echo "   1. 仓库 URL 不正确"
    echo "   2. 没有权限推送到该仓库"
    echo "   3. 需要配置 Git 凭据或 Personal Access Token"
    echo ""
    echo "💡 提示：访问 DEPLOYMENT.md 查看详细的部署指南"
    echo ""
    
    # 清理
    echo "是否移除刚添加的远程仓库？(y/n)"
    read CLEANUP
    if [ "$CLEANUP" == "y" ] || [ "$CLEANUP" == "Y" ]; then
        git remote remove test
        echo "✓ 已移除远程仓库"
    fi
    
    exit 1
fi

echo "================================================"
