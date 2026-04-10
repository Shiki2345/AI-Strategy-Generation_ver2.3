"""
初始化 RAG 数据库

从 data/amazon_urls.json 读取初始数据并导入到 RAG 系统
"""

import os
import sys
import json
from pathlib import Path

# 添加父目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

from rag_system import AmazonURLRAG


def load_initial_data(data_file: str = "../data/amazon_urls.json") -> list:
    """
    加载初始数据
    
    Args:
        data_file: 数据文件路径
        
    Returns:
        数据列表
    """
    # 获取脚本所在目录
    script_dir = Path(__file__).parent
    data_path = script_dir / data_file
    
    print(f"📂 读取数据文件: {data_path}")
    
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"✅ 成功读取 {len(data)} 条数据")
    return data


def init_rag_database():
    """初始化 RAG 数据库"""
    print("=" * 70)
    print("🚀 开始初始化 Amazon URL RAG 数据库")
    print("=" * 70)
    
    try:
        # 1. 初始化 RAG 系统
        print("\n📝 步骤 1: 初始化 RAG 系统...")
        rag = AmazonURLRAG(db_path="../rag_db")
        
        # 2. 检查是否已有数据
        current_count = rag.collection.count()
        if current_count > 0:
            print(f"\n⚠️  数据库已包含 {current_count} 条数据")
            response = input("是否清空并重新导入？(y/N): ").strip().lower()
            
            if response == 'y':
                print("🗑️  清空现有数据...")
                rag.chroma_client.delete_collection("amazon_urls")
                rag._init_chromadb()
            else:
                print("✋ 取消操作")
                return
        
        # 3. 加载初始数据
        print("\n📝 步骤 2: 加载初始数据...")
        data = load_initial_data()
        
        # 4. 导入数据
        print("\n📝 步骤 3: 导入数据到 RAG 系统...")
        print("-" * 70)
        
        success_count = 0
        for i, entry in enumerate(data, 1):
            try:
                entry_id = rag.add_url_entry(
                    user_description=entry['user_description'],
                    exact_url=entry['exact_url'],
                    page_description=entry['page_description'],
                    aliases=entry.get('aliases', []),
                    keywords=entry.get('keywords', []),
                    marketplace=entry.get('marketplace', 'ALL'),
                    category=entry.get('category', 'general')
                )
                success_count += 1
                print(f"  [{i}/{len(data)}] {entry['user_description'][:30]}...")
            except Exception as e:
                print(f"  ❌ 导入失败: {entry['user_description']} - {e}")
        
        print("-" * 70)
        print(f"✅ 成功导入 {success_count}/{len(data)} 条数据")
        
        # 5. 导出备份
        print("\n📝 步骤 4: 导出 JSON 备份...")
        rag.export_to_json("../rag_backup.json")
        
        # 6. 显示统计信息
        print("\n📊 步骤 5: 数据库统计...")
        stats = rag.get_statistics()
        print("-" * 70)
        print(f"总条目数: {stats['total_entries']}")
        print(f"分类统计: {json.dumps(stats['categories'], indent=2, ensure_ascii=False)}")
        print(f"站点统计: {json.dumps(stats['marketplaces'], indent=2, ensure_ascii=False)}")
        print("-" * 70)
        
        print("\n" + "=" * 70)
        print("🎉 RAG 数据库初始化完成！")
        print("=" * 70)
        
        print("\n📌 下一步:")
        print("  1. 运行测试: python test_rag.py")
        print("  2. 查看数据库: ../rag_db/")
        print("  3. 查看备份: ../rag_backup.json")
        
    except ValueError as e:
        print(f"\n❌ 错误: {e}")
        print("\n💡 解决方案:")
        print("  1. 创建 .env 文件")
        print("  2. 添加: OPENAI_API_KEY=your_key_here")
        print("  或者设置环境变量: set OPENAI_API_KEY=your_key")
    except FileNotFoundError as e:
        print(f"\n❌ 文件未找到: {e}")
        print("💡 请确保 data/amazon_urls.json 文件存在")
    except Exception as e:
        print(f"\n❌ 初始化失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    init_rag_database()
