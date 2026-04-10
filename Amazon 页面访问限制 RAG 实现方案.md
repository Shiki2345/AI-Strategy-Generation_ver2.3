# Amazon 页面访问限制 RAG 实现方案

## 🎯 核心目标

实现一个 RAG 系统，能够：
- 将用户的自然语言描述（"美国亚马逊账户详情页"）映射到精确的 URL
- 支持模糊匹配和语义相似度搜索
- 随着对话不断学习和更新知识库

---

## 📊 系统架构

```
┌─────────────────┐
│  用户输入       │
│  "美国站账户页" │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  文本向量化     │
│  (Embedding)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  向量数据库     │
│  检索相似条目   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  排序 + 过滤    │
│  返回Top-K结果  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  LLM 确认       │
│  用户选择正确项 │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  更新 RAG 库    │
│  记录新映射     │
└─────────────────┘
```

---

## 🗄️ 数据结构设计

### 1. RAG 知识库条目 (JSON)

```json
{
  "id": "rag_001",
  "user_description": "美国亚马逊账户详情页",
  "aliases": [
    "美国站账户页",
    "US站账户信息页",
    "Seller Central账户详情"
  ],
  "exact_url": "https://sellercentral.amazon.com/sw/AccountInfo/",
  "url_pattern": "sellercentral.amazon.com/sw/AccountInfo",
  "page_description": "包含账户设置、银行信息、税务信息等",
  "keywords": ["账户", "详情", "美国", "Seller Central"],
  "marketplace": "US",
  "category": "account_management",
  "embedding": [0.123, 0.456, ...],  // 向量表示
  "confidence": 0.95,
  "usage_count": 5,
  "created_at": "2024-01-15T10:00:00Z",
  "last_used": "2024-01-20T15:30:00Z",
  "learned_from": "user_conversation"
}
```

### 2. Skill 文件结构

```json
{
  "skill_id": "amazon_account_page_restriction_v1",
  "skill_name": "限制运营人员访问Amazon特定页面",
  "version": "1.0",
  "domain": "amazon.com",
  
  "rag_references": [
    "rag_001",
    "rag_002"
  ],
  
  "conversation_template": { ... },
  "learned_rules": [ ... ]
}
```

---

## 🔧 技术实现方案

### 方案 A：本地向量数据库（推荐）

**使用技术栈：**
- **Embedding 模型**: OpenAI `text-embedding-3-small` 或 `text-embedding-ada-002`
- **向量数据库**: Chroma / LanceDB / FAISS
- **存储格式**: JSON + 向量索引

**优点：**
- 完全本地运行，数据隐私安全
- 轻量级，适合中小规模数据（< 10,000条）
- 与 VSCode Continue + Claude 集成良好

**实现步骤：**

#### 1. 安装依赖（Python）

```bash
pip install chromadb openai sentence-transformers
```

#### 2. 初始化 RAG 系统

```python
import chromadb
from chromadb.config import Settings
import openai
import json

# 初始化 Chroma 客户端
client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="./amazon_rag_db"
))

# 创建集合
collection = client.create_collection(
    name="amazon_urls",
    metadata={"description": "Amazon页面URL映射"}
)

# 添加初始数据
def add_url_entry(user_description, exact_url, page_description, aliases=[]):
    # 生成向量
    embedding = openai.Embedding.create(
        input=user_description,
        model="text-embedding-3-small"
    )['data'][0]['embedding']
    
    # 存储到向量库
    collection.add(
        embeddings=[embedding],
        documents=[user_description],
        metadatas=[{
            "exact_url": exact_url,
            "page_description": page_description,
            "aliases": json.dumps(aliases),
            "created_at": datetime.now().isoformat()
        }],
        ids=[f"rag_{collection.count() + 1}"]
    )

# 检索相似条目
def search_url(query, top_k=3):
    query_embedding = openai.Embedding.create(
        input=query,
        model="text-embedding-3-small"
    )['data'][0]['embedding']
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    
    return results
```

#### 3. 集成到 Continue Skill

在 Continue 的 Skill 中调用 RAG：

```python
# skill_context.py
from rag_system import search_url

def handle_user_query(user_input):
    # 提取页面描述
    page_description = extract_page_description(user_input)
    
    # RAG 检索
    results = search_url(page_description, top_k=3)
    
    if results['distances'][0][0] < 0.3:  # 高相似度
        return {
            "status": "match_found",
            "url": results['metadatas'][0]['exact_url'],
            "confidence": 1 - results['distances'][0][0],
            "alternatives": results['metadatas'][1:]
        }
    else:
        return {
            "status": "no_match",
            "suggestions": results['metadatas']
        }
```

