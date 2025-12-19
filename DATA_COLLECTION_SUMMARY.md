# 数据收集模块总结

## ✅ 整体评估：**数据收集完整且详细**

本实验系统设计了全面的数据收集机制，能够记录用户在 Pattern DSL 实验中的所有关键行为和状态。

---

## 📊 一、Task Phase（谜题任务阶段）

### 1. Trial 级别记录（currentTrialRecord）

每个 trial 记录包含：

```javascript
{
    trial: Number,                    // Trial 序号
    actualProblemIndex: Number,       // 实际问题索引
    testName: String,                 // 测试名称
    targetPattern: Array,             // 目标图案
    
    // 操作记录
    steps: Array,                     // 详细的步骤记录（见下方）
    operations: Array,                // 操作字符串数组
    stepsCount: Number,               // 步骤总数
    
    // 行为记录
    buttonClickActions: Array,        // 按钮点击记录
    favoriteActions: Array,           // Helper 使用记录
    workflowActions: Array,           // 工作流操作记录
    previewActions: Array,            // 预览操作记录
    undoActions: Array,               // 撤销操作记录
    
    // 结果和时间
    timeSpent: Number,                // 耗时（毫秒）
    success: Boolean,                 // 是否成功
    submitted: Boolean,               // 是否提交
    startedAt: Number                 // 开始时间戳
}
```

### 2. Step 级别详细记录

每个操作步骤包含：

```javascript
{
    id: String,                       // 唯一标识
    operation: String,                // 操作描述
    pattern: Array,                   // 操作后的图案状态
    timestamp: Number,                // 时间戳
    intervalFromLast: Number,         // 距上次操作的时间间隔（毫秒）
    
    // 认知分析数据
    opFn: String,                     // 操作函数名称
    operands: {                       // 操作数
        a: Array,                     // 操作数 A
        b: Array,                     // 操作数 B
        input: Array                  // 输入图案
    }
}
```

### 3. operationsHistory（跨 trial 累积）

**重要特性**：在 cumulative-history 分支中，`operationsHistory` 在同一阶段内**不清空**

- ✅ 每个操作包含：`operation`, `pattern`, `timestamp`, `intervalFromLast`
- ✅ 累积记录用户在整个 task 阶段的所有操作
- ✅ 用于 step sequence 的可视化和回放

### 4. 导出格式

Task Only 数据：
```javascript
{
    metadata: {
        experimentName: String,
        experimentCondition: String,  // 'puzzleFirst' or 'freeplayFirst'
        completionTime: String,       // ISO timestamp
        browserInfo: Object,
        includesFreePlay: Boolean
    },
    taskData: {
        trials: Array,                // 所有 trial 记录
        summary: {
            totalTrials: Number,
            successfulTrials: Number
        }
    }
}
```

---

## 🎨 二、Free Play Phase（自由创作阶段）

### 1. Session 级别记录（sessionRecord）

每次用户提交 pattern 到 gallery 时保存一个 session：

```javascript
{
    sessionId: String,                // 唯一 session ID
    startTime: Number,                // 开始时间
    endTime: Number,                  // 结束时间
    totalDuration: Number,            // 总时长（毫秒）
    
    // 行为记录
    buttonClickActions: Array,        // 按钮点击
    favoriteActions: Array,           // Helper 操作
    operationActions: Array,          // 操作动作
    
    // 最终状态
    finalPattern: Array,              // 最终图案
    totalOperations: Number,          // 操作总数
    patternsCreated: Array,           // 创建的图案列表
    helperUsageCount: Object,         // Helper 使用统计
    
    // 元数据
    userAgent: String,
    screenSize: Object
}
```

### 2. Gallery 记录

每个提交到 gallery 的 pattern 包含：

```javascript
{
    id: Number,                       // 唯一 ID
    name: String,                     // 用户命名
    pattern: Array,                   // 图案数据
    operations: Array,                // 操作字符串数组
    operationsHistory: Array,         // 完整操作历史（包含 pattern, timestamp 等）
    totalOperations: Number,          // 操作总数
    timestamp: String,                // ISO timestamp
    createdAt: Number,                // Unix timestamp
    sessionId: String                 // 关联的 session ID
}
```

### 3. operationsHistory（跨 trial 累积）

**重要特性**：在 Free Play 中，`operationsHistory` **不清空**直到切换到 task 阶段

- ✅ 记录用户在整个 free play 阶段的所有操作
- ✅ 每个提交到 gallery 的 pattern 都包含完整的 `operationsHistory`
- ✅ 可以回溯用户的创作过程

### 4. 导出格式

Free Play Only 数据：
```javascript
{
    sessions: Array,                  // 所有 session 记录
    gallery: Array,                   // Gallery 中的所有 pattern
    helpers: Array,                   // 保存的 helpers
    completionTime: String            // 完成时间
}
```

---

## 🔄 三、Combined Data（组合数据）

### Puzzle First 条件

当用户先完成 puzzle task，再完成 free play 时：

