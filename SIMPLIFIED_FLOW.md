# 简化后的实验流程 (Simplified Experiment Flow)

## 设计理念

**核心原则**：
1. ✅ **自动保存**：每个阶段完成时自动保存数据到 localStorage
2. ✅ **单一按钮**：只显示"Continue"按钮，根据条件自动决定下一步
3. ✅ **最终提交**：只在实验的最后阶段才提交数据到服务器
4. ✅ **回退机制**：如果服务器提交失败，自动下载数据作为备份

## 用户体验流程

### Condition 1: puzzleFirst

```
┌─────────────────────┐
│  Task 阶段 (Puzzle) │
│  - 完成 20个 trials │
└──────────┬──────────┘
           │ 自动保存 taskExperimentData
           │
           ▼
    ┌──────────────┐
    │  完成模态框  │
    │  显示分数    │
    └──────┬───────┘
           │
           ▼
   ┌────────────────────┐
   │ "→ Continue" 按钮  │
   │   (绿色)           │
   └────────┬───────────┘
            │ 点击
            ▼
┌──────────────────────────┐
│  Freeplay 阶段 (创作)   │
│  - 10 分钟自由创作       │
│  - 自动记录所有操作      │
└──────────┬───────────────┘
           │ 计时器结束
           │ 自动保存 freeplayExperimentData
           ▼
    ┌──────────────┐
    │  完成模态框  │
    │  显示作品    │
    └──────┬───────┘
           │
           ▼
   ┌────────────────────┐
   │ "✓ Submit Data"    │
   │   (蓝色)           │
   └────────┬───────────┘
            │ 点击
            ▼
   ┌─────────────────────┐
   │ 提交到服务器        │
   │ taskData + freeplay │
   └─────────────────────┘
            │
            ▼
      ┌─────────┐
      │ 成功提示 │
      └─────────┘
```

### Condition 2: freeplayFirst

```
┌──────────────────────────┐
│  Freeplay 阶段 (创作)   │
│  - 10 分钟自由创作       │
│  - 自动记录所有操作      │
└──────────┬───────────────┘
           │ 计时器结束
           │ 自动保存 freeplayExperimentData
           ▼
    ┌──────────────┐
    │  完成模态框  │
    │  显示作品    │
    └──────┬───────┘
           │
           ▼
   ┌──────────────────────────┐
   │ "→ Continue to Puzzle    │
   │     Phase" (绿色)        │
   └────────┬─────────────────┘
            │ 点击
            ▼
┌─────────────────────┐
│  Task 阶段 (Puzzle) │
│  - 完成 20个 trials │
└──────────┬──────────┘
           │ 自动保存 taskExperimentData
           │
           ▼
    ┌──────────────┐
    │  完成模态框  │
    │  显示分数    │
    └──────┬───────┘
           │
           ▼
   ┌────────────────────┐
   │ "✓ Submit Data"    │
   │   (蓝色)           │
   └────────┬───────────┘
            │ 点击
            ▼
   ┌─────────────────────┐
   │ 提交到服务器        │
   │ taskData + freeplay │
   └─────────────────────┘
            │
            ▼
      ┌─────────┐
      │ 成功提示 │
      └─────────┘
```

## 按钮设计

### Task 完成后的按钮

**单一按钮，文本固定为**：`"→ Continue"`（绿色）

**行为**：
- **puzzleFirst**：跳转到 Freeplay
- **freeplayFirst**：提交数据到服务器（这是最后阶段）

### Freeplay 完成后的按钮

**单一按钮，文本根据条件动态变化**：

