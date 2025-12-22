#!/usr/bin/env python3
"""深度策略和过程分析 - 参与者2和3"""

import json
from collections import Counter, defaultdict
from datetime import datetime

# 读取数据
with open('/Users/mac/Downloads/experiment_data.json', 'r') as f:
    data = json.load(f)

participants_data = data[2]['data']

def analyze_strategy_evolution(trials):
    """分析策略演化"""
    print("\n" + "="*100)
    print("🧠 策略演化分析")
    print("="*100)
    
    # 操作复杂度随时间变化
    complexity_over_time = []
    for t in trials:
        steps = t.get('stepsCount', 0)
        complexity_over_time.append(steps)
    
    # 分段分析
    third = len(trials) // 3
    early_complexity = sum(complexity_over_time[:third]) / third if third > 0 else 0
    mid_complexity = sum(complexity_over_time[third:third*2]) / third if third > 0 else 0
    late_complexity = sum(complexity_over_time[third*2:]) / (len(trials) - third*2) if len(trials) > third*2 else 0
    
    print(f"\n  步骤复杂度变化:")
    print(f"    前期(1-8题):   {early_complexity:.1f}步/题")
    print(f"    中期(9-16题):  {mid_complexity:.1f}步/题")
    print(f"    后期(17-25题): {late_complexity:.1f}步/题")
    
    # 操作类型偏好演化
    early_ops = []
    mid_ops = []
    late_ops = []
    
    for i, t in enumerate(trials):
        if i < third:
            early_ops.extend(t.get('operations', []))
        elif i < third*2:
            mid_ops.extend(t.get('operations', []))
        else:
            late_ops.extend(t.get('operations', []))
    
    print(f"\n  操作类型偏好演化:")
    
    def count_op_types(ops):
        return {
            'add': sum(1 for op in ops if 'add' in op.lower()),
            'subtract': sum(1 for op in ops if 'subtract' in op.lower()),
            'reflect': sum(1 for op in ops if 'reflect' in op.lower()),
            'invert': sum(1 for op in ops if 'invert' in op.lower()),
            'overlap': sum(1 for op in ops if 'overlap' in op.lower()),
        }
    
    early_types = count_op_types(early_ops)
    mid_types = count_op_types(mid_ops)
    late_types = count_op_types(late_ops)
    
    for op_type in ['add', 'subtract', 'reflect', 'invert', 'overlap']:
        e = early_types.get(op_type, 0)
        m = mid_types.get(op_type, 0)
        l = late_types.get(op_type, 0)
        print(f"    {op_type:<12} 前期:{e:>2}次  中期:{m:>2}次  后期:{l:>2}次")

def analyze_helper_strategy(trials):
    """分析Helper使用策略"""
    print("\n" + "="*100)
    print("⭐ Helper策略分析")
    print("="*100)
    
    # Helper创建时机
    create_trials = []
    use_trials = []
    
    for t in trials:
        fav_actions = t.get('favoriteActions', [])
        for action in fav_actions:
            if action.get('action') == 'add':
                create_trials.append(t.get('trial'))
            elif action.get('action') == 'use':
                use_trials.append(t.get('trial'))
    
    print(f"\n  Helper创建模式:")
    print(f"    总创建次数: {len(create_trials)}")
    print(f"    平均创建间隔: {(max(create_trials) - min(create_trials)) / len(create_trials):.1f}题" if create_trials else "    无创建")
    
    if create_trials:
        print(f"    创建集中在: 试次 {', '.join(map(str, create_trials[:10]))}{' ...' if len(create_trials) > 10 else ''}")
    
    print(f"\n  Helper使用模式:")
    print(f"    总使用次数: {len(use_trials)}")
    print(f"    使用覆盖率: {len(set(use_trials))}/{len(trials)}题 ({len(set(use_trials))/len(trials)*100:.1f}%)")
    
    # Helper使用与成功的关系
    trials_with_helper = [t for t in trials if any(a.get('action') == 'use' for a in t.get('favoriteActions', []))]
    trials_without_helper = [t for t in trials if not any(a.get('action') == 'use' for a in t.get('favoriteActions', []))]
    
    if trials_with_helper:
        success_with = sum(1 for t in trials_with_helper if t.get('success'))
        print(f"    使用Helper时成功率: {success_with}/{len(trials_with_helper)} ({success_with/len(trials_with_helper)*100:.1f}%)")
    
    if trials_without_helper:
        success_without = sum(1 for t in trials_without_helper if t.get('success'))
        print(f"    不用Helper时成功率: {success_without}/{len(trials_without_helper)} ({success_without/len(trials_without_helper)*100:.1f}%)")

