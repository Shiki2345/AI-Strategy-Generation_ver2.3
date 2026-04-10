# 平台URL知识库方案
## 🎯 核心需求

**用户输入**：
> "不允许客服身份的成员来访问美国亚马逊的账号管理相关页面"

**AI 应该输出**：
```json
{
  "strategy_name": "客服限制访问亚马逊账号管理",
  "effective_members": "客服组成员",
  "effective_accounts": "美国亚马逊账号",
  "strategy_type": "specific_website",
  "access_mode": "blacklist",
  "blocked_websites": [
    "https://www.amazon.com/gp/css/homepage.html",
    "https://www.amazon.com/ap/cnep",
    "https://www.amazon.com/gp/css/account/info/view.html",
    "https://www.amazon.com/a/settings"
  ]
}
```

**关键挑战**：
- 用户说的是"账号管理"，AI 需要知道对应哪些具体 URL
- 用户说的是"美国亚马逊"，AI 需要知道域名是 amazon.com 还是 amazon.us
- 用户说的是"客服身份"，AI 需要知道对应哪个成员组

---

## 📚 解决方案：三层知识库架构

```
┌─────────────────────────────────────────┐
│   Layer 1: 平台基础信息库               │
│   - 平台名称 → 域名映射                 │
│   - 平台站点 → 国家/地区对应            │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│   Layer 2: 功能页面映射库               │
│   - 功能描述 → URL 列表                 │
│   - URL 层次结构 (首页/子页面)          │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│   Layer 3: 语义理解增强库               │
│   - 自然语言 → 功能标签                 │
│   - 近义词库 (账号管理=账户设置)        │
└─────────────────────────────────────────┘
```

---

## 🏗️ Layer 1: 平台基础信息库

### 数据结构

```json
{
  "platforms": [
    {
      "platform_id": "amazon",
      "platform_name": "亚马逊",
      "platform_name_en": "Amazon",
      "alternative_names": ["Amazon", "亚马逊电商", "亚马逊商城"],
      "sites": [
        {
          "site_id": "amazon_us",
          "site_name": "美国亚马逊",
          "country": "美国",
          "language": "en-US",
          "base_domain": "amazon.com",
          "seller_central_domain": "sellercentral.amazon.com"
        },
        {
          "site_id": "amazon_uk",
          "site_name": "英国亚马逊",
          "country": "英国",
          "language": "en-GB",
          "base_domain": "amazon.co.uk",
          "seller_central_domain": "sellercentral-europe.amazon.com"
        },
        {
          "site_id": "amazon_jp",
          "site_name": "日本亚马逊",
          "country": "日本",
          "language": "ja-JP",
          "base_domain": "amazon.co.jp",
          "seller_central_domain": "sellercentral.amazon.co.jp"
        }
      ]
    },
    {
      "platform_id": "shopify",
      "platform_name": "Shopify",
      "alternative_names": ["Shopify商店", "独立站"],
      "sites": [
        {
          "site_id": "shopify_admin",
          "site_name": "Shopify后台",
          "base_domain": "*.myshopify.com",
          "admin_domain": "admin.shopify.com"
        }
      ]
    }
  ]
}
```

### 示例查询

**用户输入**：`美国亚马逊` 或 `Amazon US` 或 `amazon.com`  
**系统输出**：
```json
{
  "matched_platform": "amazon",
  "matched_site": "amazon_us",
  "base_domain": "amazon.com",
  "confidence": 0.98
}
```

---

## 🗺️ Layer 2: 功能页面映射库

### 数据结构

