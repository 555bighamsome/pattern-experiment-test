# 数据收集修复总结 (Data Collection Fix Summary)

## 修复的问题 (Issues Fixed)

### 1. NULL 数据问题的根本原因
之前用户完成测试后，数据库中 `task_data` 和 `freeplay_data` 字段为 NULL，原因是：

**puzzleFirst 条件下**：
- ❌ 旧逻辑：`handleFreeplayCompletion()` 直接调用 `submitCombinedData()`
- ❌ 问题：`downloadCombinedData()` 只在用户点击下载时才整合数据，不保存到 localStorage
- ❌ 结果：`freeplayExperimentData` key 从未被设置，导致提交 NULL

**freeplayFirst 条件下**：
- ❌ 旧逻辑：Freeplay 结束后跳转到 Task，但 Task 完成时直接提交
- ❌ 问题：`downloadTaskDataOnly()` 不保存数据到 localStorage
- ❌ 结果：`taskExperimentData` key 从未被设置，导致提交 NULL

### 2. 实施的修复

#### 修复 1: routes/task.html - handleTaskCompletion()
```javascript
// 在提交前，先保存 task 数据到 localStorage
if (typeof allTrialsData !== 'undefined') {
    localStorage.setItem('taskExperimentData', JSON.stringify(allTrialsData));
    localStorage.setItem('taskCompletionTime', new Date().toISOString());
}
```
**效果**：无论在哪个条件下，Task 完成时都会保存数据

#### 修复 2: routes/freeplay.html - handleFreeplayCompletion()
```javascript
// 总是先保存 freeplay 数据
const sessionData = {
    sessions: JSON.parse(localStorage.getItem('freeplaySessions') || '[]'),
    gallery: getGalleryFromStorage(),
    helpers: loadFavoritesFromStorage(),
    completionTime: new Date().toISOString()
};
localStorage.setItem('freeplayExperimentData', JSON.stringify(sessionData));

// 根据条件决定是跳转还是提交
if (condition === 'freeplayFirst') {
    // 跳转到 Task 阶段（不提交）
    window.location.href = 'task.html';
} else {
    // puzzleFirst：提交组合数据
    await submitCombinedData();
}
```
**效果**：
- freeplayFirst：保存数据后跳转，Task 完成时有完整数据可提交
- puzzleFirst：保存数据后立即提交完整数据

#### 修复 3: js/freeplay.js - endFreePlayMode()
更新模态框按钮文本以清楚显示下一步操作：
```javascript
if (condition === 'freeplayFirst') {
    submitBtn.innerHTML = '→ Continue to Puzzle Phase';
    submitBtn.style.background = '#10b981'; // 绿色表示继续
} else {
    submitBtn.innerHTML = '✓ Submit Data';
    submitBtn.style.background = '#3b82f6'; // 蓝色表示提交
}
```

## 数据收集完整性验证 (Data Collection Verification)

### Task 阶段数据 ✅
**收集内容**：
- ✅ 每个 trial 的所有操作步骤 (`steps[]`)
- ✅ 操作的详细信息（operation, operands, timestamp, interval）
- ✅ Trial 结果（success, timeSpent, pointsEarned）
- ✅ Metadata（试题顺序、随机化、计分规则）

**收集时机**：
- 每次操作时：`addOperation()` 添加到 `currentTrialRecord.steps[]`
- 每次提交时：更新 `currentTrialRecord.success`, `timeSpent`, `pointsEarned`
- 所有数据保存在：`allTrialsData[]` 数组

### Freeplay 阶段数据 ✅
**收集内容**：
- ✅ 每个 session 的按钮点击 (`buttonClickActions[]`)
- ✅ 每个完成的操作 (`operationActions[]`)
- ✅ 保存到 gallery 的作品（pattern, operations, timestamp）
- ✅ Helper 使用统计 (`helperUsageCount`)
- ✅ 最终工作区状态 (`finalPattern`)

**收集时机**：
- 点击按钮时：`logButtonClick()` 记录到 `sessionRecord.buttonClickActions[]`
- 完成操作时：`logOperationComplete()` 记录到 `sessionRecord.operationActions[]`
- 保存作品时：添加到 `patternGallery` localStorage
- Session 结束时：`saveSessionRecord()` 保存到 `freeplaySessions`