def analyze_problem_solving_process(trials):
    """分析问题解决过程"""
    print("\n" + "="*100)
    print("🔍 问题解决过程分析")
    print("="*100)
    
    # 一步解决 vs 多步解决
    one_step = sum(1 for t in trials if t.get('stepsCount') == 1)
    two_step = sum(1 for t in trials if t.get('stepsCount') == 2)
    three_plus = sum(1 for t in trials if t.get('stepsCount') >= 3)
    
    print(f"\n  解题路径长度分布:")
    print(f"    一步解决:   {one_step}题 ({one_step/len(trials)*100:.1f}%)")
    print(f"    两步解决:   {two_step}题 ({two_step/len(trials)*100:.1f}%)")
    print(f"    三步及以上: {three_plus}题 ({three_plus/len(trials)*100:.1f}%)")
    
    # 时间 vs 步骤关系
    print(f"\n  效率分析:")
    time_per_step = []
    for t in trials:
        if t.get('stepsCount', 0) > 0:
            time_per_step.append(t.get('timeSpent', 0) / 1000 / t['stepsCount'])
    
    if time_per_step:
        avg_time = sum(time_per_step) / len(time_per_step)
        print(f"    平均每步用时: {avg_time:.1f}秒")
        print(f"    最快单步:     {min(time_per_step):.1f}秒")
        print(f"    最慢单步:     {max(time_per_step):.1f}秒")
    
    # 思考时间 vs 执行时间
    print(f"\n  思考模式:")
    quick_decisions = sum(1 for t in trials if t.get('timeSpent', 0) < 30000 and t.get('success'))
    slow_decisions = sum(1 for t in trials if t.get('timeSpent', 0) >= 60000 and t.get('success'))
    
    print(f"    快速决策(<30s): {quick_decisions}题")
    print(f"    深思熟虑(>60s): {slow_decisions}题")

def analyze_error_recovery(trials):
    """分析错误恢复能力"""
    print("\n" + "="*100)
    print("🔧 错误恢复与调整")
    print("="*100)
    
    # Undo使用分析
    undo_counts = []
    reset_counts = []
    
    for t in trials:
        undo_actions = t.get('undoActions', [])
        total_undos = sum(action.get('stepsCleared', 0) for action in undo_actions)
        undo_counts.append(total_undos)
        reset_counts.append(len([a for a in undo_actions if a.get('type') == 'reset']))
    
    total_undos = sum(undo_counts)
    trials_with_undo = sum(1 for c in undo_counts if c > 0)
    
    print(f"\n  撤销/重置行为:")
    print(f"    总撤销步骤数: {total_undos}步")
    print(f"    使用撤销的题: {trials_with_undo}/{len(trials)}题")
    print(f"    平均撤销:     {total_undos/len(trials):.1f}步/题")
    
    # 失败后的表现
    failed_trials = [i for i, t in enumerate(trials) if t.get('success') == False]
    
    if failed_trials:
        print(f"\n  失败后的调整:")
        for fail_idx in failed_trials:
            if fail_idx + 1 < len(trials):
                next_trial = trials[fail_idx + 1]
                print(f"    失败题{trials[fail_idx].get('trial')}后 → 题{next_trial.get('trial')}: {'✅成功' if next_trial.get('success') else '❌失败'}")

def analyze_cognitive_patterns(trials):
    """分析认知模式"""
    print("\n" + "="*100)
    print("🧩 认知模式识别")
    print("="*100)
    
    # 模式复用 - 相同操作序列的重复
    operation_sequences = []
    for t in trials:
        ops = tuple(t.get('operations', []))
        if ops:
            operation_sequences.append(ops)
    
    seq_counter = Counter(operation_sequences)
    repeated_sequences = {seq: count for seq, count in seq_counter.items() if count > 1}
    
    print(f"\n  策略复用:")
    print(f"    独特操作序列: {len(seq_counter)}")
    print(f"    重复使用序列: {len(repeated_sequences)}")
    
    if repeated_sequences:
        print(f"\n    最常重复的策略:")
        for seq, count in sorted(repeated_sequences.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"      {' → '.join(seq[:2])}{'...' if len(seq) > 2 else '':<20} 使用{count}次")
    
    # 操作对的常见组合
    operation_pairs = []
    for t in trials:
        ops = t.get('operations', [])
        for i in range(len(ops) - 1):
            operation_pairs.append((ops[i], ops[i+1]))
    
    if operation_pairs:
        pair_counter = Counter(operation_pairs)
        print(f"\n  常见操作组合:")
        for (op1, op2), count in pair_counter.most_common(5):
            print(f"    {op1:<30} → {op2:<30} {count}次")

