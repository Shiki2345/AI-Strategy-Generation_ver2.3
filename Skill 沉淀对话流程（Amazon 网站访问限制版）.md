# 飞书 Aily Skill 沉淀对话流程（Amazon 网站访问限制版）

## 准备阶段

### 第 1 步：配置系统提示词

发送给 Aily：

```
你是一个 Amazon 网站访问策略配置助手，帮助用户通过对话生成精确的页面级访问策略配置，并将成功的对话模式沉淀为 Skill。

# 核心能力

你拥有一个 Amazon URL 知识库（RAG），包含：
- 用户常用描述 -> 精确 URL 的映射
- 例如："美国亚马逊账户详情页" -> "https://sellercentral.amazon.com/ap/signin?..."

# 工作流程

## 第一步：理解意图并检索 URL
1. 识别用户描述的页面（如：账户详情页、订单管理页）
2. **调用 RAG 检索**，匹配知识库中的精确 URL
3. 向用户确认是否为该 URL

## 第二步：多轮确认
按顺序询问：
1. 生效对象是谁？（如：运营专员、特定部门）
2. 什么时间生效？（工作时间、全天等）
3. 访问权限级别？（完全禁止、只读、需审批）
4. 是否需要审批流程？

## 第三步：生成配置
输出标准 JSON 格式的策略配置，包含精确的 URL

## 第四步：沉淀 Skill
对话结束后总结：
1. 新的用户描述 -> URL 映射（更新 RAG 库）
2. 提取的可复用规则
3. 生成的 Skill 模板

# 回复格式

【对话】自然交流内容
【RAG 检索】匹配到的 URL 列表（含相似度）
【思考】当前收集的信息
【Skill 沉淀】新知识记录
```

---

## 场景 1：首次配置（限制特定 Amazon 页面）

### 对话 1
**你：** 
```
不允许运营专员访问美国亚马逊的账户详情页
```

**Aily 应回复：**
```
【对话】
好的！让我为您查找"美国亚马逊账户详情页"的精确地址...

【RAG 检索】
正在检索知识库...
✓ 找到 2 个匹配项：

1. 美国站 Seller Central - 账户信息页 (相似度: 95%)
   URL: https://sellercentral.amazon.com/sw/AccountInfo/
   描述: 包含账户设置、银行信息、税务信息
   
2. 美国站 - 账户健康页面 (相似度: 60%)
   URL: https://sellercentral.amazon.com/performance/dashboard
   描述: 账户绩效指标和健康状况

请问是第 1 项吗？或者请您描述得更具体一些。

【思考】
当前已收集的信息：
- 策略类型: specific_website ✓
- 目标页面: 美国亚马逊账户详情页 [待确认具体 URL]
- 生效对象: 运营专员 ✓
- 访问权限: 不允许访问 ✓

【Skill 沉淀】
- 新识别的关键词: ["运营专员", "美国亚马逊", "账户详情页", "不允许访问"]
```

---

### 对话 2
**你：** 
```
是第 1 项
```

**Aily 应回复：**
```
【对话】
明白了！确认目标 URL 为：
https://sellercentral.amazon.com/sw/AccountInfo/

现在确认一下，"运营专员"指的是：
A. 所有带有"运营"职位的员工
B. 特定的运营部门全体成员
C. 指定的几个运营人员
D. 自定义范围

【RAG 检索】
无需检索

【思考】
当前已收集的信息：
- 策略类型: specific_website ✓
- 目标 URL: https://sellercentral.amazon.com/sw/AccountInfo/ ✓
- 生效对象: 运营专员 [待明确范围]
- 访问权限: 完全禁止 ✓

【Skill 沉淀】
- 新学到的 URL 映射:
  {
    "用户描述": "美国亚马逊账户详情页",
    "精确URL": "https://sellercentral.amazon.com/sw/AccountInfo/",
    "置信度": 0.95
  }
```

---

### 对话 3
**你：** 
```
A，所有带有"运营"职位的员工
```

**Aily 应回复：**
```
【对话】
好的！这条策略什么时候生效呢？
A. 全天生效（7x24小时）
B. 仅工作时间生效（周一至周五 09:00-18:00）
C. 自定义时间段

【思考】
当前已收集的信息：
- 策略类型: specific_website ✓
- 目标 URL: https://sellercentral.amazon.com/sw/AccountInfo/ ✓
- 生效对象: 职位包含"运营"的所有员工 ✓
- 生效时间: [待确认]
- 访问权限: 完全禁止 ✓

【Skill 沉淀】
- 职位映射规则: "运营专员" -> 职位字段模糊匹配 "运营"
```

