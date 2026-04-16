# AI 辅助策略生成模块 — 改动日志

---

## 版本演进路线总结

| 版本 | 核心主题 | 关键数字 |
|------|---------|---------|
| v1.0 | 基础 Skill 框架 + 自定义 JSON 输出 | 6 phase、自定义字段 |
| v2.0 | 输出 1:1 对齐平台表单 | 5 phase、5 类预设、2 个审批选项 |
| v2.1 | 系统提示词细化 | 部署指南 |
| v2.2 | 能力边界 + 平台地图 + RAG 扩容 | 24 模块、17 条指路规则、11 条指引原则、219 条 URL |
| v2.3 | RAG 数据质量从"有 URL"到"可检索" | 219 条全量语义补全、平均 8.6 别名 + 11.9 关键词、12 个策略样例 |

---

## v2.3 改动说明（2026-04-16）

> 改动范围：RAG 数据库全量补全 + 新增策略样例 + 项目清理
> 核心主题：RAG 数据质量从"有 URL"升级到"可检索"

### 改动背景

v2.2 将 RAG 数据库从 20 条扩容到 219 条，但这 219 条记录只有 `user_description` 和 `exact_url` 两个字段有值，`page_description`、`aliases`、`keywords` 均为空。这意味着用户用口语化表达（如"上架""铺货""广告报表"）搜索时，RAG 无法匹配到对应 URL，扩容的数据实际上处于不可检索状态。

v2.3 的核心改动：对 219 条记录逐条补全语义字段，让 RAG 从"有数据"变为"能用起来"。

### 一、RAG 数据库全量语义补全（rag_simple_db.json）

对全部 219 条记录补全 3 个关键字段：

| 字段 | 补全前 | 补全后 |
|------|--------|--------|
| `page_description` | 空（0/219 条有值） | 全部填写（219/219），每条用一句话描述页面功能 |
| `aliases` | 空（0/219 条有值） | 全部填写（219/219），平均每条 8.6 个别名 |
| `keywords` | 仅 1 个（=user_description） | 全部扩展（219/219），平均每条 11.9 个关键词 |

**补全内容覆盖：**
- **中文口语别名**：如"上架""铺货""刷评""跟卖""退款"等跨境电商黑话
- **英文原词**：如 Add Product、Listing Upload、FBA Shipment、PPC Campaign
- **缩写/行话**：如 FBA、PPC、ASIN、SKU、A+、VINE
- **操作动词**：如"查看""修改""下载""导出""申诉"
- **场景化表达**：如"为什么被封号""怎么发 FBA""广告跑了多少钱"

**数据分布（20 个类别）：**

| 类别 | 条目数 | 类别 | 条目数 |
|------|--------|------|--------|
| account_settings | 42 | pricing | 6 |
| advertising | 25 | help_support | 6 |
| inventory_fba | 24 | reports | 5 |
| marketplace_homepage | 20 | account_health | 5 |
| finance | 18 | apps_services | 5 |
| other | 17 | growth_tools | 4 |
| product_management | 15 | returns | 2 |
| promotions | 10 | b2b | 2 |
| order_management | 9 | brand | 2 |
| — | — | tax / authentication | 各 1 |

### 二、新增策略生成样例

新增 `非财务人员VAT税务文件禁止访问策略.json`，覆盖以下场景：
- **需求**：禁止运营人员查看和下载 VAT 税务文件，仅财务可访问
- **策略要点**：反选模式（选中除财务部门外所有部门）、完全禁止申请访问、仅 boss 可审批
- **RAG 匹配**：命中 rag_070（Tax Library 页面）
- 累计策略样例：11 → 12 个

### 三、项目清理

删除与本项目无关的文件：
- `体验内容/red_black_tree.cpp`（红黑树 C++ 代码，398 行）
- `体验内容/未命名.md`（空文件）

### 改动文件清单

| 文件 | 操作 | 变更量 |
|------|------|--------|
| amazon-rag-skill/rag_simple_db.json | 更新（全量语义补全） | +5,261 / -1,221 行 |
| amazon-rag-skill/generated_policies/非财务人员VAT税务文件禁止访问策略.json | 新建 | +55 行 |
| 体验内容/red_black_tree.cpp | 删除 | -398 行 |
| 体验内容/未命名.md | 删除 | -0 行 |

---

## v2.2 改动说明（2026-04-14）

> 改动范围：access_policy_skill_package 3 个文件更新 + 2 个新文件 + RAG 数据库扩容
> 详细文档：体验内容/access_policy_skill_package/README_platform_module_map.md

### 改动背景

