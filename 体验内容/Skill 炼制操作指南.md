# 🧪 Skill 炼制操作指南

> 基于飞书 Aily 实战脚本，完整的 Skill 沉淀与复用流程

---

## 📋 目录

1. [快速开始](#快速开始)
2. [步骤 1：对话数据收集](#步骤-1对话数据收集)
3. [步骤 2：Skill 提取](#步骤-2skill-提取)
4. [步骤 3：Skill 验证](#步骤-3skill-验证)
5. [步骤 4：Skill 存储](#步骤-4skill-存储)
6. [步骤 5：Skill 复用](#步骤-5skill-复用)
7. [步骤 6：Skill 演化](#步骤-6skill-演化)

---

## 🚀 快速开始

### 前置准备

```bash
# 安装依赖
pip install -r requirements.txt

# 初始化 Skill 数据库
python skill_refinery.py init
```

### 一键炼制

```bash
# 从对话日志中炼制 Skill
python skill_refinery.py refine --conversation conversation_log.json
```

---

## 步骤 1：对话数据收集

### 1.1 对话日志格式

对话日志应该是 JSON 格式，包含以下字段：

```json
{
  "conversation_id": "conv_20240115_001",
  "start_time": "2024-01-15 10:00:00",
  "end_time": "2024-01-15 10:02:30",
  "turns": [
    {
      "turn": 1,
      "role": "user",
      "content": "我想在上班时间禁止员工访问社交媒体网站",
      "timestamp": "2024-01-15 10:00:00"
    },
    {
      "turn": 2,
      "role": "assistant",
      "content": "好的！我来帮您配置这个访问策略...",
      "extracted_info": {
        "strategy_type": "specific_website",
        "target_category": "social_media",
        "time_restriction": "work_hours"
      },
      "timestamp": "2024-01-15 10:00:05"
    }
    // ... 更多对话轮次
  ],
  "final_config": {
    "strategy_name": "工作时间社交媒体访问限制",
    "strategy_type": "specific_website",
    "effective_members": "除BOSS外所有成员",
    // ... 完整配置
  },
  "success": true,
  "user_satisfaction": 5
}
```

### 1.2 手动记录对话

如果使用飞书 Aily 进行对话，可以：

1. **对话截图保存**
2. **手动整理为 JSON**（使用提供的模板）
3. **或使用录制工具**

```bash
# 启动对话录制工具
python skill_refinery.py record
```

输入命令后，按照提示进行操作：
```
请输入用户消息（输入 'done' 结束）：
> 我想在上班时间禁止员工访问社交媒体网站

请输入助手回复：
> 好的！我来帮您配置...

[提取的信息]
- 策略类型: specific_website
- 目标: 社交媒体
- 时间: 上班时间
```

---

## 步骤 2：Skill 提取

### 2.1 自动提取

```bash
python skill_refinery.py extract --conversation conversation_log.json --output extracted_skill.json
```

### 2.2 提取规则

系统会自动提取以下内容：

#### A. 触发关键词
```python
# 从用户输入中提取
- "社交媒体" → category: social_media
- "工作时间" → time_range: work_hours
- "禁止访问" → action: block
```

#### B. 对话模板
```python
# 从问答流程中提取
步骤1: 确认生效对象 → 常见答案: "除老板外所有员工" (置信度 85%)
步骤2: 确认生效时间 → 常见答案: "标准工作时间" (置信度 90%)
步骤3: 选择具体网站 → 推荐列表: [微博, 抖音, ...]
步骤4: 确认审批机制 → 常见答案: "老板审批" (置信度 75%)
```

#### C. 快速填充配置
```json
{
  "strategy_type": "specific_website",
  "effective_members": "除BOSS外所有成员",
  "effective_weekly": [1, 2, 3, 4, 5],
  "effective_time": {
    "start_time": "09:00",
    "end_time": "18:00"
  }
}
```

#### D. 学习规则
```json
{
  "rules": [
    {
      "pattern": "社交媒体",
      "entity_type": "website_category",
      "mapped_value": ["weibo.com", "douyin.com", ...]
    },
    {
      "pattern": "工作时间|上班时间",
      "entity_type": "time_range",
      "mapped_value": {
        "weekly": [1, 2, 3, 4, 5],
        "time": {"start": "09:00", "end": "18:00"}
      }
    }
  ]
}
```

### 2.3 手动调整

提取后的 Skill 可能需要人工审核和调整：

```bash
# 在交互模式下编辑
python skill_refinery.py edit --skill extracted_skill.json
```

**调整清单：**
- [ ] 关键词是否准确？
- [ ] 对话模板是否完整？
- [ ] 快速填充配置是否正确？
- [ ] 学习规则是否合理？
- [ ] Skill 名称是否清晰？

---

## 步骤 3：Skill 验证

### 3.1 相似度测试

验证 Skill 能否正确匹配相似的用户输入：

```bash
python skill_refinery.py test-match --skill extracted_skill.json
```

**测试用例：**
```
输入: "我想在上班时间禁止员工访问社交媒体网站"
匹配结果: social_media_work_hours_restriction_v1 (相似度: 95%)
✓ 通过

输入: "上班时间不让员工刷微博"
匹配结果: social_media_work_hours_restriction_v1 (相似度: 88%)
✓ 通过

输入: "限制员工看社交媒体"
匹配结果: social_media_work_hours_restriction_v1 (相似度: 65%)
✓ 通过

输入: "禁止下载文件"
匹配结果: 无匹配
✓ 通过（正确的不匹配）
```

### 3.2 配置生成测试

验证 Skill 能否生成正确的配置：

```bash
python skill_refinery.py test-generate --skill extracted_skill.json
```

**测试步骤：**
1. 使用默认参数生成配置
2. 检查必填字段是否完整
3. 检查字段值是否合理
4. 与原始对话的配置对比

```
✓ 策略类型正确: specific_website
✓ 生效对象正确: 除BOSS外所有成员
✓ 时间配置正确: 周一至周五 09:00-18:00
✓ 网站列表正确: 6个社交媒体网站
✓ 审批设置正确: 仅BOSS审批

测试通过！配置准确率: 100%
```

### 3.3 对话模拟测试

模拟用户与 Skill 的交互：

```bash
python skill_refinery.py simulate --skill extracted_skill.json
```

**模拟对话：**
```
[系统] 检测到匹配的 Skill: 工作时间社交媒体访问限制
[系统] 相似度: 95%

[助手] 🎯 我发现您的需求与已有的「工作时间社交媒体访问限制」模板非常相似！

该模板的配置是：
• 生效对象：除BOSS外所有成员
• 生效时间：周一至周五 09:00-18:00
• 限制网站：微博、抖音、小红书、Facebook、Twitter、Instagram
• 审批机制：允许申请，仅BOSS审批

您可以：
A. 直接使用这个模板（1秒生成配置）
B. 在这个模板基础上修改
C. 重新配置（不使用模板）

[用户输入] A

[助手] ✅ 配置已快速生成！（用时：0.5秒）

[系统] 测试通过！对话轮次: 2 (原始: 6)，节省时间: 66%
```

---

## 步骤 4：Skill 存储

### 4.1 保存到 Skill 库

验证通过后，将 Skill 保存到数据库：

```bash
python skill_refinery.py save --skill extracted_skill.json
```

**输出：**
```
✓ Skill ID: social_media_work_hours_restriction_v1
✓ Skill 名称: 工作时间社交媒体访问限制
✓ 触发关键词: 5个
✓ 对话步骤: 4步
✓ 学习规则: 3条

已保存到 Skill 库！
当前库中共有 1 个 Skills。
```

### 4.2 Skill 库结构

```
skills_database/
├── index.json                          # 索引文件
├── social_media_work_hours_v1.json    # 具体 Skill 文件
└── metadata.json                       # 元数据
```

**index.json 示例：**
```json
{
  "version": "1.0",
  "total_skills": 1,
  "skills": [
    {
      "skill_id": "social_media_work_hours_restriction_v1",
      "skill_name": "工作时间社交媒体访问限制",
      "skill_type": "specific_website",
      "usage_count": 1,
      "success_rate": 1.0,
      "created_at": "2024-01-15 10:30:00",
      "file_path": "social_media_work_hours_v1.json"
    }
  ]
}
```

### 4.3 查看 Skill 库

```bash
# 列出所有 Skills
python skill_refinery.py list

# 查看特定 Skill 详情
python skill_refinery.py show --skill-id social_media_work_hours_restriction_v1

# 搜索 Skill
python skill_refinery.py search --keywords "社交媒体 工作时间"
```

---

## 步骤 5：Skill 复用

### 5.1 在新对话中使用

当用户输入新的需求时，系统会自动搜索匹配的 Skill：

```python
# 在你的对话系统中集成
from skill_refinery import SkillMatcher

matcher = SkillMatcher()
user_input = "我也想在工作时间禁止员工看社交媒体"

# 搜索匹配的 Skills
matched_skills = matcher.search(user_input, threshold=0.7)

if matched_skills:
    best_skill = matched_skills[0]
    print(f"找到匹配的 Skill: {best_skill.skill_name}")
    print(f"相似度: {best_skill.similarity * 100:.1f}%")
    
    # 提示用户
    prompt = f"""
🎯 我发现您的需求与已有的「{best_skill.skill_name}」模板非常相似！

您可以：
A. 直接使用这个模板（1秒生成配置）
B. 在这个模板基础上修改
C. 重新配置（不使用模板）
    """
    # ... 等待用户选择
```

### 5.2 快速配置

用户选择使用模板后，直接生成配置：

```python
if user_choice == "A":
    # 使用快速填充配置
    config = best_skill.quick_fill_config
    
    # 补充必要的动态信息
    config["strategy_name"] = generate_strategy_name()
    config["effective_date"]["start_date"] = get_current_date()
    
    # 生成最终配置
    final_config = json.dumps(config, indent=2, ensure_ascii=False)
    
    # 更新 Skill 使用统计
    matcher.update_skill_usage(best_skill.skill_id, success=True)
```

### 5.3 复用统计

系统会自动记录 Skill 的使用情况：

```bash
python skill_refinery.py stats --skill-id social_media_work_hours_restriction_v1
```

**输出：**
```
Skill: 工作时间社交媒体访问限制
─────────────────────────────────────
使用次数: 15
成功率: 93.3%
平均对话轮次: 2.1 (原始: 6)
平均完成时间: 45秒 (原始: 2分30秒)
时间节省率: 70%
用户满意度: 4.7/5.0

最近使用:
- 2024-01-15 10:30 ✓
- 2024-01-15 14:22 ✓
- 2024-01-16 09:15 ✓
- 2024-01-16 11:40 ✗ (用户选择重新配置)
- 2024-01-17 15:30 ✓
```

---

## 步骤 6：Skill 演化

### 6.1 Skill 变体

当用户需求部分匹配时，可以创建变体：

```bash
python skill_refinery.py create-variant \
  --parent social_media_work_hours_restriction_v1 \
  --conversation new_conversation_log.json
```

**场景示例：**
```
原 Skill: 工作时间社交媒体访问限制
└── 变体1: 工作时间视频网站访问限制
    - 继承: 时间配置、生效对象、审批机制
    - 修改: 网站列表（社交媒体 → 视频网站）
```

### 6.2 Skill 合并

当多个 Skill 有大量重叠时，可以合并：

```bash
python skill_refinery.py merge \
  --skills social_media_work_hours_v1,video_work_hours_v1 \
  --output entertainment_work_hours_v1
```

**合并策略：**
- 提取公共的对话模板
- 参数化差异部分（如网站类别）
- 创建更通用的 Skill

### 6.3 Skill 优化

基于使用数据优化 Skill：

```bash
python skill_refinery.py optimize --skill-id social_media_work_hours_restriction_v1
```

**优化内容：**
1. **关键词优化**：添加用户实际使用的表述
   ```
   原: ["社交媒体", "工作时间", "禁止"]
   优化后: ["社交媒体", "社交网站", "工作时间", "上班时间", "禁止", "限制", "不让"]
   ```

2. **置信度调整**：基于用户选择调整默认值
   ```
   原: 步骤1 → "除老板外所有员工" (置信度 85%)
   优化后: "除老板外所有员工" (置信度 92%)  ← 15次使用中14次选择
   ```

3. **模板简化**：减少不必要的确认步骤
   ```
   原: 4个确认步骤
   优化后: 2个必要步骤 + 2个可选步骤
   ```

### 6.4 Skill 版本管理

```bash
# 创建新版本
python skill_refinery.py version --skill-id social_media_work_hours_restriction_v1 --action create

# 查看版本历史
python skill_refinery.py version --skill-id social_media_work_hours_restriction_v1 --action history

# 回滚到旧版本
python skill_refinery.py version --skill-id social_media_work_hours_restriction_v1 --action rollback --version v1
```

**版本历史：**
```
social_media_work_hours_restriction
├── v1 (2024-01-15) - 初始版本
├── v2 (2024-01-20) - 优化关键词，添加5个同义词
└── v3 (2024-01-25) - 简化对话流程，调整置信度 [当前]
```

---

## 🎯 完整工作流示例

### 场景：首次配置社交媒体限制

```bash
# 1. 启动对话录制
python skill_refinery.py record --output conv_001.json

# 2. 完成对话后，提取 Skill
python skill_refinery.py extract --conversation conv_001.json --output skill_001.json

# 3. 验证 Skill
python skill_refinery.py test-match --skill skill_001.json
python skill_refinery.py test-generate --skill skill_001.json

# 4. 保存到库
python skill_refinery.py save --skill skill_001.json

# 5. 查看结果
python skill_refinery.py show --skill-id social_media_work_hours_restriction_v1
```

### 场景：复用已有 Skill

```bash
# 用户输入: "我也想禁止员工上班时间看社交媒体"

# 系统自动搜索
python skill_refinery.py search --input "我也想禁止员工上班时间看社交媒体"

# 输出:
# ✓ 找到匹配: social_media_work_hours_restriction_v1 (相似度: 92%)
# 
# 是否使用该模板？(Y/n)

# 用户确认后，快速生成配置
python skill_refinery.py quick-generate \
  --skill-id social_media_work_hours_restriction_v1 \
  --output config_002.json
```

---

## 📊 关键指标监控

定期查看 Skill 库的健康度：

```bash
python skill_refinery.py dashboard
```

**输出：**
```
╔══════════════════════════════════════════╗
║      Skill 库仪表板                       ║
╚══════════════════════════════════════════╝

📚 总体统计
─────────────────────────────────────────
总 Skills 数: 8
  - specific_website 类型: 5
  - global_website 类型: 3

总使用次数: 127
平均成功率: 89.5%
平均时间节省: 68%

🏆 最受欢迎 Skills (Top 3)
─────────────────────────────────────────
1. 工作时间社交媒体访问限制 (使用 45次, 成功率 93%)
2. 工作时间视频网站访问限制 (使用 32次, 成功率 91%)
3. 全局下载权限控制 (使用 18次, 成功率 85%)

📈 本周趋势
─────────────────────────────────────────
新增 Skills: 2
总使用次数: +23 (↑ 15%)
平均成功率: 89.5% (↑ 2.3%)

⚠️  需要优化的 Skills
─────────────────────────────────────────
- shopping_website_restriction_v1
  成功率: 68% (低于阈值 75%)
  建议: 检查关键词匹配和对话模板

🔄 最近更新
─────────────────────────────────────────
- video_work_hours_restriction_v1 → v2 (优化关键词)
- password_view_control_v1 → v2 (简化对话流程)
```

---

## 🛠️ 高级功能

### 1. 批量炼制

从多个对话日志中批量提取 Skills：

```bash
python skill_refinery.py batch-extract \
  --input-dir ./conversation_logs/ \
  --output-dir ./extracted_skills/
```

### 2. Skill 导入导出

```bash
# 导出所有 Skills
python skill_refinery.py export --output skills_backup.zip

# 导入 Skills
python skill_refinery.py import --input skills_backup.zip
```

### 3. A/B 测试

对比不同版本的 Skill 效果：

```bash
python skill_refinery.py ab-test \
  --skill-a social_media_v1 \
  --skill-b social_media_v2 \
  --duration 7days
```

### 4. 智能推荐

基于对话历史推荐需要创建的 Skill：

```bash
python skill_refinery.py recommend \
  --conversation-logs ./logs/ \
  --min-frequency 5
```

**输出：**
```
发现以下高频但未被 Skill 覆盖的场景：

1. "限制购物网站" (出现 12 次)
   推荐创建: shopping_website_restriction_v1
   
2. "全局禁止下载" (出现 8 次)
   推荐创建: global_download_restriction_v1

3. "特定时间段允许访问" (出现 6 次)
   推荐创建: time_based_whitelist_v1
```

---

## ✅ 最佳实践

### 1. Skill 命名规范

```
{功能}_{场景}_{版本}
例如: social_media_work_hours_restriction_v1
```

### 2. 关键词选择

- ✓ 包含用户的自然表述
- ✓ 包含领域术语
- ✓ 包含常见同义词
- ✗ 避免过于宽泛的词（如"网站"、"时间"）

### 3. 对话模板设计

- ✓ 步骤清晰，逻辑连贯
- ✓ 提供默认值和推荐选项
- ✓ 记录用户选择的置信度
- ✗ 避免冗余的确认步骤

### 4. 定期维护

- 每周查看 Skill 使用统计
- 优化成功率低于 80% 的 Skills
- 合并高度相似的 Skills
- 删除长期未使用的 Skills

---

## 🔗 相关资源

- [Skill 数据格式规范](./skill_format_spec.md)
- [API 参考文档](./api_reference.md)
- [常见问题 FAQ](./faq.md)
- [示例 Skills 库](./example_skills/)

---

## 📞 获取帮助

```bash
# 查看帮助
python skill_refinery.py --help

# 查看特定命令的帮助
python skill_refinery.py extract --help
```

祝您 Skill 炼制顺利！🎉