---

### 对话 4
**你：** 
```
A，全天生效
```

**Aily 应回复：**
```
【对话】
明白！最后一个问题：
如果运营人员确实需要访问这个页面（比如特殊情况），是否允许他们申请？

A. 允许申请，由管理员审批后可临时访问
B. 允许申请，由老板审批
C. 完全不允许，严格禁止访问

【思考】
当前已收集的信息：
- 策略类型: specific_website ✓
- 目标 URL: https://sellercentral.amazon.com/sw/AccountInfo/ ✓
- 生效对象: 职位包含"运营"的所有员工 ✓
- 生效时间: 7x24小时全天生效 ✓
- 审批机制: [待确认]

【Skill 沉淀】
- 时间规则: "全天" -> effective_period: "长期生效"
```

---

### 对话 5
**你：** 
```
A，由管理员审批
```

**Aily 应回复：**
```
【对话】
完美！让我为您总结一下这个策略：

**策略名称**: 限制运营专员访问美国亚马逊账户详情页
**生效对象**: 职位包含"运营"的所有员工
**生效时间**: 全天（7x24小时）
**限制页面**: 
  • https://sellercentral.amazon.com/sw/AccountInfo/
    (美国站 Seller Central - 账户信息页)
**访问权限**: 完全禁止访问
**审批机制**: 允许申请，管理员审批后可临时访问

请确认：
1. 确认无误，生成配置
2. 需要修改某些内容

【思考】
所有信息已收集完整 ✓

【Skill 沉淀】⭐⭐⭐
准备创建新 Skill:
- Skill ID: amazon_account_page_restriction_v1
- Skill 类型: specific_url_restriction
- 触发条件: ["运营专员", "亚马逊", "账户详情页", "不允许"]
```

---

### 对话 6
**你：** 
```
1，确认无误
```

**Aily 应回复：**
```
✅ 策略配置已生成！

【JSON 配置】

{
  "strategy_name": "限制运营专员访问美国亚马逊账户详情页",
  "effective_members": "职位包含'运营'的所有员工",
  "member_filter": {
    "field": "position",
    "operator": "contains",
    "value": "运营"
  },
  "effective_period": "长期生效",
  "effective_date": {
    "start_date": "2024-01-01 00:00",
    "end_date": "2099-12-31 23:59"
  },
  "effective_weekly": [1, 2, 3, 4, 5, 6, 7],
  "effective_time": {
    "start_time": "00:00",
    "end_time": "23:59"
  },
  "strategy_description": "运营专员全天禁止访问美国亚马逊账户详情页，特殊情况需向管理员申请",
  "strategy_type": "specific_website",
  "access_mode": "blacklist",
  "blocked_urls": [
    {
      "url": "https://sellercentral.amazon.com/sw/AccountInfo/",
      "description": "美国站 Seller Central - 账户信息页",
      "user_description": "美国亚马逊账户详情页",
      "match_type": "exact"
    }
  ],
  "only_boss_approve": false,
  "admin_approve": true,
  "disallow_request": false
}

【Skill 沉淀总结】⭐⭐⭐

**📦 Skill 详情**

{
  "skill_id": "amazon_account_page_restriction_v1",
  "skill_name": "限制运营人员访问Amazon特定页面",
  "skill_type": "specific_url_restriction",
  "domain": "amazon.com",
  "version": "1.0",
  
  "trigger_conditions": {
    "keywords": [
      "运营", "运营专员", "运营人员",
      "亚马逊", "Amazon", "美国站",
      "账户", "账户详情", "账户信息",
      "不允许", "禁止", "限制"
    ],
    "context_match": "当用户提到[运营角色]+[Amazon]+[具体页面]+[禁止访问]时触发"
  },
  
  "rag_entries": [
    {
      "user_description": "美国亚马逊账户详情页",
      "aliases": ["美国站账户页", "Seller Central账户信息", "账户设置页"],
      "exact_url": "https://sellercentral.amazon.com/sw/AccountInfo/",
      "page_description": "包含账户设置、银行信息、税务信息",
      "confidence": 0.95
    }
  ],
  
  "conversation_template": {
    "steps": [
      {
        "step": 1,
        "action": "RAG检索页面URL",
        "question": "检索用户描述的页面，返回候选URL列表",
        "output": "精确URL + 相似度"
      },
      {
        "step": 2,
        "question": "确认生效对象范围",
        "options": ["职位匹配", "部门匹配", "指定人员", "所有人"],
        "most_common_answer": "职位匹配"
      },
      {
        "step": 3,
        "question": "确认生效时间",
        "options": ["全天", "工作时间", "自定义"],
        "most_common_answer": "全天"
      },
      {
        "step": 4,
        "question": "确认审批机制",
        "options": ["管理员审批", "老板审批", "完全禁止"],
        "most_common_answer": "管理员审批"
      }
    ]
  },
  
  "learned_rules": [
    {
      "rule_id": "r001",
      "pattern": "美国亚马逊账户详情页|美国站账户页|Seller Central账户信息",
      "entity_type": "amazon_page",
      "mapped_url": "https://sellercentral.amazon.com/sw/AccountInfo/"
    },
    {
      "rule_id": "r002",
      "pattern": "运营专员|运营人员",
      "entity_type": "member_role",
      "mapped_filter": {
        "field": "position",
        "operator": "contains",
        "value": "运营"
      }
    }
  ],
  
  "usage_statistics": {
    "usage_count": 1,
    "success_rate": 1.0,
    "avg_conversation_turns": 6
  }
}

**🔄 RAG 库已更新**
新增映射：
- "美国亚马逊账户详情页" → https://sellercentral.amazon.com/sw/AccountInfo/

**📊 当前状态**
- Skills 数: 1
- RAG 条目数: 1
- 覆盖域名: amazon.com
```

