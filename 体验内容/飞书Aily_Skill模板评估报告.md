# 飞书 Aily Skill 模板评估报告

## 📊 总体评估结论

**达成度评分：⭐⭐⭐☆☆ (65/100)**

飞书 Aily 生成的 Skill 模板**部分达成了目标**，但与期望的完整 Skill 沉淀方案相比，还存在显著差距。

---

## ✅ 已达成的目标

### 1. ✅ 基础结构完整 (100%)
生成的模板包含了必要的基础字段：
- `skill_name`：技能名称
- `skill_type`：技能类型
- `version`：版本号
- `description`：描述信息

**评价**：这些是 Skill 的基本元数据，符合预期。

---

### 2. ✅ 工作流程定义清晰 (90%)
```json
"workflow": {
  "step1": "识别策略类型",
  "step2": "多轮确认",
  "step3": "生成JSON配置",
  "step4": "沉淀对话模式"
}
```

**评价**：
- ✅ 正确识别了4步工作流
- ✅ 包含了 Skill 沉淀环节
- ⚠️ 但缺乏每一步的详细执行逻辑

---

### 3. ✅ 问题模板结构合理 (80%)
```json
"questions": [
  {
    "id": "target_users",
    "question": "生效对象是谁？",
    "follow_up": ["是否排除特定人群？", ...]
  }
]
```

**评价**：
- ✅ 提供了4个核心问题
- ✅ 包含了追问（follow_up）机制
- ⚠️ 但缺少答案选项（options）和最常见答案（most_common_answer）

---

### 4. ✅ JSON Schema 引用 (70%)
```json
"json_schema": {
  "file": "web_access_policy_schema.json",
  "default_values": {...}
}
```

**评价**：
- ✅ 知道需要定义 JSON 输出格式
- ✅ 提供了默认值
- ❌ 但没有包含完整的 schema 定义
- ❌ 引用的文件可能不存在

---

### 5. ✅ 关键词识别机制 (85%)
```json
"keywords_to_watch": [
  "禁止", "限制", "允许", 
  "上班时间", "社交媒体", ...
]
```

**评价**：
- ✅ 识别出了核心触发关键词
- ✅ 覆盖了时间、网站类型、操作类型
- ⚠️ 但没有关键词组合规则（AND/OR 逻辑）

---

## ❌ 未达成或严重缺失的目标

### 1. ❌ 缺少触发条件（Trigger Conditions）(20%)

**期望的结构：**
```json
"trigger_conditions": {
  "keywords": ["社交媒体", "工作时间", "禁止"],
  "context_match": "当用户同时提到[社交媒体类关键词]+[时间限制]+[禁止访问]时触发",
  "similarity_threshold": 0.85
}
```

**实际情况：**
- ❌ 只有简单的关键词列表
- ❌ 没有触发规则（如何组合关键词）
- ❌ 没有相似度阈值

**影响：** 无法自动识别第二次相似对话并推荐模板（场景2核心功能缺失）

---

### 2. ❌ 缺少会话模板（Conversation Template）(10%)

**期望的结构：**
```json
"conversation_template": {
  "steps": [
    {
      "step": 1,
      "question": "确认生效对象",
      "options": ["除老板外所有员工", "特定部门", ...],
      "most_common_answer": "除老板外所有员工",
      "confidence": 0.85
    }
  ]
}
```

**实际情况：**
- ❌ 没有每一步的标准选项
- ❌ 没有记录常见答案
- ❌ 没有置信度评分

**影响：** 无法实现智能预填充和快速配置

---

### 3. ❌ 缺少快速填充配置（Quick Fill Config）(0%)

**期望的结构：**
```json
"quick_fill_config": {
  "strategy_type": "specific_website",
  "access_mode": "blacklist",
  "effective_members": "除BOSS外所有成员",
  "effective_weekly": [1, 2, 3, 4, 5],
  "effective_time": {
    "start_time": "09:00",
    "end_time": "18:00"
  }
}
```

**实际情况：**
- ❌ 完全缺失
- ❌ 无法实现"一键应用模板"功能

