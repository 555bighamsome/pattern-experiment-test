# 数据库数据示例

## 数据库表结构

```sql
CREATE TABLE experiment_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    participant_id VARCHAR(100) NOT NULL,
    `condition` VARCHAR(50) NOT NULL,
    submission_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    task_data JSON,
    freeplay_data JSON,
    user_agent TEXT,
    screen_resolution VARCHAR(50),
    INDEX idx_participant (participant_id),
    INDEX idx_condition (`condition`),
    INDEX idx_time (submission_time)
);
```

---

## 正常提交的数据示例

### 示例 1: puzzleFirst 条件（先做任务，后自由创作）

#### 基本信息
| 字段 | 值 |
|------|-----|
| id | 3 |
| participant_id | P_1734793200000_abc123xyz |
| condition | puzzleFirst |
| submission_time | 2024-12-21 15:30:25 |
| user_agent | Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)... |
| screen_resolution | 1920x1080 |

#### task_data (JSON)
```json
[
  {
    "metadata": {
      "randomized": false,
      "order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
      "pointsPerTask": 1,
      "totalTasks": 10
    }
  },
  {
    "trial": 1,
    "actualProblemIndex": 0,
    "testName": "Simple Cross",
    "targetPattern": [[0,1,0], [1,1,1], [0,1,0]],
    "steps": [
      {
        "id": "s1734793205123_456",
        "operation": "add(blank, square)",
        "pattern": [[1,1,1], [1,1,1], [1,1,1]],
        "timestamp": 1734793205123,
        "intervalFromLast": 1500,
        "opFn": "add",
        "operands": {
          "a": [[0,0,0], [0,0,0], [0,0,0]],
          "b": [[1,1,1], [1,1,1], [1,1,1]]
        }
      },
      {
        "id": "s1734793208456_789",
        "operation": "intersect(square, cross)",
        "pattern": [[0,1,0], [1,1,1], [0,1,0]],
        "timestamp": 1734793208456,
        "intervalFromLast": 3333,
        "opFn": "intersect",
        "operands": {
          "a": [[1,1,1], [1,1,1], [1,1,1]],
          "b": [[0,1,0], [1,1,1], [0,1,0]]
        }
      }
    ],
    "operations": ["add(blank, square)", "intersect(square, cross)"],
    "stepsCount": 2,
    "timeSpent": 8500,
    "success": true,
    "submitted": true,
    "pointsEarned": 1,
    "pointsAwarded": 1,
    "totalPointsAfter": 1,
    "startedAt": 1734793200000
  },
  {
    "trial": 2,
    "actualProblemIndex": 1,
    "testName": "Border Frame",
    "targetPattern": [[1,1,1], [1,0,1], [1,1,1]],
    "steps": [
      {
        "id": "s1734793215000_111",
        "operation": "add(blank, square)",
        "pattern": [[1,1,1], [1,1,1], [1,1,1]],
        "timestamp": 1734793215000,
        "intervalFromLast": 2000,
        "opFn": "add",
        "operands": {
          "a": [[0,0,0], [0,0,0], [0,0,0]],
          "b": [[1,1,1], [1,1,1], [1,1,1]]
        }
      },
      {
        "id": "s1734793218500_222",
        "operation": "subtract(square, center)",
        "pattern": [[1,1,1], [1,0,1], [1,1,1]],
        "timestamp": 1734793218500,
        "intervalFromLast": 3500,
        "opFn": "subtract",
        "operands": {
          "a": [[1,1,1], [1,1,1], [1,1,1]],
          "b": [[0,0,0], [0,1,0], [0,0,0]]
        }
      }
    ],
    "operations": ["add(blank, square)", "subtract(square, center)"],
    "stepsCount": 2,
    "timeSpent": 7200,
    "success": true,
    "submitted": true,
    "pointsEarned": 1,
    "pointsAwarded": 1,
    "totalPointsAfter": 2,
    "startedAt": 1734793213000
  }
]
```