# 主分析循环
for idx in [1, 2]:  # 参与者2和3
    p = participants_data[idx]
    
    print("\n\n")
    print("█" * 100)
    print(f"{'█':<5} 参与者 {idx + 1} 深度策略分析 {'█':>85}")
    print("█" * 100)
    
    task_data = json.loads(p['task_data'])
    trials = task_data[1:]
    
    # 基本信息
    print(f"\n📋 参与者: {p['participant_id']}")
    print(f"📅 时间: {p['submission_time']}")
    print(f"🎯 成绩: {sum(1 for t in trials if t.get('success'))}/{len(trials)} ({sum(1 for t in trials if t.get('success'))/len(trials)*100:.0f}%)")
    
    # 各项分析
    analyze_strategy_evolution(trials)
    analyze_helper_strategy(trials)
    analyze_problem_solving_process(trials)
    analyze_error_recovery(trials)
    analyze_cognitive_patterns(trials)
    
    # 详细案例分析
    print("\n" + "="*100)
    print("📚 代表性任务案例分析")
    print("="*100)
    
    # 找出最快、最慢、最复杂的任务
    successful_trials = [t for t in trials if t.get('success')]
    
    if successful_trials:
        fastest = min(successful_trials, key=lambda t: t.get('timeSpent', 999999))
        slowest = max(successful_trials, key=lambda t: t.get('timeSpent', 0))
        most_complex = max(successful_trials, key=lambda t: t.get('stepsCount', 0))
        
        print(f"\n  ⚡ 最快完成 (试次{fastest.get('trial')} - {fastest.get('testName')}):")
        print(f"      用时: {fastest.get('timeSpent')/1000:.1f}秒")
        print(f"      步骤: {fastest.get('stepsCount')}步")
        print(f"      操作: {' → '.join(fastest.get('operations', []))}")
        
        print(f"\n  🐌 最慢完成 (试次{slowest.get('trial')} - {slowest.get('testName')}):")
        print(f"      用时: {slowest.get('timeSpent')/1000:.1f}秒")
        print(f"      步骤: {slowest.get('stepsCount')}步")
        print(f"      操作: {' → '.join(slowest.get('operations', []))}")
        
        print(f"\n  🧩 最复杂解法 (试次{most_complex.get('trial')} - {most_complex.get('testName')}):")
        print(f"      用时: {most_complex.get('timeSpent')/1000:.1f}秒")
        print(f"      步骤: {most_complex.get('stepsCount')}步")
        print(f"      操作: {' → '.join(most_complex.get('operations', []))}")
    
    # 关键转折点
    print("\n" + "="*100)
    print("🎯 关键转折点")
    print("="*100)
    
    # 找出效率提升的转折点
    time_per_trial = [t.get('timeSpent', 0) / 1000 for t in trials]
    
    # 寻找时间显著下降的点
    for i in range(3, len(trials)):
        before_avg = sum(time_per_trial[:i]) / i
        after_avg = sum(time_per_trial[i:]) / (len(trials) - i)
        
        if before_avg > after_avg * 1.5:  # 效率提升50%以上
            print(f"\n  ⭐ 效率突破点: 第{i+1}题")
            print(f"      之前平均: {before_avg:.1f}秒/题")
            print(f"      之后平均: {after_avg:.1f}秒/题")
            print(f"      提升: {(before_avg - after_avg) / before_avg * 100:.1f}%")
            break
    
    # 总结性洞察
    print("\n" + "="*100)
    print("💡 策略特征总结")
    print("="*100)
    
    # 主导策略识别
    all_ops = []
    for t in trials:
        all_ops.extend(t.get('operations', []))
    
    op_types = {
        'add': sum(1 for op in all_ops if 'add' in op.lower()),
        'subtract': sum(1 for op in all_ops if 'subtract' in op.lower()),
        'reflect': sum(1 for op in all_ops if 'reflect' in op.lower()),
        'invert': sum(1 for op in all_ops if 'invert' in op.lower()),
        'overlap': sum(1 for op in all_ops if 'overlap' in op.lower()),
    }
    
    dominant_strategy = max(op_types.items(), key=lambda x: x[1])
    
    avg_steps = sum(t.get('stepsCount', 0) for t in trials) / len(trials)
    avg_time = sum(t.get('timeSpent', 0) for t in trials) / len(trials) / 1000
    
    print(f"\n  核心特征:")
    print(f"    • 主导策略: {dominant_strategy[0]} ({dominant_strategy[1]}次, {dominant_strategy[1]/len(all_ops)*100:.1f}%)")
    print(f"    • 解题风格: {'简洁高效' if avg_steps < 2.5 else '稳健复杂'} (平均{avg_steps:.1f}步)")
    print(f"    • 决策速度: {'快速果断' if avg_time < 60 else '深思熟虑'} (平均{avg_time:.1f}秒)")
    
    helper_usage = sum(len([a for a in t.get('favoriteActions', []) if a.get('action') == 'use']) for t in trials)
    print(f"    • Helper依赖: {'高度依赖' if helper_usage > 100 else '适度使用' if helper_usage > 50 else '轻度使用'} ({helper_usage}次)")
    
    undo_total = sum(sum(a.get('stepsCleared', 0) for a in t.get('undoActions', [])) for t in trials)
    print(f"    • 错误容忍: {'频繁调整' if undo_total > 20 else '偶尔修正' if undo_total > 5 else '很少撤销'} ({undo_total}次撤销)")

print("\n\n")
print("█" * 100)
print("✅ 深度策略分析完成!")
print("█" * 100)