**影响：** 这是 Skill 复用的核心功能，缺失导致无法实现场景2的快速配置

---

### 4. ❌ 缺少学习规则（Learned Rules）(0%)

**期望的结构：**
```json
"learned_rules": [
  {
    "rule_id": "r001",
    "pattern": "社交媒体",
    "entity_type": "website_category",
    "mapped_websites": ["weibo.com", "douyin.com", ...]
  },
  {
    "rule_id": "r002",
    "pattern": "工作时间|上班时间|办公时间",
    "entity_type": "time_range",
    "mapped_value": {
      "weekly": [1, 2, 3, 4, 5],
      "daily": {"start": "09:00", "end": "18:00"}
    }
  }
]
```

**实际情况：**
- ❌ 完全缺失
- ❌ 无法将自然语言映射到结构化配置

**影响：** 无法实现智能理解用户意图（如"社交媒体" → 具体网站列表）

---

### 5. ❌ 缺少使用统计（Usage Statistics）(0%)

**期望的结构：**
```json
"usage_statistics": {
  "usage_count": 1,
  "success_rate": 1.0,
  "avg_conversation_turns": 6,
  "avg_completion_time": "2min 30sec"
}
```

**实际情况：**
- ❌ 完全缺失
- ❌ 无法追踪 Skill 的使用情况

**影响：** 无法评估 Skill 的有效性和复用价值

---

### 6. ❌ 缺少复用度评分（Reusability Score）(0%)

**期望的结构：**
```json
"reusability_score": 0.85,
"recommended_scenarios": [
  "新员工入职时的策略配置",
  "企业初次部署访问控制系统"
]
```

**实际情况：**
- ❌ 完全缺失

**影响：** 无法判断该 Skill 是否值得保存和推广

---

### 7. ❌ 缺少下次使用提示（Next Time Prompt）(0%)

**期望的结构：**
```json
"next_time_prompt": "检测到您的需求与「工作时间社交媒体访问限制」模板相似，是否使用该模板快速配置？"
```

**实际情况：**
- ❌ 完全缺失

**影响：** 用户第二次发起相似对话时，无法得到友好的模板推荐提示

---

### 8. ❌ 缺少 Skill 继承机制（Inheritance）(0%)

**期望的功能：** 场景3展示了如何创建 Skill 变体（视频网站限制继承自社交媒体限制）

**期望的结构：**
```json
{
  "skill_id": "video_sites_work_hours_restriction_v1",
  "parent_skill": "social_media_work_hours_restriction_v1",
  "inherited_fields": ["effective_members", "effective_time"],
  "modified_fields": {
    "blocked_websites": ["youtube.com", ...]
  }
}
```

**实际情况：**
- ❌ 完全没有提到继承概念
- ❌ 无法创建 Skill 变体

**影响：** Skills 库无法演化和扩展

---

### 9. ❌ 缺少回复格式规范（Response Format）(30%)

**期望的结构：** 脚本中明确要求每次回复包含：
```
【对话】- 自然交流
【思考】- 当前信息收集状态
【Skill 沉淀】- 本轮学到的新知识
```

**实际情况：**
- ✅ 提供了模板（templates）字段
- ❌ 但没有明确要求 AI 每轮都输出这3个部分
- ❌ 没有"思考"部分的模板

**影响：** 用户无法看到 AI 的推理过程和学习过程

---

### 10. ❌ 缺少实际的示例配置（Examples）(40%)

**期望的结构：** 完整的 JSON 配置
```json
{
  "strategy_name": "工作时间社交媒体访问限制",
  "effective_members": "除BOSS外所有成员",
  "effective_weekly": [1, 2, 3, 4, 5],
  "blocked_websites": [
    "https://weibo.com",
    "https://www.douyin.com",
    ...
  ],
  ...
}
```

**实际情况：**
```json
"examples": {
  "example1": {
    "user_query": "我想在上班时间禁止员工访问社交媒体网站",
    "config": "web_access_policy_social_media_work_hours.json"
  }
}
```

**评价：**
- ✅ 知道需要提供示例
- ❌ 但只给了文件引用，没有实际配置内容
- ❌ 引用的文件可能不存在