#### freeplay_data (JSON)
```json
{
  "sessions": [
    {
      "sessionId": "freeplay_1734793300000",
      "startTime": 1734793300000,
      "endTime": 1734793450000,
      "totalDuration": 150000,
      "buttonClickActions": [
        {
          "buttonType": "primitive",
          "operation": "square",
          "context": {"source": "primitives-panel"},
          "timestamp": 1734793305000
        },
        {
          "buttonType": "binary",
          "operation": "add",
          "context": {"operandA": "square", "operandB": "cross"},
          "timestamp": 1734793310000
        },
        {
          "buttonType": "transform",
          "operation": "rotateRight",
          "context": {"inputPattern": "combined_pattern"},
          "timestamp": 1734793320000
        }
      ],
      "favoriteActions": [
        {
          "action": "save",
          "helperName": "MySquare",
          "pattern": [[1,1,1], [1,1,1], [1,1,1]],
          "timestamp": 1734793330000
        }
      ],
      "operationActions": [
        {
          "operation": "add(square, cross)",
          "operands": {
            "a": [[1,1,1], [1,1,1], [1,1,1]],
            "b": [[0,1,0], [1,1,1], [0,1,0]],
            "input": null
          },
          "result": [[1,1,1], [1,1,1], [1,1,1]],
          "operationIndex": 1,
          "timestamp": 1734793310500
        },
        {
          "operation": "rotateRight(combined)",
          "operands": {
            "a": null,
            "b": null,
            "input": [[1,1,1], [1,1,1], [1,1,1]]
          },
          "result": [[1,1,1], [1,1,1], [1,1,1]],
          "operationIndex": 2,
          "timestamp": 1734793320500
        }
      ],
      "finalPattern": [[1,1,1], [1,1,1], [1,1,1]],
      "totalOperations": 2,
      "patternsCreated": [],
      "helperUsageCount": {"MySquare": 3},
      "userAgent": "Mozilla/5.0...",
      "screenSize": {"width": 1920, "height": 1080}
    }
  ],
  "gallery": [
    {
      "id": 1734793340000,
      "name": "My Beautiful Flower",
      "pattern": [[0,1,0], [1,1,1], [0,1,0]],
      "operations": ["add(blank, cross)", "rotateRight(cross)"],
      "operationsHistory": [
        {
          "operation": "add(blank, cross)",
          "pattern": [[0,1,0], [1,1,1], [0,1,0]],
          "timestamp": 1734793335000,
          "intervalFromLast": 5000
        },
        {
          "operation": "rotateRight(cross)",
          "pattern": [[0,1,0], [1,1,1], [0,1,0]],
          "timestamp": 1734793338000,
          "intervalFromLast": 3000
        }
      ],
      "totalOperations": 2,
      "timestamp": "2024-12-21T15:35:40.000Z",
      "createdAt": 1734793340000,
      "sessionId": "freeplay_1734793300000"
    },
    {
      "id": 1734793400000,
      "name": null,
      "pattern": [[1,0,1], [0,1,0], [1,0,1]],
      "operations": ["add(blank, corners)"],
      "operationsHistory": [
        {
          "operation": "add(blank, corners)",
          "pattern": [[1,0,1], [0,1,0], [1,0,1]],
          "timestamp": 1734793398000,
          "intervalFromLast": 2000
        }
      ],
      "totalOperations": 1,
      "timestamp": "2024-12-21T15:36:40.000Z",
      "createdAt": 1734793400000,
      "sessionId": "freeplay_1734793300000"
    }
  ],
  "helpers": [
    {
      "id": 1734793330000,
      "name": "MySquare",
      "pattern": [[1,1,1], [1,1,1], [1,1,1]],
      "createdAt": 1734793330000,
      "usageCount": 3
    }
  ],
  "completionTime": "2024-12-21T15:37:30.000Z"
}
```

---

### 示例 2: freeplayFirst 条件（先自由创作，后做任务）

#### 基本信息
| 字段 | 值 |
|------|-----|
| id | 4 |
| participant_id | P_1734793800000_def456uvw |
| condition | freeplayFirst |
| submission_time | 2024-12-21 16:15:45 |
| user_agent | Mozilla/5.0 (Windows NT 10.0; Win64; x64)... |
| screen_resolution | 2560x1440 |