v2.0 解决了"输出对齐表单"的问题，但当用户需求超出访问策略能力时，Agent 的响应存在两个问题：
1. 展示技术方案（Row-Level Security、API 网关等），小白用户看不懂
2. Agent 只了解"访问策略"这一个模块，无法指路到平台其他功能

v2.2 的核心改动：让 Agent 拥有紫鸟平台的完整能力地图，能精确指路；建议边界收敛到平台内，不推荐外部系统。

### 一、能力边界指引优化（skill_definition.json + 提示词.md）

**not_supported 数据结构重构**

改动前：
```json
{
  "capability": "业务系统字段级权限",
  "alternative": "在业务系统的角色权限模块中配置"
}
```

改动后：
```json
{
  "capability": "业务系统字段级权限",
  "user_explanation": "访问策略可以控制整个页面的访问权限，但没办法只隐藏页面里的某几个字段。",
  "platform_suggestion": "如果您想隐藏的是页面上的某个按钮或特定区域，可以试试「网页元素采集」功能...",
  "if_cannot_solve": "如果需要隐藏的是表格里的某一列数据，这个目前做不到。"
}
```

**on_not_supported 响应模板重写**，新增 response_tone 约束和 routing_fallback 规则。

**conditionally_supported（共用账号场景）** 去掉技术术语，改为平台内替代建议（拆分独立账号）。

**提示词.md 指引原则确立**，从 4 条扩展到 11 条平台内指路场景。

### 二、平台能力地图（新建 platform_module_map.json）

通过 9 次截图收集紫鸟浏览器实际界面，建立完整的平台模块地图：
- 24 个模块（安全监管 9 个、企业管理 7 个、账号/设备 2 个、云号 1 个、更多菜单 4 个、费用管理 1 个）
- 17 条指路规则（routing_rules）
- 每个模块标注置信度（verified/inferred）、导航路径、触发用语

### 三、指引原则收敛

确立核心原则：**Agent 的建议边界 = 紫鸟平台的能力边界**
- 不推荐外部系统（ERP、OA 等）
- 不出现「找技术团队」「找服务商」等指向外部角色的引导
- 平台内有替代方案就推荐，有现成模板就推荐模板
- 确实做不到的需求，坦诚告知「目前做不到」

### 四、RAG 数据库扩容（20 → 219 条）

从紫鸟平台网页资源管理 API 获取真实亚马逊 URL 数据，编写导入脚本自动修复编码 + 自动分类（20 个类别），写入 rag_simple_db.json。

### 五、产出文档

新建 README_platform_module_map.md，记录能力地图的完整产出过程。

### 改动文件清单

| 文件 | 操作 |
|------|------|
| access_policy_skill_package/platform_module_map.json | 新建 |
| access_policy_skill_package/README_platform_module_map.md | 新建 |
| access_policy_skill_package/skill_definition.json | 更新 |
| 体验内容/提示词.md | 更新 |
| amazon-rag-skill/rag_simple_db.json | 覆盖（20→219 条） |
| amazon-rag-skill/rag_backup.json | 备份旧数据 |
| amazon-rag-skill/scripts/import_real_urls.py | 新建 |

---

## v2.0 改动说明（2026-04-13）

> 改动范围：access_policy_skill_package 全部 4 个文件 + approval_based_access_control_skill 1 个文件

---

## 改动背景

v1.0 的 skill 输出是一份自定义结构的 JSON 策略文档，包含审计日志、合规声明、部署建议等字段。这些字段在实际使用的零信任平台「新增访问策略」表单中没有对应的输入位置，导致生成的结果无法直接使用，需要人工翻译才能填入表单。

v2.0 的核心改动：让输出结构 1:1 对齐平台表单字段，生成的结果可以直接照着填表。

---

## 一、config_template.json

### 改了什么

整个模板从自定义抽象字段重构为平台表单字段的精确映射。

### v1.0 的结构

```json
{
  "policy_name": "{{POLICY_NAME}}",
  "policy_type": "time_based_blacklist",
  "time_restrictions": {
    "schedule": {
      "days_of_week": "{{DAYS_OF_WEEK}}",
      "time_range": { "start": "{{START_TIME}}", "end": "{{END_TIME}}" },
      "timezone": "{{TIMEZONE}}"
    }
  },
  "blacklist": {
    "domains": "{{BLOCKED_DOMAINS}}",
    "match_type": "{{MATCH_TYPE}}",
    "block_message": "{{BLOCK_MESSAGE}}"
  },
  "user_scope": {
    "apply_to": "{{APPLY_TO}}",
    "exceptions": { "roles": "{{EXCEPTION_ROLES}}" }
  },
  "enforcement": {
    "strict_mode": true,
    "log_violations": true
  }
}
```