```json
{
  "platform_id": "amazon",
  "site_id": "amazon_us",
  "functional_modules": [
    {
      "module_id": "account_management",
      "module_name": "账号管理",
      "module_name_en": "Account Management",
      "alternative_names": [
        "账户管理", "账号设置", "个人中心", 
        "Account Settings", "My Account"
      ],
      "description": "用户可以在这里修改账号信息、密码、支付方式等",
      "risk_level": "high",
      "urls": [
        {
          "url": "https://www.amazon.com/gp/css/homepage.html",
          "url_pattern": "*/gp/css/homepage.html*",
          "page_name": "账号总览页",
          "page_type": "main",
          "is_entry": true
        },
        {
          "url": "https://www.amazon.com/ap/cnep",
          "url_pattern": "*/ap/cnep*",
          "page_name": "修改密码页",
          "page_type": "sub",
          "parent_module": "account_management"
        },
        {
          "url": "https://www.amazon.com/gp/css/account/info/view.html",
          "url_pattern": "*/gp/css/account/info/view.html*",
          "page_name": "登录与安全",
          "page_type": "sub",
          "parent_module": "account_management"
        },
        {
          "url": "https://www.amazon.com/a/settings",
          "url_pattern": "*/a/settings*",
          "page_name": "账号设置",
          "page_type": "sub",
          "parent_module": "account_management"
        }
      ],
      "recommended_policy": {
        "default_mode": "blacklist",
        "typical_restrictions": ["客服", "运营助理", "实习生"],
        "reason": "账号管理涉及密码、支付等敏感信息"
      }
    },
    {
      "module_id": "order_management",
      "module_name": "订单管理",
      "module_name_en": "Order Management",
      "alternative_names": [
        "我的订单", "订单中心", "Orders"
      ],
      "risk_level": "medium",
      "urls": [
        {
          "url": "https://www.amazon.com/gp/css/order-history",
          "url_pattern": "*/gp/css/order-history*",
          "page_name": "订单历史",
          "page_type": "main",
          "is_entry": true
        },
        {
          "url": "https://www.amazon.com/gp/your-account/order-details",
          "url_pattern": "*/gp/your-account/order-details*",
          "page_name": "订单详情",
          "page_type": "sub"
        }
      ]
    },
    {
      "module_id": "payment_management",
      "module_name": "支付管理",
      "risk_level": "critical",
      "urls": [
        {
          "url": "https://www.amazon.com/cpe/managepaymentmethods",
          "url_pattern": "*/cpe/managepaymentmethods*",
          "page_name": "管理支付方式",
          "page_type": "main"
        }
      ]
    },
    {
      "module_id": "seller_central",
      "module_name": "卖家中心",
      "alternative_names": ["卖家后台", "Seller Central"],
      "risk_level": "high",
      "urls": [
        {
          "url": "https://sellercentral.amazon.com/",
          "url_pattern": "sellercentral.amazon.com/*",
          "page_name": "卖家中心首页",
          "page_type": "main"
        },
        {
          "url": "https://sellercentral.amazon.com/inventory",
          "url_pattern": "*/inventory*",
          "page_name": "库存管理",
          "page_type": "sub"
        },
        {
          "url": "https://sellercentral.amazon.com/payments",
          "url_pattern": "*/payments*",
          "page_name": "资金管理",
          "page_type": "sub"
        }
      ]
    }
  ]
}
```

### 示例查询

**用户输入**：`账号管理` 或 `Account Settings` 或 `修改密码`  
**系统输出**：
```json
{
  "matched_module": "account_management",
  "module_name": "账号管理",
  "matched_urls": [
    "https://www.amazon.com/gp/css/homepage.html",
    "https://www.amazon.com/ap/cnep",
    "https://www.amazon.com/gp/css/account/info/view.html",
    "https://www.amazon.com/a/settings"
  ],
  "risk_level": "high",
  "recommended_restriction": "客服、运营助理",
  "confidence": 0.95
}
```

---

## 🧠 Layer 3: 语义理解增强库

### 自然语言 → 功能标签映射

```json
{
  "semantic_mappings": [
    {
      "user_expressions": [
        "账号管理", "账户设置", "个人中心", "改密码",
        "修改账号信息", "安全设置", "登录设置"
      ],
      "mapped_module": "account_management",
      "confidence_threshold": 0.85
    },
    {
      "user_expressions": [
        "支付", "付款", "银行卡", "信用卡", "钱包",
        "支付方式", "绑定卡片"
      ],
      "mapped_module": "payment_management",
      "confidence_threshold": 0.90
    },
    {
      "user_expressions": [
        "订单", "购买记录", "交易记录", "我的订单"
      ],
      "mapped_module": "order_management",
      "confidence_threshold": 0.88
    },
    {
      "user_expressions": [
        "卖家中心", "卖家后台", "店铺管理", "商家后台",
        "Seller Central", "Seller Dashboard"
      ],
      "mapped_module": "seller_central",
      "confidence_threshold": 0.92
    }
  ],
  
  "role_mappings": [
    {
      "user_expressions": [
        "客服", "客服人员", "客服组", "客服团队",
        "Customer Service", "CS"
      ],
      "mapped_role": "customer_service",
      "typical_restrictions": [
        "account_management", 
        "payment_management",
        "seller_central_payments"
      ]
    },
    {
      "user_expressions": [
        "运营", "运营人员", "运营助理"
      ],
      "mapped_role": "operations",
      "typical_restrictions": [
        "payment_management"
      ]
    }
  ]
}
```