#### freeplay_data (JSON)
```json
{
  "sessions": [
    {
      "sessionId": "freeplay_1734793800000",
      "startTime": 1734793800000,
      "endTime": 1734794400000,
      "totalDuration": 600000,
      "buttonClickActions": [
        {
          "buttonType": "primitive",
          "operation": "cross",
          "context": {"source": "primitives-panel"},
          "timestamp": 1734793810000
        }
      ],
      "favoriteActions": [],
      "operationActions": [
        {
          "operation": "add(blank, cross)",
          "operands": {
            "a": [[0,0,0], [0,0,0], [0,0,0]],
            "b": [[0,1,0], [1,1,1], [0,1,0]],
            "input": null
          },
          "result": [[0,1,0], [1,1,1], [0,1,0]],
          "operationIndex": 1,
          "timestamp": 1734793815000
        }
      ],
      "finalPattern": [[0,1,0], [1,1,1], [0,1,0]],
      "totalOperations": 1,
      "patternsCreated": [],
      "helperUsageCount": {},
      "userAgent": "Mozilla/5.0...",
      "screenSize": {"width": 2560, "height": 1440}
    }
  ],
  "gallery": [
    {
      "id": 1734794100000,
      "name": "Star Pattern",
      "pattern": [[1,0,1], [0,1,0], [1,0,1]],
      "operations": ["add(blank, corners)", "add(corners, center)"],
      "operationsHistory": [
        {
          "operation": "add(blank, corners)",
          "pattern": [[1,0,1], [0,0,0], [1,0,1]],
          "timestamp": 1734794095000,
          "intervalFromLast": 3000
        },
        {
          "operation": "add(corners, center)",
          "pattern": [[1,0,1], [0,1,0], [1,0,1]],
          "timestamp": 1734794098000,
          "intervalFromLast": 3000
        }
      ],
      "totalOperations": 2,
      "timestamp": "2024-12-21T16:08:20.000Z",
      "createdAt": 1734794100000,
      "sessionId": "freeplay_1734793800000"
    }
  ],
  "helpers": [],
  "completionTime": "2024-12-21T16:10:00.000Z"
}
```

#### task_data (JSON)
```json
[
  {
    "metadata": {
      "randomized": false,
      "order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
      "pointsPerTask": 1,
      "totalTasks": 10
    }
  },
  {
    "trial": 1,
    "actualProblemIndex": 0,
    "testName": "Simple Cross",
    "targetPattern": [[0,1,0], [1,1,1], [0,1,0]],
    "steps": [
      {
        "id": "s1734794410000_333",
        "operation": "add(blank, cross)",
        "pattern": [[0,1,0], [1,1,1], [0,1,0]],
        "timestamp": 1734794410000,
        "intervalFromLast": 1200,
        "opFn": "add",
        "operands": {
          "a": [[0,0,0], [0,0,0], [0,0,0]],
          "b": [[0,1,0], [1,1,1], [0,1,0]]
        }
      }
    ],
    "operations": ["add(blank, cross)"],
    "stepsCount": 1,
    "timeSpent": 5500,
    "success": true,
    "submitted": true,
    "pointsEarned": 1,
    "pointsAwarded": 1,
    "totalPointsAfter": 1,
    "startedAt": 1734794405000
  }
]
```

---

## 数据字段说明

### 表级字段

| 字段名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| id | INT | 自增主键 | 3 |
| participant_id | VARCHAR(100) | 参与者唯一标识符 | P_1734793200000_abc123xyz |
| condition | VARCHAR(50) | 实验条件 | puzzleFirst 或 freeplayFirst |
| submission_time | TIMESTAMP | 提交时间 | 2024-12-21 15:30:25 |
| task_data | JSON | 任务阶段数据 | 见下方详细说明 |
| freeplay_data | JSON | 自由创作阶段数据 | 见下方详细说明 |
| user_agent | TEXT | 浏览器信息 | Mozilla/5.0... |
| screen_resolution | VARCHAR(50) | 屏幕分辨率 | 1920x1080 |

### task_data JSON 结构

**第一个元素：元数据**
```json
{
  "metadata": {
    "randomized": false,           // 是否随机化任务顺序
    "order": [0,1,2,...],          // 任务呈现顺序
    "pointsPerTask": 1,            // 每题分数
    "totalTasks": 10               // 总任务数
  }
}
```