---

### 方案 B：使用云端向量数据库

**使用技术栈：**
- **向量数据库**: Pinecone / Weaviate / Qdrant Cloud
- **Embedding 模型**: OpenAI API

**优点：**
- 可扩展性强
- 无需本地维护数据库

**缺点：**
- 需要网络连接
- 数据存储在云端

---

## 🎯 Continue 插件集成方案

### 1. Skill 文件结构

```
skill.zip
├── skill.json           # Skill 元数据
├── rag_db/              # RAG 数据库文件夹
│   ├── chroma.sqlite3   # Chroma 数据库
│   ├── embeddings.json  # 向量数据
│   └── metadata.json    # 元数据
├── templates/           # 对话模板
│   └── amazon_url_restriction.json
└── scripts/
    ├── rag_search.py    # RAG 检索脚本
    └── update_rag.py    # RAG 更新脚本
```

### 2. skill.json 示例

```json
{
  "name": "Amazon URL 访问限制配置助手",
  "version": "1.0.0",
  "description": "通过RAG检索实现精确的Amazon页面访问限制配置",
  "triggers": ["amazon", "亚马逊", "限制访问", "账户详情"],
  
  "rag_config": {
    "enabled": true,
    "db_path": "./rag_db",
    "embedding_model": "text-embedding-3-small",
    "similarity_threshold": 0.7
  },
  
  "conversation_flow": {
    "steps": [
      {
        "id": "url_identification",
        "type": "rag_search",
        "prompt": "正在检索知识库...",
        "next_step": "confirm_url"
      },
      {
        "id": "confirm_url",
        "type": "user_confirmation",
        "prompt": "找到以下匹配项，请确认：",
        "next_step": "collect_restrictions"
      }
    ]
  }
}
```

### 3. 在 Continue 中使用

#### 选项 1：使用 Continue 的 Context Provider

```typescript
// .continue/config.json
{
  "contextProviders": [
    {
      "name": "amazon-rag",
      "params": {
        "dbPath": "./skills/amazon_rag_db",
        "embeddingModel": "text-embedding-3-small"
      }
    }
  ]
}
```

#### 选项 2：使用 Custom Command

在 Continue 中定义自定义命令：

```typescript
// .continue/config.json
{
  "customCommands": [
    {
      "name": "search-amazon-url",
      "prompt": "搜索Amazon URL: {input}",
      "description": "在RAG库中搜索Amazon页面URL"
    }
  ]
}
```

---

## 📦 导出 Skill 的完整流程

### 1. 准备 RAG 数据

```python
# export_skill.py
import json
import shutil
import zipfile
from pathlib import Path

def export_skill():
    skill_dir = Path("./skill_export")
    skill_dir.mkdir(exist_ok=True)
    
    # 1. 导出 RAG 数据库
    shutil.copytree("./amazon_rag_db", skill_dir / "rag_db")
    
    # 2. 生成 skill.json
    skill_meta = {
        "name": "Amazon URL Restriction Helper",
        "version": "1.0.0",
        "rag_entries_count": collection.count(),
        "skills_count": 3,
        "last_updated": datetime.now().isoformat()
    }
    
    with open(skill_dir / "skill.json", "w") as f:
        json.dump(skill_meta, f, indent=2)
    
    # 3. 打包成 zip
    with zipfile.ZipFile("skill.zip", "w") as zf:
        for file in skill_dir.rglob("*"):
            zf.write(file, file.relative_to(skill_dir))
    
    print("✅ Skill 导出成功: skill.zip")

export_skill()
```

### 2. 在新环境中导入

```python
# import_skill.py
import zipfile

def import_skill(skill_zip_path):
    with zipfile.ZipFile(skill_zip_path, "r") as zf:
        zf.extractall("./imported_skill")
    
    # 重新加载 RAG 数据库
    client = chromadb.Client(Settings(
        persist_directory="./imported_skill/rag_db"
    ))
    
    print("✅ Skill 导入成功")

import_skill("skill.zip")
```

---

## 🔄 RAG 更新机制

### 1. 对话中学习新 URL

```python
def learn_new_url(user_description, exact_url, page_description):
    # 检查是否已存在
    existing = search_url(user_description, top_k=1)
    
    if existing['distances'][0][0] > 0.2:  # 不够相似，添加新条目
        add_url_entry(
            user_description=user_description,
            exact_url=exact_url,
            page_description=page_description
        )
        print(f"📚 RAG 库已更新: {user_description} -> {exact_url}")
    else:
        # 更新已有条目的别名
        update_aliases(existing['ids'][0], user_description)
```