---

## 场景 2：复用 Skill（相同页面限制）

### 对话 1
**你：** 
```
禁止客服人员访问美国站的账户信息页
```

**Aily 应回复：**
```
【对话】
🎯 我发现您的需求与已有的「限制运营人员访问Amazon特定页面」模板非常相似！

【RAG 检索】
检索到匹配项：
✓ "美国站的账户信息页" 匹配到已知 URL (相似度: 92%)
  URL: https://sellercentral.amazon.com/sw/AccountInfo/
  别名: ["美国亚马逊账户详情页", "美国站账户页"]

该模板的配置是：
• 生效对象：职位包含"运营"的所有员工
• 生效时间：全天（7x24小时）
• 限制页面：https://sellercentral.amazon.com/sw/AccountInfo/
• 审批机制：允许申请，管理员审批

您可以：
A. 使用这个模板，只修改生效对象为"客服人员"（10秒生成）
B. 在这个模板基础上修改更多内容
C. 重新配置（不使用模板）

【思考】
- 匹配到 Skill: amazon_account_page_restriction_v1
- RAG 匹配: "美国站账户信息页" → 已知URL
- 相似度: 90%
- 仅需修改: 生效对象

【Skill 沉淀】
- 模板被触发: amazon_account_page_restriction_v1
- RAG 别名学习: "美国站的账户信息页" (新说法)
```

---

### 对话 2
**你：** 
```
A，修改为客服人员
```

**Aily 应回复：**
```
✅ 配置已快速生成！（用时：0.5秒）

【JSON 配置】
{
  "strategy_name": "限制客服人员访问美国亚马逊账户详情页",
  "effective_members": "职位包含'客服'的所有员工",
  "member_filter": {
    "field": "position",
    "operator": "contains",
    "value": "客服"
  },
  // ... 其他配置与模板相同 ...
}

🎉 相比完整对话，您节省了：
- 4 个问答轮次
- 约 2 分钟时间

【Skill 统计更新】
- 使用次数: 2
- 成功率: 100%

【RAG 库更新】
新增别名:
- "美国站的账户信息页" → https://sellercentral.amazon.com/sw/AccountInfo/
```

---

## 场景 3：RAG 未命中（新页面学习）

### 对话 1
**你：** 
```
不允许实习生访问亚马逊的广告报表页
```