| 条件 | 按钮文本 | 颜色 | 行为 |
|------|---------|------|------|
| freeplayFirst | `"→ Continue to Puzzle Phase"` | 绿色 (#10b981) | 跳转到 Task |
| puzzleFirst | `"✓ Submit Data"` | 蓝色 (#3b82f6) | 提交到服务器 |

## 数据保存时机

### 自动保存点

| 阶段 | 时机 | localStorage Key | 数据内容 |
|------|------|-----------------|---------|
| Task 完成 | 点击 Continue 按钮前 | `taskExperimentData` | allTrialsData 完整数组 |
| Freeplay 完成 | 点击按钮前 | `freeplayExperimentData` | sessions + gallery + helpers |

### 服务器提交时机

**只在实验最后阶段提交**：
- puzzleFirst：Freeplay 完成时
- freeplayFirst：Task 完成时

## 代码逻辑

### routes/task.html - handleTaskContinue()

```javascript
async function handleTaskContinue() {
    // 1. 检测条件
    let condition = localStorage.getItem('experimentCondition');
    
    // 2. 总是先保存数据
    localStorage.setItem('taskExperimentData', JSON.stringify(allTrialsData));
    
    // 3. 根据条件决定行为
    if (condition === 'freeplayFirst') {
        // 这是最后阶段 - 提交数据
        await submitCombinedData();
    } else {
        // puzzleFirst - 继续到 Freeplay
        enterFreePlayMode(); // 跳转到 freeplay.html
    }
}
```

### routes/freeplay.html - handleFreeplayCompletion()

```javascript
async function handleFreeplayCompletion() {
    // 1. 检测条件
    let condition = localStorage.getItem('experimentCondition');
    
    // 2. 总是先保存数据
    const sessionData = {
        sessions: JSON.parse(localStorage.getItem('freeplaySessions') || '[]'),
        gallery: getGalleryFromStorage(),
        helpers: loadFavoritesFromStorage(),
        completionTime: new Date().toISOString()
    };
    localStorage.setItem('freeplayExperimentData', JSON.stringify(sessionData));
    
    // 3. 根据条件决定行为
    if (condition === 'freeplayFirst') {
        // 继续到 Task 阶段
        window.location.href = 'task.html';
    } else {
        // puzzleFirst - 这是最后阶段，提交数据
        await submitCombinedData();
    }
}
```

### js/freeplay.js - endFreePlayMode()

```javascript
// 更新按钮文本
const submitBtn = document.querySelector('#freeplayCompletionModal button');
if (condition === 'freeplayFirst') {
    submitBtn.innerHTML = '→ Continue to Puzzle Phase';
    submitBtn.style.background = '#10b981'; // 绿色
} else {
    submitBtn.innerHTML = '✓ Submit Data';
    submitBtn.style.background = '#3b82f6'; // 蓝色
}
```

## 优势

### 用户体验
✅ **简洁明了**：每个阶段只有一个明确的"下一步"按钮
✅ **无需选择**：系统自动判断应该跳转还是提交
✅ **进度清晰**：用户知道还有下一步（绿色Continue）或已完成（蓝色Submit）

### 技术优势
✅ **自动保存**：不依赖用户手动选择，避免数据丢失
✅ **条件分离**：逻辑清晰，两种条件的处理流程独立
✅ **回退安全**：服务器提交失败时自动下载备份

### 数据完整性
✅ **强制保存**：每次点击按钮前必须先保存到 localStorage
✅ **双重保障**：服务器提交 + 本地存储
✅ **可追溯性**：所有操作都有时间戳和完整记录

## 与之前版本的区别

| 方面 | 旧版本 | 新版本（简化后） |
|------|--------|-----------------|
| Task 完成按钮 | 2个："Submit & Exit" + "Continue to Free Play" | 1个："→ Continue" |
| 用户选择 | 需要选择提交还是继续 | 无需选择，自动判断 |
| 数据保存 | 部分场景需手动触发 | 总是自动保存 |
| 提交时机 | 可能在中途提交 | 只在最终阶段提交 |
| 代码复杂度 | 多个分支逻辑 | 单一流程，条件判断 |

## 测试检查清单

### puzzleFirst 测试
- [ ] 完成 Task，点击"→ Continue"
- [ ] 验证自动跳转到 Freeplay
- [ ] 完成 Freeplay（或等10分钟）
- [ ] 验证按钮显示"✓ Submit Data"（蓝色）
- [ ] 点击提交
- [ ] 检查数据库有完整的 task_data + freeplay_data

### freeplayFirst 测试
- [ ] 完成 Freeplay，点击"→ Continue to Puzzle Phase"
- [ ] 验证自动跳转到 Task
- [ ] 完成 Task，点击"→ Continue"
- [ ] 验证开始提交数据（无跳转）
- [ ] 检查数据库有完整的 task_data + freeplay_data

### 边缘情况
- [ ] 服务器提交失败时，验证自动下载数据
- [ ] localStorage 已有旧数据时，验证覆盖正确
- [ ] 刷新页面后，验证条件仍然正确