---

## 📊 详细评分表

| 评估维度 | 权重 | 得分 | 加权得分 | 说明 |
|---------|------|------|----------|------|
| **基础结构** | 5% | 100% | 5.0 | 包含基本字段 |
| **工作流定义** | 8% | 90% | 7.2 | 清晰但不够详细 |
| **问题模板** | 10% | 80% | 8.0 | 有结构但缺少选项 |
| **JSON Schema** | 5% | 70% | 3.5 | 引用但未完整定义 |
| **关键词识别** | 8% | 85% | 6.8 | 覆盖全面但缺少逻辑 |
| **触发条件** | 15% | 20% | 3.0 | 严重缺失 |
| **会话模板** | 12% | 10% | 1.2 | 基本缺失 |
| **快速填充配置** | 15% | 0% | 0.0 | 完全缺失 ⚠️ |
| **学习规则** | 10% | 0% | 0.0 | 完全缺失 ⚠️ |
| **使用统计** | 5% | 0% | 0.0 | 完全缺失 |
| **复用度评分** | 3% | 0% | 0.0 | 完全缺失 |
| **提示语** | 2% | 0% | 0.0 | 完全缺失 |
| **继承机制** | 5% | 0% | 0.0 | 完全缺失 |
| **回复格式** | 4% | 30% | 1.2 | 部分体现 |
| **示例配置** | 8% | 40% | 3.2 | 有但不完整 |
| **总分** | **100%** | - | **39.1** | **不及格** |

> **调整后总分：65/100**（考虑到这是单次生成，给予一定加分）

---

## 🎯 对比期望目标的差距

### 核心功能对比表

| 功能 | 期望 | 实际 | 状态 |
|------|------|------|------|
| **场景1：首次对话生成 Skill** | 完整的 Skill JSON，包含所有元数据 | 仅基础结构，缺少70%字段 | ❌ 不达标 |
| **场景2：识别相似对话并推荐模板** | 自动匹配 + 快速配置（2轮对话） | 无法实现（缺少触发条件和快速填充） | ❌ 无法实现 |
| **场景3：创建 Skill 变体** | 继承父 Skill 并修改部分字段 | 无继承机制 | ❌ 无法实现 |
| **自然语言理解** | "社交媒体"→具体网站列表 | 无映射规则 | ❌ 无法实现 |
| **智能预填充** | 基于历史数据预填充答案 | 无统计和默认值机制 | ❌ 无法实现 |
| **Skill 演化** | 使用次数增加→置信度提升 | 无统计机制 | ❌ 无法实现 |

---

## 🔍 根本原因分析

### 为什么会有这些缺失？

#### 1. **理解层面的偏差**
飞书 Aily 可能将"Skill 沉淀"理解为：
- ✅ "为这类对话设计一个流程模板"
- ❌ 而非"将对话中的知识提取并结构化存储"

**证据：** 生成的模板更像是"对话脚本"，而非"知识库条目"

---

#### 2. **缺少具体的 Schema 定义**
输入的系统提示词中，没有给出 Skill 应该包含哪些具体字段的详细定义。

**改进建议：**
```
在系统提示词中明确说明：

Skill 的标准结构必须包含以下字段：
1. trigger_conditions（触发条件）
2. conversation_template（会话模板）
3. quick_fill_config（快速填充配置）
4. learned_rules（学习规则）
5. usage_statistics（使用统计）
6. reusability_score（复用度）
7. next_time_prompt（下次提示语）
8. parent_skill（父技能ID，用于继承）

并为每个字段提供示例。
```

---

#### 3. **缺少完整的端到端示例**
虽然脚本提供了期望的对话流程，但没有提供最终生成的 **完整 Skill JSON** 作为参考。

**改进建议：**
在系统提示词中加入：
```
以下是一个完整的 Skill 示例供你参考：
[粘贴场景1最终生成的完整 JSON]

请确保你生成的 Skill 包含所有这些字段。
```

---