## 提交流程 (Submission Flow)

### puzzleFirst 完整流程 ✅
```
1. Task 阶段
   ↓ (用户完成所有 trials)
2. 点击 "Submit & Exit"
   → handleTaskCompletion() 保存 taskExperimentData
   → enterFreePlayMode() 跳转到 Freeplay
   ↓
3. Freeplay 阶段 (10 分钟)
   ↓ (自动记录所有操作到 sessionRecord)
4. 计时器结束
   → endFreePlayMode() 显示模态框
   ↓
5. 用户点击 "✓ Submit Data"
   → handleFreeplayCompletion() 检测 puzzleFirst
   → 保存 freeplayExperimentData
   → submitCombinedData() 提交完整数据到服务器
   ✓ 数据库记录包含 task_data + freeplay_data
```

### freeplayFirst 完整流程 ✅
```
1. Freeplay 阶段 (10 分钟)
   ↓ (自动记录所有操作到 sessionRecord)
2. 计时器结束
   → endFreePlayMode() 显示模态框
   ↓
3. 用户点击 "→ Continue to Puzzle Phase"
   → handleFreeplayCompletion() 检测 freeplayFirst
   → 保存 freeplayExperimentData 到 localStorage
   → 跳转到 Task 阶段
   ↓
4. Task 阶段
   ↓ (用户完成所有 trials)
5. 点击 "Submit & Exit"
   → handleTaskCompletion() 保存 taskExperimentData
   → submitCombinedData() 读取 localStorage 中的两个数据集
   → 提交完整数据到服务器
   ✓ 数据库记录包含 task_data + freeplay_data
```

## 代码修改文件清单

| 文件 | 修改内容 | 目的 |
|------|---------|------|
| `routes/task.html` | 修改 `handleTaskCompletion()` | 在提交前保存 task 数据到 localStorage |
| `routes/freeplay.html` | 重写 `handleFreeplayCompletion()` | 根据条件决定跳转或提交，总是先保存数据 |
| `js/freeplay.js` | 更新 `endFreePlayMode()` | 按条件更新按钮文本和提示信息 |
| `DATA_FLOW_VERIFICATION.md` | 新建文档 | 详细说明数据流和验证步骤 |

## 下一步：测试与部署

### 本地测试 ✓ (代码检查完成)
- ✅ 检查了 Task 数据记录逻辑（allTrialsData）
- ✅ 检查了 Freeplay 数据记录逻辑（sessionRecord）
- ✅ 检查了 localStorage 存储时机
- ✅ 检查了 API payload 格式
- ✅ 无语法错误

### 部署步骤
1. Git commit 修改
2. Push 到 GitHub
3. 在 cPanel Git Version Control 中 Pull
4. 复制文件到 public_html
5. 运行端到端测试（两种条件各一次）
6. 验证数据库记录完整性

### 验证数据库
```sql
-- 查看最新提交的数据
SELECT 
    id,
    participant_id,
    `condition`,
    submission_time,
    CASE WHEN task_data IS NULL THEN 'NULL' ELSE 'HAS DATA' END as task_status,
    CASE WHEN freeplay_data IS NULL THEN 'NULL' ELSE 'HAS DATA' END as freeplay_status,
    JSON_LENGTH(task_data) as task_items,
    JSON_LENGTH(freeplay_data, '$.sessions') as freeplay_sessions
FROM experiment_data
ORDER BY id DESC
LIMIT 5;
```

期望结果：
- task_status: `HAS DATA`
- freeplay_status: `HAS DATA`
- task_items: > 0 (至少有 metadata)
- freeplay_sessions: ≥ 0 (可能为 0 如果用户没创建 pattern)

## 关键改进点总结

✅ **解决 NULL 数据问题**：所有阶段完成时强制保存到 localStorage
✅ **区分两种条件流程**：freeplayFirst 不在中途提交，puzzleFirst 在最后提交
✅ **保持向后兼容**：如果服务器提交失败，仍然回退到下载
✅ **用户体验优化**：按钮文本清楚显示下一步操作
✅ **数据完整性**：所有用户操作都被记录（按钮点击、操作、保存的作品）
