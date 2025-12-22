#!/usr/bin/env python3
"""快速分析导出的实验数据"""

import json
from datetime import datetime

# 原始数据
data_json = """[{"metadata":{"randomized":false,"order":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24],"pointsPerTask":1,"totalTasks":25}},{"trial":1,"actualProblemIndex":0,"testName":"Pattern-01","success":true,"submitted":true,"timeSpent":24489,"stepsCount":5,"pointsEarned":1,"totalPointsAfter":1,"operations":["add(•, •)","reflect_vertical(1)","add(2, 1)","reflect_diag(3)","add(3, 4)"],"buttonClickActions":[{"buttonType":"binary","operation":"add","timestamp":1766353671517}],"favoriteActions":[{"action":"add","favoriteId":"fav_1766353687813_866","timestamp":1766353687814}],"undoActions":[{"type":"reset","stepsCleared":5,"timestamp":1766353691162}],"startedAt":1766353664670},{"trial":2,"actualProblemIndex":1,"testName":"Pattern-02","success":true,"submitted":true,"timeSpent":4298,"stepsCount":1,"pointsEarned":1,"totalPointsAfter":2,"operations":["add(•, •)"],"buttonClickActions":[{"buttonType":"binary","operation":"add","timestamp":1766353692968}],"favoriteActions":[{"action":"use","favoriteId":"fav_1766353687813_866","timestamp":1766353694030}],"undoActions":[{"type":"reset","stepsCleared":1,"timestamp":1766353697465}],"startedAt":1766353691163},{"trial":3,"actualProblemIndex":2,"testName":"Pattern-03","success":false,"submitted":true,"timeSpent":6677,"stepsCount":1,"pointsEarned":0,"totalPointsAfter":2,"operations":["invert(•)"],"buttonClickActions":[{"buttonType":"transform","operation":"invert","timestamp":1766353701131}],"favoriteActions":[{"action":"use","favoriteId":"fav_1766353687813_866","timestamp":1766353701847}],"undoActions":[{"type":"reset","stepsCleared":1,"timestamp":1766353706147}],"startedAt":1766353697468},{"trial":4,"testName":"Pattern-04","steps":[],"operations":[],"stepsCount":0,"timeSpent":4566,"success":false,"submitted":true,"pointsEarned":0,"totalPointsAfter":2,"favoriteActions":[{"action":"remove","favoriteId":"fav_1766353687813_866","timestamp":1766353707114}],"undoActions":[{"type":"reset","stepsCleared":0,"timestamp":1766353710747}],"startedAt":1766353706149},{"trial":5,"testName":"Pattern-05","steps":[],"operations":[],"stepsCount":0,"timeSpent":51,"success":false,"submitted":true,"pointsEarned":0,"totalPointsAfter":2,"undoActions":[{"type":"reset","timestamp":1766353710810}],"startedAt":1766353710748},{"trial":6,"testName":"Pattern-06","stepsCount":0,"timeSpent":489,"success":false,"startedAt":1766353710811},{"trial":7,"testName":"Pattern-07","stepsCount":0,"timeSpent":78,"success":false,"startedAt":1766353711304},{"trial":8,"testName":"Pattern-08","stepsCount":0,"timeSpent":0,"success":null,"submitted":false,"startedAt":1766353711390},{"trial":9,"testName":"Pattern-09","stepsCount":0,"timeSpent":2,"success":false,"startedAt":1766353711469},{"trial":10,"testName":"Pattern-10","stepsCount":0,"timeSpent":0,"success":false,"startedAt":1766353711555},{"trial":11,"testName":"Pattern-11","stepsCount":0,"timeSpent":85,"success":false,"startedAt":1766353711635},{"trial":12,"testName":"Pattern-12","stepsCount":0,"timeSpent":0,"success":null,"submitted":false,"startedAt":1766353711738},{"trial":13,"testName":"Pattern-13","stepsCount":0,"timeSpent":3,"success":false,"startedAt":1766353711800},{"trial":14,"testName":"Pattern-14","stepsCount":0,"timeSpent":4,"success":false,"startedAt":1766353711884},{"trial":15,"testName":"Pattern-15","stepsCount":0,"timeSpent":1,"success":false,"startedAt":1766353711969},{"trial":16,"testName":"Pattern-16","stepsCount":0,"timeSpent":0,"success":false,"startedAt":1766353712054},{"trial":17,"testName":"Pattern-17","stepsCount":0,"timeSpent":0,"success":false,"startedAt":1766353712136},{"trial":18,"testName":"Pattern-18","stepsCount":0,"timeSpent":4,"success":false,"startedAt":1766353712217},{"trial":19,"testName":"Pattern-19","stepsCount":0,"timeSpent":6,"success":false,"startedAt":1766353712301},{"trial":20,"testName":"Pattern-20","stepsCount":0,"timeSpent":6,"success":false,"startedAt":1766353712384},{"trial":21,"testName":"Pattern-21","stepsCount":0,"timeSpent":6,"success":false,"startedAt":1766353712467},{"trial":22,"testName":"Pattern-22","stepsCount":0,"timeSpent":7,"success":false,"startedAt":1766353712550},{"trial":23,"testName":"Pattern-24","stepsCount":0,"timeSpent":6,"success":false,"startedAt":1766353712634},{"trial":24,"testName":"Pattern-25","stepsCount":0,"timeSpent":4,"success":false,"startedAt":1766353712718},{"trial":25,"testName":"Pattern-26","stepsCount":0,"timeSpent":342,"success":false,"startedAt":1766353712802}]"""