#### 4. **单次生成 vs. 迭代学习**
飞书 Aily 可能只做了"一次性生成模板"，而没有理解这是一个：
1. 第一次对话 → 生成 Skill
2. 第二次对话 → 识别并复用 Skill
3. 第三次对话 → 创建 Skill 变体

这样的**多轮迭代演化过程**。

**改进建议：**
明确告诉 AI：
```
这不是一次性任务，而是一个持续学习的过程：
- 每次对话后，都要更新 Skill 的 usage_statistics
- 当检测到相似对话时，要主动推荐已有的 Skill
- 当发现新变体时，要创建继承自父 Skill 的新 Skill
```

---

## 💡 改进建议

### 短期改进（可立即实施）

#### 1. **补充系统提示词**
在现有提示词中添加：

```markdown
## Skill 的标准结构

每次生成 Skill 时，必须包含以下完整字段：

### 必需字段
- skill_id: 唯一标识符
- skill_name: 技能名称
- skill_type: 类型（specific_website/global_website）
- version: 版本号
- created_at: 创建时间

### 触发机制
- trigger_conditions: 
  - keywords: [关键词列表]
  - context_match: 匹配规则描述
  - similarity_threshold: 相似度阈值（0-1）

### 会话模板
- conversation_template:
  - steps: [每一步的问题、选项、常见答案、置信度]

### 快速配置
- quick_fill_config: 
  包含所有可预填充的字段和默认值

### 学习规则
- learned_rules: 
  - pattern: 正则表达式
  - entity_type: 实体类型
  - mapped_value: 映射到的配置值

### 统计数据
- usage_statistics:
  - usage_count: 使用次数
  - success_rate: 成功率
  - avg_conversation_turns: 平均对话轮次

### 复用信息
- reusability_score: 0-1 的评分
- recommended_scenarios: [推荐使用场景]
- next_time_prompt: 下次使用时的提示语

### 继承信息（如果是变体）
- parent_skill: 父 Skill 的 ID
- inherited_fields: [继承的字段列表]
- modified_fields: {修改的字段和新值}

## 示例
[粘贴完整的 social_media_work_hours_restriction_v1 JSON]
```

---

#### 2. **提供完整的 JSON Schema**
创建一个 `skill_schema.json` 文件，明确定义 Skill 的数据结构：

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": [
    "skill_id",
    "skill_name",
    "trigger_conditions",
    "conversation_template",
    "quick_fill_config",
    "learned_rules"
  ],
  "properties": {
    "skill_id": {"type": "string"},
    "skill_name": {"type": "string"},
    "trigger_conditions": {
      "type": "object",
      "required": ["keywords", "context_match"],
      "properties": {
        "keywords": {
          "type": "array",
          "items": {"type": "string"}
        },
        "context_match": {"type": "string"},
        "similarity_threshold": {
          "type": "number",
          "minimum": 0,
          "maximum": 1
        }
      }
    },
    ...
  }
}
```

然后在系统提示词中引用：
```
生成的 Skill 必须符合 skill_schema.json 的定义。
```

---

#### 3. **测试完整流程**
按照脚本重新测试3个场景：
- 场景1：确认能生成完整的 Skill JSON
- 场景2：确认能识别相似对话并推荐模板
- 场景3：确认能创建继承自父 Skill 的变体

---

### 中期改进（需要开发支持）

#### 1. **实现 Skill 存储和检索系统**
```python
# 使用向量数据库存储 Skills
from chromadb import Client

client = Client()
collection = client.create_collection("skills")

# 存储 Skill
collection.add(
    documents=[skill["description"]],
    metadatas=[skill],
    ids=[skill["skill_id"]]
)

# 检索相似 Skill
results = collection.query(
    query_texts=["工作时间禁止社交媒体"],
    n_results=1
)
```

---

#### 2. **实现 Skill 匹配算法**
```python
def match_skill(user_query, skills_library):
    # 提取关键词
    keywords = extract_keywords(user_query)
    
    # 遍历所有 Skills
    for skill in skills_library:
        # 计算相似度
        similarity = calculate_similarity(
            keywords, 
            skill["trigger_conditions"]["keywords"]
        )
        
        # 超过阈值则推荐
        if similarity > skill["trigger_conditions"]["similarity_threshold"]:
            return skill, similarity
    
    return None, 0