问题：`policy_type`、`blacklist.block_message`、`enforcement`、`timezone` 等字段在平台表单中没有对应输入框。

### v2.0 的结构

```json
{
  "form_fields": {
    "策略名称":      { "type": "text",      "max_length": 24 },
    "生效成员":      { "type": "selector",   "options": ["所有成员","除BOSS外所有成员","指定成员"] },
    "生效平台账号":   { "type": "selector",   "options": ["所有账号","指定账号"] },
    "生效时段": {
      "生效日期":    { "type": "date_range"  },
      "生效周期":    { "type": "weekday_selector", "options": ["一","二","三","四","五","六","七"] },
      "生效时间":    { "type": "time_range"  }
    },
    "访问策略描述":   { "type": "textarea",   "max_length": 400 },
    "访问审批限制": {
      "仅boss账号可审批": { "type": "checkbox" },
      "不允许申请访问":   { "type": "checkbox" }
    }
  },
  "tab_指定网页生效策略": { "type": "url_rule_list" },
  "tab_所有网页通用策略": {
    "复制":        { "options": ["允许且记录","限制"] },
    "文件上传":     { "options": ["允许且记录","限制"] },
    "文件下载":     { "options": ["允许且记录","限制"] },
    "打印":        { "options": ["允许且记录","限制"] },
    "开发者模式":   { "options": ["允许且记录","限制"] },
    "查看密码框":   { "options": ["允许且记录","限制"] }
  }
}
```

每个字段名就是表单上的标签名，每个值就是要填入的内容。

---

## 二、example_output.json

### 改了什么

示例输出从自定义文档格式换成表单填写版，展示"工作时间视频网站限制"场景生成的结果长什么样。

### v1.0 的示例输出

```json
{
  "policy_name": "工作时间视频网站限制",
  "policy_type": "time_based_blacklist",
  "time_restrictions": { "schedule": { "days_of_week": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "time_range": {"start":"09:00","end":"18:00"}, "timezone": "Asia/Shanghai" } },
  "blacklist": { "domains": ["*.bilibili.com","*.iqiyi.com","*.youku.com","*.v.qq.com","*.mgtv.com"], "match_type": "wildcard", "block_message": "工作时间禁止访问视频网站" },
  "user_scope": { "apply_to": "all_users", "exceptions": { "roles": ["BOSS"] } },
  "enforcement": { "strict_mode": true, "log_violations": true }
}
```

问题：`policy_type`、`timezone`、`match_type`、`block_message`、`enforcement` 在表单里填不进去。

### v2.0 的示例输出

```json
{
  "form_output": {
    "策略名称": "工作时间视频网站限制",
    "生效成员": "除BOSS外所有成员",
    "生效平台账号": "所有账号",
    "生效时段": {
      "模式": "指定时段生效",
      "生效日期": { "启用": false },
      "生效周期": { "启用": true, "选中": ["一","二","三","四","五"] },
      "生效时间": { "启用": true, "开始时间": "09:00", "结束时间": "18:00" }
    },
    "访问策略描述": "工作日9:00-18:00禁止访问视频网站（B站、爱奇艺、优酷、腾讯视频、芒果TV），BOSS不受限。防止工作时间浏览娱乐内容影响效率。",
    "访问审批限制": { "仅boss账号可审批": false, "不允许申请访问": false }
  },
  "tab_指定网页生效策略": [
    { "url_rule": "*.bilibili.com", "说明": "B站" },
    { "url_rule": "*.iqiyi.com",    "说明": "爱奇艺" },
    { "url_rule": "*.youku.com",    "说明": "优酷" },
    { "url_rule": "*.v.qq.com",     "说明": "腾讯视频" },
    { "url_rule": "*.mgtv.com",     "说明": "芒果TV" }
  ],
  "tab_所有网页通用策略": {
    "复制": "允许且记录",
    "文件上传": "允许且记录",
    "文件下载": "允许且记录",
    "打印": "允许且记录",
    "开发者模式": "允许且记录",
    "查看密码框": "允许且记录"
  }
}
```

拿到这个 JSON，每一行就是表单上一个框要填的值。

---

## 三、skill_definition.json

### 改了什么

三处关键变更，对话收集流程本身保留不变。

### 变更 1：新增平台能力边界定义

v1.0 没有这个概念，任何用户需求都会走完全流程并生成输出。

v2.0 新增 `platform_capability` 节点，明确列出平台能做和不能做的事：

