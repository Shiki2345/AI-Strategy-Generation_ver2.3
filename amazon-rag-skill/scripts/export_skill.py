"""
导出 Skill 为 ZIP 文件

将 RAG 数据库、配置文件、脚本等打包为可分发的 skill.zip
"""

import os
import sys
import json
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

# 添加父目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

from rag_system import AmazonURLRAG


def create_skill_metadata(rag: AmazonURLRAG) -> dict:
    """
    创建 Skill 元数据
    
    Args:
        rag: RAG 系统实例
        
    Returns:
        元数据字典
    """
    stats = rag.get_statistics()
    
    metadata = {
        "name": "Amazon URL 访问限制配置助手",
        "version": "1.0.0",
        "description": "通过RAG检索实现精确的Amazon页面访问限制配置",
        "author": "Your Name",
        "created_at": datetime.now().isoformat(),
        
        "rag_config": {
            "enabled": True,
            "embedding_model": "text-embedding-3-small",
            "similarity_threshold": 0.7,
            "entries_count": stats['total_entries']
        },
        
        "statistics": stats,
        
        "triggers": [
            "amazon", "亚马逊", "限制访问", "账户详情",
            "订单管理", "广告报告", "库存管理"
        ],
        
        "supported_marketplaces": list(stats['marketplaces'].keys()),
        "categories": list(stats['categories'].keys()),
        
        "conversation_flow": {
            "steps": [
                {
                    "id": "url_identification",
                    "type": "rag_search",
                    "description": "使用RAG检索识别用户描述的页面"
                },
                {
                    "id": "confirm_url",
                    "type": "user_confirmation",
                    "description": "用户确认检索到的URL"
                },
                {
                    "id": "collect_member_info",
                    "type": "collect_info",
                    "description": "收集生效对象信息"
                },
                {
                    "id": "collect_time_info",
                    "type": "collect_info",
                    "description": "收集生效时间信息"
                },
                {
                    "id": "collect_approval_info",
                    "type": "collect_info",
                    "description": "收集审批机制信息"
                },
                {
                    "id": "generate_config",
                    "type": "generate",
                    "description": "生成最终的JSON配置"
                }
            ]
        },
        
        "requirements": [
            "chromadb>=0.4.22",
            "openai>=1.12.0",
            "python-dotenv>=1.0.0"
        ]
    }
    
    return metadata