```javascript
{
    metadata: {
        experimentName: "Pattern Experiment - Complete",
        taskCompletionTime: String,
        freePlayCompletionTime: String,
        includesFreePlay: true,
        exportDate: String
    },
    taskData: {                       // Task 阶段数据
        trials: Array,
        summary: Object
    },
    freePlayData: {                   // Free Play 阶段数据
        totalSessions: Number,
        sessions: Array,
        gallery: Array,
        finalHelpers: Array,
        summary: {
            totalPatternsSaved: Number,
            totalOperations: Number,
            totalButtonClicks: Number,
            uniqueHelpersCreated: Number
        }
    }
}
```

### Freeplay First 条件

当用户先完成 free play，再完成 puzzle task 时，数据结构类似，但顺序相反。

---

## 🎯 四、关键行为追踪

### 1. 按钮点击（buttonClickActions）

```javascript
{
    buttonId: String,                 // 按钮 ID
    buttonType: String,               // 按钮类型
    timestamp: Number                 // 时间戳
}
```

### 2. Helper 操作（favoriteActions）

```javascript
{
    action: String,                   // 'add', 'delete', 'use'
    favoriteId: Number/String,
    name: String,
    pattern: Array,
    timestamp: Number
}
```

### 3. 操作动作（operationActions）

```javascript
{
    operation: String,                // 操作描述
    operationIndex: Number,           // 操作索引
    timestamp: Number
}
```

### 4. 工作流操作（workflowActions）

记录用户在 step sequence 中的选择和交互

### 5. 预览操作（previewActions）

记录用户的预览行为（confirm/cancel）

### 6. 撤销操作（undoActions）

记录撤销操作的时间和状态

---

## ⏱️ 五、时间数据收集

### 精确的时间间隔记录

- ✅ **intervalFromLast**: 每个操作记录距离上次操作的时间间隔
- ✅ **timestamp**: 每个操作的绝对时间戳
- ✅ **timeSpent**: 每个 trial 的总耗时
- ✅ **totalDuration**: 每个 session 的总时长

### Timer 功能（Free Play）

- 10 分钟倒计时
- 每分钟 console 日志输出
- 开发者命令：`checkFreeplayTime()`, `endFreeplayNow()`

---

## 🔍 六、认知过程分析数据

### 操作数记录（operands）

每个操作记录包含：
- 操作函数名称（`opFn`）
- 输入图案（`operands.a`, `operands.b`, `operands.input`）
- 输出图案（`pattern`）

这使得研究人员可以：
- 分析用户的问题解决策略
- 追踪用户如何组合和重用中间结果
- 理解用户的认知过程和决策模式

---

## 📝 七、数据持久化

### localStorage 存储

- `taskExperimentData`: Task 阶段数据
- `freeplayExperimentData`: Free Play 阶段数据
- `freeplaySessions`: Free Play sessions
- `patternGallery`: Gallery patterns
- `favorites`: Saved helpers
- `clearHistoryOnLoad`: 阶段切换标志

### 数据导出

- JSON 格式
- 带时间戳的文件名
- 结构化的嵌套数据
- 可直接用于分析工具

---

## ✅ 总结：数据收集是否完整？

### ✅ 完全记录的数据：

1. **用户行为**：
   - ✅ 所有按钮点击
   - ✅ 所有操作执行
   - ✅ Helper 的创建、使用、删除
   - ✅ 预览和确认行为
   - ✅ 撤销操作

2. **图案状态**：
   - ✅ 每个操作后的图案状态
   - ✅ 目标图案
   - ✅ 最终图案
   - ✅ 中间结果

3. **时间信息**：
   - ✅ 绝对时间戳
   - ✅ 相对时间间隔
   - ✅ Trial 总耗时
   - ✅ Session 总时长

4. **认知数据**：
   - ✅ 操作函数和操作数
   - ✅ 操作序列
   - ✅ 问题解决路径
   - ✅ 策略演化

5. **元数据**：
   - ✅ 实验条件
   - ✅ 浏览器信息
   - ✅ 屏幕尺寸
   - ✅ 完成时间

### ✅ 累积历史特性（cumulative-history 分支）：

- ✅ **同一阶段内**：operationsHistory 累积保存，不清空
- ✅ **阶段切换时**：通过 `clearHistoryOnLoad` 标志清空
- ✅ **数据完整性**：每个 gallery pattern 包含完整的 operationsHistory

---

## 🎓 用于研究分析

这套数据收集系统支持以下研究分析：

1. **认知过程研究**：追踪用户的问题解决策略
2. **学习曲线分析**：观察用户如何掌握 DSL
3. **操作效率研究**：分析操作序列的复杂度
4. **创造力评估**：评估 free play 中的创作模式
5. **Helper 使用模式**：理解用户如何抽象和重用子模式
6. **时间行为分析**：研究用户的思考和执行时间
7. **比较研究**：对比 puzzleFirst vs freeplayFirst 条件

---

## 💡 建议

目前的数据收集系统**非常完善**，已经能够支持深入的认知和行为研究。如果需要进一步改进，可以考虑：

1. **可选增强**：
   - 鼠标移动轨迹（如需要注意力研究）
   - 眼动追踪集成接口（如有设备）
   - A/B 测试标识符
   
2. **数据验证**：
   - 添加数据完整性检查
   - 异常行为检测
   - 数据质量报告

3. **隐私保护**：
   - 确认是否需要匿名化处理
   - 添加用户同意确认

但就目前的实验目标而言，**现有的数据收集已经非常充分和全面**。
