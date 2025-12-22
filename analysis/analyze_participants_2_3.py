#!/usr/bin/env python3
"""分析参与者2和参与者3的详细数据"""

import json
from datetime import datetime
from collections import Counter

# 读取数据
with open('/Users/mac/Downloads/experiment_data.json', 'r') as f:
    data = json.load(f)

participants_data = data[2]['data']

# 分析参与者2和3
for idx in [1, 2]:  # 参与者2和3 (索引1和2)
    p = participants_data[idx]
    
    print("=" * 100)
    print(f"🎯 参与者 {idx + 1} 详细分析报告")
    print("=" * 100)
    print(f"\n📋 基本信息")
    print(f"  参与者ID:     {p['participant_id']}")
    print(f"  实验条件:     {p['condition']}")
    print(f"  提交时间:     {p['submission_time']}")
    print(f"  设备:         {p['user_agent'].split(') ')[0].split('(')[1] if '(' in p['user_agent'] else 'Unknown'}")
    print(f"  分辨率:       {p['screen_resolution']}")
    print()
    
    # 解析task_data
    task_data = json.loads(p['task_data'])
    metadata = task_data[0]
    trials = task_data[1:]
    
    # 基本统计
    print("=" * 100)
    print("📊 任务完成情况")
    print("=" * 100)
    
    total = len(trials)
    successful = sum(1 for t in trials if t.get('success') == True)
    failed = sum(1 for t in trials if t.get('success') == False)
    null = sum(1 for t in trials if t.get('success') is None)
    
    total_time = sum(t.get('timeSpent', 0) for t in trials) / 1000
    total_steps = sum(t.get('stepsCount', 0) for t in trials)
    total_points = trials[-1].get('totalPointsAfter', 0) if trials else 0
    
    print(f"  总任务数:         {total}")
    print(f"  ✅ 成功完成:      {successful} ({successful/total*100:.1f}%)")
    print(f"  ❌ 失败:          {failed} ({failed/total*100:.1f}%)")
    print(f"  ⚪ 未完成:        {null}")
    print(f"  🏆 总得分:        {total_points}/{metadata.get('totalTasks', total)}")
    print(f"  ⏱️  总用时:        {total_time:.1f}秒 ({total_time/60:.1f}分钟)")
    print(f"  🔧 总操作步骤:    {total_steps}步")
    print(f"  📈 平均步骤/题:   {total_steps/total:.1f}步")
    print()
    
    # 时间分析
    print("=" * 100)
    print("⏱️  时间效率分析")
    print("=" * 100)
    
    engaged = [t for t in trials if t.get('timeSpent', 0) >= 1000]
    successful_trials = [t for t in trials if t.get('success') == True]
    
    if successful_trials:
        avg_success_time = sum(t['timeSpent'] for t in successful_trials) / len(successful_trials) / 1000
        min_time = min(t['timeSpent'] for t in successful_trials) / 1000
        max_time = max(t['timeSpent'] for t in successful_trials) / 1000
        
        print(f"  平均完成时间:     {avg_success_time:.1f}秒/题")
        print(f"  最快完成:         {min_time:.1f}秒")
        print(f"  最慢完成:         {max_time:.1f}秒")
        
        # 时间分布
        fast = sum(1 for t in successful_trials if t['timeSpent'] < 10000)
        medium = sum(1 for t in successful_trials if 10000 <= t['timeSpent'] < 30000)
        slow = sum(1 for t in successful_trials if t['timeSpent'] >= 30000)
        
        print(f"  快速(<10s):       {fast}题")
        print(f"  中速(10-30s):     {medium}题")
        print(f"  慢速(>30s):       {slow}题")
    print()
    
    # 操作分析
    print("=" * 100)
    print("🔧 操作策略分析")
    print("=" * 100)
    
    all_ops = []
    for t in trials:
        all_ops.extend(t.get('operations', []))
    
    if all_ops:
        op_counts = Counter(all_ops)
        
        print(f"  总操作次数:       {len(all_ops)}")
        print(f"  独特操作类型:     {len(op_counts)}")
        print(f"  平均操作/题:      {len(all_ops)/total:.1f}")
        print()
        print("  最常用操作 (Top 10):")
        for op, count in op_counts.most_common(10):
            print(f"    {op:<40} {count:>3}次 ({count/len(all_ops)*100:>5.1f}%)")
    print()
    
    # 操作类型分类
    op_types = {
        'add': sum(1 for op in all_ops if 'add' in op.lower()),
        'subtract': sum(1 for op in all_ops if 'subtract' in op.lower()),
        'reflect': sum(1 for op in all_ops if 'reflect' in op.lower()),
        'rotate': sum(1 for op in all_ops if 'rotate' in op.lower()),
        'invert': sum(1 for op in all_ops if 'invert' in op.lower()),
    }
    
    print("  操作类型分布:")
    for op_type, count in sorted(op_types.items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            print(f"    {op_type:<15} {count:>3}次 ({count/len(all_ops)*100:>5.1f}%)")
    print()
    
    # 收藏夹使用
    print("=" * 100)
    print("⭐ 收藏夹(Helper)使用分析")
    print("=" * 100)
    
    all_fav_actions = []
    for t in trials:
        all_fav_actions.extend(t.get('favoriteActions', []))
    
    fav_add = sum(1 for f in all_fav_actions if f.get('action') == 'add')
    fav_use = sum(1 for f in all_fav_actions if f.get('action') == 'use')
    fav_remove = sum(1 for f in all_fav_actions if f.get('action') == 'remove')
    
    print(f"  创建Helper:       {fav_add}次")
    print(f"  使用Helper:       {fav_use}次")
    print(f"  删除Helper:       {fav_remove}次")
    
    trials_with_fav = [t for t in trials if any(f.get('action') == 'use' for f in t.get('favoriteActions', []))]
    if trials_with_fav:
        success_with_fav = sum(1 for t in trials_with_fav if t.get('success'))
        print(f"  使用Helper的任务: {len(trials_with_fav)}题")
        print(f"  使用时成功率:     {success_with_fav}/{len(trials_with_fav)} ({success_with_fav/len(trials_with_fav)*100:.1f}%)")
    print()
    
    # 学习曲线
    print("=" * 100)
    print("📈 学习曲线分析")
    print("=" * 100)
    
    # 分成前中后三段
    third = len(trials) // 3
    early = trials[:third]
    middle = trials[third:third*2]
    late = trials[third*2:]
    
    for phase_name, phase_trials in [('前期(1-8题)', early), ('中期(9-16题)', middle), ('后期(17-25题)', late)]:
        phase_success = sum(1 for t in phase_trials if t.get('success'))
        phase_time = sum(t.get('timeSpent', 0) for t in phase_trials) / len(phase_trials) / 1000 if phase_trials else 0
        phase_steps = sum(t.get('stepsCount', 0) for t in phase_trials) / len(phase_trials) if phase_trials else 0
        
        print(f"  {phase_name}")
        print(f"    成功率:         {phase_success}/{len(phase_trials)} ({phase_success/len(phase_trials)*100:.1f}%)")
        print(f"    平均用时:       {phase_time:.1f}秒")
        print(f"    平均步骤:       {phase_steps:.1f}步")
    
    # 效率改进
    early_time = sum(t.get('timeSpent', 0) for t in early) / len(early) / 1000 if early else 0
    late_time = sum(t.get('timeSpent', 0) for t in late) / len(late) / 1000 if late else 0
    time_improvement = early_time - late_time
    
    early_success_rate = sum(1 for t in early if t.get('success')) / len(early) if early else 0
    late_success_rate = sum(1 for t in late if t.get('success')) / len(late) if late else 0
    
    print()
    print(f"  💡 学习效果:")
    print(f"    时间改进:       {time_improvement:+.1f}秒 ({time_improvement/early_time*100:+.1f}%)" if early_time > 0 else "    时间改进:       N/A")
    print(f"    成功率变化:     {(late_success_rate - early_success_rate)*100:+.1f}%")
    print()
    
    # 失败任务分析
    if failed > 0:
        print("=" * 100)
        print("❌ 失败任务分析")
        print("=" * 100)
        
        failed_trials = [t for t in trials if t.get('success') == False]
        print(f"  失败任务列表:")
        for t in failed_trials:
            print(f"    试次{t.get('trial'):>2}: {t.get('testName'):<15} 用时{t.get('timeSpent', 0)/1000:>6.1f}秒  步骤{t.get('stepsCount', 0):>2}  操作: {', '.join(t.get('operations', [])[:3])}")
        print()
    
    # 详细任务列表
    print("=" * 100)
    print("📝 详细任务完成记录")
    print("=" * 100)
    print()
    print(f"{'试次':<5} {'图案':<15} {'用时':<8} {'步骤':<5} {'操作数':<6} {'结果':<6} {'主要操作':<30}")
    print("-" * 100)
    
    for t in trials:
        trial_num = t.get('trial', '?')
        pattern = t.get('testName', 'Unknown')
        time_sec = t.get('timeSpent', 0) / 1000
        steps = t.get('stepsCount', 0)
        ops_count = len(t.get('operations', []))
        success = t.get('success')
        
        if success == True:
            result = "✅"
        elif success == False:
            result = "❌"
        else:
            result = "⚪"
        
        main_ops = ', '.join(t.get('operations', [])[:2]) if t.get('operations') else '-'
        if len(t.get('operations', [])) > 2:
            main_ops += '...'
        
        print(f"{trial_num:<5} {pattern:<15} {time_sec:<8.1f} {steps:<5} {ops_count:<6} {result:<6} {main_ops:<30}")
    
    print()
    
    # Freeplay数据分析
    if p['freeplay_data']:
        print("=" * 100)
        print("🎨 Freeplay阶段分析")
        print("=" * 100)
        
        freeplay_data = json.loads(p['freeplay_data'])
        
        sessions = freeplay_data.get('sessions', [])
        gallery = freeplay_data.get('gallery', [])
        helpers = freeplay_data.get('helpers', [])
        
        print(f"  创作会话数:       {len(sessions)}")
        print(f"  保存图案数:       {len(gallery)}")
        print(f"  创建Helper数:     {len(helpers)}")
        
        if sessions:
            total_ops = sum(len(s.get('operationActions', [])) for s in sessions)
            total_clicks = sum(len(s.get('buttonClickActions', [])) for s in sessions)
            print(f"  总操作数:         {total_ops}")
            print(f"  总点击数:         {total_clicks}")
        
        if gallery:
            print()
            print(f"  创作的图案:")
            for i, item in enumerate(gallery[:10], 1):  # 只显示前10个
                name = item.get('name', f'图案{i}')
                print(f"    {i}. {name}")
            if len(gallery) > 10:
                print(f"    ... 还有 {len(gallery) - 10} 个图案")
        print()
    
    # 总结
    print("=" * 100)
    print("💡 表现总结")
    print("=" * 100)
    
    if successful >= 20:
        print("  🌟 优秀表现!")
        print(f"    • 成功率高达 {successful/total*100:.1f}%,展示了卓越的问题解决能力")
        print(f"    • 平均每题用时 {total_time/total:.1f}秒,效率很高")
        print(f"    • 有效使用了Helper功能,展现良好的学习迁移能力")
    elif successful >= 15:
        print("  👍 良好表现!")
        print(f"    • 成功完成了大部分任务 ({successful}/{total})")
        print(f"    • 展示了持续的学习和改进")
    
    if time_improvement > 0:
        print(f"    • 学习效率提升明显,后期比前期快了 {time_improvement:.1f}秒")
    
    print()
    print("=" * 100)
    print()
    print()

print("✅ 分析完成!")