def export_skill(output_name: str = "skill.zip"):
    """
    导出 Skill 为 ZIP 文件
    
    Args:
        output_name: 输出文件名
    """
    print("=" * 70)
    print("📦 开始导出 Skill")
    print("=" * 70)
    
    try:
        # 1. 初始化 RAG 系统
        print("\n📝 步骤 1: 加载 RAG 系统...")
        rag = AmazonURLRAG(db_path="../rag_db")
        stats = rag.get_statistics()
        print(f"✅ 已加载 {stats['total_entries']} 条数据")
        
        # 2. 创建临时导出目录
        print("\n📝 步骤 2: 创建导出目录...")
        export_dir = Path("../skill_export")
        if export_dir.exists():
            shutil.rmtree(export_dir)
        export_dir.mkdir()
        print(f"✅ 创建目录: {export_dir}")
        
        # 3. 复制 RAG 数据库
        print("\n📝 步骤 3: 复制 RAG 数据库...")
        rag_db_source = Path("../rag_db")
        rag_db_dest = export_dir / "rag_db"
        shutil.copytree(rag_db_source, rag_db_dest)
        print(f"✅ 已复制数据库: {rag_db_dest}")
        
        # 4. 导出 JSON 备份
        print("\n📝 步骤 4: 导出 JSON 备份...")
        rag.export_to_json(str(export_dir / "rag_backup.json"))
        
        # 5. 创建 Skill 元数据
        print("\n📝 步骤 5: 生成 Skill 元数据...")
        metadata = create_skill_metadata(rag)
        with open(export_dir / "skill.json", 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        print("✅ 已生成 skill.json")
        
        # 6. 复制脚本
        print("\n📝 步骤 6: 复制脚本文件...")
        scripts_dir = export_dir / "scripts"
        scripts_dir.mkdir()
        
        script_files = [
            "rag_system.py",
            "init_rag.py",
            "test_rag.py"
        ]
        
        for script_file in script_files:
            src = Path(__file__).parent / script_file
            if src.exists():
                shutil.copy(src, scripts_dir / script_file)
                print(f"  ✅ {script_file}")
        
        # 7. 复制数据文件
        print("\n📝 步骤 7: 复制数据文件...")
        data_dir = export_dir / "data"
        data_dir.mkdir()
        
        data_source = Path("../data/amazon_urls.json")
        if data_source.exists():
            shutil.copy(data_source, data_dir / "amazon_urls.json")
            print("  ✅ amazon_urls.json")
        
        # 8. 复制配置文件
        print("\n📝 步骤 8: 复制配置文件...")
        
        # requirements.txt
        req_source = Path("../requirements.txt")
        if req_source.exists():
            shutil.copy(req_source, export_dir / "requirements.txt")
            print("  ✅ requirements.txt")
        
        # 9. 创建 README
        print("\n📝 步骤 9: 生成 README...")
        readme_content = f"""# Amazon URL 访问限制配置助手 Skill

## 版本信息
- 版本: {metadata['version']}
- 创建时间: {metadata['created_at']}
- RAG 条目数: {metadata['rag_config']['entries_count']}

## 功能特性
- ✅ 基于 RAG 的智能 URL 识别
- ✅ 支持模糊匹配和语义搜索
- ✅ 支持多站点（{', '.join(metadata['supported_marketplaces'])}）
- ✅ 覆盖 {len(metadata['categories'])} 个分类

## 安装使用

### 1. 解压文件
```bash
unzip skill.zip
cd skill_export
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置 API Key
创建 .env 文件并添加：
```
OPENAI_API_KEY=your_openai_api_key
```

### 4. 测试 RAG 系统
```bash
cd scripts
python test_rag.py
```

## 文件结构
```
skill_export/
├── skill.json              # Skill 元数据
├── rag_db/                 # RAG 向量数据库
├── rag_backup.json         # JSON 格式备份
├── scripts/                # Python 脚本
│   ├── rag_system.py       # RAG 核心系统
│   ├── init_rag.py         # 初始化脚本
│   └── test_rag.py         # 测试脚本
├── data/                   # 初始数据
│   └── amazon_urls.json
├── requirements.txt        # 依赖列表
└── README.md              # 本文件
```

## 使用示例

```python
from scripts.rag_system import AmazonURLRAG

# 初始化
rag = AmazonURLRAG(db_path="./rag_db")

# 检索 URL
result = rag.search_url("美国亚马逊账户详情页", top_k=3)

# 查看结果
for item in result['results']:
    print(f"URL: {{item['exact_url']}}")
    print(f"相似度: {{item['similarity']*100:.1f}}%")
```

## 统计信息
- 总条目数: {stats['total_entries']}
- 分类: {', '.join(stats['categories'].keys())}
- 站点: {', '.join(stats['marketplaces'].keys())}

## 技术栈
- ChromaDB: 向量数据库
- OpenAI Embedding: text-embedding-3-small
- Python 3.8+

## 支持
如有问题，请查看测试脚本或联系开发者。
"""
        
        with open(export_dir / "README.md", 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print("  ✅ README.md")
        
        # 10. 打包成 ZIP
        print("\n📝 步骤 10: 打包为 ZIP...")
        output_path = Path("..") / output_name
        
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file in export_dir.rglob("*"):
                if file.is_file():
                    arcname = file.relative_to(export_dir)
                    zf.write(file, arcname)
                    
        file_size = output_path.stat().st_size / 1024 / 1024  # MB
        print(f"✅ 已创建: {output_path.absolute()}")
        print(f"📦 文件大小: {file_size:.2f} MB")
        
        # 11. 清理临时目录
        print("\n📝 步骤 11: 清理临时文件...")
        shutil.rmtree(export_dir)
        print("✅ 已清理临时目录")
        
        # 12. 显示摘要
        print("\n" + "=" * 70)
        print("🎉 Skill 导出成功！")
        print("=" * 70)
        print(f"\n📦 文件位置: {output_path.absolute()}")
        print(f"📊 包含内容:")
        print(f"  - RAG 数据库: {stats['total_entries']} 条")
        print(f"  - JSON 备份: rag_backup.json")
        print(f"  - Python 脚本: 3 个")
        print(f"  - 配置文件: skill.json")
        print(f"\n📌 下一步:")
        print(f"  1. 分发 {output_name} 文件")
        print(f"  2. 接收方解压后按 README.md 操作")
        print(f"  3. 运行 test_rag.py 验证")
        
    except Exception as e:
        print(f"\n❌ 导出失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="导出 Amazon RAG Skill")
    parser.add_argument(
        "--output",
        "-o",
        default="skill.zip",
        help="输出文件名（默认: skill.zip）"
    )
    
    args = parser.parse_args()
    export_skill(args.output)