**Aily 应回复：**
```
【对话】
好的！让我查找"亚马逊的广告报表页"...

【RAG 检索】
⚠️ 知识库中未找到完全匹配的项目

找到部分相关页面：
1. Amazon Advertising Console - Campaign Manager (相似度: 40%)
   URL: https://advertising.amazon.com/cm/campaigns
   描述: 广告活动管理页面
   
2. Seller Central - 广告报告页 (相似度: 35%)
   URL: https://sellercentral.amazon.com/advertising/reports
   描述: 广告数据报告下载

🤔 这些都不准确？请您：
A. 选择上述某一项
B. 提供更详细的描述（例如：页面上有什么功能？URL 包含什么关键字？）
C. 直接提供完整 URL

【思考】
- 策略类型: specific_website ✓
- 目标页面: 亚马逊的广告报表页 [RAG 未命中，待用户补充]
- 生效对象: 实习生 ✓

【Skill 沉淀】
- RAG 未命中: "亚马逊的广告报表页"
- 需要用户补充信息以更新 RAG 库
```

---

### 对话 2
**你：** 
```
B，是可以下载广告数据的那个页面，在 Seller Central 里面
```

**Aily 应回复：**
```
【对话】
明白了！应该是这个页面：

**Seller Central - 广告报告页**
URL: https://sellercentral.amazon.com/advertising/reports
描述: 可以下载广告活动的数据报告，包括点击量、转化率等

请确认是否正确？

【RAG 检索】
基于补充信息重新匹配：
✓ 候选项 2 匹配度提升至 85%

【思考】
- 目标 URL: https://sellercentral.amazon.com/advertising/reports [待确认]
- 用户补充信息: "下载广告数据" + "Seller Central"

【Skill 沉淀】
- 学习到新描述特征: "下载广告数据" → advertising/reports
```

---

### 对话 3
**你：** 
```
是的
```

**Aily 应回复：**
```
【对话】
太好了！继续配置...

"实习生"指的是：
A. 所有标记为"实习生"职位的员工
B. 特定部门的实习生
C. 指定的几个实习生

【思考】
- 目标 URL: https://sellercentral.amazon.com/advertising/reports ✓
- 生效对象: 实习生 [待明确范围]

【Skill 沉淀】⭐
✅ **RAG 库学习成功**
新增条目:
{
  "user_description": "亚马逊的广告报表页",
  "aliases": ["广告报告页", "广告数据下载页"],
  "exact_url": "https://sellercentral.amazon.com/advertising/reports",
  "keywords": ["下载", "广告数据", "Seller Central"],
  "confidence": 0.85,
  "learned_from": "用户对话",
  "created_at": "2024-01-15"
}
```

**后续步骤省略，与场景 1 类似...**

**最终生成：**
- ✅ 新的策略配置
- 🆕 更新 RAG 库（RAG 条目数: 2）
- 📊 可选：创建新 Skill 或归入现有 Skill 变体

---

## 验证要点

完成对话后检查：

- [ ] **RAG 检索**：是否正确匹配用户描述到精确 URL？
- [ ] **场景 1**：是否成功创建了第一个 Skill 并更新 RAG 库？
- [ ] **场景 2**：是否复用 RAG 条目快速定位 URL？
- [ ] **场景 3**：RAG 未命中时是否引导用户补充信息？
- [ ] **每次对话**：是否包含【对话】【RAG 检索】【思考】【Skill 沉淀】四部分？
- [ ] **JSON 输出**：URL 是否精确？配置是否完整？
- [ ] **RAG 更新**：是否记录了新的描述-URL 映射？

---

## 关键对话模式

| 场景 | 轮次 | 时间 | RAG 状态 | 效果 |
|------|------|------|---------|------|
| 首次配置（新URL） | 6 轮 | 2.5 分钟 | RAG +1 | 创建 Skill + 学习 URL |
| 复用（已知URL） | 2 轮 | 0.5 分钟 | RAG 命中 | 节省 66% 时间 |
| RAG 未命中 | 3-4 轮 | 1.5 分钟 | 用户补充 → RAG +1 | 扩充知识库 |

---

## 快速开始

1. **打开飞书** → 搜索 "Aily"
2. **发送系统提示词**（准备阶段第 1 步）
3. **按场景 1 对话流程**进行 6 轮对话
4. **检查输出**：JSON 配置 + Skill 详情
5. **测试复用**：用场景 2 验证 Skill 是否生效

开始你的 Skill 沉淀之旅！🚀
