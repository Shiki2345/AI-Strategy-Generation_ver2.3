# Amazon RAG Skill 项目

## 项目结构

```
amazon-rag-skill/
├── data/                   # 数据文件
│   └── amazon_urls.json    # 初始 URL 数据
├── scripts/                # 脚本文件
│   ├── rag_system.py       # RAG 核心系统
│   ├── init_rag.py         # 初始化脚本
│   ├── test_rag.py         # 测试脚本
│   └── export_skill.py     # 导出 Skill 脚本
├── tests/                  # 测试用例
├── rag_db/                 # RAG 数据库（运行后生成）
├── requirements.txt        # Python 依赖
└── README.md              # 本文件

## 环境配置

1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 配置 OpenAI API Key（请创建 .env 文件）：
   ```
   OPENAI_API_KEY=your_key_here
   ```

## 使用流程

### 1. 初始化 RAG 库
```bash
python scripts/init_rag.py
```

### 2. 测试检索功能
```bash
python scripts/test_rag.py
```

### 3. 导出 Skill
```bash
python scripts/export_skill.py
```

## 注意事项

- 请确保已配置 OpenAI API Key
- 首次运行需要联网下载 embedding 数据
- RAG 数据库会自动持久化到 rag_db 目录