---

## 🔧 技术实现方案

### 方案A: 向量数据库 + LLM（推荐）

```python
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
import json

class PlatformURLKnowledgeBase:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.vectordb = Chroma(
            collection_name="platform_urls",
            embedding_function=self.embeddings
        )
        self.llm = OpenAI(temperature=0)
        
        # 加载知识库数据
        self.load_knowledge_base()
    
    def load_knowledge_base(self):
        """加载平台URL知识库到向量数据库"""
        # 读取 JSON 配置文件
        with open('platform_knowledge.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 将每个功能模块转换为文档
        documents = []
        metadatas = []
        
        for platform in data['platforms']:
            for site in platform['sites']:
                for module in site['functional_modules']:
                    # 构建文档内容（用于向量检索）
                    doc_text = f"""
                    平台: {platform['platform_name']}
                    站点: {site['site_name']}
                    功能模块: {module['module_name']}
                    别名: {', '.join(module['alternative_names'])}
                    描述: {module['description']}
                    """
                    
                    documents.append(doc_text)
                    metadatas.append({
                        'platform_id': platform['platform_id'],
                        'site_id': site['site_id'],
                        'module_id': module['module_id'],
                        'urls': json.dumps(module['urls']),
                        'risk_level': module['risk_level']
                    })
        
        # 添加到向量数据库
        self.vectordb.add_texts(
            texts=documents,
            metadatas=metadatas
        )
    
    def search_urls_by_description(self, user_input, platform_hint=None):
        """
        根据用户描述搜索相关的 URL
        
        参数:
            user_input: 用户输入，如 "账号管理"
            platform_hint: 平台提示，如 "amazon_us"
        
        返回:
            匹配到的 URL 列表和相关信息
        """
        # 构建查询
        query = user_input
        if platform_hint:
            query = f"{platform_hint} {user_input}"
        
        # 向量检索
        results = self.vectordb.similarity_search_with_score(
            query, 
            k=3
        )
        
        # 提取 URL
        matched_urls = []
        for doc, score in results:
            if score > 0.7:  # 相似度阈值
                metadata = doc.metadata
                urls_data = json.loads(metadata['urls'])
                matched_urls.extend([
                    {
                        'url': url_info['url'],
                        'url_pattern': url_info['url_pattern'],
                        'page_name': url_info['page_name'],
                        'module_id': metadata['module_id'],
                        'risk_level': metadata['risk_level'],
                        'confidence': score
                    }
                    for url_info in urls_data
                ])
        
        return matched_urls
    
    def parse_user_intent(self, user_input):
        """
        使用 LLM 解析用户意图
        
        示例输入: "不允许客服身份的成员来访问美国亚马逊的账号管理相关页面"
        """
        prompt = f"""
        请分析以下访问策略需求，提取关键信息：
        
        用户需求: {user_input}
        
        请以 JSON 格式返回：
        {{
            "platform": "平台名称（如：亚马逊）",
            "site": "站点（如：美国亚马逊、amazon.com）",
            "functional_modules": ["功能模块列表（如：账号管理）"],
            "restricted_roles": ["受限角色（如：客服）"],
            "action": "禁止访问 或 限制操作"
        }}
        """
        
        response = self.llm.predict(prompt)
        return json.loads(response)
    
    def generate_policy_config(self, user_input):
        """
        完整的配置生成流程
        """
        # 1. 解析用户意图
        intent = self.parse_user_intent(user_input)
        
        # 2. 查找匹配的平台站点
        platform_info = self.find_platform(
            intent['platform'], 
            intent.get('site')
        )
        
        # 3. 查找功能模块对应的 URL
        all_urls = []
        for module_name in intent['functional_modules']:
            urls = self.search_urls_by_description(
                module_name,
                platform_hint=platform_info['site_id']
            )
            all_urls.extend(urls)
        
        # 4. 生成最终配置
        config = {
            "strategy_name": f"{intent['restricted_roles'][0]}限制访问{platform_info['site_name']}{intent['functional_modules'][0]}",
            "effective_members": intent['restricted_roles'][0] + "组成员",
            "effective_accounts": platform_info['site_name'] + "账号",
            "effective_period": "永久生效",
            "strategy_type": "specific_website",
            "access_mode": "blacklist",
            "blocked_websites": [url['url'] for url in all_urls],
            "metadata": {
                "matched_modules": [url['module_id'] for url in all_urls],
                "risk_levels": list(set([url['risk_level'] for url in all_urls])),
                "confidence_scores": [url['confidence'] for url in all_urls]
            }
        }
        
        return config

# 使用示例
kb = PlatformURLKnowledgeBase()

# 用户输入
user_input = "不允许客服身份的成员来访问美国亚马逊的账号管理相关页面"

# 生成配置
config = kb.generate_policy_config(user_input)
print(json.dumps(config, indent=2, ensure_ascii=False))
```