**后续元素：每个试次的详细记录**
```json
{
  "trial": 1,                      // 试次编号（从1开始）
  "actualProblemIndex": 0,         // 实际题目索引
  "testName": "Simple Cross",      // 题目名称
  "targetPattern": [...],          // 目标图案（3x3数组）
  "steps": [                       // 操作步骤详细记录
    {
      "id": "s1734793205123_456", // 步骤唯一ID
      "operation": "add(blank, square)", // 操作描述
      "pattern": [...],            // 操作后的图案
      "timestamp": 1734793205123,  // 时间戳（毫秒）
      "intervalFromLast": 1500,    // 距上次操作间隔（毫秒）
      "opFn": "add",               // 操作函数名
      "operands": {                // 操作数
        "a": [...],                // 左操作数
        "b": [...]                 // 右操作数
      }
    }
  ],
  "operations": ["add(blank, square)"], // 操作字符串列表
  "stepsCount": 2,                 // 步骤总数
  "timeSpent": 8500,               // 耗时（毫秒）
  "success": true,                 // 是否成功
  "submitted": true,               // 是否已提交
  "pointsEarned": 1,               // 获得分数
  "pointsAwarded": 1,              // 本次奖励分数
  "totalPointsAfter": 1,           // 累计总分
  "startedAt": 1734793200000       // 开始时间戳
}
```

### freeplay_data JSON 结构

**顶层结构**
```json
{
  "sessions": [...],               // 会话列表
  "gallery": [...],                // 保存的图案库
  "helpers": [...],                // 自定义辅助工具
  "completionTime": "2024-12-21T15:37:30.000Z" // 完成时间
}
```

**sessions 元素**
```json
{
  "sessionId": "freeplay_1734793300000", // 会话ID
  "startTime": 1734793300000,      // 开始时间戳
  "endTime": 1734793450000,        // 结束时间戳
  "totalDuration": 150000,         // 总时长（毫秒）
  "buttonClickActions": [          // 按钮点击记录
    {
      "buttonType": "primitive",   // 按钮类型
      "operation": "square",       // 操作名称
      "context": {...},            // 上下文信息
      "timestamp": 1734793305000   // 时间戳
    }
  ],
  "favoriteActions": [             // 辅助工具操作
    {
      "action": "save",            // 动作类型
      "helperName": "MySquare",    // 工具名称
      "pattern": [...],            // 图案
      "timestamp": 1734793330000   // 时间戳
    }
  ],
  "operationActions": [            // 完成的操作记录
    {
      "operation": "add(square, cross)", // 操作描述
      "operands": {                // 操作数
        "a": [...],
        "b": [...],
        "input": null
      },
      "result": [...],             // 结果图案
      "operationIndex": 1,         // 操作索引
      "timestamp": 1734793310500   // 时间戳
    }
  ],
  "finalPattern": [...],           // 最终图案
  "totalOperations": 2,            // 操作总数
  "patternsCreated": [],           // 创建的图案（已弃用）
  "helperUsageCount": {"MySquare": 3}, // 工具使用次数
  "userAgent": "...",              // 浏览器信息
  "screenSize": {"width": 1920, "height": 1080} // 屏幕尺寸
}
```

**gallery 元素**
```json
{
  "id": 1734793340000,             // 图案ID
  "name": "My Beautiful Flower",   // 图案名称（可为null）
  "pattern": [...],                // 图案数据
  "operations": ["add(blank, cross)"], // 操作列表
  "operationsHistory": [           // 操作历史
    {
      "operation": "add(blank, cross)",
      "pattern": [...],
      "timestamp": 1734793335000,
      "intervalFromLast": 5000
    }
  ],
  "totalOperations": 2,            // 操作总数
  "timestamp": "2024-12-21T15:35:40.000Z", // ISO时间戳
  "createdAt": 1734793340000,      // 创建时间戳
  "sessionId": "freeplay_1734793300000" // 所属会话ID
}
```