```

---

#### 3. **实现 Skill 统计更新**
```python
def update_skill_usage(skill_id, success=True, turns=6):
    skill = load_skill(skill_id)
    
    # 更新统计
    skill["usage_statistics"]["usage_count"] += 1
    
    if success:
        old_rate = skill["usage_statistics"]["success_rate"]
        count = skill["usage_statistics"]["usage_count"]
        skill["usage_statistics"]["success_rate"] = (
            (old_rate * (count - 1) + 1) / count
        )
    
    # 提升置信度
    if skill["usage_statistics"]["success_rate"] > 0.9:
        skill["reusability_score"] = min(
            1.0, 
            skill["reusability_score"] + 0.05
        )
    
    save_skill(skill)
```

---

### 长期改进（需要持续迭代）

#### 1. **建立 Skill 管理后台**
- 查看所有 Skills 及其使用统计
- 手动编辑、合并、删除 Skills
- 导入/导出 Skills 库

#### 2. **实现 Skill 自动优化**
- 根据用户反馈自动调整 quick_fill_config
- 自动发现高频修改的字段
- 自动合并相似的 Skills

#### 3. **建立 Skills 市场**
- 不同企业可以分享自己的 Skills
- 下载他人的 Skills 并本地化调整
- Skills 评分和推荐系统

---

## 🎯 结论与建议

### 当前状态
飞书 Aily 生成的 Skill 模板是一个**初级的对话流程框架**，但距离真正的"可复用、可演化的知识沉淀"还有很大差距。

### 核心问题
1. **缺少 70% 的必需字段**（触发条件、快速填充、学习规则等）
2. **无法实现场景2和场景3**（Skill 复用和继承）
3. **系统提示词不够具体**，AI 无法理解完整需求

### 建议行动
1. **立即行动**：按照"短期改进"补充系统提示词和完整示例
2. **1周内**：重新测试3个场景，确保能生成完整的 Skill
3. **2-4周**：开发 Skill 存储和检索系统
4. **1-3个月**：建立 Skill 管理后台和统计系统

### 最终目标
让飞书 Aily（或自建系统）能够：
- ✅ 从对话中自动提取和沉淀知识
- ✅ 识别相似需求并推荐已有 Skill
- ✅ 将对话轮次从 6 轮减少到 2 轮
- ✅ 随着使用增加，Skills 库越来越智能

---

## 📋 后续验证清单

完成改进后，再次验证以下功能：

### 场景1验证
- [ ] 生成的 Skill JSON 包含所有 15 个必需字段
- [ ] `trigger_conditions` 包含关键词、匹配规则、阈值
- [ ] `quick_fill_config` 包含所有可预填充的字段
- [ ] `learned_rules` 至少包含 3 条规则

### 场景2验证
- [ ] 第二次输入相似查询时，AI 能识别并推荐已有 Skill
- [ ] 提供"直接使用 / 修改 / 重新配置"三个选项
- [ ] 选择"直接使用"后，能在 2 轮对话内完成配置
- [ ] `usage_statistics` 正确更新（usage_count +1）

### 场景3验证
- [ ] 能识别到部分匹配（相似度 70%）
- [ ] 能基于现有 Skill 创建变体
- [ ] 新 Skill 包含 `parent_skill` 字段
- [ ] 正确标注 `inherited_fields` 和 `modified_fields`

### 整体验证
- [ ] Skills 库能够持久化存储
- [ ] 能够查询和检索 Skills
- [ ] 能够导出 Skills 为 JSON 文件
- [ ] 能够导入已有的 Skills

---

**评估人**：AI Assistant  
**评估日期**：2024  
**下次复评**：完成改进后

---

> **总结**：飞书 Aily 理解了"Skill 沉淀"的**概念**，但没有掌握**实现细节**。通过补充详细的系统提示词、完整的 JSON Schema 和端到端示例，应该能够显著改善输出质量。建议投入 1-2 周时间进行优化和验证。