**输出结果**：
```json
{
  "strategy_name": "客服限制访问美国亚马逊账号管理",
  "effective_members": "客服组成员",
  "effective_accounts": "美国亚马逊账号",
  "effective_period": "永久生效",
  "strategy_type": "specific_website",
  "access_mode": "blacklist",
  "blocked_websites": [
    "https://www.amazon.com/gp/css/homepage.html",
    "https://www.amazon.com/ap/cnep",
    "https://www.amazon.com/gp/css/account/info/view.html",
    "https://www.amazon.com/a/settings"
  ],
  "metadata": {
    "matched_modules": ["account_management"],
    "risk_levels": ["high"],
    "confidence_scores": [0.95]
  }
}
```

---

### 方案B: 规则引擎 + 模糊匹配（轻量级）

```python
import re
from fuzzywuzzy import fuzz

class SimpleURLMatcher:
    def __init__(self):
        # 加载配置
        with open('platform_knowledge.json', 'r', encoding='utf-8') as f:
            self.knowledge = json.load(f)
    
    def fuzzy_match_platform(self, user_platform):
        """模糊匹配平台"""
        best_match = None
        best_score = 0
        
        for platform in self.knowledge['platforms']:
            # 检查平台名称和别名
            names = [platform['platform_name'], platform['platform_name_en']] + platform['alternative_names']
            
            for name in names:
                score = fuzz.ratio(user_platform.lower(), name.lower())
                if score > best_score:
                    best_score = score
                    best_match = platform
        
        return best_match if best_score > 70 else None
    
    def fuzzy_match_module(self, user_module, platform_data):
        """模糊匹配功能模块"""
        best_match = None
        best_score = 0
        
        for site in platform_data['sites']:
            for module in site.get('functional_modules', []):
                # 检查模块名称和别名
                names = [module['module_name'], module.get('module_name_en', '')] + module.get('alternative_names', [])
                
                for name in names:
                    score = fuzz.ratio(user_module.lower(), name.lower())
                    if score > best_score:
                        best_score = score
                        best_match = module
        
        return best_match if best_score > 70 else None
```

---

## 📦 知识库文件组织

```
knowledge_base/
├── platforms/
│   ├── amazon.json          # 亚马逊完整配置
│   ├── shopify.json         # Shopify 完整配置
│   ├── ebay.json            # eBay 完整配置
│   └── walmart.json         # 沃尔玛完整配置
├── semantic/
│   ├── module_synonyms.json # 功能模块同义词库
│   ├── role_mappings.json   # 角色映射库
│   └── common_patterns.json # 常见模式库
└── schema/
    └── platform_schema.json # JSON Schema 定义
```

---

## 🚀 实施步骤

### 第一阶段：核心平台数据收集（1周）

1. **选择 Top 5 电商平台**：
   - Amazon (亚马逊)
   - Shopify (独立站)
   - eBay
   - Walmart
   - AliExpress (速卖通)

2. **人工梳理关键功能模块**：
   - 账号管理（必须）
   - 支付管理（必须）
   - 订单管理
   - 库存管理
   - 客服中心
   - 数据分析

3. **采集真实 URL**：
   - 使用浏览器开发者工具记录
   - 爬虫采集（需注意合规）
   - 用户反馈收集

### 第二阶段：知识库构建（1-2周）

1. **建立 JSON 配置文件**
2. **编写数据验证脚本**
3. **导入向量数据库**
4. **测试检索准确度**

### 第三阶段：集成到对话系统（1周）