**helpers 元素**
```json
{
  "id": 1734793330000,             // 工具ID
  "name": "MySquare",              // 工具名称
  "pattern": [...],                // 工具图案
  "createdAt": 1734793330000,      // 创建时间戳
  "usageCount": 3                  // 使用次数
}
```

---

## NULL 值情况说明

### 正常的 NULL 情况

在某些实验条件下，某个阶段可能不适用，此时相应字段会是 NULL：

1. **仅测试任务阶段**（用于调试）
   - task_data: 有数据
   - freeplay_data: NULL

2. **仅测试自由创作阶段**（用于调试）
   - task_data: NULL
   - freeplay_data: 有数据

### 异常的 NULL 情况（需要修复）

如果正式实验中出现以下情况，说明代码有问题：

1. **puzzleFirst 条件下 task_data 为 NULL**
   - 原因：`handleTaskCompletion()` 没有保存数据到 localStorage
   - 解决：已在代码中添加保存逻辑

2. **puzzleFirst 条件下 freeplay_data 为 NULL**
   - 原因：`handleFreeplayCompletion()` 没有保存数据到 localStorage
   - 解决：已在代码中添加保存逻辑

3. **freeplayFirst 条件下 freeplay_data 为 NULL**
   - 原因：完成 freeplay 后没有保存就跳转到 task
   - 解决：已在 `handleFreeplayCompletion()` 中添加保存逻辑

4. **freeplayFirst 条件下 task_data 为 NULL**
   - 原因：`handleTaskCompletion()` 没有保存数据
   - 解决：已在代码中添加保存逻辑

---

## 如何查看数据库数据

### 方法 1: phpMyAdmin（推荐）

1. 登录 cPanel
2. 找到 "Databases" → "phpMyAdmin"
3. 选择数据库 `bococo81_pattern_language_experiment_db`
4. 点击表 `experiment_data`
5. 点击 "Browse" 查看所有记录

### 方法 2: 直接查看 JSON 字段

对于 JSON 字段，phpMyAdmin 会显示压缩的 JSON。要查看格式化的内容：

1. 点击某一行的 "Edit" 或 "View"
2. JSON 字段会显示在文本框中
3. 复制内容到在线 JSON 格式化工具（如 jsonformatter.org）

### 方法 3: SQL 查询

```sql
-- 查看最近10条记录
SELECT 
    id,
    participant_id,
    `condition`,
    submission_time,
    CASE 
        WHEN task_data IS NULL THEN 'NULL'
        ELSE 'Has Data'
    END as task_status,
    CASE 
        WHEN freeplay_data IS NULL THEN 'NULL'
        ELSE 'Has Data'
    END as freeplay_status
FROM experiment_data
ORDER BY submission_time DESC
LIMIT 10;

-- 查看特定参与者的完整数据
SELECT 
    id,
    participant_id,
    `condition`,
    submission_time,
    JSON_PRETTY(task_data) as task_data_formatted,
    JSON_PRETTY(freeplay_data) as freeplay_data_formatted
FROM experiment_data
WHERE participant_id = 'P_1766351552481_4302czgnx';

-- 统计每个条件下的提交数量
SELECT 
    `condition`,
    COUNT(*) as count,
    SUM(CASE WHEN task_data IS NOT NULL THEN 1 ELSE 0 END) as has_task_data,
    SUM(CASE WHEN freeplay_data IS NOT NULL THEN 1 ELSE 0 END) as has_freeplay_data
FROM experiment_data
GROUP BY `condition`;
```

---

## 数据验证检查清单

提交后检查以下项目确保数据完整：

- [ ] **participant_id** 格式正确（P_时间戳_随机字符串）
- [ ] **condition** 是 `puzzleFirst` 或 `freeplayFirst`
- [ ] **task_data** 不为 NULL（两种条件都应该有）
- [ ] **freeplay_data** 不为 NULL（两种条件都应该有）
- [ ] **task_data[0]** 包含 metadata 对象
- [ ] **task_data** 其他元素都有 trial, steps, success 等字段
- [ ] **freeplay_data.sessions** 数组不为空
- [ ] **freeplay_data.gallery** 包含保存的图案（如果用户有保存）
- [ ] **所有时间戳** 格式正确且合理
- [ ] **user_agent** 和 **screen_resolution** 有值