data = json.loads(data_json)

print("=" * 80)
print("🎯 被试数据分析报告")
print("=" * 80)
print(f"\n📋 参与者ID: P_1766351552481_4302czgnx")
print(f"🔄 实验条件: freeplayFirst")
print(f"📅 提交时间: 2025-12-21 21:48:35")
print(f"💻 设备信息: Macintosh (2240x1260)")
print()

# 基本统计
metadata = data[0]
trials = data[1:]

print("=" * 80)
print("📊 整体表现")
print("=" * 80)

total_trials = len(trials)
successful = sum(1 for t in trials if t.get('success') == True)
failed = sum(1 for t in trials if t.get('success') == False)
null = sum(1 for t in trials if t.get('success') is None)
submitted = sum(1 for t in trials if t.get('submitted', False))

total_time = sum(t.get('timeSpent', 0) for t in trials) / 1000  # 转换为秒
total_steps = sum(t.get('stepsCount', 0) for t in trials)
total_points = trials[-1].get('totalPointsAfter', 0) if trials else 0
max_points = metadata.get('totalTasks', total_trials)

print(f"  总任务数:        {total_trials}")
print(f"  成功任务:        {successful} ({successful/total_trials*100:.1f}%)")
print(f"  失败任务:        {failed} ({failed/total_trials*100:.1f}%)")
print(f"  未完成任务:      {null}")
print(f"  总得分:          {total_points}/{max_points}")
print(f"  总用时:          {total_time:.1f}秒 ({total_time/60:.1f}分钟)")
print(f"  总操作步骤:      {total_steps}步")
print()

# 时间分析
print("=" * 80)
print("⏱️  时间分析")
print("=" * 80)

engaged_trials = [t for t in trials if t.get('timeSpent', 0) >= 1000]  # 大于1秒
quick_skips = [t for t in trials if t.get('timeSpent', 0) < 1000]

if engaged_trials:
    avg_engaged_time = sum(t['timeSpent'] for t in engaged_trials) / len(engaged_trials) / 1000
    print(f"  有效参与任务:    {len(engaged_trials)}题")
    print(f"  平均用时:        {avg_engaged_time:.1f}秒/题")
    
print(f"  快速跳过任务:    {len(quick_skips)}题")
print()

# 放弃点分析
print("=" * 80)
print("🚨 放弃模式分析")
print("=" * 80)

abandonment_point = None
for i, trial in enumerate(trials):
    if trial.get('stepsCount', 0) == 0 and trial.get('timeSpent', 0) < 1000:
        # 检查后续是否持续为0
        if i + 2 < len(trials):
            next_two = trials[i:i+3]
            if all(t.get('stepsCount', 0) == 0 for t in next_two):
                abandonment_point = trial['trial']
                break

if abandonment_point:
    pre_abandon = [t for t in trials if t['trial'] < abandonment_point]
    post_abandon = [t for t in trials if t['trial'] >= abandonment_point]
    
    pre_success = sum(1 for t in pre_abandon if t.get('success'))
    post_success = sum(1 for t in post_abandon if t.get('success'))
    
    print(f"  ⚠️  放弃时间点:    第 {abandonment_point} 题")
    print(f"  放弃前表现:      {pre_success}/{len(pre_abandon)} 成功")
    print(f"  放弃后表现:      {post_success}/{len(post_abandon)} 成功")
else:
    print(f"  ✅ 未检测到明显放弃模式")
print()

# 详细任务进度
print("=" * 80)
print("📝 任务完成详情")
print("=" * 80)
print()
print(f"{'试次':<6} {'图案':<12} {'用时':<10} {'步骤':<6} {'结果':<8} {'状态':<10}")
print("-" * 80)