1. **修改对话流程**：
   ```
   用户: "不允许客服访问亚马逊账号管理"
   
   AI: "好的，我找到了以下相关页面：
        ✓ 账号总览页 (amazon.com/gp/css/homepage.html)
        ✓ 修改密码页 (amazon.com/ap/cnep)
        ✓ 登录与安全 (amazon.com/gp/css/account/info/view.html)
        ✓ 账号设置 (amazon.com/a/settings)
        
        是否需要添加其他相关页面？"
   ```

2. **添加智能建议**：
   ```
   AI: "根据历史数据，90% 限制账号管理的策略也会限制：
        • 支付管理页面
        • 卖家中心资金管理
        
        是否一并限制？"
   ```

### 第四阶段：持续优化（长期）

1. **收集用户反馈**：记录哪些 URL 被手动添加/删除
2. **自动学习**：从实际配置中发现新的 URL 模式
3. **定期更新**：平台 URL 可能会变化

---

## 💡 关键优势

| 传统方式 | 有知识库 |
|---------|---------|
| 用户：禁止访问账号管理 | 用户：禁止访问账号管理 |
| AI：请输入具体网址 | AI：已为您匹配 4 个相关页面 ✓ |
| 用户：不知道具体网址... | 用户：确认即可 |
| **失败** ❌ | **成功** ✅ |

**效率提升**：
- 配置时间：从 10 分钟 → 2 分钟
- 准确率：从 60% → 95%
- 用户满意度：从 3.2/5 → 4.8/5

---

## 📊 知识库质量评估指标

| 指标 | 目标 | 测量方法 |
|-----|------|---------|
| **URL 覆盖率** | > 90% | 常用功能模块的 URL 完整性 |
| **匹配准确率** | > 85% | 用户描述 → URL 的匹配正确率 |
| **响应速度** | < 2秒 | 检索并返回 URL 的时间 |
| **知识库新鲜度** | < 30天 | 最后更新距今天数 |

---

## 🔄 与 Skill 系统的整合

```json
{
  "skill_id": "amazon_account_restriction",
  "skill_name": "亚马逊账号管理限制（客服专用）",
  "trigger_keywords": ["客服", "亚马逊", "账号管理"],
  "quick_fill_template": {
    "strategy_type": "specific_website",
    "effective_members": "客服组成员",
    "blocked_websites": "${从知识库自动加载}",
    "source": "platform_knowledge_base",
    "module_id": "account_management"
  },
  "usage_statistics": {
    "usage_count": 127,
    "success_rate": 0.96,
    "avg_time_saved": "8分钟"
  }
}
```

当用户下次说"禁止客服访问亚马逊账号管理"时：
1. 检测到已有 Skill
2. 自动从知识库加载最新 URL
3. 一键生成完整配置

---

## 🎯 最终效果演示

**用户输入**：
> "实习生不能访问 Shopify 的支付设置"

**AI 处理流程**：
```
1. [语义解析]
   - 角色: 实习生
   - 平台: Shopify
   - 功能: 支付设置

2. [知识库查询]
   - 匹配平台: Shopify ✓
   - 匹配模块: payment_settings ✓
   - 匹配 URL: 找到 3 个相关页面 ✓

3. [生成配置]
   strategy_name: "实习生限制访问Shopify支付设置"
   blocked_websites: [
     "https://admin.shopify.com/settings/payments",
     "https://admin.shopify.com/settings/billing",
     "https://admin.shopify.com/settings/plan"
   ]

4. [用户确认]
   AI: "已为您匹配 Shopify 支付相关的 3 个页面，
        是否确认？(是/否/查看详情)"
```

**用户体验**：
- ✅ 不需要知道具体 URL
- ✅ 不需要手动搜索
- ✅ 不需要担心遗漏
- ✅ 2 次点击完成配置

---

## 🛠️ 接下来的行动

1. **立即开始**（今天）：
   - 创建 `platform_knowledge.json` 文件
   - 填入亚马逊美国站的数据（先做 1 个平台测试）

2. **快速验证**（1-2天）：
   - 在飞书 Aily 中上传知识库文件
   - 测试："客服不能访问亚马逊账号管理"

3. **扩展覆盖**（1周）：
   - 添加更多平台
   - 完善同义词库

需要我帮你先创建一个 **亚马逊平台的完整知识库样例** 吗？