**能做的（生成表单输出）：**
- URL 级页面屏蔽/放行 → 对应「指定网页生效策略」
- 浏览器行为控制（复制/下载/打印/F12/密码框）→ 对应「所有网页通用策略」
- 按成员/账号/时段生效 → 对应「生效成员」「生效平台账号」「生效时段」
- 审批控制 → 对应「访问审批限制」的两个勾选项

**做不了的（终止流程，给替代方案）：**
- 数据库行级记录过滤（如"6组只能看自己的Case"）→ 建议在业务系统后端实现
- 业务系统字段级权限（如"隐藏价格列"）→ 建议在业务系统角色模块配置
- 多级审批链 / 自定义审批表单 → 平台仅支持两个勾选项，复杂审批需在OA实现
- API / 接口级访问控制 → 建议在API网关实现

### 变更 2：phase_1 从"识别意图"升级为"检查+识别"

v1.0 的 phase_1 只做意图分类（时间黑名单/审批制/只读等）。

v2.0 的 phase_1 先检查平台能力边界：
- 匹配到 `supported` → 继续后续流程
- 匹配到 `not_supported` → 立即告知用户不可实现，给出替代方案，不再生成输出

### 变更 3：phase_4 输出规则对齐表单

v1.0 的 `parameter_mapping` 映射到自定义字段：

```
time_range    → time_restrictions.schedule
blocked_sites → blacklist.domains
user_scope    → user_scope
```

v2.0 映射到表单字段：

```
policy_name          → form_fields.策略名称
effective_members    → form_fields.生效成员
effective_period     → form_fields.生效时段
url_rules            → tab_指定网页生效策略
browser_controls     → tab_所有网页通用策略
approval             → form_fields.访问审批限制
```

新增 `output_rules`：
- 每个字段的值必须直接可填入表单，不需要二次加工
- 策略名称不超过 24 字符
- 策略描述不超过 400 字符
- 表单中没有的字段一律不输出

---

## 四、presets.json

### 改了什么

所有预设值从通用格式改为平台表单的实际选项格式，新增多个预设类别。

### URL 预设格式变更

v1.0：
```json
{ "domains": ["*.bilibili.com", "*.iqiyi.com"] }
```

v2.0：
```json
{ "rules": [
    { "url_rule": "*.bilibili.com", "说明": "B站" },
    { "url_rule": "*.iqiyi.com",    "说明": "爱奇艺" }
]}
```

每条带说明，且新增 `amazon_buyer_checkout` 类别（含已验证的 checkout URL）。

### 时段预设格式变更

v1.0：
```json
{ "days": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "hours": "09:00-18:00" }
```

v2.0：
```json
{ "生效周期": { "启用": true, "选中": ["一","二","三","四","五"] },
  "生效时间": { "启用": true, "开始时间": "09:00", "结束时间": "18:00" } }
```

新增 `after_work`（下班后 17:30-23:59）和 `weekend_only`（仅周末）预设。

### 新增预设类别

v1.0 只有 URL 预设和时间预设。v2.0 新增：
- `member_presets` — 所有成员 / 除BOSS外所有成员 / 指定成员
- `browser_control_presets` — 默认全允许 / 账号安全(限密码框) / 严格锁定(全限制)
- `approval_presets` — 不限制 / 仅boss审批 / 完全禁止

---

## 五、approval_based_access_control_skill.json

### 改了什么

将审批制访问控制的输出从自定义审批流文档收敛为平台表单能支持的范围。

### 审批能力收敛

v1.0 输出包含：
- `approval_chain`：多级审批链（主管 → 经理 → BOSS）
- `temporary_access`：临时权限有效期（15分钟/1小时/自定义）
- `application_form`：自定义申请表单（理由/紧急程度/预计时长）
- `approval_notification`：多渠道通知模板（邮件/短信/APP推送）
- `access_granted_reminder`：访问期间倒计时横幅

v2.0 收敛为平台支持的两个勾选项：
- `仅boss账号可审批`：true / false
- `不允许申请访问`：true / false

超出平台能力的审批功能不再输出。

### 对话流程精简

v1.0 有 6 个 phase，其中 phase_3（收集审批参数）和 phase_4（配置通知）包含大量平台不支持的选项。

v2.0 精简为 5 个 phase：
1. 检查平台能力 + RAG检索URL
2. 收集表单参数
3. 确认配置
4. 生成表单输出
5. 交付 + 同步RAG

### 新增表单填写版示例

提供两个完整的 `example_form_outputs`：
- 示例 1：运营专员访问账户详情页需BOSS审批（审批制）
- 示例 2：买家号Checkout结账页完全屏蔽 17:30起（黑名单）

每个示例都是可以直接照着填表单的 JSON。