### 2. 自动保存和同步

```python
# 每次更新后自动持久化
collection.persist()

# 导出为可读的 JSON 备份
def backup_rag_to_json():
    all_entries = collection.get()
    backup = []
    
    for i, doc in enumerate(all_entries['documents']):
        backup.append({
            "id": all_entries['ids'][i],
            "description": doc,
            "url": all_entries['metadatas'][i]['exact_url'],
            "page_info": all_entries['metadatas'][i]['page_description']
        })
    
    with open("rag_backup.json", "w", encoding="utf-8") as f:
        json.dump(backup, f, ensure_ascii=False, indent=2)
```

---

## 🚀 快速启动指南

### 步骤 1：准备环境

```bash
# 创建项目目录
mkdir amazon-rag-skill
cd amazon-rag-skill

# 安装依赖
pip install chromadb openai python-dotenv

# 配置 OpenAI API Key
echo "OPENAI_API_KEY=your_key_here" > .env
```

### 步骤 2：初始化 RAG 库

```python
# init_rag.py
from rag_system import add_url_entry

# 添加初始数据
add_url_entry(
    user_description="美国亚马逊账户详情页",
    exact_url="https://sellercentral.amazon.com/sw/AccountInfo/",
    page_description="包含账户设置、银行信息、税务信息",
    aliases=["美国站账户页", "Seller Central账户信息"]
)

add_url_entry(
    user_description="亚马逊广告报告页",
    exact_url="https://sellercentral.amazon.com/advertising/reports",
    page_description="可以下载广告数据报告",
    aliases=["广告数据下载页", "广告报表页"]
)

print("✅ RAG 库初始化完成")
```

### 步骤 3：测试检索

```python
# test_rag.py
from rag_system import search_url

# 测试检索
results = search_url("美国站的账户信息页面", top_k=3)

print("检索结果：")
for i, metadata in enumerate(results['metadatas'][0]):
    print(f"{i+1}. {metadata['exact_url']}")
    print(f"   相似度: {1 - results['distances'][0][i]:.2%}")
    print(f"   描述: {metadata['page_description']}")
```

### 步骤 4：导出 Skill

```bash
python export_skill.py
# 生成 skill.zip 文件
```

---

## 📊 预期效果

| 场景 | RAG 命中率 | 用户体验 |
|------|-----------|---------|
| 精确匹配 | > 95% | 1秒内返回精确URL |
| 模糊匹配 | 70-90% | 提供2-3个候选项 |
| 未知页面 | < 30% | 引导用户补充信息 |

---

## 💡 进阶优化

### 1. 多语言支持

```python
# 使用多语言 Embedding 模型
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
embedding = model.encode(user_description)
```

### 2. 自动别名生成

```python
def generate_aliases(user_description, exact_url):
    prompt = f"""
    根据以下信息生成3-5个常见的别名：
    
    用户描述: {user_description}
    URL: {exact_url}
    
    返回格式：["别名1", "别名2", ...]
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return json.loads(response.choices[0].message.content)
```

### 3. URL 模式匹配

```python
import re

def extract_url_pattern(url):
    # 提取关键路径
    pattern = re.sub(r'\?.*', '', url)  # 去除查询参数
    pattern = re.sub(r'https?://', '', pattern)  # 去除协议
    return pattern

# 使用模式匹配增强检索
def search_with_pattern(query):
    results = search_url(query)
    
    # 如果语义检索失败，尝试关键词匹配
    if results['distances'][0][0] > 0.5:
        keyword_results = keyword_search(query)
        results = merge_results(results, keyword_results)
    
    return results
```

---

## ✅ 总结

**最佳实践：**
1. ✅ 使用 **ChromaDB** + **OpenAI Embedding** 作为 RAG 基础
2. ✅ 在每次对话后**自动更新** RAG 库
3. ✅ 定期**导出 JSON 备份**，便于版本控制
4. ✅ 将 RAG 数据库打包进 **skill.zip**，便于分发
5. ✅ 在 VSCode Continue 中通过 **Context Provider** 集成

**下一步行动：**
- [ ] 搭建本地 ChromaDB 环境
- [ ] 准备初始 Amazon URL 数据集（10-20条）
- [ ] 编写 RAG 检索和更新脚本
- [ ] 测试与 Continue Skill 的集成
- [ ] 导出第一个可用的 skill.zip

祝开发顺利！🚀