for trial in trials[:10]:  # 只显示前10题
    trial_num = trial.get('trial', '?')
    pattern = trial.get('testName', 'Unknown')
    time_sec = trial.get('timeSpent', 0) / 1000
    steps = trial.get('stepsCount', 0)
    success = trial.get('success')
    
    if success == True:
        result = "✅ 成功"
    elif success == False:
        result = "❌ 失败"
    else:
        result = "⚪ 未完成"
    
    if steps == 0 and time_sec < 1:
        status = "跳过"
    elif steps >= 1:
        status = "尝试"
    else:
        status = "-"
    
    print(f"{trial_num:<6} {pattern:<12} {time_sec:<10.1f} {steps:<6} {result:<8} {status:<10}")

if len(trials) > 10:
    print(f"... (省略 {len(trials) - 10} 题)")
print()

# 操作使用分析
print("=" * 80)
print("🔧 操作使用分析")
print("=" * 80)

all_operations = []
for trial in trials:
    ops = trial.get('operations', [])
    all_operations.extend(ops)

if all_operations:
    from collections import Counter
    op_counts = Counter(all_operations)
    
    print(f"  总操作数:        {len(all_operations)}")
    print(f"  独特操作:        {len(op_counts)}")
    print()
    print("  最常用操作:")
    for op, count in op_counts.most_common(5):
        print(f"    {op:<30} {count}次")
else:
    print("  ⚠️  无操作记录")
print()

# 收藏夹使用
print("=" * 80)
print("⭐ 收藏夹使用分析")
print("=" * 80)

fav_actions = []
for trial in trials:
    fav_actions.extend(trial.get('favoriteActions', []))

fav_add = sum(1 for f in fav_actions if f.get('action') == 'add')
fav_use = sum(1 for f in fav_actions if f.get('action') == 'use')
fav_remove = sum(1 for f in fav_actions if f.get('action') == 'remove')

print(f"  添加收藏:        {fav_add}次")
print(f"  使用收藏:        {fav_use}次")
print(f"  删除收藏:        {fav_remove}次")

if fav_use > 0:
    trials_with_fav = [t for t in trials if t.get('favoriteActions', [])]
    success_with_fav = sum(1 for t in trials_with_fav if t.get('success'))
    print(f"  使用收藏的成功率: {success_with_fav}/{len(trials_with_fav)} ({success_with_fav/len(trials_with_fav)*100:.1f}%)")
print()

# 学习曲线
print("=" * 80)
print("📈 学习曲线分析")
print("=" * 80)

if len(engaged_trials) >= 3:
    first_third = engaged_trials[:len(engaged_trials)//3] if len(engaged_trials) >= 3 else engaged_trials[:1]
    last_third = engaged_trials[-len(engaged_trials)//3:] if len(engaged_trials) >= 3 else engaged_trials[-1:]
    
    early_success = sum(1 for t in first_third if t.get('success')) / len(first_third) if first_third else 0
    late_success = sum(1 for t in last_third if t.get('success')) / len(last_third) if last_third else 0
    
    early_time = sum(t.get('timeSpent', 0) for t in first_third) / len(first_third) / 1000 if first_third else 0
    late_time = sum(t.get('timeSpent', 0) for t in last_third) / len(last_third) / 1000 if last_third else 0
    
    print(f"  早期成功率:      {early_success:.1%}")
    print(f"  后期成功率:      {late_success:.1%}")
    print(f"  早期平均用时:    {early_time:.1f}秒")
    print(f"  后期平均用时:    {late_time:.1f}秒")
    print(f"  时间改进:        {early_time - late_time:.1f}秒")
    print(f"  效率改进:        {(late_success - early_success)*100:.1f}%")
else:
    print("  ⚠️  数据不足,无法分析学习曲线")
print()

# 关键洞察
print("=" * 80)
print("💡 关键洞察")
print("=" * 80)
print()

if successful >= 2 and abandonment_point:
    print("  ✅ 前期表现优秀: 成功完成了前2题,展示了良好的问题解决能力")
    print(f"  ⚠️  第{abandonment_point}题开始放弃: 可能遇到难度陡增")
    print("  📊 放弃模式明显: 后续21题基本都是快速跳过")
    print("  🎯 有效数据: 只有前3题有分析价值")
    print()
    print("  建议:")
    print("    • 优化难度曲线,避免第3题的难度突增")
    print("    • 增加提示系统帮助参与者从失败中恢复")
    print("    • 考虑减少总任务数到10-15题")
    print("    • 添加阶段性反馈和激励机制")
elif successful == 0:
    print("  ❌ 全部失败: 参与者可能未理解任务")
    print("  建议: 改进教程和示例")
else:
    print("  📊 数据已记录")

print()
print("=" * 80)
print("✅ 分析完成")
print("=" * 80)
